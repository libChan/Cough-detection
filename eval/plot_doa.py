"""
plot the result of DoA estimation.
"""
import matplotlib.pyplot as plt

azimuth = []
distance = []
music = []
srp = []
with open('eval/doa_eval_2doa.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')
        azimuth.append([float(temp[0]), float(temp[2])])
        distance.append([float(temp[1]), float(temp[3])])
        music.append(float(temp[4]))
        srp.append(float(temp[5]))

x = [i[1] for i in azimuth]
plt.plot(x, music, marker='.', color='b', label='music')
plt.plot(x, srp, marker='.',color='r', label='srp')
for a, b in zip(x, srp):
    plt.text(a, b+1, b, ha='center', va='bottom', fontsize=8)
for a, b in zip(x, music):
    plt.text(a, b - 4, b, ha='center', va='bottom', fontsize=8)
plt.xlabel('DoA(°)')
plt.ylabel('DoA error')
plt.title('2 sources DoA estimation')
plt.legend(loc='upper right')
plt.show()