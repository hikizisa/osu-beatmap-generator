import numpy as np
import os, configparser
import osuT as o
import makeDataset,readSongList

# This is a main script that automatically makes dataset according to given configuration.

readSongList.main()
makeDataset.main()