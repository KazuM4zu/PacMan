from mazegenerator.mazegenerator import MazeGenerator
from back.config import Config
from typing import List
from PIL import Image
import math
import arcade


class Map:
    def __init__(self, config_data: Config, win: List[int]):
        self.first_game = True
        self.seed = 0
        self.win = win
        self.size = config_data.lvl_size

        self.game_zone = (self.win[0] // 2, self.win[1])


        cell_w = self.game_zone[0] // self.size[0]
        cell_h = self.game_zone[1] // self.size[1]
        self.cell = min(cell_w, cell_h)

        maze_w = self.cell * self.size[0]
        maze_h = self.cell * self.size[1]

        zone_x_start = self.win[0] // 4
        self.margin = (
            zone_x_start + (self.game_zone[0] - maze_w) // 2,
            (self.win[1] - maze_h) // 2
        )

        self.grid = []
        self.map = []
        self.tile_list = arcade.SpriteList()

    def generate_maze(self):
        self.generator = MazeGenerator(size=self.size, seed=self.seed)
        if self.first_game is True:
            self.generator.generate(self.generator._seed)
            self.first_game = False
        else:
            self.generator.generate(0)
        self.maze = self.generator._maze
        self.build_sprites()

    def build_sprites(self):
        self.tile_list = arcade.SpriteList()
        scale = self.cell / 16

        # Découpe la spritesheet avec PIL
        sheet = Image.open("assets/sprite/pixil-frame-0.png")
        textures = []
        for i in range(16):
            region = sheet.crop((i * 16, 0, i * 16 + 16, 16))
            texture = arcade.Texture(image=region, name=f"tile_{i}")
            textures.append(texture)

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                cx, cy = self.grid[y][x]
                tile_index = self.maze[y][x]

                sprite = arcade.Sprite(scale=scale)
                sprite.texture = textures[tile_index]
                sprite.center_x = cx
                sprite.center_y = cy
                self.tile_list.append(sprite)

    def draw(self):
        self.tile_list.draw()

    def calculate_grid(self):
        x0 = self.margin[0] + self.cell // 2
        y0 = self.win[1] - self.margin[1] - self.cell // 2

        for y in range(self.size[1]):
            self.grid.append([])
            for x in range(self.size[0]):
                self.grid[y].append((x0 + x * self.cell, y0 - y * self.cell))
