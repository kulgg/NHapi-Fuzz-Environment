#!/usr/bin/python3

import sys
import glob
import logging

from utils.extract import *
from utils.minimizecrashes import *
from utils.minimizehangs import *
from utils.processresults import *
from utils.init import *

exec1 = ["dotnet", "Harness/nHapi.Fuzz/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"]
execrunonce = ["dotnet", "Harness/nHapi.RunOnce/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"]
outputdir = ""
inpdir = ""
timeout = 2.0
nhangs = 1
max_threads = 4

def processInputs():
    global inpdir, outputdir, timeout, nhangs, max_threads
    # Set args
    inpdir = sys.argv[1]
    outputdir = sys.argv[2]
    if len(sys.argv) >= 4:
        timeout = float(sys.argv[3]) 
        if len(sys.argv) >= 5:
            nhangs = int(sys.argv[4])
            if len(sys.argv) == 6:
                max_threads = int(sys.argv[5])
    logging.info("Using Input dir {}".format(inpdir))
    logging.info("Using Output dir {}".format(outputdir))
    logging.info("Setting {} sec timeout".format(timeout))
    logging.info("Minimizing {} of found hangs".format(nhangs))
    logging.info("afl-tmin_max_threads = {}".format(max_threads))

def main():
    # Init Logging
    initLogging()
    # Requires at least 2 and a maximum of 5 arguments
    if(len(sys.argv) < 3 or len(sys.argv) > 6):
        logging.info("Usage:   minFindings [inputs] [output dir] (timeout=2.0) (num hangs to minimize=1) (max_afltmin_threads=4)")
        logging.info("Example: minFindings \"Crashes/id*\" MinimizedOut 1.0 2 10")
        exit(1)

    logging.info("Processing inputs")
    processInputs()
    # Make needed Dirs
    makeDirs(outputdir)
    #Get input files
    inputpaths = glob.glob(inpdir)
    if len(inputpaths) == 0:
        logging.error("No input files found")
        exit(1)
    else:
        logging.info("Found {} input files".format(len(inputpaths)))
    
    logging.info("# Phase1 # Extract unique stack trace crashes and hangs above the timeout threshold")
    crashes, hangs = extractCrashesAndHangs(inputpaths, exec1, timeout)
    uniquecrashes = processExtractedCrashes(crashes, outputdir)
    logging.info("Found {} unique trace crashes".format(len(uniquecrashes)))
    processExtractedHangs(hangs, outputdir)

    logging.info("# Phase2 # Minimizing unique crash inputs with afl-tmin")
    minuniquecrashes = minimizeUniqueCrashes(uniquecrashes, outputdir, timeout, max_threads, exec1, execrunonce)
    logging.info("# Phase3 # Deleting duplicates of minimized crashes")
    minuniquecrashesminafter = processUniqueMinCrashes(minuniquecrashes, outputdir)

    minuniquehangs = []
    minuniquehangsminafter = []
    logging.info("# Phase4 # Minimize hang inputs by removing useless blocks")
    if len(hangs) > 0 and nhangs > 0:
        minuniquehangs = minimizeHangs(hangs[:nhangs], exec1, timeout)
        minuniquehangsminafter = processUniqueMinHangs(minuniquehangs, outputdir)
    else:
        logging.info("Minimized no hangfiles")

    logging.info("Found these minimized crashes")
    for m in minuniquecrashes:
        if m in minuniquecrashesminafter:
            logging.info("UNIQUE {} {}".format(m.content, m.stderr))
        else:
            logging.info("NOT UNIQUE {} {}".format(m.content, m.stderr))
    logging.info("Found these minimized hangs")
    for m in minuniquehangs:
        if m in minuniquehangsminafter:
            logging.info("UNIQUE {} {}".format(m.content, m.stderr))
        else:
            logging.info("NOT UNIQUE {} {}".format(m.content, m.stderr))

    logging.info("Produced {} minimized unique crashes ({} unique trace crashes)".format(len(minuniquecrashesminafter), len(uniquecrashes)))
    if len(hangs) > 0 and nhangs > 0:    
        logging.info("Produced {} minimized unique hangs after post deduplication (Processed {}/{} hangs. Found {} hangs before post deduplication)".format(len(minuniquehangsminafter), nhangs, len(hangs), len(minuniquehangs)))
    else:
        logging.info("Produced no hangs")
    logging.info("All steps completed. Bye!")

if __name__ == "__main__":
    main()