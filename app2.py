from flask import Flask, redirect, url_for, render_template, request, json, flash, session, make_response
import requests
import time

from logging_logic import configure_logging
from login_logic import login
from mytools_logic import mytools
from infochk_logic import infochk

app = Flask(__name__)

# configure_logging(app)

app.config['SECRET_KEY'] = 'Satya#507'

#This will redirect to login_route in the starting
@app.route('/')
def index():
    return redirect(url_for("login_route"))

#redirect to login_logic for login validation with RACF user id and password.
@app.route("/login", methods=["POST", "GET"])
def login_route():
    return login()

#This will redirect to mytools_logic to select the tool to be used.
@app.route("/mytools", methods=["POST", "GET"])
def mytools_route():
    return mytools()

#This will redirect to infochk_logic to find or add person details with name and date of birth.
@app.route("/infochk", methods=["GET", "POST"])
def infochk_route():
    return infochk()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
