from back.map import Map
from back.player import Player
from front.escape_menu import EscapeMenu
import arcade.key as key
import arcade.gui as gui
import arcade


class GameView(arcade.View):
    def __init__(self, config_data):
        super().__init__()

        self.config_data = config_data
        self.map = Map(config_data, (self.window.width, self.window.height))
        self.map.seed = 42
        self.map.calculate_grid()
        self.map.generate_maze()
        self.manager = gui.UIManager()
        self.escape_menu = None
        self.settings_menu = None
        self.player = Player(self.map)

    def on_draw(self):
        self.clear()
        self.map.draw()
        self.player.draw()
        self.manager.draw()
        self.window.set_caption("Pacman - In Game")
        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, symbol, modifiers):
        self.player.on_key_press(symbol, modifiers)
        if symbol == key.ESCAPE:
            if self.escape_menu:
                self.manager.remove(self.escape_menu)
                self.escape_menu = None
            else:
                self.escape_menu = EscapeMenu(self)
                self.manager.add(self.escape_menu, layer=1)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_update(self, delta_time):
        if self.escape_menu:
            return
        self.player.update()
