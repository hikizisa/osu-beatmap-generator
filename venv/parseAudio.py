import os, configparser
import scipy.io.wavfile as wavfile, scipy
import subprocess as sp, numpy as np

# this is a main script for making audio dataset with fft

def findffmpeg():
    config = configparser.ConfigParser()
    config.read("automapper.cfg")

    ffmpegDir = config.get('ParseAudio', 'ffmpeg')
    ffmpeg = os.path.join(ffmpegDir,'ffmpeg.exe')
    if os.path.isfile(ffmpeg) == False:
        raise Exception("Failed to find ffmpeg")
    else:
        return ffmpeg

# convert mp3 file to wav file
def toWav(audio):
    if os.path.isfile(audio) == False:
        raise Exception("Failed to load audio : " + audio)
    wav = ('.').join(audio.split('.')[:-1]) + '.wav'

    p = sp.Popen([findffmpeg(), '-i', audio, wav], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    return wav

# make array of wave data from wav file
def dataWav(wav):
    if os.path.isfile(wav) == False:
        raise Exception("Couldn't find wav file : " + wav)

    data = wavfile.read(wav)[1]

    return data

# make fft result for given timing point(ms).
# stft for entire data takes so long time.
def doFft(data, time):
    config = configparser.ConfigParser()
    config.read("automapper.cfg")
    try:
        samples = int(config.get('ParseAudio', 'samples'))
    except SyntaxError:
        samples = 1000

    # Samplerate = 44100/s
    timeframe = int(44.1*time)

    ftdata = []
    for i in range(0, int(samples/2), 1):
        ftdata.append(scipy.fft(data[timeframe - int(samples/2) + i : timeframe + int(samples/2) + i]))

    # Array consists of data for each frequency, tuple of data for each channel.
    return ftdata

def loadSongData(audio):
    return dataWav(toWav(audio))

if __name__ == "__main__":
    pass
# testcode