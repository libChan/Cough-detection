import logging

import pyaudio
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
from real_time_detection.doa import DoAEstimation
import threading
from queue import Queue
import collections
import wave
from pyAudioAnalysis import audioTrainTest as aT
from pydub import silence
from pydub import AudioSegment
import pyroomacoustics as pra
import warnings
import pylab
warnings.filterwarnings("ignore")


class AudioStream(object):
    def __init__(self):
        threading.Thread.__init__(self)
        self.log_init()
        self.quit_event = threading.Event()
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 7
        self.queue = Queue()
        self.RATE = 16000
        self.CHUNK = self.RATE / 100
        self.p = pyaudio.PyAudio()
        self.frames = list()
        for i in range(0, self.CHANNELS):
            self.frames.append([])
        device_index = self.find_device_index()
        if device_index < 0:
            print('No Azure Kinect found')
            sys.exit(1)

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  start=False,
                                  input_device_index=device_index,
                                  frames_per_buffer=int(self.CHUNK),
                                  stream_callback=self._callback)

    def _callback(self, in_data, frame_count, time_info, status):
        self.queue.put(in_data)
        return None, pyaudio.paContinue

    def start(self):
        self.queue.queue.clear()
        self.stream.start_stream()

    def read_chunks(self):
        self.quit_event.clear()
        while not self.quit_event.is_set():
            frames = self.queue.get()
            if not frames:
                break
            frames = np.fromstring(frames, dtype='int16')
            yield frames

    def stop(self):
        self.quit_event.set()
        self.stream.stop_stream()
        self.queue.put('')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        if value:
            return False
        self.stop()

    def find_device_index(self):
        found = -1
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            name = dev['name']
            if name.find('Azure') >= 0 and dev['maxInputChannels'] > 0:
                found = i
                print("------Azure Kinect Index:", i, "------")
                break
        return found

    def record(self, sege):
        for i in range(0, int(self.RATE / self.CHUNK * sege)):
            # convert string to numpy array
            data_array = np.fromstring(self.stream.read(self.CHUNK), dtype='int16')
            for j in range(0, self.CHANNELS):
                channel = data_array[j::self.CHANNELS]
                self.frames[j].append(channel)

    def run(self):
        while True:
            self.record(8)
            self.mic.doa(np.array(self.frames))
        pass

    def write(self, chunk):
        for i in range(self.CHANNELS):
            wf = wave.open('./data/kinect' + str(i) + '.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(chunk[i::self.CHANNELS]))
            wf.close()

    def log_init(self):
        self.logger = logging.getLogger('Automatic Cough location and detection')
        self.logger.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s][%(thread)d][%(levelname)s] ---- %(message)s')
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)


if __name__ == '__main__':
    print(' -- init doa estimation')
    cnt = 0
    sum = 0
    doa = DoAEstimation()
    history = collections.deque(maxlen=400)
    initial = time.time()
    with AudioStream() as mic:
        t0 = time.time()
        for chunk in mic.read_chunks():
            history.append(chunk)
            if time.time() - t0 > 2:
                cnt += 1
                t0 = time.time()
                start = time.time()
                mic.logger.info('############################################')
                frame = []
                for i in range(7):
                    frame.append([])
                for i in range(7):
                    frame[i].append(np.concatenate(history)[i::7])
                a = np.concatenate(frame)
                signal = frame[0][0]
                seg = AudioSegment(data=b''.join(signal), sample_width=2, frame_rate=mic.RATE, channels=1)
                pylab.plot(np.arange(len(signal)) / mic.RATE, signal)
                pylab.axis([0, 4, -2000, 2000])
                pylab.savefig('audio.png', dpi=50)
                pylab.close('all')
                index = silence.detect_nonsilent(seg, silence_thresh=-50)

                if len(index) != 0:
                    doa.doa(a)
                    mic.logger.info('SRP-PHAT estimate azimuth:'+ str(doa.azimuth / np.pi * 180.)+ 'degrees')
                    res = aT.wav_classification(signal, 16000, "../svmSMtemp", "svm_rbf")
                    if res[0] == -1:
                        pass
                    elif res[1][0] - res[1][1] > 0.3:
                        mic.logger.info('Cough')
                    else:
                        mic.logger.info('nonCough')
                else:
                    mic.logger.info('silent')
                end = time.time()
                sum += (end-start)
                mic.logger.info("Total run time: "+str("%.2f" % (time.time()-initial))+"s |Mean process time: " + str("%.2f" % (sum/cnt))+'s')
