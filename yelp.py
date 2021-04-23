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

def get_url(location, offset):

    return 'https://api.yelp.com/v3/businesses/search?location=' + location + '&limit=25' + '&offset=' + str(offset)

def request_data(url):

    headers = {'Authorization': 'Bearer %s' % API_KEY,}
    r = requests.get(url, headers=headers)
    return r.text

def setUpDatabase(db_name):

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS Restaurants')
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants ("restaurant_id" TEXT PRIMARY KEY, "name" TEXT, "category" TEXT, "rating" REAL, "price" TEXT)')

    cur.execute('DROP TABLE IF EXISTS Locations')
    cur.execute('CREATE TABLE IF NOT EXISTS Locations ("restaurant_id" TEXT PRIMARY KEY, "name" TEXT, "location" TEXT, "address" TEXT, "latitude" REAL, "longitude" REAL)')

    conn.commit()

    return cur, conn

def addEntriesToDatabase(cur, conn, data, location):
    
    for d in data['businesses']:
        try:
            cur.execute('INSERT INTO Restaurants (restaurant_id, name, category, rating, price) VALUES (?, ?, ?, ?, ?)', (d["id"], d["name"], d["categories"][0]["title"], float(d["rating"]), d["price"],))
            cur.execute('INSERT INTO Locations (restaurant_id, name, location, address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)', (d["id"], d["name"], location, d["location"]["address1"], float(d["coordinates"]["latitude"]), float(d["coordinates"]["longitude"])))
        except:
            cur.execute('INSERT INTO Restaurants (restaurant_id, name, category, rating, price) VALUES (?, ?, ?, ?, ?)', (d["id"], d["name"], d["categories"][0]["title"], float(d["rating"]), "$$$$",))

    conn.commit()

def main():

    cur, conn = setUpDatabase("Database.db")

    for x in range(4):

        url = get_url('Ann Arbor', x * 25)
        data = request_data(url)
        data = json.loads(data)

        addEntriesToDatabase(cur, conn, data, "Ann Arbor")



if __name__ == "__main__":
    main()