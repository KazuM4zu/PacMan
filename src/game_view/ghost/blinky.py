from collections import deque
import threading
import time
from typing import Any, Deque, List, Optional, Tuple

import arcade


class Blinky:
    def __init__(self, manager: Any) -> None:
        self.manager = manager
        self.map = self.manager.map
        self.player = self.manager.player

        self.cell_pos: List[int] = [0, 0]
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
        self.cell_pos = [0, 0]
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])

    def algo(self) -> Tuple[int, int]:
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
        if not self.visible or self.player.freeze:
            return
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
        self.visible = False
        self.player.score += self.player.config_data.pt_per_ghost

        def reset() -> None:
            self.init_pos()
            time.sleep(3)
            self.visible = True

        threading.Thread(target=reset).start()

    def flight(self) -> Tuple[int, int]:
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
