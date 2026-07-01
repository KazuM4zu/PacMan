import arcade.gui as gui
from game_view.game_menu.panel import PanelInterface
import arcade
from game_view.cheat import Cheat as ch

from typing import Any, Dict, List

L_INVI = "Press 'I' to become invincible"
L_FREE = "Press 'f' to freeze the minotaurs"


class CheatPanel(PanelInterface):
    """Display cheat options and handle related keyboard shortcuts."""

    def __init__(self, width: int,
                 height: int,
                 player: Any,
                 view: Any) -> None:
        """Initialize the cheat panel with its menu options and state.

        Args:
            width: Width of the panel in pixels.
            height: Height of the panel in pixels.
            player: Player instance used by cheat actions.
            view: Parent game view that owns the panel.
        """
        self.menu_options: List[str] = [
            L_INVI,
            L_FREE,
            "Press '+' to add points",
            "Press '-' to remove points",
            "Press 'L' to add a life",
            "Press 'R' to remove a life",
            "Press 'N' to skip to the next level"
            ]
        self.selected_index: int = 0
        self.labels: Dict[int, gui.UILabel] = {}
        self.view: Any = view
        self.b_invicible: bool = False
        self.b_freeze: bool = False
        super().__init__(width, height, player)

    def setup_ui(self) -> None:
        """Create the cheat menu box layout and populate it.

        Returns:
            None
        """
        self.box = gui.UIBoxLayout(vertical=True, space_between=25)
        self.layout.add(child=self.box,
                        anchor_x="center_x",
                        anchor_y="center_y")
        self.update_labels()

    def update_labels(self) -> None:
        """Refresh the visible cheat labels and their colors.

        Returns:
            None
        """
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

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle key presses for cheat actions.

        Args:
            symbol: Key code that was pressed.
            modifiers: Any keyboard modifiers active during the press.

        Returns:
            None
        """
        if symbol == arcade.key.I:
            ch.set_invicible(self.player)
        elif symbol == arcade.key.F:
            ch.freeze_minotaurs(self.player)
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
        if self.view.stat_panel is not None:
            self.view.stat_panel.update_label()
