from mazegenerator.mazegenerator import MazeGenerator
import math
import arcade

class Game:
    def __init__(self, size: tuple[int, int], seed: int, win: tuple[int, int]):
        self.size = size
        self.seed = seed
        self.first_game = True

        self.win = win
        ref = self.win[0] if self.win[0] < self.win[1] else self.win[1]
        self.cell = math.floor((ref - (2 * 5)) / size[0])
        self.margin = (((win[0] - self.size[0] * self.cell) / 2),
                       (win[1] - self.size[1] * self.cell) / 2)

        self.maze = []

    def generate_maze(self):
        self.generator = MazeGenerator(size=self.size, seed=self.seed)
        if self.first_game is True:
            self.generator.generate(self.generator._seed)
            self.first_game = False
        else:
            self.generator.generate(0)
        self.maze = self.generator._maze

    def print_game(self):
        north = [1, 3, 5, 7, 9, 11, 13, 15]
        est = [2, 3, 6, 7, 10, 11, 14, 15]
        south = [4, 5, 6, 7, 12, 13, 14, 15]
        west = [8, 9, 10, 11, 12, 13, 14, 15]

        for y in range(self.size[0]):
            for x in range(self.size[0]):
                c0 = ((self.margin[0] + self.cell * x),
                      (self.win[1] - self.margin[0] - self.cell * y))
                c1 = ((self.margin[0] + self.cell * (x + 1)),
                      (self.win[1] - self.margin[0] - self.cell * y))
                c2 = ((self.margin[0] + self.cell * x),
                      (self.win[1] - self.margin[0] - self.cell * (y + 1)))
                c3 = ((self.margin[0] + self.cell * (x + 1)),
                      (self.win[1] - self.margin[0] - self.cell * (y + 1)))

                if self.maze[y][x] in north:
                    arcade.draw_line(c0[0], c0[1], c1[0], c1[1], arcade.color.WHITE, 1)
                if self.maze[y][x] in south:
                    arcade.draw_line(c2[0], c2[1], c3[0], c3[1], arcade.color.WHITE, 1)
                if self.maze[y][x] in est:
                    arcade.draw_line(c1[0], c1[1], c3[0], c3[1], arcade.color.WHITE, 1)
                if self.maze[y][x] in west:
                    arcade.draw_line(c0[0], c0[1], c2[0], c2[1], arcade.color.WHITE, 1)


window = arcade.Window(500, 520, "Pac-Man")
grrr = Game((15,15), 69, (500, 520))
grrr.generate_maze()
grrr.print_game()
arcade.run()