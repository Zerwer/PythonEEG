# Run file to collect data when exposed to random letter
from data import *
from tkinter import *
import os
import random as r
import threading
import numpy as np

# Set values for data
wait_time = 1000  # How long to wait in between exposures
expose_time = 1000  # How long letter should be exposed

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
def display_letter(canvas, frame, wait):
    canvas.delete('all')

    if wait:

        file_list = []
        for name in os.listdir(path[:-1]):
            if name[0] == save_info[1]:
                file_list.append(int(name[1:-4]))

        if len(file_list) < 1:
            code = 0

        else:
            code = max(file_list) + 1

        if len(save_info[2]) >= 500:
            np.savetxt(path+save_info[1]+str(code)+'.csv', np.array(save_info[2][:500]), delimiter=',')
        else:
            pass

        letter = samples[r.randint(0, len(samples) - 1)]
        canvas.create_text(w/2, h/2, font="Arial "+str(int(round(h/3, 0))), text=letter, anchor='center')
        # For the next 5 sec collect data
        save_info[0] = False
        save_info[1] = letter.lower()
        save_info[2] = []

        frame.after(wait_time, display_letter, canvas, frame, False)

    else:
        save_info[0] = True
        frame.after(expose_time, display_letter, canvas, frame, True)


thread = threading.Thread(target=data_loop, args=[False, False, False, 1, True])
thread.start()

graphing_area.create_text(w/2, h/2, font="Arial "+str(int(round(h/3, 0))), text='Loading...', anchor='center')

root.after(10000, display_letter, graphing_area, root, True)
root.mainloop()
