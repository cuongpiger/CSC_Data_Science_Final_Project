import wordcloud
import matplotlib.pyplot as plt
import re

url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

vietnamese_upper_pattern = r"[^A-ZÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]"

vietnamese_letters_pattern = r"[^a-z áàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"

vietnamese_letters_pattern_no_space = r"[^a-záàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]"


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