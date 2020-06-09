import matplotlib.pyplot as plt
import numpy as np


def plot_svm_eval():
    c = []
    cough = []
    non_cough = []
    all = []
    for line in open('./result/svm.txt'):
        tmp = line.split('\t')
        c.append(tmp[0])
        cough.append([float(tmp[1]), float(tmp[2]), float(tmp[3])])
        non_cough.append([float(tmp[4]), float(tmp[5]), float(tmp[6])])
        all.append([float(tmp[7]), float(tmp[8])])

    fig = plt.figure()
    fig.suptitle('SVM_RBF Parameter Evaluation')
    ax1 = fig.add_subplot(2, 2, 1)

    ax1.plot(c, [i[0] for i in cough], color='b', label='Precision', marker='.')
    ax1.plot(c, [i[1] for i in cough], color='g', label='Recall', marker='x')
    ax1.plot(c, [i[2] for i in cough], color='r', label='F1', marker='o')
    for a, b in zip(c, [i[0] for i in cough]):
        plt.text(a, b-7, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(c, [i[1] for i in cough]):
        plt.text(a, b+2, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(c, [i[2] for i in cough]):
        plt.text(a, b-3, b, ha='center', va='bottom', fontsize=10)

    ax1.set_xlabel('C parameter')
    ax1.legend(loc='lower right')
    ax1.set_title('cough')

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(c, [i[0] for i in non_cough], color='b', label='Precision', marker='.')
    ax2.plot(c, [i[1] for i in non_cough], color='g', label='Recall', marker='x')
    ax2.plot(c, [i[2] for i in non_cough], color='r', label='F1', marker='o')
    for a, b in zip(c, [i[0] for i in non_cough]):
        plt.text(a, b-0.6, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(c, [i[1] for i in non_cough]):
        plt.text(a, b-0.6, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(c, [i[2] for i in non_cough]):
        plt.text(a, b-0.6, b, ha='center', va='bottom', fontsize=10)
    ax2.set_xlabel('C parameter')
    ax2.legend(loc='lower right')
    ax2.set_title('non_cough')

    ax3 = fig.add_subplot(2, 1, 2)
    ax3.plot(c, [i[0] for i in all], color='b', label='ACC')
    ax3.plot(c, [i[1] for i in all], color='g', label='F1')
    ax3.set_xlabel('C parameter')
    for a, b in zip(c, [i[0] for i in all]):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(c, [i[1] for i in all]):
        plt.text(a, b-4.5, b, ha='center', va='bottom', fontsize=10)

    ax3.legend(loc='lower right')
    ax3.set_title('Overall')
    plt.show()


def plot_linear_vs_rbf():
    fig = plt.figure()
    plt.title('rbf vs linear with best c')
    name = ['ACC', 'F1']
    y1 = [95.3, 95.3]
    y2 = [91.7, 91.7]
    x = np.arange(2)
    width = 0.2
    plt.bar(x+width, y1, width, color='b', align='center', label='rbf', alpha=0.5)
    plt.bar(x, y2, width, color='c', align='center', label='linear', alpha=0.5)

    plt.ylim(80, 100)

    plt.legend(loc='upper right')
    plt.xticks(x+width/2, name)
    plt.show()


def plot_eval_score():
    fig = plt.figure()
    plt.title('Test of SVM_RBF')
    x = range(5)
    y = [0.87, 0.84, 0.91, 0.91, 0.83]
    plt.bar(x[0], y[0], 0.5, color='blue', align='center', label='acc', alpha=0.5)
    plt.bar(x[1], y[1], 0.5, color='red', align='center', label='pre', alpha=0.5)
    plt.bar(x[2], y[2], 0.5, color='orange', align='center', label='rec', alpha=0.5)
    plt.bar(x[3], y[3], 0.5, color='springgreen', align='center', label='sen', alpha=0.5)
    plt.bar(x[4], y[4], 0.5, color='purple', align='center', label='spe', alpha=0.5)
    plt.text(x[0],y[0], y[0], ha='center', va='bottom', fontsize=10)
    plt.text(x[1],y[1], y[1], ha='center', va='bottom', fontsize=10)
    plt.text(x[2],y[2], y[2], ha='center', va='bottom', fontsize=10)
    plt.text(x[3],y[3], y[3], ha='center', va='bottom', fontsize=10)
    plt.text(x[4],y[4], y[4], ha='center', va='bottom', fontsize=10)
    plt.ylim(0.5, 1)
    plt.legend(loc='upper right')
    plt.show()


if __name__ == '__main__':
    plot_svm_eval()
    # plot_linear_vs_rbf()
    # plot_eval_score()