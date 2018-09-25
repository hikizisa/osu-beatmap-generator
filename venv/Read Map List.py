import numpy as np
import os

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

#get path of .py file
curdir = os.path.dirname(os.path.realpath(__file__))

#relative path to song folder
reldir = "/songs"