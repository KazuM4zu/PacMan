import arcade.gui as gui
import arcade
from ..panel import PanelInterface


class MenuEchapPanel(PanelInterface):
    def __init__(self, width, height, player, view):
        self.menu_options = ["Resume", "Settings", "Back to Menu", "Quit"]
        self.selected_index = 0
        self.labels = {}
        self.view = view
        super().__init__(width, height, player)

    def setup_ui(self):
        self.box = gui.UIBoxLayout(vertical=True, space_between=25)
        self.layout.add(child=self.box,
                        anchor_x="center_x",
                        anchor_y="center_y")
        self.update_labels()

    def update_labels(self):
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

    def draw_triangle(self):
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

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selected_index = ((self.selected_index - 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.DOWN:
            self.selected_index = ((self.selected_index + 1)
                                   % len(self.menu_options))
        elif symbol == arcade.key.SPACE:
            self.execute_action()

    def on_mouse_motion(self, x, y, dx, dy):
        for i, label in self.labels.items():
            left = label.rect.left - 40
            right = label.rect.right + 40
            bottom = label.rect.bottom - 10
            top = label.rect.top + 10
            if left < x < right and bottom < y < top:
                if self.selected_index != i:
                    self.selected_index = i
                    self.update_labels()
                break

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i, label in self.labels.items():
                left = label.rect.left - 40
                right = label.rect.right + 40
                bottom = label.rect.bottom - 10
                top = label.rect.top + 10
                if left < x < right and bottom < y < top:
                    self.selected_index = i
                    self.execute_action()
                    break

    def execute_action(self):
        selected = self.menu_options[self.selected_index]
        if selected == "Quit":
            arcade.exit()
        elif selected == "Resume":
            self.view.pause_game()
        elif selected == "Back to Menu":
            self.view.music.stop(self.view.music_player)
            from menu_view.menu_view import MenuView
            menu = MenuView(self.view.config_data)
            self.view.window.show_view(menu)
