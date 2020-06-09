import numpy as np
import matplotlib.pyplot as plt

snr = []
music = []
srp = []
with open('eval/doa_eval_2doa.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')
        snr.append(float(temp[0]))
        music.append(float(temp[1]))
        srp.append(float(temp[2]))
plt.plot(snr, music, color='b', marker='.', label='music')
plt.plot(snr, srp, color='r', marker='.', label='srp')

for a, b in zip(snr, music):
    plt.text(a, b-5, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(snr, srp):
    plt.text(a, b+1, b, ha='center', va='bottom', fontsize=10)
plt.xlabel('SNR(dB)')
plt.ylabel('DoA error')
plt.title('SNR in DoA estimation')
plt.legend(loc='upper right')
plt.show()