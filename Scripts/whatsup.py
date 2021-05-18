#!/usr/bin/python3

import os
from time import sleep
import sys

def main():
    if len(sys.argv) == 2:
        outputdir = sys.argv[1]
        while True:
            os.system("afl-whatsup {}".format(outputdir))
            sleep(10)
    else:
        print("./whatsup.py outputdir")
        exit(1)

if __name__ == "__main__":
    main()