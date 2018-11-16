# Run to collect raw data or graph live data
from data import *
from graphics import start_loop
import threading
import argparse

# Argparse for optional options
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--save', action='store_true', help='saves to data.out')
parser.add_argument('-g', '--graphics', action='store_true', help='displays data live to a graph')
parser.add_argument('-t', '--text', action='store_true', help='print all live data as text to console')

args = parser.parse_args()

graphic_mode = args.graphics
save_mode = args.save
text_mode = args.text

# Load arguments
if graphic_mode:
    # Serial reader must be in separate thread, tkinter must be run on main thread
    thread = threading.Thread(target=data_loop, args=[text_mode, save_mode, graphic_mode, 10, False])
    thread.start()
    start_loop()

# graphic_mode will always be false if this executes and average should be one without graphics
elif text_mode:
    data_loop(text_mode, save_mode, False, 1, False)
