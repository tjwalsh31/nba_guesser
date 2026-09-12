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
    return [game.playing, game.num_guesses]

@app.route("/guess", methods=["POST"])
def guess():
    player_name = request.form["player"]
    game.guess(player_name)
    return redirect(url_for("index"))

@app.route("/get_game_data")
def get_guess_data():
    s = ""
    guess_data = {
        "name": game.player.name,
        "team": game.comparison["team"],
        "division": game.comparison['division'],
        "conference": game.comparison['conference'],
        "position": game.comparison['position'],
        "height": s.join(game.comparison['height']),
        "age": s.join(game.comparison['age']),
        "jersey": s.join(game.comparison['jersey']),
        "player": game.comparison['player']
    }
    return jsonify(guess_data)