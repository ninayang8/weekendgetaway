# yelp.py
#
# SI 206 Final Project
# Ashley Anderson (andrsn), Anthony Ho (anthhocy), Nina Yang (ninayang)
# 04.16.2021   
#

import json
import requests

API_KEY = "YuijH5s1qzWZVSOfuGknf5--ccUjwSLWR2XDFJSrghEuRipM8ouL-wm4-ib3ARRdqTZVW3Pd8rMoA4jPf6I6DKBTOCu4AdorRGMVPv1PL1SWssRnjXfSDip1ACh6YHYx"
CLIENT_ID = "IGLDk-j90I9w05zBZUo5qw"

# Reading and Writing to a Cache
def read_cache(CACHE_FNAME):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_yelp.json"
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):

    jsonDict = json.dumps(CACHE_DICT)
    f = open(CACHE_FNAME, "w")
    f.write(jsonDict)
    f.close()

def main():

    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    url = "https://api.yelp.com/v3/businesses/search?location=NYC&limit=50"
    r = requests.get(url, headers=headers)
    data = r.text
    print(data)


if __name__ == "__main__":
    main()