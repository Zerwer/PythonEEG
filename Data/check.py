# Use to verify if device is functional
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

# Loop of collecting information
while True:
    size = s.inWaiting()  # Returns int of packets waiting to be read
    if size:
        print(s.read(size).hex())

