import scipy.io.wavfile as wf
import numpy as np
from pathlib import Path
from math import cos,pi
# 16000hz, 16bit, stereo wav file
# path = Path("music/Post Malone - Die For Me Ft. Halsey, Future.wav")
# path = Path("music/helicopter2.wav")
path = Path("music/House Fire Alarm.wav")


rate, data = wf.read(path)

left = data[:, 0]
right = data[:, 1]
right.setflags(write=1)
left.setflags(write=1)

# print(rate, data.shape)

# 한바퀴 회전
for i in range(16000 * 11):
    right[i] = right[i] * (cos(float(i)/(16000*2) * pi - pi/4)+1) / 2.0
    left[i]  = left[i]  * (cos(float(i)/(16000*2) * pi + pi/4)+1) / 2.0 

# left, right 순서로 concat
sum = np.concatenate((left.reshape(-1,1), right.reshape(-1,1)),axis =1)
wf.write('out/sum.wav', rate, sum)