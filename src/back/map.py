from mazegenerator.mazegenerator import MazeGenerator
from back.config import Config
from typing import List
from PIL import Image
import math
import arcade
import random


class Map:
    def __init__(self, config_data: Config, win: List[int]):
        self.config_data = config_data
        self.first_game = True
        self.seed = self.config_data.seed
        self.win = win
        self.size = self.config_data.lvl_size

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
        self.collectibles = []
        self.tile_list = arcade.SpriteList()
        self.pacgums_list = arcade.SpriteList()
        self.super_pacgums_list = arcade.SpriteList()
        self.sprites = {}


    def generate_maze(self):
        self.generator = MazeGenerator(size=self.size, seed=self.seed)
        if self.first_game is True:
            self.generator.generate(self.generator._seed)
            self.first_game = False
        else:
            self.generator.generate(0)
        self.maze = self.generator._maze
        self.init_pacgum()
        self.build_sprites()

    def build_sprites(self):
        scale = self.cell / 16
        wall_sheet = Image.open("assets/sprite/pixil-frame-0.png")
        wall_textures = []
        pacgum_image = Image.open("assets/sprite/pacgum.png")
        super_pacgum_image = Image.open("assets/sprite/super_pacgum.png")
        for i in range(16):
            region = wall_sheet.crop((i * 16, 0, i * 16 + 16, 16))
            wall_texture = arcade.Texture(image=region, name=f"tile_{i}")
            wall_textures.append(wall_texture)
        pacgums_texture = arcade.Texture(image=pacgum_image, name=f"pacgum")
        super_pacgum_texture = arcade.Texture(image=super_pacgum_image, name=f"super_pacgum")
        self.sprites["pacgum"] = pacgums_texture
        self.sprites["super_pacgum"] = super_pacgum_texture


        for y in range(self.size[1]):
            for x in range(self.size[0]):
                cx, cy = self.grid[y][x]
                cell_index = self.maze[y][x]

                sprite = arcade.Sprite(wall_textures[cell_index], scale=scale, center_x=cx, center_y=cy)

                if self.collectibles[y][x] == 1:
                    pacgums = arcade.Sprite(pacgums_texture, scale=scale, center_x=cx, center_y=cy)
                    self.pacgums_list.append(pacgums)

                if self.collectibles[y][x] == 2:
                    super_pacgums = arcade.Sprite(super_pacgum_texture, scale=scale, center_x=cx, center_y=cy)
                    self.super_pacgums_list.append(super_pacgums)
                
                self.tile_list.append(sprite)


    def draw(self):
        self.tile_list.draw()
        self.pacgums_list.draw()
        self.super_pacgums_list.draw()

    def calculate_grid(self):
        x0 = self.margin[0] + self.cell // 2
        y0 = self.win[1] - self.margin[1] - self.cell // 2

        for y in range(self.size[1]):
            self.grid.append([])
            for x in range(self.size[0]):
                self.grid[y].append((x0 + x * self.cell, y0 - y * self.cell))

    def init_pacgum(self):
        for y in range(self.size[1]):
            line = []
            for x in range(self.size[0]):
                if self.maze[y][x] == 15 or (x == round(self.size[0] / 2) - 1 and y == round(self.size[1] / 2) - 1):
                    line.append(int(9))
                elif ((y == 0 and x == 0) or 
                    (y == self.size[1] - 1 and x == 0) or 
                    (x == self.size[0] - 1 and y == 0) or 
                    (y == self.size[1] - 1 and x == self.size[0] - 1)):
                    line.append(int(2))
                else:
                    line.append(int(0))
            self.collectibles.append(line)

        cell_void = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.collectibles[y][x] == 0:
                    cell_void.append((y, x))

        if self.config_data.nb_pacgum > len(cell_void):
            raise ValueError("y a un pb")
        
        pacgums = random.sample(cell_void, self.config_data.nb_pacgum)

        for x, y in pacgums:
            self.collectibles[x][y] = 1
        
        # for line in self.collectibles:
        #     print(line)
        # print()

        # count = 0
        # for line in self.collectibles:
        #     for cell in line:
        #         if cell == 1:
        #             count += 1
        # print(count)
