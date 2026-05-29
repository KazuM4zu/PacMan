import arcade.gui as gui
from ..panel import PanelInterface


class MenuEchapPanel(PanelInterface):
    def setup_ui(self):
        label = gui.UILabel(
            text="Back Menu",
            align="center",
            font_name="Press Start 2P",
            multiline=True
        )
        self.layout.add(child=label,
                        anchor_x="center_x",
                        anchor_y="center_y")
