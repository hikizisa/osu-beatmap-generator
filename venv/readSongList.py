import numpy as np
import os, configparser

# this script is a script to get song lists from given folder

def getosulist(dir):
    #if there's no song folder, create one
    if not (os.path.isdir(dir)):
        os.makedirs(os.path.join(dir))
    files = os.listdir(dir)
    listfile = []
    for file in files:
        dirfile = os.path.join(dir, file)
        if os.path.isdir(dirfile):
            indirosu = getosulist(dirfile)
            listfile = listfile + indirosu
        else:
            ext = os.path.splitext(dirfile)[-1]
            if ext == '.osu':
                listfile.append(dirfile)
    return listfile

def saveosulist(list, outputfile):
    nplist = np.array(list)
    np.save(outputfile, nplist)

def main():
    config = configparser.ConfigParser()
    config.read("automapper.cfg")

    osuList = getosulist(config.get('ReadSongs', 'songsdir'))
    savePath = os.path.join(config.get('ReadSongs','savename'))
    saveosulist(osuList, savePath)

    print(np.load(savePath+'.npy'))