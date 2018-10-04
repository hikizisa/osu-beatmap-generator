import os
import osuT as o
import configparser
import subprocess as sp

# this is a main script for making audio dataset with fft

# read audio file
def readAudio(audio):
    config = configparser.ConfigParser()
    config.read("automapper.cfg")

    ffmpegDir = config.get('ParseAudio', 'ffmpeg')

def loadSongData(audio):
    readAudio(audio)
    pass

if __name__ == "__main__":
# testcode