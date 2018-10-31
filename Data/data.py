import serial

# Connects to HC-06 at a baudrate of 57600
s = serial.Serial(port='/dev/tty.HC-06-DevB', baudrate=57600)

# Loop of collecting information
while True:
    size = s.inWaiting()  # Returns int of packets waiting to be read
    if size:
        print(int.from_bytes(s.read(size), byteorder='big'))  # Convert read bytes to integer using big byte order
