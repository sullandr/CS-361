import os
import requests
import json
import random
import time

from flask import Flask, json

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
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
    api.run()
#if __name__ == '__main__':
    #run_server = 'python -m http.server'
    #os.system(run_server)
    #while True:
    #    time.sleep(1)
    #    with open("./CS-361/cities.json",'r') as file:
    #        cities = json.load(file)
    #        keys = list(cities.keys())
    #        rand_key = int(random.random() * 1000 % 51)        
    #        state = (keys[rand_key])
    #        print(state)
    #        city = (cities[state])
    #        rand_city = int(random.random() * 1000 % len(city))
    #        location = city[rand_city]
    #        print(location)
    #        response = {"city":location, "state":state}
    #        print(response)
    #        response_json = json.dumps(response)
    #        print(response_json)