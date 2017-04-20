import pygame
from pygame.locals import *


BOARD_COLOR = (255, 204, 33)
COLOR=(0, 0, 0)

class Coach(object):
    pass

class GameManager(object):
    def __init__(self, screen, board_witdh, turns):
        self.turns = turns
        self.turn_index = 0
        self.screen = screen

        self.board_width = board_witdh

        self.board = [[0 for j in range(board_witdh)] for i in range(board_witdh)]
        self.board_line = [[[(x * 30) + 30, (y * 30) + 30] for x in range(board_witdh)] for y in range(board_witdh)]

        self.turn_color = [(0, 0, 0), (255, 255, 255)]

    def update_scene(self):
        self.draw_base_board()
        count = 0
        for turn in self.turns:
            self.draw_stone(turn["x"], turn["y"], self.turn_color[count % 2])
            if count == self.turn_index: break
            count += 1

    def draw_stone(self, x, y, color):
        pygame.draw.circle(self.screen, color, self.board_line[y][x], 14)

    def before(self):
        self.turn_index = (self.turn_index + len(self.turns) - 1) % len(self.turns)

    def after(self):
        self.turn_index = (self.turn_index + 1) % len(self.turns)

    def draw_base_board(self):
        self.screen.fill(BOARD_COLOR)
        for i in range(self.board_width):
            pygame.draw.line(self.screen,
                             COLOR,
                             (self.board_line[i][0][0], self.board_line[i][0][1]),
                             (self.board_line[i][self.board_width - 1][0], self.board_line[i][self.board_width - 1][1]))
            pygame.draw.line(self.screen,
                             COLOR,
                             (self.board_line[0][i][0], self.board_line[0][i][1]),
                             (self.board_line[self.board_width - 1][i][0], self.board_line[self.board_width - 1][i][1]))

        pygame.draw.circle(self.screen, COLOR, self.board_line[3][3], 3)
        pygame.draw.circle(self.screen, COLOR, self.board_line[15][3], 3)
        pygame.draw.circle(self.screen, COLOR, self.board_line[3][15], 3)
        pygame.draw.circle(self.screen, COLOR, self.board_line[15][15], 3)
        pygame.draw.circle(self.screen, COLOR, self.board_line[9][9], 3)


def start_game(turn_info):
    import pygame

    turns = turn_info[1:]

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    game_manager = GameManager(screen, 19, turns)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_manager.update_scene()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            game_manager.before()
            game_manager.update_scene()
        if pressed[pygame.K_RIGHT]:
            game_manager.after()
            game_manager.update_scene()

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    start_game([{"x": 15, "y":10}, {"x": 16, "y":10}, {"x": 13, "y":10}])