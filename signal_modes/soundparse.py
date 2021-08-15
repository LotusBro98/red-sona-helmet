import sounddevice as sd
import numpy as np
import time

from display import SIZE

CHANNELS = 1
RATE = 44100
TAKE_RATE = 11025
TIME = 0.03
CHUNK = int(RATE * TIME)
DEVICE = 0
SIGNAL_LEN = SIZE[1]

print(sd.query_devices())


def global_callback(indata, frames, tim, status):
    global signal_callback

    indata = indata[::int(RATE / TAKE_RATE), 0]
    spectrum = np.fft.fft(indata)

    spectrum[0] = 0
    spectrum[-1] = 0
    main_freq = np.argmax(np.abs(spectrum[:len(spectrum)//SIGNAL_LEN]))
    spectrum = spectrum[:main_freq * SIGNAL_LEN:main_freq]

    norm = np.linalg.norm(spectrum)

    # rot = spectrum[1] / np.abs(spectrum[1]) * np.exp(0.5j * np.pi)
    rot = spectrum[1] * np.exp(0.5j * np.pi) / np.abs(spectrum[1])
    spectrum /= np.power(rot, np.arange(len(spectrum)))
    spectrum /= norm

    signal = np.real(np.fft.ifft(spectrum))

    signal_callback(signal, main_freq * 1 / TIME)


def start_signal(callback):
    global stream
    global signal_callback
    signal_callback = callback

    stream = sd.InputStream(channels=CHANNELS, device=DEVICE, callback=global_callback, samplerate=RATE, blocksize=CHUNK)
    stream.start()


def signal_active():
    global stream
    return stream.active


def stop_signal():
    global stream
    stream.stop()
    stream.close()