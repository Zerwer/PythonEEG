# Packet dissection:
# aa - start (static)
# 048002 - key (dynamic) changes each session
# ff7905 - data (dynamic)
# aa - end (static)
#
# keys:
# 068204
# 048002
import serial
import time

# Device used
device = '/dev/tty.HC-06-DevB'

# Initialization of HC-06 at a baud rate of 9600(default) sending 0x02 to initiate (twice for certainty)
s = serial.Serial(port=device, baudrate=9600)
s.write(b'\x02')  # Must be sent in bytes
time.sleep(1)
s.write(b'\x02')
s.close()


# Connects to HC-06 at a baudrate of 57600
s = serial.Serial(port=device, baudrate=57600)

# Open file to output to
file = open('out.bin', 'wb')
file2 = open('data.out', 'w')

# Declare blank storage packet
packet = ''

# Loop of collecting information
while True:
    data = s.read(1)
    if data.hex() == 'aa':
        if packet != '':
            # print(int(packet[-6::], 16))
            print(packet)
            file2.write(str(int(packet[-6::], 16))+'\n')
            packet = ''
    else:
        packet = packet+data.hex()

    file.write(data)
