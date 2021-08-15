import numpy as np
from display import SIZE
import colorsys

MIN_COLOR = (1, 0, 0)
MAX_COLOR = (1, 0, 1)
MAX_FREQ = 1000

def gen_colors(main_freq):

    min_color_hsv = np.float32(colorsys.rgb_to_hsv(MIN_COLOR[0], MIN_COLOR[1], MIN_COLOR[2]))
    max_color_hsv = np.float32(colorsys.rgb_to_hsv(MAX_COLOR[0], MAX_COLOR[1], MAX_COLOR[2]))

    t = main_freq / MAX_FREQ

    if t > 2 * MAX_FREQ:
        t = 0
    elif t > MAX_FREQ:
        t = 1

    color0 = min_color_hsv + 0.8 * t * (max_color_hsv - min_color_hsv)
    color1 = min_color_hsv + t * (max_color_hsv - min_color_hsv)

    color0 = colorsys.hsv_to_rgb(color0[0], color0[1], color0[2])
    color1 = colorsys.hsv_to_rgb(color1[0], color1[1], color1[2])

    return color0, color1


def gen_image(signal: np.ndarray, main_freq):

    color0, color1 = gen_colors(main_freq)

    signal = (signal * -0.5 + 0.5) * SIZE[0]
    signal = np.clip(signal, 0, SIZE[0] - 1)
    color0 = np.float32(color0)
    color1 = np.float32(color1)
    image = np.zeros((SIZE[1], SIZE[0], 3))
    for j in range(-1, SIZE[1] - 1):
        i_start = signal[j]
        i_end = signal[j + 1]
        if int(i_end) == int(i_start):
            t = np.linspace(1, 1, 1)
        elif i_start > i_end:
            i_start, i_end = i_end, i_start
            t = np.linspace(0, 1, int(i_end) + 1 - int(i_start))
        else:
            t = np.linspace(1, 0, int(i_end) + 1 - int(i_start))
        t0 = np.square(t[:, np.newaxis])
        t1 = np.square(1 - t[:, np.newaxis])
        image[j, int(i_start): int(i_end) + 1] += t0 * ((1 - t0) * color0 + t0 * color1)
        image[j + 1, int(i_start): int(i_end) + 1] += t1 * ((1 - t1) * color0 + t1 * color1)

    image = np.clip(image, 0, 1)
    image = np.transpose(image, (1, 0, 2))

    return image