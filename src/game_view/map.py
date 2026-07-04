import random
from typing import Any, Dict, List, Tuple

import arcade
from PIL import Image

from src.config import Config
from mazegenerator.mazegenerator import MazeGenerator


class Map:
    """Represents a single game level's maze, grid, and visual tiles.

    Generates the maze layout, computes the pixel grid used to place
    sprites, places pac-gums and super pac-gums, and builds all the
    sprite lists required to draw the level.

    Attributes:
        config_data (Config): Overall game configuration.
        level_index (int): Index of the current level in the
            configuration's level list.
        current (Any): Configuration data specific to this level
            (width, height, number of pac-gums, etc.).
        seed (Any): Random seed used for maze generation.
        win (List[int]): Window dimensions ``[width, height]``.
        size (List[int]): Maze size in cells ``[width, height]``.
        game_zone (Tuple[int, int]): Pixel dimensions of the playable
            area within the window.
        cell (int): Size in pixels of a single maze cell.
        margin (Tuple[int, int]): Pixel offset of the maze's top-left
            corner within the window.
        grid (List[List[Tuple[float, float]]]): Pixel center coordinates
            of each maze cell, indexed as ``grid[y][x]``.
        map (List[Any]): Reserved/unused general-purpose map data.
        collects (List[List[int]]): Collectible markers per cell
            (``0`` empty, ``1`` pac-gum, ``2`` super pac-gum, ``9``
            wall/spawn-blocked cell).
        sprites (Dict[str, Any]): Loaded textures keyed by name
            (``"wall"``, ``"pacgum"``, ``"super_pacgum"``).
        scale (float): Sprite scale factor derived from cell size.
        tile_list (arcade.SpriteList): Sprites for maze wall tiles.
        pacgums_list (arcade.SpriteList): Sprites for regular pac-gums.
        super_pacgums_list (arcade.SpriteList): Sprites for super
            pac-gums.
        maze (List[List[int]]): Raw maze data, where each cell's value
            encodes its wall configuration.
        generator (Any): The maze generator instance used to build the
            maze.
    """

    def __init__(self, config_data: Config,
                 level_index: int,
                 win: List[int]) -> None:
        """Initialize the map's geometry for a given level.

        Computes the cell size, playable game zone, and margins based
        on the window size and level dimensions, and prepares empty
        containers for the grid, collectibles, and sprites (populated
        later by ``generate_maze``).

        Args:
            config_data (Config): Overall game configuration.
            level_index (int): Index of the level to load within
                ``config_data.level``.
            win (List[int]): Window dimensions ``[width, height]``.

        Returns:
            None
        """
        self.config_data = config_data
        self.level_index = level_index
        self.current = self.config_data.level[self.level_index]
        self.seed = self.config_data.seed
        self.win = win
        self.size: List[int] = [self.current.width, self.current.height]

        self.game_zone: Tuple[int, int] = (self.win[0] // 2, self.win[1])

        cell_w: int = self.game_zone[0] // self.size[0]
        cell_h: int = self.game_zone[1] // self.size[1]
        self.cell: int = min(cell_w, cell_h)

        maze_w: int = self.cell * self.size[0]
        maze_h: int = self.cell * self.size[1]

        zone_x_start: int = self.win[0] // 4
        self.margin: Tuple[int, int] = (
            zone_x_start + (self.game_zone[0] - maze_w) // 2,
            (self.win[1] - maze_h) // 2
        )

        self.grid: List[List[Tuple[float, float]]] = []
        self.map: List[Any] = []
        self.collects: List[List[int]] = []

        self.sprites: Dict[str, Any] = {}
        self.scale: float = self.cell / 16
        self.tile_list: arcade.SpriteList = arcade.SpriteList()
        self.pacgums_list: arcade.SpriteList = arcade.SpriteList()
        self.super_pacgums_list: arcade.SpriteList = arcade.SpriteList()

        self.maze: List[List[int]] = []
        self.generator: Any = None

    def generate_maze(self) -> None:
        """Generate the maze layout and build its visual representation.

        Creates a maze generator, generates the maze (using a fixed
        seed for the first level, or a randomized run for subsequent
        levels), then computes the pixel grid, places pac-gums, and
        builds the sprites for drawing.

        Returns:
            None
        """
        self.generator = MazeGenerator(size=self.size, seed=self.seed)

        if self.level_index == 0:
            self.generator.generate(self.generator._seed)
        else:
            self.generator.generate(0)

        self.maze = self.generator._maze
        self.calculate_grid()
        self.init_pacgum()
        self.build_sprites()

    def build_sprites(self) -> None:
        """Load textures and build all sprites for the level.

        Loads the wall tile sheet, pac-gum, and super pac-gum images,
        slices the wall tile sheet into 16 individual textures, stores
        them in ``sprites``, and delegates building individual tile
        and pac-gum sprites to ``build_pacgums_sprites``.

        Returns:
            None
        """
        wall_sheet = Image.open("assets/sprite/pixil-frame-0.png")
        wall_textures: List[arcade.Texture] = []
        pacgum_image = Image.open("assets/sprite/pacgum.png")
        super_pacgum_image = Image.open("assets/sprite/super_pacgum.png")

        for i in range(16):
            region = wall_sheet.crop((i * 16, 0, i * 16 + 16, 16))
            wall_texture = arcade.Texture(image=region, name=f"tile_{i}")
            wall_textures.append(wall_texture)

        pacgums_texture = arcade.Texture(image=pacgum_image, name="pacgum")
        super_pacgum_texture = arcade.Texture(
            image=super_pacgum_image,
            name="super_pacgum"
        )

        self.sprites["wall"] = wall_textures
        self.sprites["pacgum"] = pacgums_texture
        self.sprites["super_pacgum"] = super_pacgum_texture
        self.build_pacgums_sprites()

    def build_pacgums_sprites(self) -> None:
        """Create wall, pac-gum, and super pac-gum sprites for every cell.

        Iterates over every cell of the maze, creates the corresponding
        wall tile sprite, and adds a pac-gum or super pac-gum sprite
        at that position when ``collects`` marks it as collectible.
        Populates ``tile_list``, ``pacgums_list``, and
        ``super_pacgums_list``.

        Returns:
            None
        """
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                cx, cy = self.grid[y][x]
                cell_index = self.maze[y][x]

                sprite = arcade.Sprite(
                    self.sprites["wall"][cell_index],
                    scale=self.scale,
                    center_x=cx,
                    center_y=cy
                )

                if self.collects[y][x] == 1:
                    pacgums = arcade.Sprite(
                        self.sprites["pacgum"],
                        scale=self.scale,
                        center_x=cx,
                        center_y=cy
                    )
                    self.pacgums_list.append(pacgums)

                elif self.collects[y][x] == 2:
                    super_pacgums = arcade.Sprite(
                        self.sprites["super_pacgum"],
                        scale=self.scale,
                        center_x=cx,
                        center_y=cy
                    )
                    self.super_pacgums_list.append(super_pacgums)

                self.tile_list.append(sprite)

    def draw(self) -> None:
        """Draw the maze tiles, pac-gums, and super pac-gums.

        Returns:
            None
        """
        self.tile_list.draw()
        self.pacgums_list.draw()
        self.super_pacgums_list.draw()

    def calculate_grid(self) -> None:
        """Compute the pixel center coordinates of every maze cell.

        Fills ``grid`` with a 2D list of ``(x, y)`` pixel positions,
        one per maze cell, based on the cell size and margins
        computed in ``__init__``.

        Returns:
            None
        """
        x0 = self.margin[0] + self.cell // 2
        y0 = self.win[1] - self.margin[1] - self.cell // 2

        for y in range(self.size[1]):
            self.grid.append([])
            for x in range(self.size[0]):
                self.grid[y].append((x0 + x * self.cell, y0 - y * self.cell))

    def init_pacgum(self) -> None:
        """Initialize the ``collects`` grid and randomly place pac-gums.

        Marks unreachable/reserved cells (walls, spawn point) as
        non-collectible, marks the four corners as super pac-gums, and
        randomly distributes the configured number of regular
        pac-gums among the remaining empty cells.

        Raises:
            ValueError: If the configured number of pac-gums exceeds
                the number of available empty cells.

        Returns:
            None
        """
        for y in range(self.size[1]):
            line: List[int] = []
            for x in range(self.size[0]):
                if (self.maze[y][x] == 15 or
                    (x == round(self.size[0] / 2) - 1 and
                     y == round(self.size[1] / 2) - 1)):
                    line.append(int(9))
                elif ((y == 0 and x == 0) or
                      (y == self.size[1] - 1 and x == 0) or
                      (x == self.size[0] - 1 and y == 0) or
                      (y == self.size[1] - 1 and x == self.size[0] - 1)):
                    line.append(int(2))
                else:
                    line.append(int(0))
            self.collects.append(line)

        cell_void: List[Tuple[int, int]] = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.collects[y][x] == 0:
                    cell_void.append((y, x))

        if self.current.nb_pacgum > len(cell_void):
            raise ValueError("y a un pb")

        pacgums = random.sample(cell_void, self.current.nb_pacgum)

        for y, x in pacgums:
            self.collects[y][x] = 1
