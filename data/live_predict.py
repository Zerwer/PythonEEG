from data import *
from tkinter import *
from keras.models import load_model
import threading

# Time variables
start_wait = 10000
wait = 3100

# Set dimensions
w = 900
h = 556

root = Tk()
root.geometry(str(w)+'x'+str(h))
root.title('Predictor')

graphing_area = Canvas(root, width=w, height=h)
graphing_area.pack()

# Import model to be used
saved_model = load_model('model.h5')

# Begin data thread
thread = threading.Thread(target=data_loop, args=[False, False, False, 1, False])
thread.start()


# Predicts the input values and returns predicted letter
def predict(values, model):
    # TODO stuff
    print(values[0])
    return 'A'


def display_prediction(canvas, frame, model):
    prediction = predict(last_values[-1500:], model)

    canvas.delete('all')
    canvas.create_text(w / 2, h / 2, font="Arial " + str(int(round(h / 3, 0))), text=prediction, anchor='center')

    root.after(wait, display_prediction, canvas, frame, model)


root.after(start_wait, display_prediction, graphing_area, root, saved_model)
root.mainloop()
