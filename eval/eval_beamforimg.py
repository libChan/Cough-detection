"""
Beamforming evaluation.
Set the cough sound as interest signal, white noise as interference signal.
Compute the time domain MVDR filter.
Output: SNR before and after MVDR filter processing.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pyroomacoustics as pra
from mir_eval.separation import bss_eval_sources

# Some simulation parameters
Fs = 8000
t0 = 1. / (Fs * np.pi * 1e-2)  # starting time function of sinc decay in RIR response
absorption = 0.1
max_order_sim = 2
sigma2_n = 5e-7

# Microphone array design parameters
mic1 = np.array([10, 10])  # position
M = 8  # number of microphones
d = 0.08  # distance between microphones
phi = 0.  # angle from horizontal
max_order_design = 1  # maximum image generation used in design
Lg_t = 0.100  # Filter size in seconds
Lg = np.ceil(Lg_t * Fs)  # Filter size in samples
delay = 0.  # Beamformer delay in seconds

# Define the FFT length
N = 1024

# Create a microphone array
R = pra.circular_2D_array(mic1, M, phi, d * M / (2 * np.pi))

rate1, signal1 = wavfile.read('./data/audioset_40fIOkLK3j4_65_70.wav')  # cough sound
print(rate1)
signal1 = np.array(signal1, dtype=float)
signal1 = pra.normalize(signal1)
signal1 = pra.highpass(signal1, Fs)

rate2, signal2 = wavfile.read('./result/noise.wav')     # white noise
print(rate2)
signal2 = np.array(signal2, dtype=float)
signal2 = pra.normalize(signal2)
signal2 = pra.highpass(signal2, Fs)


def beamforming(para):
    with open('./result/beamforming_eval_noise_5m.txt', 'w') as f:
        for i in para:
            # Create the room
            room_dim = [20, 20]
            room1 = pra.ShoeBox(
                room_dim,
                absorption=absorption,
                fs=Fs,
                t0=t0,
                max_order=max_order_sim,
                sigma2_awgn=sigma2_n)

            good_source = mic1 + i[1] * np.r_[np.cos(i[0]), np.sin(i[0])]   # interest signal
            interferer = mic1 + i[3] * np.r_[np.cos(i[2]), np.sin(i[2])]    # interference signal
            room1.add_source(good_source, signal=signal1)
            room1.add_source(interferer, signal=signal2)

            # add mic array
            mics = pra.Beamformer(R, Fs, N=N, Lg=Lg)
            room1.add_microphone_array(mics)
            room1.compute_rir()
            room1.simulate()
            # compute beamforming filters
            mics.rake_mvdr_filters(room1.sources[0][0:1],
                                   room1.sources[1][0:1],
                                   sigma2_n * np.eye(mics.Lg * mics.M))

            # process the signal
            output = mics.process()

            input_mic = pra.normalize(pra.highpass(mics.signals[mics.M // 2], Fs))
            out_DirectMVDR = pra.normalize(pra.highpass(output, Fs))

            # compute the sdr(=snr in beamforming)
            sdr_1, sir, sar, perm = bss_eval_sources(signal1, out_DirectMVDR[:len(signal1)])
            sdr_2, sir, sar, perm = bss_eval_sources(signal1, input_mic[:len(signal1)])

            f.write(str(i[0]) + '\t' + str(i[1]) + '\t' + str(i[2]) + '\t' + str(i[3]) + '\t' + str(
                sdr_1[0] - sdr_2[0]) + '\n')
            print(i)
    f.close()


test = []
with open('./result/beamforming.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')
        test.append([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3])])

beamforming(test)
