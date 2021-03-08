import pygame
import pygame.freetype
from board import Board
from colours import *
from time import sleep, time
import random


class Game:
    def __init__(self, rows=12, columns=17, difficulty=0.13):
        pygame.init()
        self.rows = rows
        self.columns = columns
        self.cell_size = 35

        self.board = Board(self.rows, self.columns, difficulty)
        self.width = self.cell_size * self.columns
        self.height = self.cell_size * (self.rows + 2)
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.difficulty = difficulty
        self.game_time = None
        self.new_game_button_color = GREY
        self.font = pygame.freetype.Font("rosemary.ttf", self.cell_size - 4)
        self.click_sound = pygame.mixer.Sound("sounds/click.wav")

    def draw_grid(self):
        for i in range(self.columns):
            new_width = round(i * self.cell_size)
            pygame.draw.line(self.screen, GREED, (new_width, self.cell_size * 2), (new_width, self.height), 3)
        for i in range(2, self.rows + 2):
            new_height = round(i * self.cell_size)
            pygame.draw.line(self.screen, GREED, (0, new_height), (self.width, new_height), 3)

    def draw_top(self):
        pygame.draw.rect(self.screen, LIGHT_GREY, (0, 0, self.width, self.height))

    def draw_time(self, start_time):
        self.game_time = int(time() - start_time)
        if self.game_time >= 10**4:
            self.game_time = 9999
        self.font.render_to(self.screen,
                            (self.cell_size * (self.columns - 2), self.cell_size / 1.5),
                            f"{self.game_time:04d}")

    def draw_bomb_count(self):
        bombs = len(self.board.bombs_coordinate)
        self.font.render_to(self.screen, (10, self.cell_size / 1.5), f"{bombs}")

    def draw_new_game_button(self, color, pressed=False):
        x = (self.width / 2) - self.cell_size * 2.5
        y = self.cell_size / 4
        width = self.cell_size * 5
        height = self.cell_size * 1.5
        if pressed:
            pygame.draw.rect(self.screen, color, [x + 2, y + 2, width, height], border_radius=3)
            self.font.render_to(self.screen,
                                (int(x + self.cell_size / 2 + 2), int(y + self.cell_size / 3 + 2)), "New Game")
        else:
            pygame.draw.rect(self.screen, BLACK, [x + 2, y + 2, width, height], 2, border_radius=4)
            pygame.draw.rect(self.screen, color, [x, y, width, height], border_radius=3)
            self.font.render_to(self.screen,
                                (int(x + self.cell_size / 2), int(y + self.cell_size / 3)), "New Game", (0, 0, 0))

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
                    pygame.draw.rect(self.screen, PINK, parameters)
                    self.font.render_to(self.screen,
                                        (self.cell_size * column + self.cell_size // 3,
                                         self.cell_size * (row + 2) + self.cell_size // 5), "B", (0, 0, 0))
                elif cell.mistake:
                    pygame.draw.rect(self.screen, PINK, parameters)
                    self.font.render_to(self.screen,
                                        (self.cell_size * column + self.cell_size // 3,
                                         self.cell_size * (row + 2) + self.cell_size // 5), "X", (0, 0, 0))
                elif not cell.clicked:
                    pygame.draw.rect(self.screen, GREY, parameters)
                elif cell.bomb:
                    pygame.draw.rect(self.screen, RED, parameters)
                elif cell.nearby_bombs_count:
                    pygame.draw.rect(self.screen, BLUE, parameters)
                    self.font.render_to(self.screen,
                                        (self.cell_size * column + self.cell_size // 3,
                                         self.cell_size * (row + 2) + self.cell_size // 5),
                                        f"{self.board.game_map[row][column]}", (0, 0, 0))
                else:
                    pygame.draw.rect(self.screen, GREEN, parameters)

    def draw_win(self, text):
        win_sound = pygame.mixer.Sound("sounds/win.mp3")
        win_sound.set_volume(0.2)
        win_sound.play()
        char = iter(text)
        t = 0.025
        for row in range(self.rows):
            for column in range(self.columns):
                parameters = (self.cell_size * column, self.cell_size * (row + 2), self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GREEN, parameters)
                if row >= (self.rows / 2) - 2 and column >= (self.columns - len(text)) / 2:
                    try:
                        self.font.render_to(self.screen,
                                            (self.cell_size * column + self.cell_size // 3,
                                             self.cell_size * (row + 2) + self.cell_size // 5 - 1), f"{next(char)}")
                    except StopIteration:
                        pass
                self.draw_grid()
                pygame.display.update()
                sleep(t)
                t /= 1.01

    def draw_lose(self):
        bomb_sound = pygame.mixer.Sound("sounds/lose.mp3")
        bomb_sound.set_volume(0.2)
        bomb_sound.play()
        sleep(1)
        random.shuffle(self.board.bombs_coordinate)
        for x, y in self.board.bombs_coordinate:
            cell = self.board.game_map[x][y]
            if cell.bomb and not cell.clicked and not cell.flag:
                bomb_sound = pygame.mixer.Sound("sounds/bomb.mp3")
                bomb_sound.set_volume(0.3)
                bomb_sound.play()
                cell.clicked = True
                self.draw_cells()
                self.draw_grid()
                pygame.display.update()
                sleep(random.randint(6, 30) / 100)
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board.game_map[row][column].flag and not self.board.game_map[row][column].bomb:
                    self.board.game_map[row][column].flag = not self.board.game_map[row][column].flag
                    self.board.game_map[row][column].mistake = True
                    self.draw_cells()
                    self.draw_grid()
                    pygame.display.update()

    def run(self):
        game = True
        first_click = True
        lose_or_win = False
        pressed = False

        while game:
            pos = pygame.mouse.get_pos()
            pygame.time.Clock().tick(75)
            for event in pygame.event.get():
                left, _, right = pygame.mouse.get_pressed(num_buttons=3)
                if event.type == pygame.QUIT:
                    game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_sound.play(fade_ms=200)
                    if self.is_over_new_game_button(pos) and event.button == 1:
                        self.board = Board(self.rows, self.columns, self.difficulty)
                        first_click = True
                        lose_or_win = False
                        pressed = True
                    if first_click and pos[1] > (self.cell_size * 2) and not lose_or_win:
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
                        self.new_game_button_color = OVER_BUTTON
                    else:
                        self.new_game_button_color = BUTTON

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
                                    f"{self.game_time:04d}")
                self.draw_bomb_count()
                pygame.display.update(pygame.Rect(0, 0, self.width, self.cell_size * 2))

            if (self.board.check_loss() or self.board.check_win()) and not lose_or_win:
                if self.board.check_loss():
                    self.draw_lose()
                else:
                    self.draw_win("YOU WIN!")
                lose_or_win = True
                first_click = True
