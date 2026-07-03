from collections import deque
import threading
import time
from typing import Any, Deque, List, Optional, Tuple

import arcade


class Inky:
    """Represents the Inky ghost in the Pac-Man game.

    Inky chases the player directly by computing the shortest path
    to the player's position using a breadth-first search (BFS) of
    the maze. When the player is in "super" mode (``super_mod``),
    Inky instead flees from the player, heading toward the
    farthest reachable cell.

    Attributes:
        manager (Any): The GhostManager instance that owns all ghosts.
        map (Any): The current level map (grid, cells, walls, etc.).
        player (Any): The player instance being chased or fled from.
        cell_pos (List[int]): Ghost position in grid-cell coordinates
        ``[x, y]``.
        pos (List[float]): Ghost position in pixel coordinates ``[x, y]``.
        dir (Tuple[int, int]): Current movement direction ``(dx, dy)``.
        dx (int): Horizontal component of the current direction.
        dy (int): Vertical component of the current direction.
        speed (int): Movement speed in pixels per frame.
        visible (bool): Whether the ghost is currently visible (``False``
            while respawning after being eaten).
        normal_texture (arcade.Texture): Texture used in normal state.
        eat_texture (arcade.Texture): Texture used when the ghost is
            edible (player in super mode).
        sprite_size (float): On-screen size of the ghost sprite.
    """
    def __init__(self, manager: Any) -> None:
        """Initialize the Inky ghost.

        Args:
            manager (Any): The GhostManager instance, used to access
                the game map and the player.

        Returns:
            None
        """
        self.manager = manager
        self.map = self.manager.map
        self.player = self.manager.player

        self.cell_pos: List[int] = [self.map.current.width - 1,
                                    self.map.current.height - 1]
        x, y = self.cell_pos
        self.pos: List[float] = list(self.map.grid[y][x])

        N: Tuple[int, int] = (0, -1)

        self.dir: Tuple[int, int] = N
        self.dx, self.dy = self.dir
        self.speed: int = self.map.cell // 20
        self.visible: bool = True
        self.normal_texture = arcade.load_texture(
            f"assets/sprite/{self.__class__.__name__.lower()}.png"
        )
        self.eat_texture = arcade.load_texture("assets/sprite/eat.png")
        self.sprite_size: float = self.map.cell * 0.8

    def init_pos(self) -> None:
        """Reset the ghost to its starting position (cell ``[0, 0]``).

        Returns:
            None
        """
        self.cell_pos = [self.map.current.width - 1,
                         self.map.current.height - 1]
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])

    def algo(self) -> Tuple[int, int]:
        """Compute the best direction to move toward the player.

        Performs a breadth-first search (BFS) from the ghost's current
        cell to the player's cell, avoiding walls, and returns the
        very first direction taken along the shortest path found.

        Returns:
            Tuple[int, int]: The direction ``(dx, dy)`` to move in.
            Falls back to the ghost's current direction if no path
            to the player is found.
        """
        N = (0, -1)
        S = (0, 1)
        E = (1, 0)
        W = (-1, 0)

        start: Tuple[int, int] = (self.cell_pos[0], self.cell_pos[1])
        target: Tuple[int, int] = (self.player.cell_pos[0],
                                   self.player.cell_pos[1])

        queue: Deque[Tuple[Tuple[int, int],
                           Optional[Tuple[int, int]]]] = deque([(start, None)])
        visited: List[Tuple[int, int]] = [start]

        while queue:
            pos, first_dir = queue.popleft()

            if pos == target:
                return first_dir if first_dir is not None else self.dir

            for direction in [N, S, E, W]:
                neighbor = (pos[0] + direction[0], pos[1] + direction[1])

                if (
                    0 <= neighbor[0] < len(self.map.maze[0])
                    and 0 <= neighbor[1] < len(self.map.maze)
                    and neighbor not in visited
                    and not self.have_wall(list(pos), direction)
                ):
                    visited.append(neighbor)

                    if first_dir is None:
                        queue.append((neighbor, direction))
                    else:
                        queue.append((neighbor, first_dir))

        return self.dir

    def have_wall(self, pos: List[int], direction: Tuple[int, int]) -> bool:
        """Check whether a wall blocks movement in a given direction.

        Args:
            pos (List[int]): Grid-cell position ``[x, y]`` from which
                the move is being tested.
            direction (Tuple[int, int]): Direction to test, as a
                ``(dx, dy)`` tuple (north, south, east, or west).

        Returns:
            bool: ``True`` if a wall blocks movement in that direction
            from that position, ``False`` otherwise.
        """
        N = (0, -1)
        S = (0, 1)
        E = (1, 0)
        W = (-1, 0)

        current = self.map.maze[pos[1]][pos[0]]
        north = [1, 3, 5, 7, 9, 11, 13, 15]
        east = [2, 3, 6, 7, 10, 11, 14, 15]
        south = [4, 5, 6, 7, 12, 13, 14, 15]
        west = [8, 9, 10, 11, 12, 13, 14, 15]

        if direction == E and current in east:
            return True
        if direction == W and current in west:
            return True
        if direction == S and current in south:
            return True
        if direction == N and current in north:
            return True

        return False

    def draw(self) -> None:
        """Draw the ghost sprite at its current position.

        Selects the edible texture when the player is in super mode
        or when the ghost is temporarily invisible; otherwise uses
        the normal texture.

        Returns:
            None
        """
        texture = (self.eat_texture
                   if self.player.super_mod or
                   not self.visible else self.normal_texture)
        rect = arcade.Rect(
            self.pos[0] - self.sprite_size / 2,
            self.pos[0] + self.sprite_size / 2,
            self.pos[1] - self.sprite_size / 2,
            self.pos[1] + self.sprite_size / 2,
            self.sprite_size,
            self.sprite_size,
            self.pos[0],
            self.pos[1],
        )
        arcade.draw_texture_rect(texture, rect)

    def update(self) -> None:
        """Update the ghost's position, direction, and state each frame.

        Does nothing if the ghost is not visible. Otherwise, while the
        player is not frozen, moves the ghost cell by cell toward its
        target using the chase algorithm (``algo``) or the flee
        algorithm (``flight``), depending on the player's state.
        Also detects collisions with the player: kills the player if
        they are neither invincible nor in super mode, or triggers
        this ghost's own "death" (see ``death``) if the player is in
        super mode.

        Returns:
            None
        """
        if not self.visible:
            return

        if not self.player.freeze:
            target = list(self.map.grid[self.cell_pos[1]][self.cell_pos[0]])

            if self.pos == target:
                if self.player.super_mod:
                    new_dir = self.flight()
                else:
                    new_dir = self.algo()
                if new_dir:
                    self.dir = new_dir
                    self.dx, self.dy = self.dir
                if not self.have_wall(self.cell_pos, self.dir):
                    self.cell_pos[0] += self.dx
                    self.cell_pos[1] += self.dy

            target = list(self.map.grid[self.cell_pos[1]][self.cell_pos[0]])

            if self.pos[0] < target[0]:
                self.pos[0] = min(self.pos[0] + self.speed, target[0])
            elif self.pos[0] > target[0]:
                self.pos[0] = max(self.pos[0] - self.speed, target[0])
            if self.pos[1] < target[1]:
                self.pos[1] = min(self.pos[1] + self.speed, target[1])
            elif self.pos[1] > target[1]:
                self.pos[1] = max(self.pos[1] - self.speed, target[1])

        radius = self.map.cell // 3 - 2
        if (
            abs(self.pos[0] - self.player.pos[0]) <= radius
            and abs(self.pos[1] - self.player.pos[1]) <= radius
        ):
            if not self.player.super_mod and not self.player.invicible:
                self.manager.kill_player()
            elif self.player.super_mod:
                self.death()

    def death(self) -> None:
        """Handle the ghost being eaten by the player.

        Makes the ghost invisible, awards points to the player, and
        starts a background thread that resets the ghost to its
        initial position and makes it visible again after a 3-second
        delay.

        Returns:
            None
        """
        self.visible = False
        self.player.score += self.player.config_data.pt_per_ghost

        def reset() -> None:
            self.init_pos()
            time.sleep(3)
            self.visible = True

        threading.Thread(target=reset).start()

    def flight(self) -> Tuple[int, int]:
        """Compute the best direction to flee from the player.

        Explores reachable cells from the ghost's position via BFS
        and returns the first direction leading toward the farthest
        reachable cell from the player (Manhattan distance). Used
        when the player is in super mode.

        Returns:
            Tuple[int, int]: The direction ``(dx, dy)`` that moves the
            ghost as far away from the player as possible.
        """
        N = (0, -1)
        S = (0, 1)
        E = (1, 0)
        W = (-1, 0)

        start: Tuple[int, int] = (self.cell_pos[0], self.cell_pos[1])
        player: Tuple[int, int] = (self.player.cell_pos[0],
                                   self.player.cell_pos[1])

        queue: Deque[Tuple[Tuple[int, int],
                           Optional[Tuple[int, int]]]] = deque([(start, None)])
        visited: List[Tuple[int, int]] = [start]
        best_dir: Tuple[int, int] = self.dir
        best_dist = -1

        while queue:
            pos, first_dir = queue.popleft()
            dist = abs(pos[0] - player[0]) + abs(pos[1] - player[1])
            if dist > best_dist:
                best_dist = dist
                if first_dir is not None:
                    best_dir = first_dir

            for direction in [N, S, E, W]:
                neighbor = (pos[0] + direction[0], pos[1] + direction[1])
                if (
                    0 <= neighbor[0] < len(self.map.maze[0])
                    and 0 <= neighbor[1] < len(self.map.maze)
                    and neighbor not in visited
                    and not self.have_wall(list(pos), direction)
                ):
                    visited.append(neighbor)
                    if first_dir is None:
                        queue.append((neighbor, direction))
                    else:
                        queue.append((neighbor, first_dir))

        return best_dir
