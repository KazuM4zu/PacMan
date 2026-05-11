import arcade
import arcade.gui as gui
import arcade.key as key
from game import GameView
import pyglet


class SettingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        back_button = gui.UIFlatButton(text="Back", width=50)

        @back_button.event("on_click")
        def on_click_back_button(event):
            menu_view = MenuView()
            self.window.show_view(menu_view)

        self.top_grid = gui.UIGridLayout(
            column_count=3, row_count=1, horizontal_spacing=100
        )
        self.top_grid.add(back_button, column=0, row=0)

        self.top_anchor = self.manager.add(gui.UIAnchorLayout())
        self.top_anchor.add(
            anchor_x="left",
            anchor_y="top",
            child=self.top_grid,
        )

    def on_show_view(self):
        self.window.set_caption("Pacman - Settings")
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

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
            setting_view = SettingView()
            self.window.show_view(setting_view)

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


#class SubMenu(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
#    def __init__(self,):
#        super().__init__(size_hint=(1, 1))
        
#        frame = self.add(gui.UIAnchorLayout(width=300, height=400,
#                                            size_hint=None))
#        frame.with_padding(all=20)

#        frame.with_background(
#            texture=gui.NinePatchTexture(
#                left=7,
#                right=7,
#                bottom=7,
#                top=7,
#                texture=arcade.load_texture(
#                        ":resources:gui_basic_assets/window/dark_blue_gray_panel.png"
#                    ),
#            )
#        )

def main():
    window = arcade.Window(500, 520, "Pacman - Menu")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()