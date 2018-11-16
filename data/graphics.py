# File for graphical functions
from data import *
from tkinter import *

root = Tk()
root.geometry('900x556')
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()


# Function called to redraw points
def draw_point():
    graphing_area.delete('all')  # Clear every redraw

    i = 0
    for point in y_values:
        graphing_area.create_rectangle(int(i), int(int(point)/(-1))+556, int(i), int(int(point)/(-1))+556)
        i += 1

    root.after(500, draw_point)


# Lets main graphical loop begin after serial reader initiated
def start_loop():
    root.after(500, draw_point)
    root.mainloop()
