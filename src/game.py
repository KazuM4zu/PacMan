from map import Map
from player import Player
import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.map = Map()
        self.map.size = (15, 15)
        self.map.seed = 42
        self.map.win = (500, 520)
        self.map.generate_maze()

        self.player = Player()

    def on_draw(self):
        self.clear()
        self.map.draw()

if __name__ == "__main__":
    window = arcade.Window(500, 520, "Pac-Man")
    grr = GameView()
    window.show_view(grr)
    arcade.run()
