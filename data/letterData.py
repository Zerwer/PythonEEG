from tkinter import *
import random as r
import time

w = 900
h = 556

root = Tk()
root.geometry('900x556')
root.title('Letter Viewer')

graphing_area = Canvas(root, width=w, height=h)
graphing_area.pack()


def display_letter(canvas):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    canvas.delete('all')

    letter = alphabet[r.randint(0, 25)]
    
    canvas.create_text(w/2, h/2, font="Courier 120", text=letter, anchor='center')
    
    root.after(1000, display_letter, canvas)


root.after(1000, display_letter, graphing_area)

root.mainloop()