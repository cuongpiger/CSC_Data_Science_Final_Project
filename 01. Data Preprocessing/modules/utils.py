from __future__ import unicode_literals
import emojis
import re
from os import listdir
from os.path import isfile, join

detect_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
remove_special_characters = r"[^a-z àáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹý]"

def extract_emoji(pText):
    return " ".join(list(emojis.get(pText)))

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

def removeSpecialCharacters(pText):
    return re.sub("\s+", " ", re.sub(remove_special_characters, " ", pText)).strip() 

def removeDupplicateLetters(pText):
    words = pText.split(" ")
    
    for i, word in enumerate(words):
        words[i] = re.sub(r'(.)\1+', r'\1', word)
        
    return " ".join(words)

def removeGibbish(pDictionary, pText):
    words = []
    
    for word in pText.split(" "):
        if pDictionary.get(word) is not None:
            words.append(word)
            
    return " ".join(words)


def fixAcronymWords(pDictionary, pText):
    words = []
    
    for word in pText.split(" "):
        acronym = pDictionary.get(word)
        
        if acronym is None:
            words.append(word)
        else:
            words.append(acronym)
            
    return " ".join(words)

def combineCommentAndEmoji(pText, pEmoji):
    if pEmoji == "nan":
        pEmoji = ""
        
    return (pText + " " + pEmoji).strip()