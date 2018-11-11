# Use to verify if device is functional
import serial
import time

# Device used
device = '/dev/tty.HC-06-DevB'

# Connects to HC-06 at a baud rate of 57600
s = serial.Serial(port=device, baudrate=57600)

s.write(b'\x00\xf8\x00\x00\x00\xe0')
time.sleep(0.001)

# Loop of collecting information
while True:
    size = s.inWaiting()  # Returns int of packets waiting to be read
    if size:
        print(s.read(size).hex())

