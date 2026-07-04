import arcade
import arcade.gui as gui
from src.game_view.player import Player
from typing import Any


class PanelInterface:
    """Base interface for game menu panels.

    This class provides common layout, font loading, and widget access
    behavior for the menu panels used in the game.
    """

    def __init__(self, width: int,
                 height: int,
                 player: Player,
                 config_data: Any = None) -> None:
        """Initialize the panel with layout, player, and configuration data.

        Args:
            width: Width of the panel in pixels.
            height: Height of the panel in pixels.
            player: Player instance associated with the panel.
            config_data: Optional configuration data for the panel.
        """
        self.width: int = width
        self.height: int = height
        self.player: Any = player
        self.layout = gui.UIAnchorLayout(
            width=self.width,
            height=self.height,
            size_hint=None
        )
        self.config_data: Any = config_data
        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")
        self.setup_ui()

    def setup_ui(self) -> None:
        """Build the panel's user interface components.

        Returns:
            None
        """
        pass

    def get_widget(self) -> gui.UIAnchorLayout:
        """Return the panel widget with a visible border.

        Returns:
            A bordered anchor layout representing the panel.
        """
        return self.layout.with_border(
            color=arcade.color.RED_DEVIL,
            width=4)
