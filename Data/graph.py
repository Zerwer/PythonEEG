# See data.py for packet dissection
from tkinter import *
import threading
import serial

root = Tk()
root.geometry('900x556')
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()


def draw_point(points):
    graphing_area.delete('all') # Clear every redraw

    i = 0
    for point in points:
        graphing_area.create_rectangle(int(i), int(int(point)/(-1))+556, int(i), int(int(point)/(-1))+556)
        i += 1


def read_EEG():
    # Device used
    device = '/dev/tty.HC-06-DevB'

    # Initialization of HC-06 at a baud rate of 9600(default) sending 0x02 to initiate (twice for certainty)
    s = serial.Serial(port=device, baudrate=9600)
    s.write(b'\x02')  # Must be sent in bytes
    s.close()

    # Connects to HC-06 at a baud rate of 57600
    s = serial.Serial(port=device, baudrate=57600)

    # Open file to output to
    file = open('out.bin', 'wb')
    file2 = open('data.out', 'w')

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
                # Remove first six characters (key)
                value = int(packet[-6::], 16)
                file2.write(str(value)+'\n')
                if int(packet[-6::], 16) < 99000:
                    del points[0]
                    points.append((int(packet[-6::], 16)/99000)*556)
                    draw_point(points)

                packet = ''
        else:
            packet = packet+data.hex()

        file.write(data)


thread = threading.Thread(target=read_EEG)
thread.start()
root.mainloop()