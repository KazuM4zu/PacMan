import arcade.gui as gui
from ..panel import PanelInterface
import arcade
from ...cheat import Cheat as ch


L_INVI = "Press 'I' to become invincible"
L_FREE = "Press 'f' to freeze the minotaurs"


class CheatPanel(PanelInterface):
    def __init__(self, width, height, player, view):
        self.menu_options = [
            L_INVI,
            L_FREE,
            "Press '+' to add points",
            "Press '-' to remove points",
            "Press 'L' to add a life",
            "Press 'R' to remove a life",
            "Press 'N' to skip to the next level"
            ]
        self.selected_index = 0
        self.labels = {}
        self.view = view
        self.b_invicible = False
        self.b_freeze = False
        super().__init__(width, height, player)

    def setup_ui(self):
        self.box = gui.UIBoxLayout(vertical=True, space_between=25)
        self.layout.add(child=self.box,
                        anchor_x="center_x",
                        anchor_y="center_y")
        self.update_labels()

    def update_labels(self):
        self.box.clear()
        for i, option in enumerate(self.menu_options):
            color = arcade.color.WHITE
            if option in (L_INVI, L_FREE):
                if option == L_INVI and self.b_invicible:
                    color = arcade.color.GREEN
                elif option == L_FREE and self.b_freeze:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.RED

            label = gui.UILabel(
                text=option,
                font_name="Press Start 2P",
                font_size=10,
                text_color=color
            )
            self.labels[i] = label
            self.box.add(label)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.I:
            if not self.b_invicible:
                ch.set_invicible()
            self.b_invicible = not self.b_invicible
        elif symbol == arcade.key.F:
            if not self.b_freeze:
                ch.freeze_minotaurs()
            self.b_freeze = not self.b_freeze
        elif symbol == arcade.key.NUM_ADD:
            ch.add_points(self.player)
        elif symbol == arcade.key.NUM_SUBTRACT:
            ch.remove_points(self.player)
        elif symbol == arcade.key.L:
            ch.add_life(self.player)
        elif symbol == arcade.key.R:
            ch.remove_life(self.player)
        elif symbol == arcade.key.N:
            ch.next_level(self.view)

        self.update_labels()
        self.view.stat_panel.update_label()
