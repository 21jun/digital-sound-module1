import scipy.io.wavfile as wf
import numpy as np
from pathlib import Path
# 16000hz, 16bit, stereo wav file
path = Path("music/Post Malone - Die For Me Ft. Halsey, Future.wav")

rate, data = wf.read(path)

left = data[:, 0]
right = data[:, 1]
# right.flags : default setting is read-only 
right.setflags(write=1)

# 오른쪽 체널 1분간 음소거 (16000hz * 60 sec)
for i in range(16000*60):
    right[i] = 0

# left, right 순서로 concat
sum = np.concatenate((left.reshape(-1,1), right.reshape(-1,1)),axis =1)
wf.write('out/sum.wav', rate, sum)