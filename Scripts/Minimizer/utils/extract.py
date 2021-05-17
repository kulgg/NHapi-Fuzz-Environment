import re
import logging

from .runprocess import RunProcess
from ..modules.crash import crash
from ..modules.hang import hang

def extractCrashesAndHangs(inputpaths, execpath, timeout):
    global crashfiles, hangfiles, unique_errors

    logging.info("[*] # Phase1 # Extracting unique stack trace crash inputs")
    ninputs = 1
    crashes = []
    hangs = []

    for path in inputpaths:
        if input % int(len(inputpaths) / 10):
            logging.info("[*] Input: {}  Crashes: {}   Hangs: {}   Total Inputs: {}".format(ninputs, len(crashes), len(hangs),len(inputpaths)))
        fd = open(path, 'rb')
        # Get the input bytes that created a crash/hang in afl
        filecontent = fd.read()
        fd.close()
        # Execute with the crash input
        r = RunProcess(execpath, filecontent, timeout).Run()
        # If hang add it to hangfile list
        if r[0]:
            h = hang(path, filecontent, stdout=r[1], stderr=r[2])
            hangs.append(h)
        # If there is an error make sure its previously unencountered and then add it to unique_errors and add the input file to crashfiles
        elif r[2] != b'':
            c = crash(path, filecontent, stdout=r[1], stderr=r[2])
            # Filters out variable Stack Traces where input print is confusing the uniqueness
            p1 = re.compile(b"(.*):").match(r[2])
            p2 = re.compile(b".*\\n(.*)").match(r[2])
            e = r[2] + b" #" + bytes(str(ninputs), "ascii")
            if p1 and p2:
                e = p1.group(1) + b" " + p2.group(1)
            c = crash(path, filecontent, stdout=r[1], stderr=r[2], mintrace=e)
            crashes.append(c)
        ninputs += 1
    
    return crashes, hangs