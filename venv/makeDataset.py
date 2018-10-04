import numpy as np, os, configparser
import osuT as o
import parseAudio, parseMap

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
