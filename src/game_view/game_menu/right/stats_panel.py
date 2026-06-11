import arcade
import arcade.gui as gui
from ..panel import PanelInterface


class StatPanel(PanelInterface):
    def setup_ui(self):
        box = gui.UIBoxLayout(vertical=True, space_between=20)

        title = gui.UILabel(
            text="==== STATS ====",
            font_name="Press Start 2P",
            font_size=14,
            text_color=arcade.color.YELLOW
        )
        box.add(title)

        self.score_label = gui.UILabel(
            text="Score: 0000",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.score_label)

        self.live_label = gui.UILabel(
            text=f"Lifes : {self.player.lives}",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.live_label)

        self.level_label = gui.UILabel(
            text="Level: 0",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.level_label)
        self.layout.add(
            child=box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

    def update_label(self):
        self.score_label.text = f"Score: {self.player.score:04d}"
        self.live_label.text = f"Lifes: {self.player.lives}"
