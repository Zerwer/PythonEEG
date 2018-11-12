from tkinter import *

root = Tk()
root.geometry('900x556')
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()


# Function called to redraw points
def draw_point(points):
    graphing_area.delete('all')  # Clear every redraw

    i = 0
    for point in points:
        graphing_area.create_rectangle(int(i), int(int(point)/(-1))+556, int(i), int(int(point)/(-1))+556)
        i += 1


# Lets main graphical loop begin after serial reader initiated
def start_loop():
    root.mainloop()
