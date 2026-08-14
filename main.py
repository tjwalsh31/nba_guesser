from getplayer import *
from compare_players import *

class Game:
    """Represents game logic"""

    def __init__(self):
        self.playing = False
        self.guesses = None
        self.num_guesses = None


    def start_game(self):
        self.playing = True
        self.guesses = []
        self.num_guesses = 0
        self.target = Player()
        self.target.set_target()


    def guess(self, string):
        """Process user input for a guess."""
        self.player = Player()
        if (self.player.set_player_by_name(string)) == 1:
            print("Player not found.")
            return 1
        if self.process_guess() in self.guesses:
            print("Player already guessed.")
            return 1
        # print(self.player)


    def process_guess(self):
        """Processes the user input for a guess and does work."""
        print(f"{self.num_guesses}\t{self.player}")
        self.num_guesses += 1
        self.compare_guess()

    def compare_guess(self):
        """Compare the guess to the target player."""
        self.comparison = {
            "team": compare_teams(self.target, self.player),
            "division": compare_division(self.target, self.player),
            "conference": compare_conference(self.target, self.player),
            "position": compare_position(self.target, self.player),
            "height": compare_height(self.target, self.player),
            "age": compare_age(self.target, self.player),
            "jersey": compare_jersey(self.target, self.player),
            "player": compare_player(self.target, self.player)
        }
        print(f"\n{self.comparison}")


    
    def __str__(self):
        return f"Game playing: {self.playing}, guesses: {self.num_guesses}, target: {self.target.name}"



def main():
    game = Game()
    game.start_game()
    while game.playing:
        guess_name = input("Enter your guess for the player: ")
        if (game.guess(guess_name)) == 1:
            print("Enter another player...")
            continue
        if guess_name.lower() == "exit":
            game.playing = False
        if game.num_guesses == 8:
            print("No more guesses")
            game.playing = False
        if game.comparison["player"] == "=":
            print(f"You guessed the player in {game.num_guesses} guesses!")
            game.playing = False
        


if __name__ == "__main__":
    main()
