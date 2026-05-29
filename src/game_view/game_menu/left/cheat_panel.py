import arcade.gui as gui
from ..panel import PanelInterface


class CheatPanel(PanelInterface):
    def setup_ui(self):
        label = gui.UILabel(
            text="Cheat",
            align="center",
            font_size=12,
            font_name="Press Start 2P"
        )
        self.layout.add(child=label,
                        anchor_x="center_x",
                        anchor_y="center_y")
