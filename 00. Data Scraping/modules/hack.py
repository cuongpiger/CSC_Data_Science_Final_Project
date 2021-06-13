import wordcloud
import matplotlib.pyplot as plt
import re

from typing import Dict, List

url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

upper_pattern = r"[^A-ZÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]"

letters_pattern = r"[^a-z áàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

letters_pattern_no_space = r"[^a-záàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

letters = r"[a-záàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

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
    tmp = re.sub(upper_pattern, "", pText)
    
    return len(tmp) / len(pText) >= 0.5

def loadVietnameseSyllables():
    vietnamese_syllables = {}
    
    with open("./modules/dependencies/syllables.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            vietnamese_syllables[word] = 1
            
    return vietnamese_syllables

def isVietnamese(pText: str, pVietnameseWord: dict):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
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
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
    text = []
    
    for phrase in pPhrases:
        matches = re.findall(f"{letters}* {phrase} {letters}*", pText)
        
        if matches:
            matches = ["_".join(match.split(" ")) for match in matches]
            matches = " ".join(matches)
            
            text.append(matches)
            
    return " ".join(text)
        
def removeSyllables(pText: str, pVietnameseWord: dict):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
    words = pText.split(" ")
    res = set()
    cnt = 0
    
    for word in words:
        flag = 0
        if (pVietnameseWord.get(word, 0) == 0):
            res.add(word)
            
    print(cnt)
            
    return " ".join(res)

def loadAbbreviate():
    abbreviate = {}
    
    with open("./modules/dependencies/abbreviate.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            tmp = word.split("=")
            abbreviate[tmp[0]] = tmp[1]
            
    return abbreviate

def removeAbbreviates(pText: str, pAbbreviate: dict):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
    words = pText.split(" ")
    res = set()
    
    for word in words:
        if (pAbbreviate.get(word, "") == ""):
            res.add(word)
            
    return " ".join(res)

def standardAbbreviate():
    pass

def createCommentColumn(pText: str, pSyllables: dict, pAbbreviates: dict):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText.strip())
    pText = f" {pText} "
    text = []
    
    for key, value in pAbbreviates.items():
        pText = re.sub(f"{letters_pattern_no_space}+{key}{letters_pattern_no_space}+", value, pText)

    words = pText.strip().split(" ")   
    for word in words:
        if pSyllables.get(word, 0) == 1:
            text.append(word)
            
    return " ".join(text)