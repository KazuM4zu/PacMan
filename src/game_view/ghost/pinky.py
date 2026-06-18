from collections import deque
import arcade.key as key
import arcade.gui as gui
import arcade
import time


class Pinky():
    def __init__(self, manager):
        self.manager = manager
        self.map = self.manager.map
        self.player = self.manager.player

        self.cell_pos = [0, self.map.current.height - 1]
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])

        N = (0, -1)
        S = (0,  1)
        E = (1,  0)
        W = (-1, 0)
        self.dir = N
        self.dx, self.dy = self.dir
        self.speed = self.map.cell // 20

    def init_pos(self):
        self.cell_pos = [0, self.map.current.height - 1]
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])

    def algo(self):
        N = (0, -1)
        S = (0,  1)
        E = (1,  0)
        W = (-1, 0)

        start = tuple(self.cell_pos)
        target = tuple(self.player.cell_pos)

        queue = deque([(start, None)])
        visited = [start]

        while queue:
            pos, first_dir = queue.popleft()

            if pos == target:
                return first_dir

            for direction in [N, S, E, W]:
                neighbor = (pos[0] + direction[0], pos[1] + direction[1])

                if (0 <= neighbor[0] < len(self.map.maze[0]) and
                    0 <= neighbor[1] < len(self.map.maze) and
                    neighbor not in visited and not
                    self.have_wall(list(pos), direction)):
                    visited.append(neighbor)

                    if first_dir is None:
                        queue.append((neighbor, direction))
                    else:
                        queue.append((neighbor, first_dir))

        return self.dir

    def have_wall(self, pos, direction):
        N = (0, -1)
        S = (0,  1)
        E = (1,  0)
        W = (-1, 0)

        current = self.map.maze[pos[1]][pos[0]]
        north = [1, 3, 5, 7, 9, 11, 13, 15]
        east  = [2, 3, 6, 7, 10, 11, 14, 15]
        south = [4, 5, 6, 7, 12, 13, 14, 15]
        west  = [8, 9, 10, 11, 12, 13, 14, 15]

        if direction == E and current in east:
            return True
        elif direction == W and current in west:
            return True
        elif direction == S and current in south:
            return True
        elif direction == N and current in north:
            return True

        return False

    def draw(self):
        arcade.draw_circle_filled(self.pos[0],
                                  self.pos[1],
                                  self.map.cell // 3 - 2,
                                  arcade.color.PINK_PEARL)

    def update(self):
        target = list(self.map.grid[self.cell_pos[1]][self.cell_pos[0]])

        if self.pos == target:
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
        if (abs(self.pos[0] - self.player.pos[0]) <= radius and
            abs(self.pos[1] - self.player.pos[1]) <= radius):
            self.manager.kill_player()
