import arcade
import arcade.color
import arcade.key
from typing import List, Any


class SettingView(arcade.View):
    """Display and update the settings menu options."""

    def __init__(self, last_view: arcade.View, config_data: Any) -> None:
        """Initialize the settings view and load its UI state.

        Args:
            last_view: The view to return to when leaving settings.
            config_data: Configuration object storing current settings.
        """
        super().__init__()
        self.config_data = config_data
        self.last_view = last_view

        self.selected_index = 0
        self.volume = self.config_data.volume
        self.menu_options = ["Volume", "Cheats", "Back"]
        self.menu_spacing = 45

        self.b_cheat = self.config_data.cheats_enabled

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.font_size = 20
        self.title_text = arcade.Text(
            "Settings",
            0, 0,
            arcade.color.WHITE,
            font_size=40,
            font_name="Press Start 2P",
            anchor_x="center",
            anchor_y="center"
        )
        self.menu_texts: List[arcade.Text] = []
        for option in self.menu_options:
            text_obj = arcade.Text(
                text=option,
                x=0,
                y=0,
                color=arcade.color.LIGHT_GRAY,
                font_name="Press Start 2P",
                font_size=self.font_size,
                anchor_x="center",
                anchor_y="center"
            )
            self.menu_texts.append(text_obj)

    def on_show_view(self) -> None:
        """Prepare the settings view when it becomes active.

        Returns:
            None
        """
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.window.set_caption("Pacman - Settings")

    def update_position(self) -> None:
        """Update widget positions based on the current window size.

        Returns:
            None
        """
        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)

        self.title_text.x = center_x
        self.title_text.y = self.window.height - 80

        self.menu_texts[0].text = f"Volume : < {self.volume}% >"

        cheat_state = "ON" if self.b_cheat else "OFF"
        self.menu_texts[1].text = f"Cheats : < {cheat_state} >"

        for i, text_obj in enumerate(self.menu_texts):
            text_obj.x = center_x
            text_obj.y = start_y - (i * self.menu_spacing)

    def on_draw(self) -> None:
        """Draw the settings screen and currently selected option.

        Returns:
            None
        """
        self.clear()
        self.update_position()
        self.title_text.draw()
        center_x = self.window.width // 2
        for i, text_obj in enumerate(self.menu_texts):
            if i == self.selected_index:
                text_obj.color = arcade.color.WHITE
            else:
                text_obj.color = arcade.color.ASH_GREY

            text_obj.draw()

            if i == self.selected_index:
                y = text_obj.y
                text_width = text_obj.content_width
                triangle_x = center_x - (text_width // 2) - 30

                arcade.draw_triangle_filled(
                    triangle_x, y - 8,
                    triangle_x, y + 8,
                    triangle_x + 12, y,
                    arcade.color.RED_DEVIL
                )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle keyboard input for changing settings.

        Args:
            symbol: Key code that was pressed.
            modifiers: Keyboard modifiers active during the press.
        """
        if symbol == arcade.key.UP:
            self.selected_index = ((self.selected_index - 1) %
                                   len(self.menu_options))
        elif symbol == arcade.key.DOWN:
            self.selected_index = ((self.selected_index + 1) %
                                   len(self.menu_options))
        elif symbol == arcade.key.LEFT:
            if self.selected_index == 0:
                self.volume = max(0, self.volume - 5)
                self.apply_volume()
            elif self.selected_index == 1:
                self.execute_action()
        elif symbol == arcade.key.RIGHT:
            if self.selected_index == 0:
                self.volume = min(100, self.volume + 5)
                self.apply_volume()
            elif self.selected_index == 1:
                self.execute_action()
        elif symbol in (arcade.key.ENTER, arcade.key.SPACE):
            self.execute_action()

    def on_update(self, delta_time: float) -> None:
        """Persist the current settings to the configuration file when needed.

        Args:
            delta_time: Time elapsed since the previous frame.
        """
        if (self.config_data.volume != self.volume or
           self.b_cheat != self.config_data.cheats_enabled):
            self.config_data.volume = self.volume
            self.config_data.cheats_enabled = self.b_cheat
            try:
                self.config_data.save("config.json")
            except Exception as e:
                print("Could not save config:", e)

    def apply_volume(self) -> None:
        """Update the volume of the previous view's music player if available.

        Returns:
            None
        """
        if hasattr(self.last_view, "music_player"):
            self.last_view.music_player.volume = self.volume / 100

    def execute_action(self) -> None:
        """Toggle the selected option or return to the previous view.

        Returns:
            None
        """
        if self.selected_index == 1:
            self.b_cheat = not self.b_cheat
        elif self.selected_index == 2:
            self.window.show_view(self.last_view)

    def on_mouse_motion(self, x: float, y: float,
                        dx: float, dy: float) -> None:
        """Update the selected setting when the mouse moves over it.

        Args:
            x: Mouse x position.
            y: Mouse y position.
            dx: Horizontal mouse movement.
            dy: Vertical mouse movement.
        """
        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)

        for i in range(len(self.menu_options)):
            item_y = start_y - (i * self.menu_spacing)

            text_width = self.menu_texts[i].content_width
            hitbox_width = text_width + 80
            hitbox_height = self.font_size + 15

            left = center_x - hitbox_width // 2
            right = center_x + hitbox_width // 2
            bottom = item_y - hitbox_height // 2
            top = item_y + hitbox_height // 2

            if left < x < right and bottom < y < top:
                self.selected_index = i
                break

    def on_mouse_press(self, x: float, y: float,
                       button: int, modifiers: int) -> None:
        """Apply the clicked setting action.

        Args:
            x: Mouse x position.
            y: Mouse y position.
            button: Mouse button identifier.
            modifiers: Keyboard modifiers active during the click.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            center_x = self.window.width // 2
            start_y = int(self.window.height * 0.6)

            for i in range(len(self.menu_options)):
                item_y = start_y - (i * self.menu_spacing)

                text_width = self.menu_texts[i].content_width
                hitbox_width = text_width + 80
                hitbox_height = self.font_size + 15

                left = center_x - hitbox_width // 2
                right = center_x + hitbox_width // 2
                bottom = item_y - hitbox_height // 2
                top = item_y + hitbox_height // 2

                if left < x < right and bottom < y < top:
                    self.selected_index = i

                    if self.selected_index == 0:
                        if x < center_x + 80:
                            self.volume = max(0, self.volume - 5)
                        else:
                            self.volume = min(100, self.volume + 5)
                        self.apply_volume()
                    elif self.selected_index == 1:
                        self.b_cheat = not self.b_cheat
                    elif self.selected_index == 2:
                        self.execute_action()
                    break
