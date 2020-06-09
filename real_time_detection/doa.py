import numpy as np
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
import librosa
import pyroomacoustics as pra


class MicrophoneArray(object):
    """
    generate circular mic array locations

    r = radius
    n = channels
    """
    def __init__(self, center, n, r):
        self.center = center
        self.n = n
        self.r = r
        self.first = None

    def coordinates(self):
        phi = np.arange(self.n - 1) * 2. * np.pi / (self.n - 1)
        return np.hstack((self.center[:, np.newaxis], np.array(self.center)[:, np.newaxis] + \
                          self.r * np.vstack((np.sin(phi), np.cos(phi)))))


class DoAEstimation(object):
    """
    Doa estimation module(default algorithm is SRP-PHAT, grid size = 360)
    """
    def __init__(self):
        self.room_dim = np.r_[10., 10.]
        CHANNEL = 7
        self.nfft = 256  # FFT size
        self.fs = 16000  # sampling frequency
        Lg_t = 0.100  # Filter size in seconds
        self.Lg = np.ceil(Lg_t * self.fs)
        self.freq_bins = np.arange(5, 60)  # FFT bins to use for estimation
        mic = MicrophoneArray(self.room_dim / 2, n=CHANNEL, r=0.0425)
        self.R = mic.coordinates()
        self.azimuth = []
        self.beamformer = pra.Beamformer(self.R, self.fs, N=self.nfft, Lg=self.Lg)  # beamforming

    def doa(self, mic_signal_array, algorithm='SRP', view=True):
        X = np.array([
            pra.stft(signal, self.nfft, self.nfft // 2, transform=np.fft.rfft).T
            for signal in mic_signal_array])
        doa = pra.doa.algorithms[algorithm](self.R, self.fs, self.nfft, c=343., max_four=4)
        # this call here perform localization on the frames in X
        doa.locate_sources(X, num_src=1, freq_bins=self.freq_bins)
        self.azimuth = doa.azimuth_recon
        if view:
            doa.polar_plt_dirac()
            plt.title(algorithm)
            plt.savefig('doa.png')
            plt.close()