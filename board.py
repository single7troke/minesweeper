from cell import Cell
from random import random
import time


class Board:
    def __init__(self, rows, columns, difficulty):
        self.rows = rows
        self.columns = columns
        self.difficulty = difficulty
        self.game_map = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        self.neighbor_cells_coordinates = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        self.bombs_coordinate = []
        self.start_time = 0

    def create_map(self, first_click_row, first_click_column):
        self.start_time = time.time()
        cells_near_first_click = [(first_click_row + i, first_click_column + j) for i, j in self.neighbor_cells_coordinates]
        cells_near_first_click.append((first_click_row, first_click_column))
        for row in range(self.rows):
            for column in range(self.columns):
                if random() < self.difficulty and (row, column) not in cells_near_first_click:
                    self.game_map[row][column].set_bomb()
                    self.bombs_coordinate.append((row, column))
                    self.count_of_neighbor_bombs(row, column)

    def count_of_neighbor_bombs(self, row, column):
        for x, y in self.neighbor_cells_coordinates:
            neighbor_row = row + x
            neighbor_column = column + y
            if 0 <= neighbor_row < self.rows and 0 <= neighbor_column < self.columns and not self.game_map[neighbor_row][neighbor_column].bomb:
                self.game_map[neighbor_row][neighbor_column].empty = False
                self.game_map[neighbor_row][neighbor_column].nearby_bombs_count += 1

    def open_empty_cells(self, row, column, cell):
        if cell.nearby_bombs_count and cell.flag:
            return
        elif cell.nearby_bombs_count:
            cell.set_clicked()
            return
        elif cell.empty and not cell.clicked:
            cell.set_clicked()
            for x, y in self.neighbor_cells_coordinates:
                next_row = row + x
                next_column = column + y
                if 0 <= next_row < self.rows and 0 <= next_column < self.columns:
                    cell = self.game_map[next_row][next_column]
                    self.open_empty_cells(next_row, next_column, cell)

    def click_handler(self, left, right, pos, cell_size):
        s = cell_size
        if pos[1] / s > 2:
            try:
                cell = self.game_map[(pos[1] // s) - 2][pos[0] // s]
            except IndexError:
                return
            if left and cell.flag:
                return
            elif left and not cell.clicked and cell.empty:
                self.open_empty_cells((pos[1] // s) - 2, pos[0] // s, cell)
            elif left and not cell.clicked and cell.nearby_bombs_count:
                cell.set_clicked()
            elif left and not cell.clicked and cell.bomb:
                self.show_all_bombs()
            elif right and not cell.clicked:
                cell.flag = not cell.flag

    def show_all_bombs(self):
        for row, column in self.bombs_coordinate:
            self.game_map[row][column].clicked = True

    def check_win(self):
        flagged_cells = 0
        for row in self.game_map:
            for cell in row:
                if not cell.bomb and not cell.clicked:
                    return False
                elif cell.bomb and cell.flag:
                    flagged_cells += 1
        if flagged_cells == len(self.bombs_coordinate):
            return True

    def check_loss(self):
        for row, column in self.bombs_coordinate:
            if self.game_map[row][column].clicked:
                return True
