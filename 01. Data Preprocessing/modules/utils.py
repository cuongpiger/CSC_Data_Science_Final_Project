from __future__ import unicode_literals
import emojis
import re
import numpy as np
from .regex_patterns import vietnamese_letters_pattern, vietnamese_letters_pattern_no_space, url_pattern
from os import listdir
from os.path import isfile, join


def labelRating(pRating: int):
    if pRating <= 2: return -1
    
    if pRating <= 4: return 0
    
    return 1


def extractEmoji(pText: str):
    return " ".join(list(emojis.get(pText)))

    
def containsURL(pText: str):
    flag = re.search(url_pattern, pText)
    
    return flag is not None


def removeDuplicateLetters(pText: str):
    words = pText.split(" ")
    
    for i, word in enumerate(words):
        words[i] = re.sub(r'(.)\1+', r'\1', word)
        
    return " ".join(words)


def loadVietnameseAbbreviate():
    vietnamese_abbreviate = {}
    
    with open("./modules/dependencies/vietnamese-abbreviate.txt", "r", encoding="utf-8") as reader:
        items = reader.read().split("\n")
        for item in items:
            abbreviate, word = item.split("=")
            vietnamese_abbreviate[abbreviate] = word
            
    return vietnamese_abbreviate


def standardVietnameseAbbreviate(pVietnameseAbbreviate, pText):
    for abbreviate, word in pVietnameseAbbreviate.items():
        pText = re.sub(f"{vietnamese_letters_pattern_no_space}+{abbreviate}{vietnamese_letters_pattern_no_space}+", f" {word} ", pText)

    return pText.strip()


def removeNotVietnameseLetters(pText: str):
    return re.sub("\s+", " ", re.sub(vietnamese_letters_pattern, " ", pText)).strip() 


def loadVietnameseSyllables():
    vietnamese_syllables = {}
    
    with open("./modules/dependencies/vietnamese-syllables.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            vietnamese_syllables[word] = True
            
    return vietnamese_syllables

def loadBoostWords():
    boost_words = {}
    
    with open("./modules/dependencies/boost-words.txt", "r", encoding="utf-8") as reader:
        words = reader.read().split("\n")
        for word in words:
            boost_words[word] = True
            
    return boost_words


def extractBoostWords(pBoostWords, pText):
    lst_words = []

    for word in pBoostWords.keys():
        if re.search(",", word):
            words = word.split(',')
            dash_word = None
            
            for split_word in words:
                if re.search(f"{vietnamese_letters_pattern_no_space}+{split_word}{vietnamese_letters_pattern_no_space}+", pText):
                    dash_word = "_".join(split_word.split(" "))
                    
            if dash_word:
                lst_words.append(dash_word)
        elif re.search(f"{vietnamese_letters_pattern_no_space}+{word}{vietnamese_letters_pattern_no_space}+", pText):
            dash_word = "_".join(word.split(" "))
            lst_words.append(dash_word)
            
    return " ".join(lst_words).strip()

def removeGibbish(pDictionary, pText):
    words = []
    
    for word in pText.split(" "):
        if pDictionary.get(word) is not None:
            words.append(word)
            
    return " ".join(words)

def combineCommentAndEmoji(pText, pEmoji):
    if pEmoji == "nan" or pEmoji == "" or pEmoji == np.nan or pEmoji == None:
        pEmoji = ""
        
    return (pText + " " + pEmoji).strip()


def getFiles(pDirectory):
    return [f for f in listdir(pDirectory) if isfile(join(pDirectory, f))]







def fixAcronymWords(pDictionary, pText):
    words = []
    
    for word in pText.split(" "):
        acronym = pDictionary.get(word)
        
        if acronym is None:
            words.append(word)
        else:
            words.append(acronym)
            
    return " ".join(words)