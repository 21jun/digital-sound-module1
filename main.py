import scipy.io.wavfile as wf
import numpy as np
from pathlib import Path
from math import cos, sin, pi, sqrt

MAX = 0
QMAX = 32000.0

def cosine_function(t):
    lch = (cos(float(t) / (16000 * 2) * pi - (pi ) * 4.0 / 5.0) + 1) / 2.0
    rch = (cos(float(t) / (16000 * 2) * pi + (pi ) * 4.0 / 5.0) + 1) / 2.0
    global MAX
    global QMAX
    lch *= QMAX / MAX
    rch *= QMAX / MAX
    return lch, rch


def euclidean(t):
    r, h = 5, 3
    x = cos(t / (16000.0 * 2) * pi + pi/2.0) * float(r)
    y = sin(t / (16000.0 * 2) * pi + pi/2.0) * float(r)
    euclidean.max = sqrt(h ** 2 + r ** 2) + r
    euclidean.min = sqrt(h ** 2 + r ** 2) - r

    lx, ly = -h, -r
    rx, ry = h, -r

    ldist = np.sqrt((x - lx) ** 2 + (y - ly) ** 2)
    rdist = np.sqrt((x - rx) ** 2 + (y - ry) ** 2)

    lch = 1 - ldist / euclidean.max
    rch = 1 - rdist / euclidean.max

    global MAX
    global QMAX
    lch *= QMAX / MAX
    rch *= QMAX / MAX

    return lch, rch


def convert(file_path, function):

    print(
        "{0:<15} converting: {1:>35} ".format(
            function.__name__, file_path.stem + ".wav ..."
        ),
        end="",
        flush=True,
    )

    rate, data = wf.read(file_path)

    if rate != 16000:
        print(f"rate is {rate}")
        return
    if data.shape[1] is not 2:
        print("file is not stereo")
        return

    left = data[:, 0]
    right = data[:, 1]
    right.setflags(write=1)
    left.setflags(write=1)

    global MAX

    MAX = left.max() if left.max() >= right.max() else right.max()

    for t in range(data.shape[0]):
        l, r = function(t)
        left[t] = left[t] * l
        right[t] = right[t] * r

    # left, right 순서로 concat
    sum = np.concatenate((left.reshape(-1, 1), right.reshape(-1, 1)), axis=1)
    wf.write(f"out/{file_path.stem}_{function.__name__}.wav", rate, sum)
    print("done")


if __name__ == "__main__":

    # 16000hz, 16bit, stereo wav files
    path = Path("music/").glob("**/*.wav")
    files = [x for x in path if x.is_file()]

    for file in files:
        convert(file_path=file, function=cosine_function)
        convert(file_path=file, function=euclidean)
