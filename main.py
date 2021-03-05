import sys
from game import Game


if __name__ == "__main__":
	columns = int(sys.argv[1])
	rows = int(sys.argv[2])
	cell_size = int(sys.argv[3])
	difficulty = float(sys.argv[4])
	new_game = Game(rows, columns, cell_size, difficulty)
	new_game.run()
