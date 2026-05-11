import arcade
import arcade.gui as gui
import arcade.color
from game import GameView
import pyglet
from settings import SettingsSubMenu


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.settings_menu = None

        play_button = gui.UIFlatButton(text="Play", width=250)
        setting_button = gui.UIFlatButton(text="Settings", width=250)
        exit_button = gui.UIFlatButton(text="Exit", width=250)

        @play_button.event("on_click")
        def on_click_play_button(event):
            game_view = GameView()
            self.window.show_view(game_view)
            self.window.set_caption("Pacman - In Game")
            arcade.set_background_color(arcade.color.BLACK)

        @setting_button.event("on_click")
        def on_click_setting_button(event):
            if not self.settings_menu:
                self.settings_menu = SettingsSubMenu(self)
                self.manager.add(self.settings_menu)

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        self.grid = gui.UIGridLayout(
            column_count=2, row_count=3, horizontal_spacing=20,
            vertical_spacing=20
        )
        self.grid.add(play_button, column=0, row=0)
        self.grid.add(setting_button, column=0, row=1)
        self.grid.add(exit_button, column=0, row=2)

        self.anchor = self.manager.add(gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLANCHED_ALMOND)
        self.manager.enable()
        self.window.set_caption("Pacman - Menu")
        try:
            icon = pyglet.image.load("../assets/images/logo.png")
            self.window.set_icon(icon)
        except FileNotFoundError:
            print("The icon image file could not be found.")

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
