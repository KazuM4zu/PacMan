import arcade
import arcade.gui as gui
from game_view.player import Player


class PanelInterface:
    def __init__(self, width: int,
                 height: int,
                 player: Player,
                 config_data=None):
        self.width = width
        self.height = height
        self.player = player
        self.layout = gui.UIAnchorLayout(
            width=self.width,
            height=self.height,
            size_hint=None
        )
        self.config_data = config_data
        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")
        self.setup_ui()

    def setup_ui(self):
        pass

    def get_widget(self):
        return self.layout.with_border(
            color=arcade.color.RED_DEVIL,
            width=4)
