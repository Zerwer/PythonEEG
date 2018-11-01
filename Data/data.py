import serial

# Initialization of HC-06 at a baud rate of 9600(default) sending 0x02 to initiate
s = serial.Serial(port='/dev/tty.HC-06-DevB', baudrate=9600)
s.write(b'\x02')  # Must be sent in bytes
s.close()


# Connects to HC-06 at a baudrate of 57600
s = serial.Serial(port='/dev/tty.HC-06-DevB', baudrate=57600)

file = open('out.bin', 'wb')

# Loop of collecting information
while True:
    size = s.inWaiting()  # Returns int of packets waiting to be read
    if size:
        #print(int.from_bytes(s.read(size), byteorder='big'))  # Convert read bytes to integer using big byte order
        print(s.read(size).hex())
        file.write(s.read(size))