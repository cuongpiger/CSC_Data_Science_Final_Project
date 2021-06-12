import wordcloud
import matplotlib.pyplot as plt
import re

from typing import Dict, List

url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

vietnamese_upper_pattern = r"[^A-ZÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]"

vietnamese_letters_pattern = r"[^a-z áàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

vietnamese_letters_pattern_no_space = r"[^a-záàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

vietnamese_letters = r"[a-záàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

def drawWordCloud(pText: str):
    plt.figure(figsize=(20,10))
    word_cloud = wordcloud.WordCloud(max_words=100,background_color ="white",
                                width=2000,height=1000,mode="RGB").generate(pText)
    plt.axis("off")
    plt.imshow(word_cloud)
    
def containsURL(pText: str):
    flag = re.search(url_pattern, pText)
    
    return flag is not None

def containAdvertisement(pText: str):
    tmp = re.sub(vietnamese_upper_pattern, "", pText)
    
    return len(tmp) / len(pText) >= 0.5

def loadVietnameseSyllables():
    vietnamese_syllables = {}
    
    with open("./modules/dependencies/vietnamese-syllables.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            vietnamese_syllables[word] = 1
            
    return vietnamese_syllables

def isVietnamese(pText: str, pVietnameseWord: dict):
    pText = re.sub(vietnamese_letters_pattern, " ", pText.lower())
    pText = re.sub(" +", " ", pText)
    words = pText.split(' ')
    vietnamese = 0
    other_langs = 0
    
    for word in words:
        if (pVietnameseWord.get(word, 0) == 1):
            vietnamese += 1
        else:
            other_langs += 1

    return vietnamese >= other_langs  

def convertToOneString(pText: List[str]):
    return " ".join(pText).lower()


def expandPhrase(pText: str, pPhrases: dict):
    pText = re.sub(vietnamese_letters_pattern, " ", pText.lower())
    pText = re.sub(" +", " ", pText)
    text = []
    
    for phrase in pPhrases:
        matches = re.findall(f"{vietnamese_letters}+ {phrase} {vietnamese_letters}+", pText)
        
        if matches:
            matches = ["_".join(match.split(" ")) for match in matches]
            matches = " ".join(matches)
            
            text.append(matches)
            
    return " ".join(text)
        
def removeStopword(pText: str, pVietnameseWord: dict):
    pText = re.sub(vietnamese_letters_pattern, " ", pText.lower())
    pText = re.sub(" +", " ", pText)
    words = pText.split(" ")
    res = []
    
    for word in words:
        if (pVietnameseWord.get(word, 0) == 0):
            res.append(word)
            
    return " ".join(res)