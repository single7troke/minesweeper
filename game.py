"""
Установить минимальный и максимальный размер клетки.

draw top:
	draw time
	draw bomb
	draw button
"""

import pygame
import pygame.freetype
from board import Board
from time import sleep, time


class Game:
	def __init__(self, rows, columns, cell_size, difficulty=0.1):
		pygame.init()
		self.board = Board(rows, columns, difficulty)
		self.cell_size = cell_size
		self.columns = columns
		self.rows = rows
		self.width = self.cell_size * self.columns
		self.height = self.cell_size * (self.rows + 2)
		self.screen = pygame.display.set_mode([self.width, self.height])
		self.difficulty = difficulty
		self.game_time = None
		self.new_game_button_color = (182, 182, 182)
		self.font = pygame.freetype.Font("rosemary.ttf", self.cell_size - 4)

	def draw_grid(self):
		colour = (50, 50, 50)
		for i in range(self.columns):
			new_width = round(i * self.cell_size)
			pygame.draw.line(self.screen, colour, (new_width, self.cell_size * 2), (new_width, self.height), 3)
		for i in range(2, self.rows + 2):
			new_height = round(i * self.cell_size)
			pygame.draw.line(self.screen, colour, (0, new_height), (self.width, new_height), 3)

	def draw_top(self):
		pygame.draw.rect(self.screen, (210, 210, 210), (0, 0, self.width, self.height))

	def draw_time(self, start_time):
		self.game_time = int(time() - start_time)
		if self.game_time >= 10**4:
			self.game_time = 9999
		self.font.render_to(self.screen,
		                    (self.cell_size * (self.columns - 2), self.cell_size / 1.5),
		                    f"{self.game_time:04d}",
		                    (0, 0, 0))

	def draw_bomb_count(self):
		bombs = len(self.board.bombs_coordinate)
		self.font.render_to(self.screen, (10, self.cell_size / 1.5), f"{bombs}", (0, 0, 0))

	def draw_new_game_button(self, color, pressed=False):
		x = (self.width / 2) - self.cell_size * 2.5
		y = self.cell_size / 4
		width = self.cell_size * 5
		height = self.cell_size * 1.5
		if pressed:
			pygame.draw.rect(self.screen, color, (x + 2, y + 2, width, height), border_radius=3)
			self.font.render_to(self.screen, (x + self.cell_size / 2 + 2, y + self.cell_size / 3 + 2), "New Game", (0, 0, 0))
		else:
			pygame.draw.rect(self.screen, (0, 0, 0), (x + 2, y + 2, width, height), 2, border_radius=4)
			pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=3)
			self.font.render_to(self.screen, (x + self.cell_size / 2, y + self.cell_size / 3), "New Game", (0, 0, 0))

	def is_over_new_game_button(self, pos):
		x = (self.width / 2) - self.cell_size * 2.5
		y = self.cell_size / 4
		width = self.cell_size * 5
		height = self.cell_size * 1.5
		if x < pos[0] < x + width and y < pos[1] < y + height:
			return True
		return False

	def draw_cells(self):
		for row in range(self.rows):
			for column in range(self.columns):
				cell = self.board.game_map[row][column]
				parameters = (self.cell_size * column, self.cell_size * (row + 2), self.cell_size, self.cell_size)

				if cell.flag:
					pygame.draw.rect(self.screen, (255, 200, 200), parameters)
					self.font.render_to(self.screen,
					                    (self.cell_size * column + self.cell_size // 3,
					                     self.cell_size * (row + 2) + self.cell_size // 5), "B", (0, 0, 0))
				elif not cell.clicked:
					pygame.draw.rect(self.screen, (182, 182, 182), parameters)
				elif cell.bomb:
					pygame.draw.rect(self.screen, (255, 100, 100), parameters)
				elif cell.nearby_bombs_count:
					pygame.draw.rect(self.screen, (150, 150, 255), parameters)
					self.font.render_to(self.screen,
					                    (self.cell_size * column + self.cell_size // 3,
					                     self.cell_size * (row + 2) + self.cell_size // 5),
					                    f"{self.board.game_map[row][column]}", (0, 0, 0))
				else:
					pygame.draw.rect(self.screen, (150, 255, 150), parameters)

	def draw_lose_or_win(self, text, colour):
		char = (_ for _ in text)
		t = 0.025
		for row in range(self.rows):
			for column in range(self.columns):
				parameters = (self.cell_size * column, self.cell_size * (row + 2), self.cell_size, self.cell_size)
				pygame.draw.rect(self.screen, colour, parameters)
				if row >= (self.rows / 2) - 2 and column >= (self.columns - len(text)) / 2:
					try:
						self.font.render_to(self.screen,
						                    (self.cell_size * column + self.cell_size // 3,
						                     self.cell_size * (row + 2) + self.cell_size // 5 - 1), f"{next(char)}", (0, 0, 0))
					except StopIteration:
						pass
				self.draw_grid()
				pygame.display.update()
				sleep(t)
				t /= 1.01

	def run(self):
		flag = True
		first_click = True
		lose_or_win = False
		pressed = False
		while flag:
			pos = pygame.mouse.get_pos()
			pygame.time.Clock().tick(75)
			for event in pygame.event.get():
				left, _, right = pygame.mouse.get_pressed(num_buttons=3)
				if event.type == pygame.QUIT:
					flag = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.is_over_new_game_button(pos) and event.button == 1:
						self.board = Board(self.rows, self.columns, self.difficulty)
						first_click = True
						lose_or_win = False
						pressed = True
					if first_click and pos[1] > (self.cell_size * 2):
						row = pos[1] // self.cell_size - 2
						column = pos[0] // self.cell_size
						self.board.create_map(row, column)
						first_click = False
					if not lose_or_win:
						self.board.click_handler(left, right, pos, self.cell_size)

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						pressed = False

				if event.type == pygame.MOUSEMOTION:
					if self.is_over_new_game_button(pos):
						self.new_game_button_color = (197, 197, 217)
					else:
						self.new_game_button_color = (182, 182, 182)

			self.draw_top()
			if not first_click:
				self.draw_time(self.board.start_time)
				self.draw_bomb_count()
			self.draw_new_game_button(self.new_game_button_color, pressed)
			self.draw_cells()
			self.draw_grid()
			if not lose_or_win:
				pygame.display.update()
			else:
				self.font.render_to(self.screen,
				                    (self.cell_size * (self.columns - 2), self.cell_size / 1.5),
				                    f"{self.game_time:04d}",
				                    (0, 0, 0))
				self.draw_bomb_count()
				pygame.display.update(pygame.Rect(0, 0, self.width, self.cell_size * 2))

			if (self.board.check_loss() or self.board.check_win()) and not lose_or_win:
				if self.board.check_loss():
					self.draw_cells()
					self.draw_grid()
					pygame.display.update()
				else:
					self.draw_lose_or_win("YOU WIN!", (150, 255, 150))
				lose_or_win = True
				first_click = True
