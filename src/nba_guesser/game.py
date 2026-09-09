from .players import Player
from .comparison import PlayerComparison

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
        if self.player.current_team.abbreviation in ("TOT", "UNK"):
            print("Player has an unknown or total team. Please guess another player.")
            return False
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
