from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Generate a random city
    city = generate_random_city()

    # Use the OpenStreetMap API to get the coordinates of the city
    city_lat, city_lng = get_coordinates_for_city(city)

    # Use the OpenStreetMap API to get an image for the city
    city_image_url = get_image_for_city(city_lat, city_lng)

    return render_template('image.html', city=city, city_image_url=city_image_url)

def generate_random_city():
    # Generate a random city name here
    cities = ["Ardmore town, Alabama"]
    return random.choice(cities)

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

def get_image_for_city(lat, lng):
    # Use the OpenStreetMap API to get an image for the city
    api_url = f"https://static-maps.yandex.ru/1.x/?lang=en_US&ll={lng},{lat}&z=12&l=map"

    # Return the API URL as the image URL
    return api_url

if __name__ == '__main__':
    app.run()