from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "NBA Guesser API is running!"