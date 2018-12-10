# File for graphical functions
from data import *
from tkinter import *
from PIL import Image, ImageDraw, ImageFont
import os

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
        graphing_area.create_rectangle(int(i), int(int(y_values[i]) / (-1)) + 556,
                                       int(i + 1), int(int(y_values[i + 1]) / (-1)) + 556)

    root.after(500, draw_point)


# Takes centered x and y and converts to top left anchor for PIL
def center_anchor(x, y, text, font, draw):
    w, h = draw.textsize(text, font=font)
    new_x = x - w / 2
    new_y = y - h / 2
    return [new_x, new_y]


# Called when the s key is pressed, saves the current displayed data to figure.jpg in screenshots/
def save_data(event):
    black = (0, 0, 0)
    font = ImageFont.truetype('Arial.ttf', 20)

    screenshot = Image.new('RGB', (900, 556), (255, 255, 255))
    draw = ImageDraw.Draw(screenshot)

    for i in range(0, len(y_values)-1):
        draw.line([int(i), int(int(y_values[i])/(-1))+556, int(i+1), int(int(y_values[i+1])/(-1))+556], black)

    draw.text(center_anchor(450, 530, 'Time (Seconds)', font, draw), 'Time (Seconds)', black, font)
    draw.line([849, 480, 847, 450], black)
    draw.text(center_anchor(848, 430, '1', font, draw), '1', black, font)
    draw.line([645, 480, 643, 450], black)
    draw.text(center_anchor(644, 430, '5', font, draw), '5', black, font)
    draw.line([389, 480, 387, 450], black)
    draw.text(center_anchor(388, 430, '10', font, draw), '10', black, font)
    draw.line([135, 480, 133, 450], black)
    draw.text(center_anchor(134, 430, '15', font, draw), '15', black, font)

    prefix = [0]
    for name in os.listdir('screenshots'):
        print(name)
        prefix.append(int(name[6:-4]))

    screenshot.save('screenshots/figure' + str(max(prefix) + 1) + '.jpg')


# Lets main graphical loop begin after serial reader initiated
def start_loop():
    root.after(500, draw_point)
    root.bind('s', save_data)
    root.mainloop()
