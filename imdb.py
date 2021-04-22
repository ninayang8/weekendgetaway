import bs4
from bs4 import BeautifulSoup
import requests
import re
import os
import csv

def get_title(soup):
    anchor = soup.find('div', class_ = 'lister list detail sub-list')
    anchor1 = anchor.find_all('h3', class_ = 'lister-item-header')
    list = []
    for movie in anchor1:
        anchor2 = movie.find('a').text
        list.append(anchor2)
    return list

def get_link(soup):
    anchor = soup.find('div', class_ = 'lister list detail sub-list')
    anchor1 = anchor.find_all('h3', class_ = 'lister-item-header')
    movie_links = []
    
    for movie in anchor1:
        a = movie.find_all('a')
        for link in a:
            link = link.get('href')
            movie_links.append(link)
    
    return movie_links

def get_movie_ratings(soup, links):
    movie_ratings = []

    for i in range(len(links)):
        movie_url = "https://www.imdb.com" + links[i]
        r = requests.get(movie_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        anchor = soup.find('div', class_ = 'ratingValue')
        anchor1 = anchor.find('span', itemprop="ratingValue").text
        rating = float(anchor1)
        movie_ratings.append(rating)

    return movie_ratings

def get_movie_reviews(soup, links):
    movie_reviews = []

    for i in range(len(links)):
        movie_url = "https://www.imdb.com" + links[i]
        r = requests.get(movie_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        anchor2 = soup.find('span', itemprop="reviewCount").text
        
        review_count = ''
        for x in anchor2:
            if x != ',':
                review_count += x
        review_count = review_count[:-5]
        review_count = int(review_count)
        movie_reviews.append(review_count)
    
    return movie_reviews




def main():
    url = 'https://www.imdb.com/list/ls091520106/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    get_title(soup)
    links = get_link(soup)
    #get_movie_ratings(soup, links)
    get_movie_reviews(soup, links)

if __name__ == "__main__":
    main()
