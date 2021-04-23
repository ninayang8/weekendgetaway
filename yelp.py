# yelp.py
#
# SI 206 Final Project
# Ashley Anderson (andrsn), Anthony Ho (anthhocy), Nina Yang (ninayang)
# 04.16.2021   
#

import os
import json
import requests
import sqlite3

API_KEY = "YuijH5s1qzWZVSOfuGknf5--ccUjwSLWR2XDFJSrghEuRipM8ouL-wm4-ib3ARRdqTZVW3Pd8rMoA4jPf6I6DKBTOCu4AdorRGMVPv1PL1SWssRnjXfSDip1ACh6YHYx"
CLIENT_ID = "IGLDk-j90I9w05zBZUo5qw"

def get_url(location):

    return 'https://api.yelp.com/v3/businesses/search?location=' + location + '&limit=50'

def request_data(url):

    headers = {'Authorization': 'Bearer %s' % API_KEY,}
    r = requests.get(url, headers=headers)
    return r.text

def setUpDatabase(db_name):

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS Restaurants")
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants ("restaurant_id" TEXT PRIMARY KEY, "name" TEXT, "location" TEXT, "category" TEXT, "rating" REAL, "price" TEXT)')

    return cur, conn

def addEntriesToDatabase(cur, conn, data, location):
    
    pass

def main():

    url = get_url('New York City')
    data = request_data(url)
    data = json.loads(data)
    cur, conn = setUpDatabase("restaurants.db")

    print(data['businesses'])


if __name__ == "__main__":
    main()