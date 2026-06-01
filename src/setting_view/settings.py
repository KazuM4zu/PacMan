import arcade
import arcade.color
import arcade.key
from typing import Any, List


class SettingView(arcade.View):
    def __init__(self, main_menu_view, config_data) -> None:
        super().__init__()
        self.config_data = config_data
        self.main_menu_view = main_menu_view

        self.selected_index = 0
        self.volume = 50
        self.menu_options = ["Volume", "Back"]
        self.menu_spacing = 45

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.font_size = 20

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
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.window.set_caption("Pacman - Settings")

    def update_position(self) -> None:

        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)

        self.menu_texts[0].text = f"Volume : < {self.volume}% >"

        for i, text_obj in enumerate(self.menu_texts):
            text_obj.x = center_x
            text_obj.y = start_y - (i * self.menu_spacing)

    def on_draw(self) -> None:
        self.clear()
        self.update_position()

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
        if symbol == arcade.key.UP:
            self.selected_index = ((self.selected_index - 1) % len(self.menu_options))
        elif symbol == arcade.key.DOWN:
            self.selected_index = ((self.selected_index + 1) % len(self.menu_options))
        elif symbol == arcade.key.LEFT:
            if self.selected_index == 0:
                self.volume = max(0, self.volume - 5)
                self.apply_volume()
        elif symbol == arcade.key.RIGHT:
            if self.selected_index == 0:
                self.volume = min(100, self.volume + 5)
                self.apply_volume()
        elif symbol in (arcade.key.ENTER, arcade.key.SPACE):
            self.execute_action()

    def apply_volume(self) -> None:
        if hasattr(self.main_menu_view, "music_player") and self.main_menu_view.music_player:
            self.main_menu_view.music_player.volume = self.volume / 100

    def execute_action(self) -> None:
        if self.selected_index == 1:
            self.window.show_view(self.main_menu_view)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        if not self.window:
            return

        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)
        for i in range(len(self.menu_options)):
            item_y = start_y - (i * self.menu_spacing)

            hitbox_width = 350
            hitbox_height = self.font_size + 15

            left = center_x - hitbox_width // 2
            right = center_x + hitbox_width // 2
            bottom = item_y - hitbox_height // 2
            top = item_y + hitbox_height // 2

            if left < x < right and bottom < y < top:
                self.selected_index = i
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if not self.window:
            return
            
        if button == arcade.MOUSE_BUTTON_LEFT:
            start_y = int(self.window.height * 0.6)
            item_y = start_y - (self.selected_index * self.menu_spacing)
            hitbox_height = self.font_size + 15

            if item_y - hitbox_height // 2 < y < item_y + hitbox_height // 2:
                if self.selected_index == 0:
                    center_x = self.window.width // 2
                    if x < center_x:
                        self.volume = max(0, self.volume - 5)
                    else:
                        self.volume = min(100, self.volume + 5)
                    self.apply_volume()
                else:
                    self.execute_action()