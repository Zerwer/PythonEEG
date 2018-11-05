from tkinter import *

root = Tk()
root.geometry('900x556')  # Golden ratio
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()

points = []

file = open('data.out', 'r')
lines = file.readlines()


def draw_point(points):
    i = 0
    for point in points:
        graphing_area.create_rectangle(i, (int(point)/99000)*556, i, (int(point)/99000)*556)
        i += 1


for line in lines:
    if int(line) > 99000: lines.remove(line)

stuff = []

for i in range(900):
    stuff.append(lines[i])

draw_point(stuff)

root.mainloop()