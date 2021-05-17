import re
import shutil
import os

def getUniqueTraceCrashes(crashes):
    uniquetraces = []
    uniquecrashobjs = []
    for crash in crashes:
        if crash.mintrace not in uniquetraces:
            uniquecrashobjs.append(crash)
            uniquetraces.append(crash.mintrace)
    return uniquecrashobjs

def processExtractedCrashes(crashes, outputdir):
    uniquecrashes = getUniqueTraceCrashes(crashes)
    fdunique = open(outputdir + "/unique_crashes", "wb")
    for crash in uniquecrashes:
        fdunique.write(crash.content + b"\n" + crash.stderr + b"\n")
        shutil.copy(crash.filepath, outputdir + '/CrashesDeduplicated/' + re.sub('.*/', '', crash.filepath).replace(":", "_"))
    fdunique.close()
    return uniquecrashes

def processExtractedHangs(hangs, outputdir):
    for hang in hangs:
        shutil.copy(hang.filepath, outputdir + '/Hangs/' + re.sub('.*/', '', hang.filepath).replace(":", "_"))

def processUniqueMinCrashes(crashes, outputdir):
    unique_inputs = []
    fdunique = open(outputdir + "/unique_min_crashes", "wb")
    for crash in crashes:
        if crash.content not in unique_inputs:
            unique_inputs.append(crash.content)
            fdunique.write(crash.content + b"\n" + crash.stderr + b"\n")
            crash.unique = True
        else:
            os.remove(crash.filepath)
    fdunique.close()
    return crashes

def processUniqueMinHangs(hangs, outputdir):
    # Open file to write all unique minimized hangs to for an overview
    fdunique = open(outputdir + "/unique_min_hangs", "wb")
    unique_hangs = []
    for h in hangs:
        if h.content not in unique_hangs:
            fdunique.write(h.content + b"\n")
            of = open(outputdir + "/HangsDeduplicatedMinimized/" + re.sub('.*/', '', h.filepath).replace(":", "_"), "wb")
            of.write(h.content)
            of.close()
            unique_hangs.append(h.content)
            h.unique = True
    return hangs