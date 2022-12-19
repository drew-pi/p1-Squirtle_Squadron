from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response        #facilitate form submission
import os 
import db_tools
from api import *

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)
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

if __name__ == "__main__": #false if this file imported as module
    app.debug = True 
    app.run()