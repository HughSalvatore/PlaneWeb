from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
import requests
import re


def getInternalLinks(includeUrl):
    html = urlopen(includeUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    print(includeUrl)
    internalLinks = []

    for link in bsObj.findAll("a", href=re.compile(includeUrl + "/tag")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


def getImageUrl(includeUrl):
    html = urlopen(includeUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    print(includeUrl)

    imageLinks = []

    for link in bsObj.find_all("img", src=re.compile("^(http://mb\.g13p\.com/).*?\.jpg")):
        if link.attrs['src'] not in imageLinks:
            print(link.attrs['src'])
            imageLinks.append(link.attrs['src'])
    return imageLinks


def download_image(imageLinks):
    # os.mkdir('images')
    os.chdir('images')
    save_images('images', imageLinks)


def save_images(floder, img_addrs, num=30):
    """
    保存图片

    """
    i = 0
    print("----------------------------------------------------")
    print(img_addrs)
    print("----------------------------------------------------")
    for img_addr in img_addrs:
        filename = str(i)
        print(img_addr)
        i = i + 1
        if (i < num):
            imagehtml = requests.get(img_addr)
            with open(filename + '.jpg', 'wb') as file:
                file.write(imagehtml.content)


allIntLinks = set()
internalLinks = getInternalLinks("http://www.girl13.com")

for link in internalLinks:
    if link not in allIntLinks:
        print("URL=" + link)
        allIntLinks.add(link)

imagelinks = getImageUrl("http://www.girl13.com/tag/nature") #头发撒
download_image(imagelinks)
