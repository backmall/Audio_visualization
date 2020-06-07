"""
Client for audio_visualization.

This is to be run on the device that has the audio playback device
"""
import queue
import socket
import matplotlib.pyplot as plt
import numpy
import struct
import matplotlib.animation as animation
from numpy import isnan
from datetime import datetime
from threading import (
    Thread,
    Lock
)
#used for fft analysis
from math import pi
from scipy.fftpack import (
    fft,
    fft2
)
from scipy.io.wavfile import write
import wave

from main import (
    read_from_device,
)

HOST = "127.0.0.1"
PORT = 42069

lock = Lock()

def run_client(data_queue):
    address_port = (HOST, PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Started client. Connecting to {address_port}")
        s.connect(address_port)
        print("Connected")

        file = open("test.txt", "w+")
        count = 0

        #fig, ax = plt.subplots(1, figsize=(15,7))
        #x = numpy.arange(0, 2 * 1024, 2)
        #line, = ax.plot(x, numpy.random.rand(1024))
        #ax.set_ylim(0, 255)
        #ax.set_xlim(0, 1024)

        frames = []

        while True:
            try:
                with lock:
                    data = data_queue.get()
                    #print(f"Got data: {data}")
                    frames.append(data)

                if data == "":
                    break
                else:
                    # TODO: Provide the data from playback device
                    s.sendall(data)

            except Exception as error:
                print(f"EXCEPTION: {error}")

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            file = open("test.txt", "a+")

            data_int = numpy.array(struct.unpack(str(2 * 1024) + 'B', data), dtype='b') + 128
            # line.set_ydata(data_int)
            # fig.canvas.draw()
            # fig.canvas.flush_events()
            # decoded = numpy.fromstring(data, 'Float32')

            print("_______")
            print(len(data_int))  # array length
            print(str(data_int))

            file.write(str(data_int))
            file.write("\n")

            # plot decoded data
            # decoded = numpy.fromstring(data, numpy.int16)
            # decoded = numpy.fromstring(data, 'Float32')

            plt.plot(data_int)
            plt.show()
            plt.clf()
            plt.close()

            count += 1
            wf = wave.open("output.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(1024)
            wf.writeframes(b''.join(frames))
            wf.close()
    print("Connection closed")


if __name__ == "__main__":
    data_queue = queue.Queue()

    thread_audio = Thread(target=read_from_device, args=(2, data_queue))
    thread_client = Thread(target=run_client, args=(data_queue,))

    with lock:
        thread_client.start()
        thread_audio.start()

    print("Started both threads")
