import numpy as np
import os, configparser
import osuT as o
import parseAudio as pA
import parseMap as pM

# this is a mainscript for making training dataset

def sortDifficulty(listBeatmap):
    pass

def makeTrainData(beatmap):
    pass

def getListnpy():
    config = configparser.ConfigParser()
    config.read("automapper.cfg")
    listBeatmap = np.load(os.path.join(config.get('ReadSongs','savename')) + '.npy')
    return listBeatmap

def main():
    listBeatmap = getListnpy()
