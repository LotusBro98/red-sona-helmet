import time
import numpy as np
from display import Display, SIZE
from display_modes.impulse import gen_image
from signal_modes.soundparse import start_signal, signal_active, stop_signal


SCALE = 5
NORMALIZE = False


display = Display()

signal0 = np.zeros((SIZE[1],))
ALPHA = 0.5

def signal_callback(signal, main_freq):
    signal = signal * SCALE
    signal = signal * ALPHA + signal0 * (1 - ALPHA)
    image = gen_image(signal, main_freq)
    display.draw_image(image)


start_signal(signal_callback)

while(signal_active()):
    time.sleep(0.1)

stop_signal()