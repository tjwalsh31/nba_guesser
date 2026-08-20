"""Main game loop for the NBA guessing game."""

from compare_players import PlayerComparison
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
        """Process a player guess and return its lookup result."""
        self.player = Player()
        lookup = self.player.set_player_by_name(string)
        if lookup.status != "found":
            return lookup

        if self.player.id in self.guesses:
            print("Player already guessed.")
            return lookup

        self.guesses.append(self.player.id)
        self.process_guess()
        return lookup

    def select_guess(self, candidate):
        """Load and process a candidate selected by the caller."""
        self.player = Player()
        self.player.set_player_by_data(candidate)
        if self.player.id in self.guesses:
            print("Player already guessed.")
            return False

        self.guesses.append(self.player.id)
        self.process_guess()
        return True

    def process_guess(self):
        """Process the current guess and compare it to the target player."""
        print(f"\n{self.num_guesses}\t{self.player}")
        self.num_guesses += 1
        self.compare_guess()
        return self.player.name

    def compare_guess(self):
        """Compare the player's guess against the target player."""
        comp = PlayerComparison(self.target, self.player)
        self.comparison = comp.comp_for_game()
        # self.comparison = {
        #     "team": compare_teams(self.target, self.player),
        #     "division": compare_division(self.target, self.player),
        #     "conference": compare_conference(self.target, self.player),
        #     "position": compare_position(self.target, self.player),
        #     "height": compare_height(self.target, self.player),
        #     "age": compare_age(self.target, self.player),
        #     "jersey": compare_jersey(self.target, self.player),
        #     "player": compare_player(self.target, self.player),
        # }

        self.display_comparison()
        # print(self.comparison)
        return self.comparison

    def display_comparison(self):
        """Display the comparison results for the current guess."""
        print("\t", end="")
        for key, value in self.comparison.items():
            if key in ["age", "height", "jersey"]:
                print(f"{key}: {value[0]}{value[1]}", end="  |  ")
            else:
                print(f"{key}: {value}", end ="  |  ")
        print("\n")



    def print_target(self):
        """Print the target player's information."""
        print(f"Target player: {self.target}")

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

            if guess_name.lower() == "target":
                game.print_target()
                continue

            lookup = game.guess(guess_name)
            if lookup.status == "ambiguous":
                for index, candidate in enumerate(lookup.candidates):
                    print(f"{index}: {candidate['full_name']}")
                while True:
                    try:
                        choice = int(input("Enter number of player you want to select: "))
                        candidate = lookup.candidates[choice]
                        break
                    except (ValueError, IndexError):
                        print("Invalid choice. Please enter a valid number.")
                game.select_guess(candidate)
                continue

            if lookup.status == "not_found":
                print("Player not found.")
                print("Enter another player...")
                continue

            elif game.player.id == game.target.id:
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
