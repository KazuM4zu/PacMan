from map import Map
from player import Player
import arcade.key as key
import arcade.gui as gui
import arcade


class EscapeMenu(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
    def __init__(self, game_view):
        super().__init__(size_hint=(1, 1))
        self.game_view = game_view

        frame = self.add(gui.UIAnchorLayout(width=300, height=400,
                                            size_hint=None))
        frame.with_padding(all=20)

        frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=arcade.load_texture(
                    ":resources:gui_basic_assets/window/dark_blue_gray_panel.png"
                ),
            )
        )
        pause_label = gui.UILabel(text="Pause", align="center", font_size=20,
                                  multiline=False)

        back_button = gui.UIFlatButton(text="Return to the game", width=250)
        back_button.on_click = self.on_click_back_button

        settings_button = gui.UIFlatButton(text="Settings", width=250)
        settings_button.on_click = self.on_click_settings_button

        exit_button = gui.UIFlatButton(text="Exit to menu", width=250)
        exit_button.on_click = self.on_click_exit_button

        widget_layout = gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(pause_label)
        widget_layout.add(settings_button)
        widget_layout.add(back_button)
        widget_layout.add(exit_button)
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        self.parent.remove(self)
        self.game_view.escape_menu = None

    def on_click_exit_button(self, event):
        from menu import MenuView
        menu_view = MenuView()
        self.game_view.window.show_view(menu_view)
    
    def on_click_settings_button(self, event):
        if not self.game_view.settings_menu:
            from settings import SettingsSubMenu
            self.game_view.settings_menu = SettingsSubMenu(self.game_view)
            self.game_view.manager.add(self.game_view.settings_menu, layer=2)
            


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.map = Map((15, 15), (500, 520))
        self.map.seed = 42
        self.map.generate_maze()
        self.manager = gui.UIManager()
        self.escape_menu = None
        self.settings_menu = None
        self.map.calculate_grid()
        self.player = Player(self.map)


    def on_draw(self):
        self.clear()
        self.map.draw()
        self.player.draw()
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        self.player.on_key_press(symbol, modifiers)
        if symbol == key.ESCAPE:
            if self.escape_menu:
                self.manager.remove(self.escape_menu)
                self.escape_menu = None
            else:
                self.escape_menu = EscapeMenu(self)
                self.manager.add(self.escape_menu, layer=1)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_update(self, delta_time):
        if self.escape_menu:
            return
        self.player.update()
