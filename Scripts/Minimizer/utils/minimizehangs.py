from utils.runprocess import RunProcess
from math import log
import logging

# Runs the hang with parts of size blocksize removed
# If a removed block does not impact the RunProcess returning a hang (r[0]=True) it is removed from hang
def removeUnimpactfulBlocks(hang, blocksize, exec1, timeout, replace_char=b''):
    a = len(hang)
    # Runs from end to beginning of hang with jumps of blocksize -> Removes block of blocksize and checks if the input is still hanging
    while a - blocksize >= 0:
        logging.info("Testing impact of [{}-{}]".format(a-blocksize, a-1))
        tmp = hang[:a-blocksize] + replace_char + hang[a:]
        r = RunProcess(exec1, tmp, timeout).Run()
        if r[0] and tmp != hang:
            if replace_char == b'':
                logging.info("Removed block")
                logging.info("Remaining Size {}".format(len(tmp)))
            else:
                logging.info("Replaced with {}".format(replace_char))
            hang = tmp
        a -= blocksize
    return hang

# Minimizes a single hang input by removing unimpactful byte blocks
def minimizeHang(hang, exec1, timeout):
    logging.info("Minimizing hang {}".format(hang))
    logging.info("Size {} Bytes".format(len(hang)))
    logging.info("Removing useless lines")

    if len(hang) < 5000:
        for line in hang.splitlines():
            a = hang.index(line)
            a2 = a + len(line)
            tmp = hang[:a] + hang[a2+1:]
            r = RunProcess(exec1, tmp, timeout).Run()
            if r[0] and tmp != hang:
                logging.info("Removed line {}".format(line))
                logging.info("Remaining Size {}".format(len(tmp)))
                hang = tmp

    blocks = reversed([ 2**j for j in range(0,int(log(len(hang))/log(2)))])
    for blocksize in blocks:
        logging.info("Blocksize {}".format(blocksize))
        hang = removeUnimpactfulBlocks(hang, blocksize, exec1, timeout)

    hang = removeUnimpactfulBlocks(hang, 1, exec1, timeout, b'A')
    return hang

# Minimizes user specified amount of hang inputs found during extractCrashesAndHangs()
def minimizeHangs(hangs, exec1, timeout):
    # Retrieve the minimized hang form for each hangfile in nhangfiles
    for hang in hangs:
        hang.content = minimizeHang(hang.content, exec1, timeout)

    logging.info("Hangfiles minimized")
    return hangs