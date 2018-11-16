from data import *
from tkinter import *
import random as r

w = 900
h = 556

root = Tk()
root.geometry(str(w)+'x'+str(h))
root.title('Letter Viewer')

graphing_area = Canvas(root, width=w, height=h)
graphing_area.pack()


def display_letter(canvas, wait):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    canvas.delete('all')

    if wait:
        canvas.create_text(w / 2, h / 2, font="Arial " + str(int(round(h / 3, 0))), text='Wait', anchor='center')
        root.after(2000, display_letter, canvas, False)

    else:
        letter = alphabet[r.randint(0, 25)]
        canvas.create_text(w/2, h/2, font="Arial "+str(int(round(h/3, 0))), text=letter, anchor='center')
        # For the next 5 sec collect data ...
        root.after(5000, display_letter, canvas, True)


root.after(0, display_letter, graphing_area, True)
root.mainloop()
