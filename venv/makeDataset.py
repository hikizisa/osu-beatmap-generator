import numpy as np, os, configparser
import osuT as o
import parseAudio, parseMap

# this is a mainscript for making training dataset

def sortDifficulty(listBeatmap):
    pass

def makeTrainData(beatmap):
    parseMap.readFile(beatmap)

def getListnpy():
    config = configparser.ConfigParser()
    config.read("automapper.cfg")
    listBeatmap = np.load(os.path.join(config.get('ReadSongs','savename')) + 'songlist.npy')
    return listBeatmap

def main():
    listBeatmap = getListnpy().tolist()

    config = configparser.ConfigParser()
    config.read("automapper.cfg")

    for beatmap in listBeatmap:
        dataset = makeTrainData(beatmap)
        title = dataset.title
        id = str(dataset.id)
        nplist = np.array(dataset)
        np.save(os.path.join(config.get('MakeDataset','dataset') + title + id + '.npy'), nplist)

