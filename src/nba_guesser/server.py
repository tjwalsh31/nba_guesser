from flask import Flask
from .comparison import PlayerComparison
from .game import Game
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "NBA Guesser API is running!"


@app.route('/api/start')
def start_game():
    game = Game()
    game.start_game()