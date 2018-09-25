import numpy as np
import sys, os, time

#returns list of files in dir
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

#get path of .py file
curdir = os.path.dirname(os.path.abspath(__file__))
#path to song folder
songsdir = "../songs"
#map np array file name
savename = "../maplist"

saveosulist(getosulist(songsdir), os.path.join(curdir, savename))

print(np.load(savename+'.npy'))