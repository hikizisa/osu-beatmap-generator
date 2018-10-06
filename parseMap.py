import numpy as np
import os, configparser
import osuType as ot

# this is a script for making beatmap dataset

# check if filestream works properly


def processLine(line):
    parsed = line.split('=')
    info = parsed[0].lstrip().rstrip();
    val = parsed[1].lstrip().rstrip()
    return [info, val]


def general(f, data):
    mp3 = '' ; stackLeniency = 0.0 ; mode = 0 ; sampleSet = 1

    while True:
        line = f.readline()
        if line.startswith('['):
            break
        [info, val] = processLine(line)

        if info == 'AudioFilename': mp3 = val
        elif info == 'StackLeniency':
            try: stackLeniency = float(val)
            except SyntaxError: stackLeniency = 0.0
        elif info == 'Mode':
            try: mode = int(val)
            except SyntaxError: mode = 0
        elif info == 'SampleSet':
            if(val == 'Normal'): sampleSet = 0
            elif(val == 'Soft'): sampleSet = 1
            elif(val == 'Drum'): sampleSet = 2

    data.general(mp3, stackLeniency, mode, sampleSet)

    return line


def metadata(f, data):
    title = '' ; id = 0 ; version = ''

    while True:
        line = f.readline()
        if line.startswith('['):
            break
        [info, val] = processLine(line)

        if info == 'Title': title = val
        elif info == 'BeatmapID': id = val
        elif info == 'Version': version = val

    data.metadata(title, id, version)

    return line


def events(f, data):
    eventdata = []

    while True:
        line = f.readline()
        if line.startswith('['):
            break
        else: eventdata.append(line)

    data.events(eventdata)

    return line


def difficulty(f, data):
    hp = 5; cs = 5; od = 5; ar = -1; sm = 1.0; st = 1.0

    def tryInt(val):
        try: result = int(val)
        except SyntaxError: return 5
        return result

    while True:
        line = f.readline()
        if line.startswith('['):
            break
        [info, val] = processLine(line)

        if info == 'HPDrainRate': hp = tryInt(val)
        elif info == 'CircleSize': cs = tryInt(val)
        elif info == 'OverallDifficulty': od = tryInt(val)
        elif info == 'ApproachRate': ar = tryInt(val)
        elif info == 'SliderMultiplier':
            try: sm = float(val)
            except SyntaxError: sm = 1.0
        elif info == 'SliderTickRate':
            try: st = float(val)
            except SyntaxError: st = 1.0

    # old map doesn't have ar value, od is the ar
    if ar == -1:
        ar = od

    data.difficulty(hp, cs, od, ar, sm, st)

    return line


def timing(f, data):
    while True:
        line = f.readline()
        if line.startswith('['):
            break
        try:
            parsed = line.split(',')
            offset = int(parsed[0])
            beatlength = float(parsed[1])
            meter = int(parsed[2])
            sampleSet = int(parsed[3])
            sample = int(parsed[4])
            volume = int(parsed[5])
            inherited = int(parsed[6])
            kiai = int(parsed[7])
        except SyntaxError:
            print("Failed parsing timing line")
            continue
        data.timing(ot.BeatmapData.TimingPoint(offset, beatlength, meter, sampleSet, sample, volume, inherited, kiai))
    return line


def getnc(type):
    if type % 8 >= 4: nc = 1
    else: nc = 0

    if nc >= 1:
        nc += (type % 128) // 16

    return nc


def geths(hitsound):
    whistle = False
    finish = False
    clap = False

    if hitsound % 4 > 2: whistle = True
    if hitsound % 8 > 4: finish = True
    if hitsound % 16 > 8: clap = True

    return ot.Hitsound(whistle, finish, clap)


def gethsinfo(data):
    extras = data.split(':')

    try:
        sampleSet = int(extras[0])
        additionSet = int(extras[1])
        customIndex = int(extras[2])
        sampleVolume = int(extras[3])
        filename = extras[4]

    except SyntaxError:
        print("Failed parsing extras")

    return ot.Hsinfo(sampleSet, additionSet, customIndex, sampleVolume, filename)



def hitobjects(f, data):
    while True:
        line = f.readline()
        if line.startswith('['):
            break

        try:
            parsed = line.split(',')
            x = int(parsed[0])
            y = int(parsed[1])
            time = int(parsed[2])
            type = int(parsed[3])
            hs = int(parsed[4])

            nc = getnc(type)
            hitsound = geths(hs)

            # create object of the type
            if type % 2 >= 1:
                # Create Circle
                hsinfo = gethsinfo(parsed[5])
                obj = ot.Circle(x, y, time, hitsound, nc, hsinfo)

            elif type % 4 >= 2:
                # Create Slider
                pass

            elif type % 16 >= 8:
                # Create Spinner
                pass

            elif type % 256 >= 128:
                # Create Hold Note
                continue

            else: continue

            data.objects.append(obj)

        except SyntaxError:
            print("Failed parsing objects")
            continue

    return line


def findHeader(header):
    return header[1:len(header)-2]


def processHeader(header, f, data):
    if header == 'General':
        line = general(f, data)

    # Editor, Events info doesn't seem to be useful for training.

    # elif header == 'Editor':
    #    line = editor(f, data)
    elif header == 'Events':
        line = events(f, data)
    elif header == 'Metadata':
        line = metadata(f, data)
    elif header == 'Difficulty':
        line = difficulty(f, data)
    elif header == 'TimingPoints':
        line = timing(f, data)
    elif header == 'HitObjects':
        line = hitobjects(f, data)
    else:
        pass

    # do I have to return file object?
    return line


def readFile(osu):
    f = open(osu, 'r')

    version = f.readline()
    data = ot.BeatmapData()

    data.setVersion(version)

    line = f.readline()
    while True:
        if not line: break
        if line.startswith('['):
            header = findHeader(line)
        else:
            line = f.readline()
            continue

        line = processHeader(header,f,data)

    f.close()


if __name__ == "__main__":
    pass
