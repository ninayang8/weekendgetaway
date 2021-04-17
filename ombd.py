import json
import os
import requests

API_KEY = "2a2f5075"

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


def create_request_url(title):
    base_url = 'http://www.omdbapi.com/?t={}&apikey=2a2f5075&type=movie&plot=short&r=json'
    request_url = base_url.format(title)
    return request_url


# def request_data(url):

#     headers = {'Authorization': 'Bearer %s' % API_KEY,}
#     r = requests.get(url, headers=headers)
#     return r.text
def main():
    open_file()

if __name__ == "__main__":
    main()