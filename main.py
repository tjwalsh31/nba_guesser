"""Main game loop for the NBA guessing game."""

from compare_players import (
    compare_age,
    compare_conference,
    compare_division,
    compare_height,
    compare_jersey,
    compare_player,
    compare_position,
    compare_teams,
)
from getplayer import Player


class Game:
    """Represents the game logic for guessing a target NBA player."""

    def __init__(self):
        self.playing = False
        self.guesses = []
        self.num_guesses = 0
        self.target = None
        self.player = None
        self.comparison = {}

    def start_game(self):
        """Start a new round and select a target player."""
        self.playing = True
        self.guesses = []
        self.num_guesses = 0
        self.target = Player()
        self.target.set_target()

    def guess(self, string):
        """Process a player guess and return whether the entry was invalid."""
        self.player = Player()
        if self.player.set_player_by_name(string) == 1:
            print("Player not found.")
            return True

        if self.player.name in self.guesses:
            print("Player already guessed.")
            return True

        self.guesses.append(self.player.name)
        self.process_guess()
        return False

    def process_guess(self):
        """Process the current guess and compare it to the target player."""
        print(f"\n{self.num_guesses}\t{self.player}")
        self.num_guesses += 1
        self.compare_guess()
        return self.player.name

    def compare_guess(self):
        """Compare the player's guess against the target player."""
        self.comparison = {
            "team": compare_teams(self.target, self.player),
            "division": compare_division(self.target, self.player),
            "conference": compare_conference(self.target, self.player),
            "position": compare_position(self.target, self.player),
            "height": compare_height(self.target, self.player),
            "age": compare_age(self.target, self.player),
            "jersey": compare_jersey(self.target, self.player),
            "player": compare_player(self.target, self.player),
        }
        print(f"\n{self.comparison}\n")

    def __str__(self):
        """Return a readable summary of the current game state."""
        target_name = self.target.name if self.target is not None else "None"
        return (
            f"Game playing: {self.playing}, guesses: {self.num_guesses}, "
            f"target: {target_name}"
        )


def main():
    """Run the main NBA guess game loop."""
    exit = False

    while exit is False:
        game = Game()
        input("Press enter to start a new game or type 'exit' to quit: ")
        game.start_game()


        while game.playing:
            guess_name = input("Enter your guess for the player: ")
            
            if guess_name.lower() == "exit":
                game.playing = False
                break

            elif game.guess(guess_name):
                print("Enter another player...")
                continue

            elif game.comparison.get("player") == "=":
                print(f"You guessed the player in {game.num_guesses} guesses!")
                game.playing = False



            elif game.num_guesses == 8:
                print("No more guesses")
                print(game.target)
                game.playing = False



        print("Play again? (y/n)")
        play_again = input().lower()
        if play_again != "y":
            exit = True
            print("Thanks for playing!")
        else:
            game.start_game()

        


if __name__ == "__main__":
    main()
