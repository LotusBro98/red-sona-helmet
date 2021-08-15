import sys
import time
import numpy as np
from display import Display, SIZE
from display_modes.impulse import gen_image
import signal_modes.soundparse
import signal_modes.stub


display = Display()

def signal_callback(signal, main_freq):
    image = gen_image(signal, main_freq)
    display.draw_image(image)


try:
    signal_modes.soundparse.start_signal(signal_callback)
    signal_active = signal_modes.soundparse.signal_active
    stop_signal = signal_modes.soundparse.stop_signal
except Exception as e:
    print(e, file=sys.stderr)
    signal_modes.stub.start_signal(signal_callback)
    signal_active = signal_modes.stub.signal_active
    stop_signal = signal_modes.stub.stop_signal

while(signal_active()):
    time.sleep(0.1)

stop_signal()

exit(-1)