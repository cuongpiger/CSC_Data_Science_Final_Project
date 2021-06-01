import emojis
import re
from os import listdir
from os.path import isfile, join

detect_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def extract_emoji(pText):
    return list(emojis.get(pText))

def get_text(pText: str):
    test = pText.lower()
    
def containsURL(pText: str):
    """ Kiểm tra pText có chứa url hay ko

    Args:
        pText ([type]): [description]

    Returns:
        (bool): True nếu có và ngc lại
    """
    flag = re.search(detect_url, pText)
    
    return flag is not None

def getFiles(pDirectory):
    return [f for f in listdir(pDirectory) if isfile(join(pDirectory, f))]