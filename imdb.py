import bs4
from bs4 import BeautifulSoup
import requests
import re
import os
import csv

def getLink(soup):
    pass

def get_title(soup):
    anchor = soup.find('div', class_ = 'lister list detail sub-list')
    anchor1 = anchor.find_all('h3', class_ = 'lister-item-header')
    list = []
    for movie in anchor1:
        anchor2 = movie.find('a').text
        list.append(anchor2)
    print(list)
    return list

def get_streaming_platforms(soup):
    pass

def main():
    url = 'https://www.imdb.com/list/ls091520106/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getLink(soup)
    get_title(soup)
    get_streaming_platforms(soup)

if __name__ == "__main__":
    main()
