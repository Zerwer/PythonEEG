import serial

s = serial.Serial(port='/dev/tty.HC-06-DevB', baudrate=57600)

while True:
    size = s.inWaiting()
    if size:
        print(int.from_bytes(s.read(size), byteorder='big'))
