import math
import random

import numpy as np
import pyfastnoisesimd as fn
import tensorflow as tf


def fastnoise(shape, freq, time=0.0, seed=None, speed=1.0, as_np=False):
    tensor = np.empty(shape, dtype=np.float32)

    seed = seed or random.randint(1, 65536)

    generator = fn.Noise()
    generator.frequency = freq[0] * .0005
    generator.noiseType = fn.NoiseType.Simplex
    generator.fractal.octaves = 1

    start = [0, 0, int(time * min(shape[0], shape[1]) * speed)]

    channel_shape = [shape[0], shape[1], 1]

    for channel in range(shape[2]):
        generator.seed = seed + channel
        tensor[:, :, channel] = tf.squeeze((generator.genAsGrid(channel_shape, start=start) + 1.0) * 0.5)

    if not as_np:
        tensor = tf.stack(tensor)

    return tensor