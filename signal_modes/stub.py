import numpy as np
import time
import threading

from display import SIZE

TIME = 0.03

running = False

def global_callback():
    global signal_callback
    global running

    while running:
        spectrum = np.random.normal(size=(SIZE[1],)) + 1j * np.random.normal(size=(SIZE[1],))
        spectrum *= 1 / np.square(np.linspace(1/SIZE[1], 1, SIZE[1]))
        spectrum[0] = 0
        spectrum[-1] = 0

        norm = np.linalg.norm(spectrum)

        rot = spectrum[1] * np.exp(0.5j * np.pi) / np.abs(spectrum[1])
        spectrum /= np.power(rot, np.arange(len(spectrum)))
        spectrum /= norm

        signal = np.real(np.fft.ifft(spectrum))

        main_freq = 1

        signal_callback(signal, main_freq * 1 / TIME)
        time.sleep(TIME)


def start_signal(callback):
    global thr
    global running
    global signal_callback
    running = True
    signal_callback = callback
    thr = threading.Thread(target=global_callback, args=[])
    thr.start()


def signal_active():
    global running
    return running


def stop_signal():
    global running
    global thr
    running = False
    thr.join()