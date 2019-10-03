import scipy.io.wavfile as wf
import numpy as np
from pathlib import Path
from math import cos, pi

def cosine_function(t):
    left = (cos(float(t) / (16000 * 2) * pi + pi * 2.0 / 3.0) + 1) / 2.0
    right= (cos(float(t) / (16000 * 2) * pi - pi * 2.0 / 3.0) + 1) / 2.0
    
    return left, right

def EUD_function(t):
    pass

def convert(file_path, function):
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

    for t in range(data.shape[0]):
        l, r = function(t)
        left[t] = left[t] * l
        right[t] = right[t] * r

    # left, right 순서로 concat
    sum = np.concatenate((left.reshape(-1, 1), right.reshape(-1, 1)), axis=1)
    wf.write("out/" + file_path.stem + ".wav", rate, sum)


if __name__ == "__main__":

    # 16000hz, 16bit, stereo wav files
    path = Path("music/").glob("**/*.wav")
    files = [x for x in path if x.is_file()]

    for file in files:
        print(f"converting : {file.stem}.wav ...", end='')
        convert(file_path=file, function=cosine_function)
        print(f"[done]")
