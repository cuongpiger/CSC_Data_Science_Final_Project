import wordcloud
import matplotlib.pyplot as plt
import re
import emojis
import numpy as np

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

def loadSyllables():
    syllables = {}
    
    with open("./modules/dependencies/syllables.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            syllables[word] = 1
            
    return syllables

def isVietnamese(pText: str, pSyllables: dict):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
    words = pText.split(' ')
    vietnamese = 0
    other_langs = 0
    
    for word in words:
        if (pSyllables.get(word, 0) == 1):
            vietnamese += 1
        else:
            other_langs += 1

    return vietnamese >= other_langs  

def extractEmoji(pText: str):
    return " ".join(list(emojis.get(pText)))


def createPreprocessColumn(pText: str):
    pText = re.sub(letters_pattern, " ", pText.lower())
    pText = re.sub(r'(.)\1+', r'\1', pText)
    
    return pText.strip()


def loadAbbreviates():
    from modules.dependencies.abbreviate import abbreviate
    abbreviates = {}
    
    for word in abbreviate:
        tmp = word.split("=")
        abbreviates[tmp[0]] = tmp[1]
            
    return abbreviates

def standardReview(pText: str, pAbbreviates: dict, pSyllables: dict):
    pText = f" {str(pText).strip()} "
    text = []
    
    for key, value in pAbbreviates.items():
        pText = re.sub(f"{letters_pattern_no_space}+{key}{letters_pattern_no_space}+", f" {value} ", pText)
        
    words = re.sub(r'(.)\1+', r'\1', pText.strip()).split(" ")   
    for word in words:
        if pSyllables.get(word, 0) == 1:
            text.append(word)
            
    return " ".join(text)

def loadBoostWords():
    from modules.dependencies.boost_words import boost_words
    return dict(zip(boost_words, np.ones(len(boost_words), dtype=int)))

def extractBoostWords(pText: str, pBoostWords: dict):
    lst_words = []
    pText = f" {str(pText).strip()} "

    for word in pBoostWords.keys():
        if re.search(f"{letters_pattern_no_space}+{word}{letters_pattern_no_space}+", pText):
            lst_words.append("_".join(word.split(" ")))
            
    lst_words = sorted(lst_words, key=len)
    rm = []
    for i in range(len(lst_words)):
        for j in range(i + 1, len(lst_words)):
            if lst_words[i] in lst_words[j]:
                rm.append(i)
                break
            
    whole = set(np.arange(len(lst_words), dtype=int))
    remaining = whole - set(rm)
    
            
    return " ".join(np.array(lst_words)[list(remaining)]).strip()

def loadStopwords():
    from modules.dependencies.stopwords import stopwords
    return dict(zip(stopwords, np.ones(len(stopwords), dtype=int)))

def combine(pText: str, pBoostwords: str, pEmoji: str, pStopwords: dict):
    pText = f" {str(pText)} "
    pBoostwords = str(pBoostwords).split(" ")
    text = []

    for boost in pBoostwords:
        bw = re.sub("_", " ", boost)
        pText = re.sub(f"{letters_pattern_no_space}+{bw}{letters_pattern_no_space}+", f" {boost} ", pText)

    for word in re.sub(r'(.)\1+', r'\1', pText.strip()).split(" "):
        if pStopwords.get(word, 0) == 0:
            text.append(word)
            
    text = " ".join(text)
            
    return f"{text} {pEmoji}".strip()

def removeBoostwords(pText: str, pBoostwords: str, pStopwords: dict):
    pText = f" {pText} "
    pBoostwords = str(pBoostwords).split(" ")
    
    for boost in pBoostwords:
        bw = re.sub("_", " ", boost)
        pText = re.sub(f"{letters_pattern_no_space}+{bw}{letters_pattern_no_space}+", " ", pText)
        
    for word in re.sub(r'(.)\1+', r'\1', pText.strip()).split(" "):
        if pStopwords.get(word, 0) == 0:
            pText = re.sub(f"{letters_pattern_no_space}+{word}{letters_pattern_no_space}+", " ", pText)
        
    return re.sub(r'(.)\1+', r'\1', pText.strip())

def combine2(pBoostwords: str, pTokenize: str, pEmoji):
    return f"{str(pBoostwords).strip()} {str(pTokenize).strip()} {str(pEmoji).strip()}".strip()