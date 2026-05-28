import arcade
import arcade.color
import arcade.key
import arcade.gui
import pyglet


from game_view.game_view import GameView
from setting_view.settings import SettingsSubMenu
from scoreboard_view.scoreboard import Scoreboard
from scoreboard_view.scoreview import ScoreView


class MenuView(arcade.View):

    def __init__(self, config_data):
        super().__init__()
        self.config_data = config_data

        self.manager = arcade.gui.UIManager()

        self.selected_index = 0
        self.menu_options = ["Play", "Scoreboards", "Settings", "Exit"]
        self.menu_spacing = 45

        self.settings_menu = None

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.font_size = 20
        self.title_text = arcade.Text(
            "DARK-MAN",
            0, 0,
            arcade.color.RED,
            font_size=50,
            font_name="Pacmania",
            anchor_x="center",
            anchor_y="center",
        )

        self.menu_texts = []
        for i, option in enumerate(self.menu_options):
            text_obj = arcade.Text(
                text=option,
                x=0,
                y=0,
                color=arcade.color.WHITE,
                font_name="Press Start 2P",
                font_size=self.font_size,
                anchor_x="center",
                anchor_y="center"
            )
            self.menu_texts.append(text_obj)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)
        self.manager.enable()
        self.window.set_caption("Pacman - Menu")
        try:
            icon = pyglet.image.load("assets/images/logo.png")
            self.window.set_icon(icon)
        except FileNotFoundError:
            print("The icon image file could not be found.")

    def on_hide_view(self):
        self.manager.disable()

    def update_position(self):
        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)

        self.title_text.x = center_x
        self.title_text.y = self.window.height - 100

        for i, text_obj in enumerate(self.menu_texts):
            text_obj.x = center_x
            text_obj.y = start_y - (i * self.menu_spacing)

    def on_draw(self):
        self.clear()
        self.update_position()
        self.title_text.draw()
        center_x = self.window.width // 2
        for i, text_obj in enumerate(self.menu_texts):
            text_obj.draw()

            if i == self.selected_index:
                y = text_obj.y
                text_width = text_obj.content_width
                triangle_x = center_x - (text_width // 2) - 30

                arcade.draw_triangle_filled(
                    triangle_x, y - 8,
                    triangle_x, y + 8,
                    triangle_x + 12, y,
                    arcade.color.GREEN
                )
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selected_index = ((self.selected_index - 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.DOWN:
            self.selected_index = ((self.selected_index + 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.SPACE:
            self.execute_action()

    def execute_action(self):
        selected = self.menu_options[self.selected_index]

        if selected == "Play":
            game_view = GameView(self.config_data)
            self.window.show_view(game_view)

        elif selected == "Settings":
            if not self.settings_menu:
                self.settings_menu = SettingsSubMenu(self)
                self.manager.add(self.settings_menu)

        elif selected == "Exit":
            arcade.exit()

        elif selected == "Scoreboards":
            score_view = ScoreView(Scoreboard(), self.config_data)
            self.window.show_view(score_view)

    def on_mouse_motion(self, x, y, dx, dy):
        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)
        for i in range(len(self.menu_options)):
            item_y = start_y - (i * self.menu_spacing)

            hitbox_width = 200
            hitbox_height = self.font_size + 15

            left = center_x - hitbox_width // 2
            right = center_x + hitbox_width // 2
            bottom = item_y - hitbox_height // 2
            top = item_y + hitbox_height // 2

            if left < x < right and bottom < y < top:
                self.selected_index = i
                break

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            start_y = int(self.window.height * 0.6)
            item_y = start_y - (self.selected_index
                                * self.menu_spacing)
            hitbox_height = self.font_size + 15
            if item_y - hitbox_height // 2 < y < item_y + hitbox_height // 2:
                self.execute_action()
