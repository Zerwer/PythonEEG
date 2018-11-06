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

# Device used
device = '/dev/tty.HC-06-DevB'

# Initialization of HC-06 at a baud rate of 9600(default) sending 0x02 to initiate (twice for certainty)
s = serial.Serial(port=device, baudrate=9600)
s.write(b'\x02')  # Must be sent in bytes
s.close()

# Connects to HC-06 at a baudrate of 57600
s = serial.Serial(port=device, baudrate=57600)

# Open file to output to
binary_output = open('out.bin', 'wb')
raw_data = open('data.out', 'w')

# Declare blank storage packet
packet = ''

# Declare blank point set
points = []

for i in range(900):
    points.append(0)

# Loop of collecting information
while True:
    data = s.read(1)
    if data.hex() == 'aa':
        if packet != '':
            value = int(packet[-6::], 16)
            raw_data.write(str(value)+'\n')
            packet = ''
    else:
        packet = packet+data.hex()

    binary_output.write(data)
