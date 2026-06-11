import arcade
import arcade.color
import arcade.key
import arcade.gui
import pyglet


from game_view.game_view import GameView
from setting_view.settings import SettingView
from scoreboard_view.scoreboard import Scoreboard
from scoreboard_view.scoreview import ScoreView


class MenuView(arcade.View):
    _fire_anim = None
    _elmo_anim = None

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
        self.sprites = arcade.SpriteList()
        self.title_logo = arcade.Sprite(
            "assets/images/logoDarkMan2.png"
        )
        self.sprites.append(self.title_logo)

        self.background_texture = arcade.load_texture("assets"
                                                      + "/images/"
                                                      + "background.png")

        self.menu_texts = []
        for i, option in enumerate(self.menu_options):
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
        self.music = arcade.load_sound("assets/sound/music/menu_music.mp3",
                                       streaming=True)
        self.music_player = arcade.play_sound(
            self.music,
            volume=self.config_data.volume / 100,
            loop=True
        )

        if MenuView._fire_anim is None:
            MenuView._fire_anim = pyglet.image.load_animation(
                "assets/images/fire.gif")

        if MenuView._elmo_anim is None:
            MenuView._elmo_anim = pyglet.image.load_animation(
                "assets/images/elmo.gif")

        self.fire_top = pyglet.sprite.Sprite(MenuView._fire_anim)
        self.elmo = pyglet.sprite.Sprite(MenuView._elmo_anim)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.manager.enable()
        self.window.set_caption("Pacman - Menu")
        try:
            icon = pyglet.image.load("assets/images/logo.png")
            self.window.set_icon(icon)
        except FileNotFoundError:
            print("The icon image file could not be found.")

        if self.window:
            self.title_logo.center_x = self.window.width // 2
            self.title_logo.center_y = self.window.height - 250

    def on_hide_view(self):
        self.manager.disable()

    def update_position(self):
        center_x = self.window.width // 2
        start_y = int(self.window.height * 0.6)

        self.title_logo.x = center_x
        self.title_logo.y = self.window.height - 100

        for i, text_obj in enumerate(self.menu_texts):
            text_obj.x = center_x
            text_obj.y = start_y - (i * self.menu_spacing)

        self.fire_top.x = 0
        self.fire_top.y = 0
        elmo_x = center_x - (self.elmo.width // 2)
        self.elmo.x = elmo_x
        self.elmo.y = self.title_logo.top - 20

    def on_draw(self):
        self.clear()
        self.update_position()
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.LRBT(100, self.window.width, 0, self.window.height)
        )
        self.fire_top.draw()
        self.elmo.draw()
        self.sprites.draw()
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
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        print(symbol)
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
            self.music.stop(player=self.music_player)
            game_view = GameView(self, self.config_data)
            self.window.show_view(game_view)

        elif selected == "Settings":
            self.settings_menu = SettingView(self, self.config_data)
            self.window.show_view(self.settings_menu)

        elif selected == "Exit":
            arcade.exit()

        elif selected == "Scoreboards":
            score_view = ScoreView(Scoreboard(), self, self.config_data)
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
