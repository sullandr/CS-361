import os
import requests
import json
import random
import time

from flask import Flask, json

api = Flask(__name__)

@api.route('/cities', methods=['GET'])
def get_cities():
    with open("./CS-361/cities.json",'r') as file:
        cities = json.load(file)
        keys = list(cities.keys())
        rand_key = int(random.random() * 1000 % 51)        
        state = (keys[rand_key])
        #print(state)
        city = (cities[state])
        rand_city = int(random.random() * 1000 % len(city))
        location = city[rand_city]
        #print(location)
        response = {"city":location, "state":state}
        #print(response)
        #response_json = json.dumps(response)
        #print(response_json)
    return json.dumps(response)

if __name__ == '__main__':
    api.run(debug=True, port=5001)
