"""Main game loop for the NBA guessing game."""

from .comparison import PlayerComparison
from .players import Player
from .game import Game

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