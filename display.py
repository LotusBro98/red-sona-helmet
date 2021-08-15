import time

from rpi_ws281x import PixelStrip, Color
import numpy as np

# LED strip configuration:
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

SIZE = (30, 10)

OFFSET = [
    [4, 3, 2, 1, 0, 0, 1, 2, 3, 4],
    [5, 3, 2, 1, 0, 0, 1, 2, 3, 5]
]

TRANSPOSE = True
INVERT_I = True
INVERT_J = True

LED_COUNT = sum([(SIZE[0] if TRANSPOSE else SIZE[1]) - OFFSET[0][i] - OFFSET[1][i] for i in range(len(OFFSET[0]))])

class Display:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        self.buffer = np.zeros(SIZE + (4,), dtype=np.uint8)
        self.slices = []
        if TRANSPOSE:
            for j in range(SIZE[1]):
                if INVERT_J:
                    j = SIZE[1] - 1 - j
                slice = self.buffer[OFFSET[0][j]: SIZE[0] - OFFSET[1][j], j]
                if INVERT_I:
                    slice = slice[::-1]
                self.slices.append(slice)
        else:
            for i in range(SIZE[0]):
                if INVERT_I:
                    i = SIZE[0] - 1 - i
                slice = self.buffer[i, OFFSET[0][i]: SIZE[1] - OFFSET[1][i]]
                if INVERT_J:
                    slice = slice[::-1]
                self.slices.append(slice)

    def draw_image(self, image):
        self.buffer[:,:,:3] = np.uint8(image * 255)[:,:,::-1]
        intbuf = np.concatenate(self.slices, axis=0)
        intbuf = np.frombuffer(intbuf.tobytes(), dtype=np.int32).tolist()
        led_data = self.strip._led_data
        for i, val in enumerate(intbuf):
            led_data[i] = val
        self.strip.show()