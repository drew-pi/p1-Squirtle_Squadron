from flask import Flask, render_template, request, redirect
import requests
import random

app = Flask(__name__)

# Global variables to store the names and populations of the two cities
city1 = None
city2 = None
city1_pop = None
city2_pop = None

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

@app.route('/')
def home():
    get_cities()

    # Render the home page template with the city names
    return render_template('game.html', city1=city1, city2=city2)

@app.route('/result', methods=['POST'])
def result():
    # Get the guess from the form submission
    guess = request.form['guess']

    # Get the names and populations of the two cities from the global variables
    global city1, city2, city1_pop, city2_pop

    # Compare the populations of the two cities
    if guess == 'Higher':
        if city1_pop > city2_pop:
            result = 'Correct'
            get_cities()
            return render_template('game.html', city1=city1, city2=city2)
        else:
            result = 'Incorrect'
    elif guess == 'Lower':
        if city1_pop < city2_pop:
            result = 'Correct'
            get_cities()
            return render_template('game.html', city1=city1, city2=city2)
        else:
            result = 'Incorrect'

    # Render the result template with the city names and result
    return render_template('result.html', city1=city1, city2=city2, result=result)

@app.route('/play-again')
def play_again():
    # Reset the global variables
    global city1, city2, city1_pop, city2_pop
    city1 = None
    city2 = None
    city1_pop = None
    city2_pop = None

    # Redirect to the home page
    return redirect('/')

if __name__ == '__main__':
    app.run()