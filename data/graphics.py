# File for graphical functions
from data import *
from tkinter import *
# from PIL import Image, ImageDraw, ImageFont

root = Tk()
root.geometry('900x556')
root.title('EEG Raw Data')

graphing_area = Canvas(root, width=900, height=556)
graphing_area.pack()


# Draws a x-axis scale for live graph
def scale():
    graphing_area.create_text(450, 530, text='Time (Seconds)', anchor='center', font="Arial 20 bold")
    graphing_area.create_rectangle(849, 480, 847, 450, fill='black')
    graphing_area.create_text(848, 430, text='1', anchor='center', font="Arial 20 bold")
    graphing_area.create_rectangle(645, 480, 643, 450, fill='black')
    graphing_area.create_text(644, 430, text='5', anchor='center', font="Arial 20 bold")
    graphing_area.create_rectangle(389, 480, 387, 450, fill='black')
    graphing_area.create_text(388, 430, text='10', anchor='center', font="Arial 20 bold")
    graphing_area.create_rectangle(135, 480, 133, 450, fill='black')
    graphing_area.create_text(134, 430, text='15', anchor='center', font="Arial 20 bold")


# Function called to redraw points
def draw_point():
    graphing_area.delete('all')  # Clear every redraw
    scale()

    for i in range(0, len(y_values)-1):
        graphing_area.create_rectangle(int(i), int(int(y_values[i])/(-1))+556,
                                       int(i+1), int(int(y_values[i+1])/(-1))+556)

    root.after(500, draw_point)


# Lets main graphical loop begin after serial reader initiated
def start_loop():
    root.after(500, draw_point)
    # root.bind('s', save_data)
    root.mainloop()
