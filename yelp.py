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
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

API_KEY = "YuijH5s1qzWZVSOfuGknf5--ccUjwSLWR2XDFJSrghEuRipM8ouL-wm4-ib3ARRdqTZVW3Pd8rMoA4jPf6I6DKBTOCu4AdorRGMVPv1PL1SWssRnjXfSDip1ACh6YHYx"
CLIENT_ID = "IGLDk-j90I9w05zBZUo5qw"

def get_url(cur, conn, location):

    rows = cur.execute('SELECT restaurant_id FROM Restaurants')
    count = 0
    for row in rows:
        count += 1
    return 'https://api.yelp.com/v3/businesses/search?location=' + location + '&limit=25' + '&offset=' + str(count)

def request_data(url):
    headers = {'Authorization': 'Bearer %s' % API_KEY,}
    r = requests.get(url, headers=headers)
    return r.text
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Restaurants ("restaurant_id" TEXT PRIMARY KEY, "name" TEXT, "category" TEXT, "rating" REAL, "price" TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Locations ("restaurant_id" TEXT PRIMARY KEY, "name" TEXT, "location" TEXT, "address" TEXT, "latitude" REAL, "longitude" REAL)')
    conn.commit()
    return cur, conn
def addEntriesToDatabase(cur, conn, data, location):
    
    rows = cur.execute('SELECT restaurant_id FROM Restaurants')
    count = 0
    for row in rows:
        count += 1
    for d in data['businesses']:
        try:
            cur.execute('INSERT INTO Restaurants (restaurant_id, name, category, rating, price) VALUES (?, ?, ?, ?, ?)', (count, d["name"], d["categories"][0]["title"], float(d["rating"]), d["price"],))
            cur.execute('INSERT INTO Locations (restaurant_id, name, location, address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)', (count, d["name"], location, d["location"]["address1"], float(d["coordinates"]["latitude"]), float(d["coordinates"]["longitude"])))
        except:
            cur.execute('INSERT INTO Restaurants (restaurant_id, name, category, rating, price) VALUES (?, ?, ?, ?, ?)', (count, d["name"], d["categories"][0]["title"], float(d["rating"]), "$$$$",))
        count += 1
    conn.commit()
def RatingVsPricePlot(cur, conn):
    rating = []
    price = []
    cursor = cur.execute("SELECT rating, price FROM Restaurants")
    for row in cursor:
        rating.append(row[0])
        price.append(row[1])
    
    values = {}
    for x in range(len(price)):
        if len(price[x]) not in values:
            values[len(price[x])] = []
        values[len(price[x])].append(rating[x])

    f = open("yelp_calculations.txt", "w")

    for x in values.keys():
        values[x] = sum(values[x]) / len(values[x])
        dollars = ""
        for y in range(x):
            dollars += "$"
        f.write(dollars + " price has an average of " + str(values[x]) + " ratings.\n")
    
    plt.bar(values.keys(), values.values())
    plt.show()

def StreetVsRating(cur, conn):

    streetRatings = {}

    cursor = cur.execute("SELECT rating, address FROM Restaurants JOIN Locations WHERE Locations.restaurant_id = Restaurants.restaurant_id")
    for row in cursor:
        address = row[1].split()
        address = address[-2] + " " + address[-1]
        if address not in streetRatings:
            streetRatings[address] = []
        streetRatings[address].append(row[0])

    # f = open("yelp_calculations.txt", "a")
    # f.write("\n------------------------------------------------\n------------------------------------------------\n\n")

    for x in streetRatings.keys():
        streetRatings[x] = sum(streetRatings[x]) / len(streetRatings[x])
    #     f.write(x + " has an average of " + str(streetRatings[x]) + " ratings on the street.\n")

    lst = list(streetRatings.items())
    print(lst)


def MapPlot(cur, conn):

    mapbox_access_token = "pk.eyJ1IjoiYW5kcnNuYXNobGV5IiwiYSI6ImNrbnV0dDkycjBlOHQydW8zeWl3cGs2NGwifQ.DyqaNgUdx8TyxGt1zMZLiQ"

    name =[]
    latitude = []
    longitude = []

    cursor = cur.execute("SELECT name, latitude, longitude FROM Locations")
    for row in cursor:
        name.append(row[0])
        latitude.append(row[1])
        longitude.append(row[2])

    fig = go.Figure(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text=name,
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=42.271,
                lon=-83.702
            ),
            pitch=0,
            zoom=10
        ),
    )

    fig.show()

def main():

    cur, conn = setUpDatabase("Database.db")

    # cur.execute("DROP TABLE IF EXISTS Restaurants")
    # cur.execute("DROP TABLE IF EXISTS Locations")

    # url = get_url(cur, conn, 'Ann Arbor')
    # data = request_data(url)
    # data = json.loads(data)

    # addEntriesToDatabase(cur, conn, data, "Ann Arbor")

    RatingVsPricePlot(cur, conn)
    # RatingVsPricePlot(cur, conn)
    StreetVsRating(cur, conn)
    MapPlot(cur, conn)
    


if __name__ == "__main__":
    main()