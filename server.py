from flask import Flask, jsonify, request, send_from_directory

from main import main, Game

app = Flask(__name__, static_folder="site", static_url_path="")
game = Game()


@app.get("/")
def index():
    return send_from_directory("site", "index.html")


@app.post("/api/start")
def start_game():
    game.start_game()
    return jsonify({"status": "started"})


@app.post("/api/guess")
def make_guess():
    data = request.get_json()
    lookup = game.guess(data["guess"])

    return jsonify({
        "status": lookup.status,
        "comparison": game.comparison,
        "player": game.player.name if game.player else None,
    })


if __name__ == "__main__":
    app.run(debug=True, port=8000)