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

def get_title_and_rating(cur, conn):
    title_and_rating = []
    cur.execute('SELECT title from Movies')
    movie_list = cur.fetchall()

    for movie in movie_list:
        url = create_request_url(movie)
        try:
            r = requests.get(url)
            data = json.loads(r.text)
            if data == {"Response":"False", "Error":"Movie not found!"}:
                continue
            else:
                t = (movie[0], data['imdbRating'])
                title_and_rating.append(t) 
        except:
            return None
    return title_and_rating

def get_box_office(cur, conn):
    box_office = []
    cur.execute('SELECT title from Movies')
    movie_list = cur.fetchall()

    for movie in movie_list:
        url = create_request_url(movie)
        try:
            r = requests.get(url)
            data = json.loads(r.text)
            b = ''
            if data['BoxOffice'] != "N/A":
                for x in data['BoxOffice']:
                    if x != '$' and x != ',':
                        b += x
            else:
                b = 'N/A'
                                        
            box_office.append(b)
        except: 
            pass
    
    return box_office
               

def create_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpMoviesTable(cur, conn):
    movie_and_rating = get_title_and_rating(cur, conn)
    box_office = get_box_office(cur, conn)

    cur.execute('CREATE TABLE IF NOT EXISTS omdbMovies("id" TEXT PRIMARY KEY, "title" TEXT, "rating" REAL, "box_office" TEXT)')
    x = 1
    for i in range(len(movie_and_rating)):
        cur.execute('INSERT INTO omdbMovies (id, title, rating, box_office) VALUES (?, ?, ?, ?)', (x, movie_and_rating[i][0], movie_and_rating[i][1], box_office[i], ))
        x += 1
    conn.commit()
# def request_data(url):

#     headers = {'Authorization': 'Bearer %s' % API_KEY,}
#     r = requests.get(url, headers=headers)
#     return r.text
def main():

    cur, conn = create_database('Database.db')
    get_title_and_rating(cur, conn)
    get_box_office(cur, conn)
    setUpMoviesTable(cur, conn)
    

if __name__ == "__main__":
    main()