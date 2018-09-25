import numpy as np
import os
import pandas as pd

#returns list of files in dir
def getosulist(dir):
    files = os.listdir(dir)
    listfile = []
    for file in files:
        dirfile = os.path.join(dir, file)
        if os.path.isdir(dirfile):
            indirosu = getosulist(dirfile)
            listfile = listfile + dirfile
        else:
            ext = os.path.splitext(full_filename)[-1]
            if ext == '.osu':
                listfile.append(os.path.join(dir,file))
    return listfile

def saveosulist(list, outputfile):
    nplist = np.array(list)
    df = pd.DataFrame(np_array)
    df.to_csv(outputfile)

#get path of .py file
curdir = os.path.dirname(os.path.realpath(__file__))

#relative path to song folder
reldir = "/songs"
#map list save name
savename = "maplist" + ".csv"

filelist = getosulist(os.path.join(curdir, reldir))

outputfile = os.path.join(curdir, savename)

saveosulist(filelist, outputfile)