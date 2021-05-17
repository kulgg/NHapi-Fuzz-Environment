import concurrent.futures
import subprocess
import re
import glob
import logging

from .runprocess import RunProcess
from ..modules.crash import crash

# Runs afl-tmin threads for each unique crash to minimize it
def minimizeUniqueCrashes(uniquecrashes, outputdir, timeout, max_threads, exec, execrunonce):
    logging.info("[*] # Phase2 # Minimizing unique crash inputs")
    filepaths = (u.filepath for u in uniquecrashes)
    commands = []
    # Create commands list for ThreadPoolExecutor mapping
    for f in filepaths:
        commands.append(["afl-tmin", "-i", f, "-o", outputdir + "/CrashesDeduplicatedMinimized/" + re.sub('.*/', '', f).replace(":", "_"), "-m", "10000" ,"-t", str(int(timeout*1000)), "-e", "--", execrunonce[0], execrunonce[1]])
    # Successively run threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        logging.info("[*] Running afl-tmin Threads")
        executor.map(subprocess.run, commands)

    logging.info("\n[*] # Phase3 # Deleting duplicates of minimized Crashes")

    mincrashesfilepaths = glob.glob(outputdir + "/CrashesDeduplicatedMinimized/*")
    uniquemincrashes = []
    # Check if there are duplicates in minimized form and remove them
    for fn in mincrashesfilepaths:
        fd = open(fn, 'rb')
        crashcontent = fd.read()
        fd.close()
        r = RunProcess(exec, crashcontent, timeout).Run()
        c = crash(fn, crashcontent, stdout=r[1], stderr=r[2])
        uniquemincrashes.append(c)
    return uniquemincrashes