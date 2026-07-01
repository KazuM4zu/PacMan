from typing import List, Any

import arcade
import threading
import time


class Player:
    """Represents the player-controlled Pac-Man character.

    Handles the player's position, movement, score, lives, and
    special states (super mode, invincibility, freeze), as well as
    collecting pac-gums and super pac-gums from the map.

    Attributes:
        config_data (Any): Game configuration data (lives, points per
            pac-gum, etc.).
        map (Any): The current level map the player moves through.
        cell_pos (List[int]): Player position in grid-cell coordinates
            ``[x, y]``.
        pos (List[float]): Player position in pixel coordinates
            ``[x, y]``.
        speed (int): Movement speed in pixels per frame.
        score (int): Current player score.
        lives (int): Number of lives remaining.
        dx (int): Current horizontal movement direction.
        dy (int): Current vertical movement direction.
        next_dx (int): Requested horizontal direction for the next move.
        next_dy (int): Requested vertical direction for the next move.
        super_mod (bool): Whether the player is currently in super mode
            (can eat ghosts).
        invicible (bool): Whether the player is currently invincible.
        freeze (bool): Whether player and ghost movement is frozen.
        stat_panel (Any): Reference to the UI stats panel, if any.
    """

    def __init__(self, map: Any, config_data: Any) -> None:
        """Initialize the player at the center of the map.

        Args:
            map (Any): The current level map.
            config_data (Any): Game configuration data.

        Returns:
            None
        """
        self.config_data = config_data
        self.map = map
        self.cell_pos = ([round(self.map.size[0] / 2) - 1,
                          round(self.map.size[1] / 2) - 1])
        x, y = self.cell_pos
        self.pos: List[float] = list(self.map.grid[y][x])
        self.speed: int = self.map.cell // 16

        self.score: int = 0
        self.lives: int = self.map.config_data.lives

        self.dx: int = 0
        self.dy: int = 0
        self.next_dx: int = 0
        self.next_dy: int = 0

        self.super_mod: bool = False
        self.invicible: bool = False
        self.freeze: bool = False

        self.stat_panel: Any = None

    def draw(self) -> None:
        """Draw the player as a yellow filled circle at its current position.

        Returns:
            None
        """
        arcade.draw_circle_filled(self.pos[0],
                                  self.pos[1],
                                  self.map.cell // 3 - 2,
                                  arcade.color.YELLOW)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Record the requested movement direction from arrow key input.

        The requested direction is stored in ``next_dx``/``next_dy``
        and applied on the next ``update`` call if the corresponding
        path is not blocked by a wall.

        Args:
            key (int): The arcade key code that was pressed.
            modifiers (int): Bitwise combination of active modifier
                keys (e.g., Shift, Ctrl).

        Returns:
            None
        """
        if key == arcade.key.LEFT:
            self.next_dx = -1
            self.next_dy = 0
        elif key == arcade.key.RIGHT:
            self.next_dx = 1
            self.next_dy = 0
        elif key == arcade.key.UP:
            self.next_dx = 0
            self.next_dy = 1
        elif key == arcade.key.DOWN:
            self.next_dx = 0
            self.next_dy = -1

    def update(self) -> None:
        """Update the player's position and handle pac-gum collection.

        Advances the player toward the target cell, changes direction
        when the requested direction is not blocked by a wall, and
        collects a pac-gum or super pac-gum (triggering ``eat_super``)
        when the player reaches a cell that contains one.

        Returns:
            None
        """
        cx, cy = self.map.grid[self.cell_pos[1]][self.cell_pos[0]]
        if self.pos == list(self.map.grid[self.cell_pos[1]][self.cell_pos[0]]):
            if not self.have_wall(self.next_dx, self.next_dy):
                self.dx = self.next_dx
                self.dy = self.next_dy

            if not self.have_wall(self.dx, self.dy):
                self.cell_pos[0] += self.dx
                self.cell_pos[1] -= self.dy
        target = list(self.map.grid[self.cell_pos[1]][self.cell_pos[0]])
        if self.pos[0] < target[0]:
            self.pos[0] = min(self.pos[0] + self.speed, target[0])
        elif self.pos[0] > target[0]:
            self.pos[0] = max(self.pos[0] - self.speed, target[0])
        if self.pos[1] < target[1]:
            self.pos[1] = min(self.pos[1] + self.speed, target[1])
        elif self.pos[1] > target[1]:
            self.pos[1] = max(self.pos[1] - self.speed, target[1])

        if (self.pos[1] == target[1] and self.pos[0] == target[0] and
           self.map.collects[self.cell_pos[1]][self.cell_pos[0]] == 1):
            for pacgum in self.map.pacgums_list:
                if pacgum.center_x == cx and pacgum.center_y == cy:
                    pacgum.kill()
                    self.map.collects[self.cell_pos[1]][self.cell_pos[0]] = 0
                    self.score += self.config_data.pt_per_pacgum
                    break

        if (self.pos[1] == target[1] and self.pos[0] == target[0] and
           self.map.collects[self.cell_pos[1]][self.cell_pos[0]] == 2):
            for super_pacgums in self.map.super_pacgums_list:
                if (super_pacgums.center_x == cx and
                   super_pacgums.center_y == cy):
                    super_pacgums.kill()
                    self.map.collects[self.cell_pos[1]][self.cell_pos[0]] = 0
                    self.score += self.config_data.pt_per_super_pacgum
                    self.eat_super()
                    break

    def have_wall(self, nx: int, ny: int) -> bool:
        """Check whether a wall blocks the player's movement in a direction.

        Args:
            nx (int): Horizontal direction to test (``-1``, ``0``, or
                ``1``).
            ny (int): Vertical direction to test (``-1``, ``0``, or
                ``1``).

        Returns:
            bool: ``True`` if a wall blocks movement in that
            direction from the player's current cell, ``False``
            otherwise.
        """
        current = self.map.maze[self.cell_pos[1]][self.cell_pos[0]]
        north = [1, 3, 5, 7, 9, 11, 13, 15]
        east = [2, 3, 6, 7, 10, 11, 14, 15]
        south = [4, 5, 6, 7, 12, 13, 14, 15]
        west = [8, 9, 10, 11, 12, 13, 14, 15]

        if nx == 1 and current in east:
            return True
        elif nx == -1 and current in west:
            return True
        elif ny == -1 and current in south:
            return True
        elif ny == 1 and current in north:
            return True

        return False

    def death(self) -> None:
        """Handle the player's death: lose a life and respawn at the center.

        Decrements ``lives``, resets movement direction, and moves the
        player back to the center cell of the map.

        Returns:
            None
        """
        self.lives -= 1
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.cell_pos = ([round(self.map.size[0] / 2) - 1,
                          round(self.map.size[1] / 2) - 1])
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])

    def eat_super(self) -> None:
        """Activate super mode for a limited duration.

        Starts a background thread that enables ``super_mod``
        immediately, then disables it again after a 7-second delay.

        Returns:
            None
        """
        def reset() -> None:
            self.super_mod = True
            time.sleep(7)
            self.super_mod = False

        thread = threading.Thread(target=reset)
        thread.start()