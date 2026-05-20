from mazegenerator.mazegenerator import MazeGenerator
import math
import arcade


class Map:
    def __init__(self, size, win):
        self.first_game = True

        self.size = size
        self.seed = 0
        self.win = win
        ref = self.win[0] if self.win[0] < self.win[1] else self.win[1]
        self.cell = int(math.floor((ref - (2 * 5)) / self.size[0]))
        self.margin = (int((self.win[0] - self.size[0] * self.cell) / 2),
                       int(self.win[1] - self.size[1] * self.cell) / 2)
        self.grid = []

        self.map = []
        # use_spatial_hash permet d'acceler la detection de colisions
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_textures = arcade.load_spritesheet(
            file_name="assets/sprite/maze_parts.png",
            sprite_width=16,
            sprite_height=16,
            columns=16,
            count=16
        )

    def generate_maze(self):
        self.generator = MazeGenerator(size=self.size, seed=self.seed)
        if self.first_game is True:
            self.generator.generate(self.generator._seed)
            self.first_game = False
        else:
            self.generator.generate(0)
        self.maze = self.generator._maze

    def draw(self):
        north = [1, 3, 5, 7, 9, 11, 13, 15]
        est = [2, 3, 6, 7, 10, 11, 14, 15]
        south = [4, 5, 6, 7, 12, 13, 14, 15]
        west = [8, 9, 10, 11, 12, 13, 14, 15]

        for y in range(self.size[1]):
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
                    arcade.draw_line(c0[0], c0[1], c1[0], c1[1],
                                     arcade.color.WHITE, 1)
                if self.maze[y][x] in south:
                    arcade.draw_line(c2[0], c2[1], c3[0], c3[1],
                                     arcade.color.WHITE, 1)
                if self.maze[y][x] in est:
                    arcade.draw_line(c1[0], c1[1], c3[0], c3[1],
                                     arcade.color.WHITE, 1)
                if self.maze[y][x] in west:
                    arcade.draw_line(c0[0], c0[1], c2[0], c2[1],
                                     arcade.color.WHITE, 1)
                if self.maze[y][x] == 15:
                    arcade.draw_lbwh_rectangle_filled(c0[0], c2[1],
                                                      (c1[0] - c0[0]),
                                                      (c0[1] - c2[1]),
                                                      arcade.color.BLUE)

                # i, j = self.grid[y][x]
                # arcade.draw_circle_filled(i, j, 3, arcade.color.RED)

    def calculate_grid(self):
        x0 = self.margin[0] + self.cell // 2
        y0 = self.win[1] - self.margin[0] - self.cell // 2

        for y in range(self.size[1]):
            self.grid.append([])
            for x in range(self.size[0]):
                self.grid[y].append((x0 + x * self.cell, y0 - y * self.cell))
