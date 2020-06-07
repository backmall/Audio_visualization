import pyaudio
import queue
import socket
import matplotlib.pyplot as plt
import numpy
import struct
from datetime import datetime

#used for fft analysis
from math import pi
from scipy.fftpack import (
    fft,
    fft2,
    fftfreq
)
from scipy.io.wavfile import write
import wave

""" Globals for params """
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
device_index = 2
filename = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=device_index,
    frames_per_buffer=CHUNK
    )

frames = []

# Store data in chunks for 5 seconds
for i in range(0, int(RATE / CHUNK * 5)):
    print("i: ")
    print(str(i))
    data = stream.read(CHUNK)
    frames.append(data)
stream.stop_stream()
stream.close()
p.terminate()

#decoding data
data_int = numpy.array(struct.unpack(str(2 * CHANNELS * CHUNK) + 'B', data), dtype='b') + 128
decoded = numpy.frombuffer(data, numpy.int16)
#decoded = numpy.fromstring(data, 'Float32')

# signal graph
plt.subplot(2, 1, 1)
plt.plot(decoded)
plt.title('Sinusoidal Signal'); plt.xlabel('Time'); plt.ylabel('Ampltude')

#frequency magnitude graph
plt.subplot(2, 1, 2)
data_fft = abs(fft(decoded))
freqs = fftfreq(len(data_fft), (1.0/RATE))
#plt.plot(freqs[range(len(data_fft)//2)], data_fft[range(len(data_fft)//2)])
plt.plot(freqs, abs(data_fft))
plt.title('Magnitude Spectrum'); plt.xlabel('Frequency'); plt.ylabel('Magnitude')

#show both plots
plt.show()

#data_fft2 = fft2(decoded)
#plt.plot(data_fft2)
#plt.show()
file = open("test.txt", "w+")
file = open("test.txt", "a+")

file.write("data_int: \n")
file.write(str(data_int))
file.write("\ndata_fft: \n")
file.write(str(data_fft))

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()