import sounddevice as sd
import numpy as np

from display import SIZE

CHANNELS = 1
RATE = 44100
TAKE_RATE = 11025
TIME = 0.03
CHUNK = int(RATE * TIME)
DEVICE = 0
SIGNAL_LEN = SIZE[1]
SCALE = 5
LOW_LEVEL_BOUND = 0.14

print(sd.query_devices())


def global_callback(indata, frames, tim, status):
    global signal_callback

    indata = indata[::int(RATE / TAKE_RATE), 0]
    spectrum = np.fft.fft(indata)

    spectrum[0] = 0
    spectrum[-1] = 0
    main_freq = np.argmax(np.abs(spectrum[:len(spectrum)//SIGNAL_LEN]))
    # spectrum = spectrum[:main_freq * SIGNAL_LEN:main_freq]
    spectrum = spectrum[:int(np.ceil(main_freq/2)) * SIGNAL_LEN:int(np.ceil(main_freq/2))]
    spectrum[0] = 0
    spectrum[1] = 0
    spectrum[-1] = 0
    spectrum[-2] = 0

    norm = np.linalg.norm(spectrum)
    if norm < LOW_LEVEL_BOUND:
        norm = LOW_LEVEL_BOUND

    rot = spectrum[2] * np.exp(0.5j * np.pi) / np.abs(spectrum[2])
    spectrum /= np.power(rot, np.arange(len(spectrum)) / 2)
    spectrum /= norm

    signal = np.real(np.fft.ifft(spectrum))

    window = np.linspace(0, np.pi, len(signal))
    window = np.sin(window)
    signal = signal * window
    signal = signal * SCALE

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