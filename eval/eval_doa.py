import itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
import pyroomacoustics as pra
from pyroomacoustics.doa import circ_dist

# algoithms parameters
c = 343.  # speed of sound
fs = 16000  # sampling frequency
nfft = 256  # FFT size
freq_bins = np.arange(5, 60)  # FFT bins to use for estimation

# ############################# sources ###########################
fs1, signal_1 = wavfile.read("./data/arctic_a0010.wav")
fs2, signal_2 = wavfile.read("./data/cmu_arctic_us_aew_a0002.wav")
# print(fs1, fs2)
signal = [signal_1, signal_2]


# ##############################################add mic array###################################################
def circular_2d_array(center, n, r):
    phi = np.arange(n - 1) * 2. * np.pi / (n - 1)
    return np.hstack((center[:, np.newaxis], np.array(center)[:, np.newaxis] + \
                      r * np.vstack((np.sin(phi), np.cos(phi)))))


azimuth = []
distance = []
with open('./data/doa.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')
        azimuth.append([float(temp[0]) / 180. * np.pi, float(temp[2]) / 180. * np.pi])
        distance.append([float(temp[1]), float(temp[3])])
f.close()

f = open('./result/doa_eval_2doa.txt', 'w')


def loop(azimuth, distance, snr):
    """
    evaluate the impact of different sources' azimuth and distance on DoA estimation, as well as SNR.
    :param azimuth: list of sources' azimuth
    :param distance: list of sources' distance
    :param snr: signal to noise ratio
    """
    room_dim = np.r_[10., 10.]
    room = pra.ShoeBox(room_dim, fs=fs, max_order=2, absorption=0.1)

    R = circular_2d_array(room_dim / 2, 7, 0.0425)  # Kinect mic array location
    room.add_microphone_array(pra.MicrophoneArray(R, room.fs))

    # add signals
    for i in range(len(azimuth)):
        source = room_dim / 2 + distance[i] * np.r_[np.cos(azimuth[i]), np.sin(azimuth[i])]
        room.add_source(source, signal=signal[i])

    # run the simulation
    room.simulate(snr)

    ################################
    # Compute the STFT frames needed
    X = np.array([
        pra.stft(signal, nfft, nfft // 2, transform=np.fft.rfft).T
        for signal in room.mic_array.signals])

    # MUSIC
    music = pra.doa.MUSIC(R, fs, nfft, c=c, max_four=2)
    music.locate_sources(X, num_src=len(azimuth), freq_bins=freq_bins)

    # SRP-PHAT
    srp = pra.doa.SRP(R, fs, nfft, c=c, max_four=2)
    srp.locate_sources(X, num_src=len(azimuth), freq_bins=freq_bins)
    srp.polar_plt_dirac(azimuth_ref=np.array(azimuth))

    def calculate_error(y, pre):
        res = []
        for elem in itertools.permutations(pre, len(pre)):
            res.append(np.mean(np.array(abs(np.array(y) - np.array(elem)))))
        return np.min(res)

    pre_music = music.azimuth_recon / np.pi * 180.  # estimation result of MUSIC
    pre_srp = srp.azimuth_recon / np.pi * 180.      # estimation result of SRP-PHAT
    y = np.array(azimuth) * 180. / np.pi
    # calculate the estimation error
    err_music = calculate_error(y, pre_music)
    err_srp = calculate_error(y, pre_srp)
    if y[0] == 0:
        y[0] = 360.
        temp_music = calculate_error(y, pre_music)
        temp_srp = calculate_error(y, pre_srp)
        err_music = temp_music if temp_music < err_music else err_music
        err_srp = temp_srp if temp_srp < err_srp else err_srp
        y[0] = 0.
    print('---------------------------------------------------')
    print(len(srp.grid.values))
    print('|snr: ', snr, '|MUSIC: %.2f' % err_music, '|SRP: %.2f' % err_srp)
    print('True azimuth:', y)
    print('MUSIC estimate azimuth:', music.azimuth_recon / np.pi * 180.)
    print('SRP estimate azimuth:', srp.azimuth_recon / np.pi * 180., 'degrees')
    f.write(str("%.2f" % y[0]) + '\t' + str("%.2f" % distance[0]) + '\t' + str(
        "%.2f" % y[1]) + '\t' + str("%.2f" % distance[1]) + '\t' + str("%.2f" % err_music)
            + '\t' + str("%.2f" % err_srp) + '\n')
    # f.write(str(snr) + '\t' + str("%.2f" % err_music)
    #         + '\t' + str("%.2f" % err_srp) + '\n')


# for snr in range(-20, 35, 5):
#     for i in range(len(azimuth)):
#         loop(azimuth[i], distance[i], snr)
for i in range(len(azimuth)):
        loop(azimuth[i], distance[i], 30.)

f.close()
