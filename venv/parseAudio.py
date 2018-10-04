import os
import osuT as o
import configparser
import subprocess as sp

# this is a main script for making audio dataset with fft

# convert mp3 file to wav file
def toWav(audio):
    if os.path.isfile(audio) == False:
        raise Exception("failed to load audio : " + audio)

    config = configparser.ConfigParser()
    config.read("automapper.cfg")

    ffmpegDir = config.get('ParseAudio', 'ffmpeg')
    wav = ('.').join(audio.split('.')[:-1]) + '.wav'

    ffmpeg = os.path.join(ffmpegDir,'ffmpeg.exe')
    if os.path.isfile(ffmpeg) == False:
        raise Exception("failed to find ffmpeg")

    p = sp.Popen([ffmpeg, '-i', audio, wav], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

    if os.path.isfile(wav) == False:
        raise Exception('error occurred while converting : ' + audio + '\n')

def loadSongData(audio):
    pass

if __name__ == "__main__":
    pass
# testcode