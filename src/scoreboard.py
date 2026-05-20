import json
import os
from pathlib import Path
import arcade
import arcade.gui as gui


class Scoreboard:
    file_path = Path(__file__).parent.parent / "scoreboard.json"

    def __init__(self):
        if not os.path.exists(self.file_path):
            print("The scoreboard.json file does not exist. Creating...")
            self.data = {}
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        else:
            print("The scoreboard.json file has been found. Loading...")
            with open(self.file_path, "r", encoding="utf-8")as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}

    def update_score(self, player, score):
        if player in self.data:
            if score > self.data[player]:
                print(f"New record for {player}: {score}")
                self.data[player] = score
        else:
            print(f"New player {player}: {score}")
            self.data[player] = score
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def print_scoreboard(self):
        print("------ Scoreboard ------")
        for name, score in self.data.items():
            print(f"- {name}: {score}")

    def get_scores(self):
        return self.data


class ScoreView(arcade.View):
    def __init__(self, scoreboard: Scoreboard):
        super().__init__()
        self.sc = scoreboard
        self.manager = gui.UIManager()
        self.get_dim_menu()
        self.menu_center_x = self.win_width // 2
        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.title_text = arcade.Text(
            "SCOREBOARD",
            0, 0,
            arcade.color.YELLOW,
            font_size=40,
            font_name="Press Start 2P",
            anchor_x="center",
            anchor_y="center"
        )

        self.scores_txt = []
        self.load_scoreboard()
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

    def update_position(self):
        center_x = self.window.width // 2

        self.title_text.x = center_x
        self.title_text.y = self.window.height - 80

        self.back_txt.x = center_x
        self.back_txt.y = 80

        start_y = int(self.window.height * 0.68)
        spacing = 40
        for i, txt_obj in enumerate(self.scores_txt):
            txt_obj.x = center_x
            txt_obj.y = start_y - (i * spacing)

    def load_scoreboard(self):
        scores = self.sc.get_scores()

        scores_tries = sorted(scores.items(),
                              key=lambda item: item[1], reverse=True)

        self.scores_txt = []

        if not scores_tries:
            txt = arcade.Text(
                "NO SCORES YET",
                0, 0,
                arcade.color.WHITE,
                font_name="Press Start 2P",
                font_size=14,
                anchor_x="center",
                anchor_y="center"
            )
            self.scores_txt.append(txt)
            return
        for i, (name, score) in enumerate(scores_tries[:6]):
            txt_line = f"{i + 1}. {name.upper()[:8].ljust(8)}... {score}"

            txt = arcade.Text(
                text=txt_line,
                x=0, y=0,
                color=arcade.color.WHITE,
                font_name="Press Start 2P",
                anchor_x="center",
                anchor_y="center"
            )
            self.scores_txt.append(txt)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)
        self.manager.enable()
        self.window.set_caption("DarkMan - Scoreboard")
        self.scores_txt = []
        self.load_scoreboard()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.update_position()
        self.title_text.draw()
        for txt in self.scores_txt:
            txt.draw()

        self.back_txt.draw()

        if self.back_selected:
            y = self.back_txt.y
            txt_width = self.back_txt.content_width
            triangle_x = (self.window.width // 2) - (txt_width // 2) - 30

            arcade.draw_triangle_filled(
                triangle_x, y - 8,
                triangle_x, y + 8,
                triangle_x + 12, y,
                arcade.color.GREEN
            )

    def on_key_press(self, symbol, modifiers):
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.back_selected = True
        elif symbol == arcade.key.ENTER and self.back_selected:
            self.execute_back()

    def on_mouse_motion(self, x, y, dx, dy):
        center_x = self.window.width // 2
        hitbox_w = 150
        hitbox_h = 35

        left = center_x - hitbox_w // 2
        right = center_x + hitbox_w // 2
        bot = self.back_y_pos - hitbox_h // 2
        top = self.back_y_pos + hitbox_h // 2

        self.back_selected = (left < x < right and bot < y < top)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.back_selected:
            self.execute_back()

    def execute_back(self):
        from menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)


if __name__ == "__main__":
    sc = Scoreboard()
    sc.print_scoreboard()
