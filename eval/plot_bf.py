import matplotlib.pyplot as plt
import numpy as np

dic_3 = {}
dic_5 = {}
dic_10 = {}


def read(dic, x):
    with open('./result/beamforming_eval_'+x+'m.txt', 'r')as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split('\t')
            if float(temp[3]) in dic.keys():
                dic[float(temp[3])].append(float(temp[4]))
            else:
                dic[float(temp[3])] = [float(temp[4])]
    f.close()
    for key in dic.keys():
        temp = np.mean(dic[key])
        dic[key] = temp
    print(dic)


read(dic_3, '3')
read(dic_5, '5')
read(dic_10, '10')

figure = plt.figure()
x = list(dic_3.keys())
y_3 = list(dic_3.values())
y_5 = list(dic_5.values())
y_10 = list(dic_10.values())
plt.plot(x, y_3, color='b', label='3m')
plt.plot(x, y_5, color='g', label='5m')
plt.plot(x, y_10, color='r', label='10m')

plt.xlabel("interference source distance(m)")
plt.ylabel("SNR Gain(dB)")
plt.title("interference: speak")
plt.legend(loc='upper right')

plt.show()




