from flask import Flask, redirect, render_template, request, url_for, jsonify
from .game import Game

app = Flask(__name__)
game = Game()

@app.get("/")
def index():
    return render_template("index.html", game=game)

@app.route("/start_game", methods=["POST"])
def start_game():
    game.start_game()
    return redirect(url_for("index"))

@app.route("/process_guess", methods=["POST"])
def process_guess():
    player_name = request.form["player"]
    game.guess(player_name)
    return redirect(url_for("index"))