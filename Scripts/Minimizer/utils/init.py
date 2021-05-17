import os
import locale
import logging

def initLogging():
    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler("out.log", "w", "utf-8"), logging.StreamHandler()])
    logging.info("Starting")

def makeDirs(outputdir):
    os.makedirs(os.path.dirname(outputdir + "/CrashesDeduplicated/"), exist_ok=True)
    os.makedirs(os.path.dirname(outputdir + "/CrashesDeduplicatedMinimized/"), exist_ok=True)
    os.makedirs(os.path.dirname(outputdir + "/Hangs/"), exist_ok=True)
    os.makedirs(os.path.dirname(outputdir + "/HangsDeduplicatedMinimized/"), exist_ok=True)