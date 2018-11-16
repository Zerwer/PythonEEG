# File for reading and parsing packets
# See mindset_communication_protocol.pdf for packet breakdown
import serial
import time
import datetime

# [0] is if saving should be set, [1] is the letter being saved, [2] is file code
save_info = [False, '', 0]

# Storage for y_values that must be graphed, must always have 900 values
y_values = []
for z in range(900):
    y_values.append(0)


# Calculates the checksum given the payload and corresponding checksum
def calc_chksum(packet, chksum):
    # See mindset_communication_protocol.pdf for chksum
    total = 0
    for i in packet:
        total += int(i, 16)

    total &= 255
    total = ~total & 255

    if total == int(chksum, 16):
        return True

    else:
        # If chksum fails disregard packet
        print('CHKSUM_FAILED')
        return False


# Parse payload into raw eeg values, delta, theta, low-alpha, high-alpha, low-beta,
# high-beta, low-gamma, and mid-gamma wave values
def parse_payload(packet):
    # If next byte is vlength
    vlength = False
    value_length = 0
    # If next byte should be ignored
    ignore = False
    # If a code should be expected
    code = True
    # If the data is raw wave values
    raw = False
    raw_value = ''
    # Saves processed values here
    processed = []

    for i in range(len(packet)):
        if ignore:
            ignore = False

        # Code for 2 byte raw eeg value
        elif code and packet[i] == '80':
            vlength = True
            code = False
            raw = True

        # Code for processed wave types payload
        elif code and packet[i] == '83':
            vlength = True
            code = False

        # Currently ignore 02-Signal quality, 04-Attention, 05-Meditation, 16-blink
        elif code and (packet[i] == '02' or packet[i] == '04' or packet[i] == '05' or packet[i] == '16'):
            ignore = True

        elif vlength:
            value_length = int(packet[i], 16)
            vlength = False

        elif value_length > 0 and raw:
            raw_value += packet[i]
            value_length -= 1

        elif value_length > 0 and not raw:
            processed.append(packet[i])
            value_length -= 1
            if value_length == 0:
                code = True

    if raw:
        val = int(raw_value[:2], 16)*256 + int(raw_value[2:], 16)
        if val >= 32768:
            val -= 65536
        # Val is final output
        return ['raw', val]
    else:
        val = []
        x = 0
        buffer = ''
        for byte in processed:
            buffer += byte
            x += 1
            if x % 3 == 0:
                val.append(buffer)
                buffer = ''
        # Processed is final output
        return ['processed', val]


# text_mode, enables text output to console
# save_mode, saves to out file
# graphic_mode, if raw data should be graphed
# average, only used if graphic_mode is true, how many points should be averaged to graph
def data_loop(text_mode, save_mode, graphic_mode, average, letter_save):
    # Device used
    device = '/dev/tty.HC-06-DevB'

    # Connects to HC-06 at a baud rate of 57600
    s = serial.Serial(port=device, baudrate=57600)

    # Initialization requires 0x02 code to be sent ata 9600 baud although HC-06 is set to 57600 baud
    # 00 F8 00 00 00 E0 when sent at 57600 baud should resemble 0x02 at 9600 as 57600 / 6 = 9600
    # 0x02 code when sent will switch device into 57600 baud and RAW_MODE
    # Must sleep for time of one bit at 9600 baud, 1(second) / 9600 is
    # the amount but one millisecond is more than enough
    s.write(b'\x00\xf8\x00\x00\x00\xe0')
    time.sleep(0.001)

    # Temporary storage for parsing
    sync = False
    plength = False
    payload_length = 0
    payload_storage = []
    counter = [0, 0]

    if save_mode:
        save_file = open('data-' + str(datetime.datetime.now()).replace(' ', '-').replace(':', '-')[:-7] + '.out', 'w')

    # See mindset_communication_protocol.pdf for parsing
    while True:
        data = s.read().hex()

        if data == 'aa' and not sync:
            sync = True
            plength = False
            payload_length = 0
            payload_storage = []

        elif data == 'aa' and sync:
            sync = False
            plength = True

        elif sync:
            sync = False

        elif plength and int(data, 16) < 170:
            plength = False
            payload_length = int(data, 16)

        elif plength and int(data, 16) <= 170:
            pass

        elif payload_length > 0:
            payload_storage.append(data)
            payload_length -= 1

        elif payload_length == 0 and payload_storage != [] and calc_chksum(payload_storage, data):
            value = parse_payload(payload_storage)

            # If packet is raw data
            if value[0] == 'raw':
                # Graphic stuff
                if graphic_mode:
                    counter[0] += 1
                    counter[1] += value[1]

                    # Determine if point is to be graphed
                    if counter[0] >= average:
                        counter[1] /= average
                        # Transform raw wave values for graphing
                        # Formula for raw wave value to voltage: [rawValue * (1.8 / 4096)] / 2000
                        # http://support.neurosky.com/kb/science/how-to-convert-raw-values-to-voltage
                        y_values.append(((counter[1]+2048)/4096)*556)
                        del y_values[0]
                        counter = [0, 0]

                # Text stuff
                if text_mode:
                    print(value[1])

                # Save stuff
                if save_mode:
                    save_file.write(str(value[1])+'\n')

                if letter_save and save_info[0]:
                    file = open('letters/' + save_info[1] + str(save_info[2]) + '.txt', 'a+')
                    file.write(str(value[1])+'\n')
                    print(value[1])
                    file.close()

            elif value[0] == 'processed':
                if text_mode:
                    print(value[1])
