import bs4
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

def where_stream(soup, links):
    stream_list = []
    for link in links:
        movie_url = "https://www.imdb.com" + link
        r = requests.get(movie_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        anchor = soup.find('span', class_ = "buybox__cta").text
        place = ""
        #remove beginning and trailing white space
        anchor2 = anchor.lstrip()
        anchor3 = anchor2.rstrip()
        #remove "watch on"
        anchor4 = anchor3.replace('Watch on ','')
        if anchor4 == "See Showtimes & Tickets":
            anchor4 = 'N/A'
        place += anchor4
        stream_list.append(place)

    return stream_list

def setUpDatabase(db_name):

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Movies ("id" TEXT PRIMARY KEY, "title" TEXT, "platform" TEXT, "reviews" INTEGER)')
    conn.commit()
    return cur, conn

def addEntriesToDatabase(cur, conn, soup, links):
    title = get_title(soup)
    platform = where_stream(soup, links)
    reviews = get_movie_reviews(soup, links)
    x = 1
    cursor = cur.execute('SELECT id from Movies')
    for row in cursor:
        x += 1
    for i in range(x, x + 25):
        try:
            cur.execute('INSERT INTO Movies (id, title, platform, reviews) VALUES (?, ?, ?, ?)', (x, title[x-1], platform[x-1], reviews[x-1],))
            x += 1
        except:
            pass
    conn.commit()

def RatingVsReviews(cur, conn):
    rating = []
    reviews = []
    cursor = cur.execute('SELECT rating FROM omdbMovies')
    for row in cursor:
        rating.append(float(row[0]))
    cursor1 = cur.execute('SELECT reviews FROM Movies')
    for row in cursor1:
        reviews.append(int(row[0]))
    fig = px.scatter(x = rating, y = reviews)
    fig.update_layout(
    title="Reviews vs Movie Ratings",
    xaxis_title="Movie Ratings",
    yaxis_title="Number ofReviews")
    fig.show()

def PlatformVsRating(cur,conn):
    platform = []
    rating = []

    cursor = cur.execute('SELECT rating FROM omdbMovies')
    for row in cursor:
        rating.append(float(row[0]))
    cursor1 = cur.execute('SELECT platform FROM Movies')
    for row in cursor1:
        platform.append(str(row[0]))
    platform_count = {}
    for x in platform:
        if x not in platform_count:
            platform_count[x] = 1
        else:
            platform_count[x] += 1
    cumulative_rating = {}
    for i in range(len(platform)):
        if platform[i] not in cumulative_rating:
            cumulative_rating[platform[i]] = rating[i]
        else:
            cumulative_rating[platform[i]] += rating[i]
    for x in platform_count.keys():
        platform_count[x] = cumulative_rating[x] / platform_count[x]
    platforms = list(platform_count.keys())[:8]
    ratings = list(platform_count.values())[:8]

    f = open('imdb_calculations.txt', "a")
    f.write("---------------------------\n")

    for i in range(len(platforms)):
        f.write(str(platforms[i]) + " has an average rating of " + str(ratings[i]) + ".\n")

    f.close()
    
    plt.bar(platforms, ratings, align='center')
    plt.ylabel('Average Movie Rating')
    plt.title('Average Movie Ratings of Movies Available on Each Platform')
    plt.show()

def main():
    url = 'https://www.imdb.com/list/ls091520106/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # get_title(soup)
    # links = get_link(soup)
    # #get_movie_ratings(soup, links)
    # get_movie_reviews(soup, links)
    # where_stream(soup, links)

    cur, conn = setUpDatabase("Database.db")
    # addEntriesToDatabase(cur, conn, soup, links)
    # RatingVsReviews(cur, conn)
    PlatformVsRating(cur,conn)


if __name__ == "__main__":
    main()
