import numpy
import pyaudio
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation

""" Globals for params """
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

fig = plt.figure()

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=2,
    frames_per_buffer=CHUNK
)
# Nadpisać używając tego: https://stackoverflow.com/questions/23856990/cant-save-matplotlib-animation
plt.rcParams['animation.ffmpeg_path'] = "C:\\Users\\Majkeliusz PC\\Desktop\\ffmpeg-20200417-889ad93-win64-static\\ffmpeg-20200417-889ad93-win64-static\\bin\\ffmpeg.exe"

def updatefig(i):
    data = stream.read(CHUNK, exception_on_overflow=False)
    data_int = numpy.array(struct.unpack(str(2 * 1024) + 'B', data), dtype='b')[::2] + 128

    fig.clear()
    p = plt.plot(data_int)
    plt.draw()
    return p


anim = animation.FuncAnimation(fig, updatefig, frames=200, interval=20, blit=True)

FFwriter = animation.FFMpegWriter()

# My output directory was "C:\Documents\", changes as needed.
# First save the mp4
anim.save(r'C:\Users\Majkeliusz PC\Dropbox\ProgrammingProjects\audio_visualization\basic_animation.mp4', writer=FFwriter)

# Now save the gif
anim.save(r'C:\Users\Majkeliusz PC\Dropbox\ProgrammingProjects\audio_visualization\basic_animation.gif', writer='imagemagick')
