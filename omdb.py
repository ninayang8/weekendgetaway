import json
import os
import requests
import sqlite3

API_KEY = "2a2f5075"

def create_request_url(title):
    base_url = 'http://www.omdbapi.com/?t={}&apikey=2a2f5075&type=movie&plot=short&r=json'
    request_url = base_url.format(title)
    return request_url

def open_file():
    root_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(root_path, 'movies.txt')        
    file_obj = open(filename, 'r', errors='replace', encoding='utf-8-sig')
    movies = file_obj.readlines()
    file_obj.close()
    list = []
    for i in range(len(movies)):
            movies[i] = movies[i].replace('\n', '')
    for movie in movies:
        list.append(movie)
    return list

def get_title_and_rating():
    d = {}
    movie_list = open_file()
    for i in range(25):
        for movie in movie_list:
            url = create_request_url(movie)
            try:
                r = requests.get(url)
                data = json.loads(r.text)
                if data == {"Response":"False", "Error":"Movie not found!"}:
                    continue
                else:
                    d[movie] = data['imdbRating']
            except:
                return None
    return d     

def create_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpMoviesTable(cur, conn):
    data = get_title_and_rating()
    cur.execute('CREATE TABLE IF NOT EXISTS Movies("id" TEXT PRIMARY KEY, "title" TEXT, "rating" REAL)')
    for d in range(len(data)):
        cur.execute('INSERT INTO Movies (id, title, rating) VALUES (?, ?, ?)', (d, data[d]["title"], float(data[d]["rating"])))
    conn.commit()
# def request_data(url):

#     headers = {'Authorization': 'Bearer %s' % API_KEY,}
#     r = requests.get(url, headers=headers)
#     return r.text
def main():
    open_file()
    get_title_and_rating()
    cur, conn = create_database('movies.db')
    setUpMoviesTable(cur, conn)

if __name__ == "__main__":
    main()