
# Python code to find the URL from an input string
import re
  
def Find(string):
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.search(regex,string)      
    return url
      
# Driver Code
string1 = 'My Profile in the portal of http://www.geeksforgeeks.org/'
string2 = "Duong Mạnh Cường"


if Find(string2) is None:
    print("ok")
else:
    print("?")