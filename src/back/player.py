import arcade


class Player:
    def __init__(self, map):
        self.map = map
        self.cell_pos = ([round(self.map.size[1] / 2) - 1,
                          round(self.map.size[0] / 2) - 1])
        x, y = self.cell_pos
        self.pos = list(self.map.grid[y][x])
        self.score = 0
        self.lives = 3

        self.speed = 3
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0

    def draw(self):
        arcade.draw_circle_filled(self.pos[0],
                                  self.pos[1],
                                  self.map.cell // 3 - 2,
                                  arcade.color.YELLOW)

    def on_key_press(self, key, modifiers):
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

    def update(self):
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

    def have_wall(self, nx: int, ny: int):
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
