from pprint import pprint
from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response        #facilitate form submission
import os 
import db_tools
from api import *
import random
import requests

city1 = None
city2 = None
city1_pop = None
city2_pop = None
score= int(0)
city1_img_url = None
city2_img_url = None
city1_lat = None 
city1_lng = None
city2_lat = None
city2_lng = None

def get_cities():
    # Choose two random cities from the API response
    api_key = 'f9ca0722a830a37dcd77c39571e64d6f691cdefe'
    api_url = f'https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=place:*&in=state:*&key={api_key}'
    api_response = requests.get(api_url).json()
    cities = random.sample(api_response[1:], 2)

    # Save the names and populations of the two cities as global variables
    global city1, city2, city1_pop, city2_pop
    city1 = cities[0][0]
    city2 = cities[1][0]
    city1_pop = int(cities[0][1])
    city2_pop = int(cities[1][1])

def get_coordinates_for_city(city):
    # Use the OpenStreetMap API to get the coordinates of the city
    api_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"

    # Make the API request
    response = requests.get(api_url)
    data = response.json()

    # Get the latitude and longitude from the API response
    lat = data[0]["lat"]
    lng = data[0]["lon"]

    return lat, lng

def get_famous_cities():
    global city1, city2, city1_pop, city2_pop, city1_lat, city1_lng, city2_lat, city2_lng, city1_img_url, city2_img_url
    # construct the API url with your API username and no bounds parameters
    api_url = f'http://api.geonames.org/citiesJSON?north=90&south=-90&east=180&west=-180&lang=en&username=squirtlesquadron'
    
    # make a GET request to the API
    response = requests.get(api_url)
    
    # check if the "geonames" key is present in the response
    if 'geonames' in response.json():
        # get the list of cities from the response
        cities = response.json()['geonames']
    else:
        # return an error message if the key is not present
        return "Error: Could not get list of cities from the API response."
    
    # choose two random cities from the list

    city1list = random.choice(cities)
    city2list = random.choice(cities)
    while city1list['name'] == city2list['name']:
        city2list = random.choice(cities)
    city1 = city1list['name']
    city2 = city2list['name']
    city1_pop = city1list['population']
    city2_pop = city2list['population']
    city1_lat, city1_lng = get_coordinates_for_city(city1)
    city1_img_url = get_image(city1_lat,city1_lng)
    city2_lat, city2_lng = get_coordinates_for_city(city2)
    city2_img_url = get_image(city2_lat,city2_lng)

    return city1,city2,city1_pop,city2_pop, city1_img_url, city2_img_url

def get_image(lat, lng):
    # Use the OpenStreetMap API to get an image for the city
    api_url = f"https://static-maps.yandex.ru/1.x/?lang=en_US&ll={lng},{lat}&z=12&l=map"

    # Return the API URL as the image URL
    return api_url

'''
Returns the key in the specified file in string format
'''
def get_key(file_name: str):
    path = f'keys/{file_name}'

    with open(path) as key:
        return key.read().strip('\n')


