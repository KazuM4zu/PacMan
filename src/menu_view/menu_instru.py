import arcade
import arcade.gui as gui
import arcade.color as col
from typing import Any, Tuple, List


class InstrucView(arcade.View):
    def __init__(self,
                 last_view: Any, config_data: Any) -> None:
        super().__init__()
        self.last_view = last_view
        self.manager = gui.UIManager()
        self.config = config_data

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.title_text = arcade.Text(
            "Instructions",
            0, 0,
            arcade.color.WHITE,
            font_size=40,
            font_name="Press Start 2P",
            anchor_x="center",
            anchor_y="center"
        )

        self.instruction_content = (
            "Welcome to Dark-Man!\n\n"
            "OBJECTIVE:\n\n"
            "Consume all pellets while avoiding ghosts.\n"
            "Clear the board to advance.\n\n\n\n"
            "CONTROLS:\n\n"
            "Use Arrow Keys to navigate.\n\n\n\n"
            "TIPS:\n"
            "- Power Pellets turn ghosts blue (edible!).\n"
            "- Collect Bonus Items in the center.\n"
            "- Toggle cheats in the Settings menu.\n\n\n"
            "NOTE: Non-blue ghosts are lethal!"
        )

        self.instru_txt: List[Tuple[str, Any]] = [
            ("Welcome to Dark-Man!", col.YELLOW_ORANGE),
            ("", col.WHITE),
            ("", col.WHITE),
            ("Objective:", col.RED_DEVIL),
            ("", col.WHITE),
            ("Consume all pac-gums while avoiding ghosts.", col.WHITE),
            ("", col.WHITE),
            ("", col.WHITE),
            ("Clear the board to advance.", col.WHITE),
            ("", col.WHITE),
            ("", col.WHITE),
            ("TIPS:", col.DARK_CERULEAN),
            ("", col.WHITE),
            ("- Super pac-gums turn ghosts blue (edible!).", col.WHITE),
            ("", col.WHITE),
            ("- Pay attention to the remaining time.", col.WHITE),
            ("", col.WHITE),
            ("", col.WHITE),
            ("NOTE: You can enable cheat mode in the settings "
             "(but that's cheating).", col.RED)
        ]
        self.lst_txt: List[arcade.Text] = []
        for txt, color in self.instru_txt:
            text_obj = arcade.Text(
                text=txt,
                x=0, y=0,
                color=color,
                font_name="Press Start 2P",
                font_size=18,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=3000,
                align="center"
            )
            self.lst_txt.append(text_obj)

        self.back_y_pos = 80
        self.back_txt = arcade.Text(
            text="BACK",
            x=0, y=0,
            color=arcade.color.WHITE,
            font_name="Press Start 2P",
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )
        self.back_selected = False

    def update_position(self) -> None:
        center_x = self.window.width // 2

        self.title_text.x = center_x
        self.title_text.y = self.window.height - 80

        self.back_txt.x = center_x
        self.back_txt.y = 80

        start_y = int(self.window.height * 0.68)
        spacing = 15
        for i, txt_obj in enumerate(self.lst_txt):
            txt_obj.x = center_x
            txt_obj.y = start_y - (i * spacing)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.manager.enable()
        self.window.set_caption("DarkMan - Instructions")

    def on_hide_view(self) -> None:
        self.manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.update_position()
        self.title_text.draw()
        for txt_obj in self.lst_txt:
            txt_obj.draw()
        self.back_txt.draw()

        if self.back_selected:
            y = self.back_txt.y
            txt_width = self.back_txt.content_width
            triangle_x = (self.window.width // 2) - (txt_width // 2) - 30

            arcade.draw_triangle_filled(
                triangle_x, y - 8,
                triangle_x, y + 8,
                triangle_x + 12, y,
                arcade.color.RED_DEVIL
            )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.back_selected = True
        elif (symbol == (arcade.key.SPACE)
              and self.back_selected):
            self.execute_back()

    def on_mouse_motion(self, x: float, y: float,
                        dx: float, dy: float) -> None:
        center_x = self.window.width // 2
        hitbox_w = 150
        hitbox_h = 35

        left = center_x - hitbox_w // 2
        right = center_x + hitbox_w // 2
        bot = self.back_y_pos - hitbox_h // 2
        top = self.back_y_pos + hitbox_h // 2

        self.back_selected = (left < x < right and bot < y < top)

    def on_mouse_press(self,
                       x: float, y: float,
                       button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT and self.back_selected:
            self.execute_back()

    def execute_back(self) -> None:
        self.window.show_view(self.last_view)
