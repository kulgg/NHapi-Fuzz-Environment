#!/usr/bin/python3

import sys
import glob

from .utils.extract import *
from .utils.minimizecrashes import *
from .utils.minimizehangs import *
from .utils.processresults import *
from .utils.init import *

exec1 = ["dotnet", "nHapi.Dbg/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"]
execrunonce = ["dotnet", "nHapi.RunOnce/bin/Debug/netcoreapp3.1/nHapi.Fuzz.dll"]
outputdir = ""
inpdir = ""
timeout = 1.0
nhangs = 0
ncrashes = 0
max_threads = 8

def processInputs():
    global inpdir, outputdir, timeout, nhangs, max_threads
    # Set args
    inpdir = sys.argv[1]
    outputdir = sys.argv[2]
    if len(sys.argv) >= 4:
        timeout = float(sys.argv[3]) 
        if len(sys.argv) == 5:
            nhangs = int(sys.argv[4])
            if len(sys.argv) == 6:
                max_threads = int(sys.argv[5])
    logging.info("[*] Using Input dir {}".format(inpdir))
    logging.info("[*] Using Output dir {}".format(outputdir))
    logging.info("[*] Setting {} sec timeout".format(timeout))

def main():
    # Init Logging
    initLogging()
    # Requires at least 2 and a maximum of 5 arguments
    if(len(sys.argv) < 3 or len(sys.argv) > 6):
        logging.info("[*] Usage minFindings.py [inputs] [output dir] (timeout=1.0) (num hangs to minimize=0) (max_afltmin_threads=8)\n[*] Example: ./minFindings \"Crashes/id*\" MinimizedOut 1.0 1 10")
        exit(1)

    logging.info("Processing inputs")
    processInputs()
    # Make needed Dirs
    makeDirs(outputdir)
    # Extract unique stack trace crashes and hangs above the timeout threshold
    inputpaths = glob.glob(inpdir)
    crashes, hangs = extractCrashesAndHangs(inputpaths)
    uniquecrashes = processExtractedCrashes(crashes, outputdir)
    logging.info("[*] Found {} unique trace crashes".format(uniquecrashes))
    processExtractedHangs(hangs, outputdir)
    # Minimize crash inputs by running afl-tmin threads on the crash inputs
    minuniquecrashes = minimizeUniqueCrashes(uniquecrashes, outputdir, timeout, max_threads, exec1, execrunonce)
    minuniquecrashes = processUniqueMinCrashes(minuniquecrashes, outputdir)
    # Minimize hang inputs by removing useless blocks
    minuniquehangs = minimizeHangs(hangs[:nhangs], exec1, timeout)
    minuniquehangs = processUniqueMinHangs(minuniquehangs, outputdir)
    for m in minuniquecrashes:
        logging.info("{} {} {}".format(m.content, m.stderr, m.unique))
    for m in minuniquehangs:
        logging.info("{} {} {}".format(m.content, m.stderr, m.unique))

    logging.info("[*] Produced {} minimized unique crashes,   {} unique trace crashes".format(len(minuniquecrashes), len(uniquecrashes)))
    logging.info("[*] Processed {}/{} hangs. Produced {} minimized unique hangs,   {} total hangs".format(nhangs, len(hangs), len(minuniquehangs)))
    logging.info("[*] All steps completed. Bye!")

if __name__ == "__main__":
    main()