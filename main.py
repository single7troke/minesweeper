import sys
from game import Game


def get_initial_params(params):
    if params and len(params) == 3:
        try:
            columns = int(params[0]) if int(params[0]) >= 10 else 10
            rows = int(params[1]) if int(params[1]) >= 5 else 5
            difficulty = float(params[2])
            return Game(rows, columns, difficulty)
        except ValueError:
            print("Input values should be integer for rows, integer for columns and float for difficulty")
            print("Game started with default parameters")
            return Game()
    else:
        return Game()


if __name__ == "__main__":
    user_input = sys.argv[1:]
    new_game = get_initial_params(user_input)
    new_game.run()
