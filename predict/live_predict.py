from data import *
from tkinter import *
from keras.models import load_model
import threading

model = load_model('model.h5')
thread = threading.Thread(target=data_loop, args=[False, False, False, 1, True])
thread.start()
