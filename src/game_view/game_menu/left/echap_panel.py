import arcade.gui as gui
import arcade
from src.game_view.game_menu.panel import PanelInterface
from typing import Any, Dict, List


class MenuEchapPanel(PanelInterface):
    """Display the pause/escape menu and handle user navigation."""

    def __init__(self, width: int,
                 height: int,
                 player: Any,
                 view: Any) -> None:
        """Initialize the menu panel with available actions.

        Args:
            width: Width of the panel in pixels.
            height: Height of the panel in pixels.
            player: Player instance associated with the panel.
            view: Parent game view that owns the menu.
        """
        self.menu_options: List[str] = [
            "Resume",
            "Settings",
            "Back to Menu",
            "Quit Game"]
        self.selected_index: int = 0
        self.labels: Dict[int, gui.UILabel] = {}
        self.view: Any = view
        super().__init__(width, height, player)

    def setup_ui(self) -> None:
        """Create the menu layout and populate options.

        Returns:
            None
        """
        self.box = gui.UIBoxLayout(vertical=True, space_between=25)
        self.layout.add(child=self.box,
                        anchor_x="center_x",
                        anchor_y="center_y")
        self.update_labels()

    def update_labels(self) -> None:
        """Refresh the labels for the current selection state.

        Returns:
            None
        """
        self.box.clear()
        for i, option in enumerate(self.menu_options):
            if i == self.selected_index:
                color = arcade.color.WHITE
            else:
                color = arcade.color.ASH_GREY
            label = gui.UILabel(
                text=option,
                font_name="Press Start 2P",
                font_size=16,
                text_color=color
            )
            self.labels[i] = label
            self.box.add(label)

    def draw_triangle(self) -> None:
        """Draw the selection marker beside the currently selected option.

        Returns:
            None
        """
        if self.selected_index in self.labels:
            selected_label = self.labels[self.selected_index]
            if selected_label.rect.width > 0:
                y = selected_label.rect.center_y
                x = selected_label.rect.left - 25
                arcade.draw_triangle_filled(
                    x, y - 8,
                    x, y + 8,
                    x + 12, y,
                    arcade.color.RED_DEVIL
                )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle keyboard navigation in the pause menu.

        Args:
            symbol: Key code that was pressed.
            modifiers: Keyboard modifiers active during the press.

        Returns:
            None
        """
        if symbol == arcade.key.UP:
            self.selected_index = ((self.selected_index - 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.DOWN:
            self.selected_index = ((self.selected_index + 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.SPACE:
            self.execute_action()

    def on_mouse_motion(self,
                        x: float, y: float, dx: float, dy: float) -> None:
        """Update the selected option when the mouse moves over a label.

        Args:
            x: Mouse x position.
            y: Mouse y position.
            dx: Horizontal mouse movement.
            dy: Vertical mouse movement.

        Returns:
            None
        """
        for i, label in self.labels.items():
            left: float = label.rect.left - 40
            right: float = label.rect.right + 40
            bottom: float = label.rect.bottom - 10
            top: float = label.rect.top + 10
            if left < x < right and bottom < y < top:
                if self.selected_index != i:
                    self.selected_index = i
                    self.update_labels()
                break

    def on_mouse_press(self,
                       x: float,
                       y: float,
                       button: int,
                       modifiers: int) -> None:
        """Execute the selected action when a menu item is clicked.

        Args:
            x: Mouse x position.
            y: Mouse y position.
            button: Mouse button identifier.
            modifiers: Keyboard modifiers active during the click.

        Returns:
            None
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i, label in self.labels.items():
                left: float = label.rect.left - 40
                right: float = label.rect.right + 40
                bottom: float = label.rect.bottom - 10
                top: float = label.rect.top + 10
                if left < x < right and bottom < y < top:
                    self.selected_index = i
                    self.execute_action()
                    break

    def execute_action(self) -> None:
        """Perform the action associated with the current menu selection.

        Returns:
            None
        """
        selected: str = self.menu_options[self.selected_index]
        if selected == "Quit Game":
            arcade.exit()
        elif selected == "Resume":
            self.view.pause_game()
        elif selected == "Back to Menu":
            if self.view.music and self.view.music_player:
                self.view.music.stop(self.view.music_player)
            from src.menu_view.menu_view import MenuView
            menu = MenuView(self.view.config_data)
            self.view.window.show_view(menu)
        elif selected == "Settings":
            from src.setting_view.settings import SettingView
            setting = SettingView(self.view, self.view.config_data)
            self.view.window.show_view(setting)
