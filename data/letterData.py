# Run file to collect data when exposed to random letter
from data import *
from tkinter import *
import os
import random as r
import threading

# Set values for data
wait_time = 1000  # How long to wait in between exposures
expose_time = 3000  # How long letter should be exposed

# Letters to be sampled
# samples = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
#            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
samples = ['A', 'B']

# Set dimensions
w = 900
h = 556

root = Tk()
root.geometry(str(w)+'x'+str(h))
root.title('Letter Viewer')

graphing_area = Canvas(root, width=w, height=h)
graphing_area.pack()


# Function to display letter to be thought of, will set saving variable
def display_letter(canvas, wait):
    canvas.delete('all')

    if wait:

        values = open(path + save_info[1] + str(save_info[2]) + '.csv', 'r').read()[:-1].split(',')
        if len(values) < 1500:
            os.remove(path + save_info[1] + str(save_info[2]) + '.csv')
        else:
            file = open(path + save_info[1] + str(save_info[2]) + '.csv', 'w')
            for i in range(1500):
                file.write(values[i]+',')

        save_info[0] = False
        save_info[1] = ''
        save_info[2] = 0

        canvas.create_text(w / 2, h / 2, font="Arial " + str(int(round(h / 3, 0))), text='Wait', anchor='center')
        root.after(wait_time, display_letter, canvas, False)

    else:
        letter = samples[r.randint(0, len(samples) - 1)]
        canvas.create_text(w/2, h/2, font="Arial "+str(int(round(h/3, 0))), text=letter, anchor='center')
        # For the next 5 sec collect data
        save_info[0] = True
        save_info[1] = letter.lower()

        file_list = []
        for name in os.listdir(path[:-1]):
            if name[0] == letter.lower():
                file_list.append(int(name[1:-4]))

        if len(file_list) < 1:
            save_info[2] = 0

        else:
            save_info[2] = max(file_list) + 1

        root.after(expose_time, display_letter, canvas, True)


thread = threading.Thread(target=data_loop, args=[False, False, False, 1, True])
thread.start()

graphing_area.create_text(w/2, h/2, font="Arial "+str(int(round(h/3, 0))), text='Loading...', anchor='center')

root.after(10000, display_letter, graphing_area, False)
root.mainloop()
