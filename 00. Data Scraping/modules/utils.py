import os
import re

from os.path import isfile, join


def getAllDirname(pPath: str):
    return [re.sub("/+", "/", f"{pPath}/{name}/") for name in os.listdir(pPath)]

def getFilenames(pDirectory: str):
    return [f for f in os.listdir(pDirectory) if isfile(join(pDirectory, f))]

def labelRating(pRating: int):
    if pRating <= 2: return -1
    
    if pRating <= 4: return 0
    
    return 1