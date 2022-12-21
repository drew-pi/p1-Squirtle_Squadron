from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response        #facilitate form submission
import os 
import db_tools
from api import *
import random
import requests

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)

# https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=place:*&in=state:*&key=f9ca0722a830a37dcd77c39571e64d6f691cdefe
# Global variables to store the names and populations of the two cities
city1 = None
city2 = None
city1_pop = None
city2_pop = None
score= int(0)

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
    print(city1_pop,city2_pop)



@app.route('/')
def index():
    if 'username' in session:
        return (url_for('home'))
    return render_template( 'login.html',)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    password = session['password']
    if db_tools.verify_account(username, password):
        return render_template("home_page.html", username = username)

@app.route('/login', methods = ['GET','POST'])
def login():
    #Check if it already exists in database and render home page if it does
    #otherwise redirect to error page which will have a button linking to the login page
    username = request.form.get('username')
    password = request.form.get('password')
    if db_tools.verify_account(username,password):
        session['username'] = username
        session['password'] = password
        return redirect("/home")
    if request.form.get('submit_button') is not None:
        return render_template("create_account.html")
    else:
        resp = make_response(render_template('error.html',msg = "Username or password is not correct"))
        return resp

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    '''
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    '''
    #print("creating account")
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password') 
        #print(userIn)
        #print(passIn)
        if db_tools.add_account(userIn, passIn) == -1:
            resp = make_response(render_template('error.html',msg = "User already exists!"))
            return resp
        else:
            return render_template("sign_up_success.html")
            #return redirect("/login")
    return render_template("create_account.html")
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

def verify_session():
    if 'username' in session and 'password' in session:
        if db_tools.verify_account(session['username'], session['password']):
            return True
    return False

@app.route('/country')
def country():
    first_city = get_rand_city()
    second_city = get_rand_city()
    first_city_text = first_city['city'] + " " + first_city['region'] + " " + first_city['country']
    second_city_text = second_city['city'] + " " + second_city['region'] + " " + second_city['country']
    first_img_url = get_city_img("city of " + first_city['city'] + " " + first_city['country'])
    second_img_url = get_city_img("city of " + second_city['city'] + " " + second_city['country'])
    return render_template('country.html', first_city_text = first_city_text, second_city_text = second_city_text, first_img_url = first_img_url, second_img_url = second_img_url, first_city_temp = "", second_city_temp = "")

@app.route('/game')
def game():
    get_cities()

    # Render the home page template with the city names
    return render_template('game.html', city1=city1, city2=city2, city1_pop=city1_pop, city2_pop=city2_pop)

@app.route('/result', methods=['POST'])
def result():
    # Get the guess from the form submission
    guess = request.form['guess']

    # Get the names and populations of the two cities from the global variables
    global city1, city2, city1_pop, city2_pop, score

    # Compare the populations of the two cities
    if guess == 'Higher':
        if city1_pop > city2_pop:
            result = 'Correct'
            get_cities()
            score=score+1
            return render_template('game.html', city1=city1, city2=city2, city1_pop=city1_pop, city2_pop=city2_pop,score=score)
        else:
            result = 'Incorrect'
    elif guess == 'Lower':
        if city1_pop < city2_pop:
            result = 'Correct'
            get_cities()
            score=score+1
            return render_template('game.html', city1=city1, city2=city2, city1_pop=city1_pop, city2_pop=city2_pop,score=score)
        else:
            result = 'Incorrect'

    # Render the result template with the city names and result
    return render_template('result.html', city1=city1, city2=city2, city1_pop=city1_pop, city2_pop=city2_pop, result=result, score=score)

@app.route('/play-again')
def play_again():
    # Reset the global variables
    global city1, city2, city1_pop, city2_pop, score
    city1 = None
    city2 = None
    city1_pop = None
    city2_pop = None
    score = int(0)

    # Redirect to the home page
    return redirect('/game')

if __name__ == "__main__": #false if this file imported as module
    app.debug = True 
    app.run()