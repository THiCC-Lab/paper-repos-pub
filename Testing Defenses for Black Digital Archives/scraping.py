import trafilatura
#import requests
#from bs4 import BeautifulSoup

url = 'https://dejaworkman.github.io/obfuscation/'
downloaded = trafilatura.fetch_url(url)
text = trafilatura.html2txt(downloaded)
print(text)

url = 'https://dejaworkman.github.io/content_overload/'
downloaded = trafilatura.fetch_url(url)
text = trafilatura.html2txt(downloaded)
print(text)

url = 'https://dejaworkman.github.io/control/'
downloaded = trafilatura.fetch_url(url)
text = trafilatura.html2txt(downloaded)
print(text)

url = 'https://dejaworkman.github.io/targeting/'
downloaded = trafilatura.fetch_url(url)
text = trafilatura.html2txt(downloaded)
#print(text)

file = open('target.txt','w',encoding='utf-8')
file.write(text)
file.close()
