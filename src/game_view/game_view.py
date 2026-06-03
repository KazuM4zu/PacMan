from game_view.map import Map
from game_view.player import Player
from scoreboard_view.scoreboard import Scoreboard
from game_view.game_menu.escape_menu import EscapeMenu
from game_view.game_menu.left.echap_panel import MenuEchapPanel
from game_view.game_menu.left.cheat_panel import CheatPanel
from game_view.game_menu.right.leader_panel import LeadPanel
from game_view.game_menu.right.stats_panel import StatPanel

import arcade.key as key
import arcade.gui as gui
import arcade


class GameView(arcade.View):
    def __init__(self, main_menu_view, config_data):
        super().__init__()

        self.main_menu_view = main_menu_view
        self.config_data = config_data
        self.sc = Scoreboard()
        self.index_level = 0
        self.first_game = True

        self.manager = gui.UIManager()
        self.manager.enable()
        self.escape_menu = None
        self.settings_menu = None

        try:
            self.music = arcade.load_sound("assets/sound/music/game_music.mp3",
                                           streaming=True)
            self.music_player = arcade.play_sound(
                self.music,
                volume=self.config_data.volume / 100,
                loop=True
            )
        except FileNotFoundError:
            print("Warning: game_music.mp3 not found or could not be loaded")
            self.music = None
            self.music_player = None

        self.generate_level()
        self.setup_ui()

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

    def setup_ui(self):
        panel_width = (self.window.width // 4) - 10

        # LEFT
        self.left_layout = gui.UIBoxLayout(vertical=True, space_between=20)

        self.panel_echap = MenuEchapPanel(width=panel_width, height=500,
                                          player=self.player)
        self.panel_cheat = CheatPanel(width=panel_width, height=500,
                                      player=self.player)

        self.left_layout.add(self.panel_echap.get_widget())
        self.left_layout.add(self.panel_cheat.get_widget())

        anchor_left = gui.UIAnchorLayout()

        anchor_left.add(
            anchor_x="left",
            anchor_y="center_y",
            child=self.left_layout
        )
        self.manager.add(anchor_left)

        # RIGHT
        self.right_layout = gui.UIBoxLayout(vertical=True, space_between=20)

        self.stat_panel = StatPanel(width=panel_width, height=200,
                                    player=self.player)
        self.lead_panel = LeadPanel(width=panel_width, height=800,
                                    player=self.player)

        self.right_layout.add(self.stat_panel.get_widget())
        self.right_layout.add(self.lead_panel.get_widget())

        self.lead_panel.update_lead(self.sc.get_scores())

        anchor_right = gui.UIAnchorLayout()

        anchor_right.add(
            anchor_x="right",
            anchor_y="center_y",
            child=self.right_layout
        )
        self.manager.add(anchor_right)

    def generate_level(self):
        self.map = Map(self.config_data, self.index_level,
                       (self.window.width, self.window.height))
        self.map.generate_maze()
        if self.index_level == 0:
            self.player = Player(self.map, self.config_data)
        else:
            self.player.map = self.map
            self.player.cell_pos = ([round(self.player.map.size[1] / 2) - 1,
                                    round(self.player.map.size[0] / 2) - 1])
            x, y = self.player.cell_pos
            self.player.pos = list(self.player.map.grid[y][x])
            self.player.speed = self.player.map.cell // 16
        self.index_level += 1

    def on_draw(self):
        self.clear()
        self.map.draw()
        self.player.draw()
        self.manager.draw()
        self.window.set_caption("Pacman - In Game")
        arcade.set_background_color(arcade.color.BLACK)

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
        self.stat_panel.update_label()
        if (len(self.map.pacgums_list) == 0 and
            len(self.map.super_pacgums_list) == 0 and
                self.index_level < len(self.config_data.level)):
            self.generate_level()
