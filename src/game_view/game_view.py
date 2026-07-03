from game_view.map import Map
from .end_view import EndView
from game_view.player import Player
from scoreboard_view.scoreboard import Scoreboard
from game_view.ghost.ghost_manager import GhostManager
from game_view.game_menu.left.echap_panel import MenuEchapPanel
from game_view.game_menu.left.cheat_panel import CheatPanel
from game_view.game_menu.right.stats_panel import StatPanel
from game_view.game_menu.right.leader_panel import LeadPanel

import arcade.key as key
import arcade.gui as gui
import arcade

from typing import Any, Optional


class GameView(arcade.View):
    """Main gameplay view, orchestrating the map, player, ghosts, and UI.

    Owns the game loop logic: level generation and progression,
    drawing the map/player/ghosts/UI, handling player input, pausing,
    background music, and transitioning to the end view on victory,
    defeat, or timeout.

    Attributes:
        main_menu_view (arcade.View): The main menu view to return to.
        config_data (Any): Global game configuration.
        sc (Scoreboard): The scoreboard used to record and read scores.
        index_level (int): Index of the level currently being played.
        first_game (bool): Whether this is the first game played in
            this session.
        manager (gui.UIManager): The arcade GUI manager for on-screen
            widgets.
        escape_menu (Optional[Any]): Reserved reference to the escape
            menu widget.
        settings_menu (Optional[Any]): Reserved reference to the
            settings menu widget.
        is_paused (bool): Whether the game is currently paused.
        stat_panel (Optional[StatPanel]): The panel displaying player
            stats (score, time, etc.).
        map (Optional[Map]): The current level's map.
        player (Optional[Player]): The player instance.
        music (Optional[arcade.Sound]): Background music, if loaded.
        music_player (Optional[Any]): Handle to the playing music
            instance, used to stop playback.
        ghost_manager (GhostManager): Manages all ghosts in the level.
    """

    def __init__(self, main_menu_view: arcade.View, config_data: Any) -> None:
        """Initialize the game view, load the first level, and start music.

        Sets up the scoreboard, UI manager, and state flags; attempts
        to load and loop the background music; generates the first
        level and its ghosts; builds the UI panels; and loads the
        game's custom fonts.

        Args:
            main_menu_view (arcade.View): The main menu view to return
                to (e.g., after the game ends).
            config_data (Any): Global game configuration.

        Returns:
            None
        """
        super().__init__()

        self.main_menu_view = main_menu_view
        self.config_data = config_data
        self.sc = Scoreboard()
        self.index_level: int = 0
        self.first_game: bool = True

        self.manager = gui.UIManager()
        self.manager.enable()

        self.escape_menu: Optional[Any] = None
        self.settings_menu: Optional[Any] = None
        self.is_paused: bool = False

        self.stat_panel: Optional[StatPanel] = None
        self.map: Optional[Map] = None
        self.player: Optional[Player] = None
        self.music: Optional[arcade.Sound] = None
        self.music_player: Optional[Any]

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
        self.ghost_manager = GhostManager(self.map, self.player)
        self.setup_ui()

        arcade.load_font("assets/font/Pacmania.ttf")
        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

    def setup_ui(self) -> None:
        """Build and register the game's UI panels and layouts.

        Creates the top "cheats enabled" label, the left-side escape
        and cheat panels (added to the UI only while paused), and the
        right-side stats and leaderboard panels, then registers them
        with the UI manager.

        Returns:
            None
        """
        panel_width: int = (self.window.width // 4) - 10
        self.top_anchor = gui.UIAnchorLayout()
        txt: str = ""
        if self.config_data.cheats_enabled:
            txt = "Cheats enabled !"
        self.cheat_lbl = gui.UILabel(
            text=txt,
            text_color=arcade.color.RED_DEVIL,
            font_name="Press Start 2P",
            font_size=10
        )
        self.top_anchor.add(
            anchor_x="center_x",
            anchor_y="top",
            child=self.cheat_lbl.with_padding(top=15)
        )
        self.manager.add(self.top_anchor)

        # LEFT
        self.panel_echap = MenuEchapPanel(
            width=panel_width,
            height=500,
            player=self.player,
            view=self
        )
        self.panel_cheat = CheatPanel(
                width=panel_width, height=500, player=self.player,
                view=self
            )
        self.left_box = gui.UIBoxLayout(vertical=True, space_between=20)

        self.left_anchor = gui.UIAnchorLayout()
        self.left_anchor.add(
            anchor_x="left",
            anchor_y="center_y",
            child=self.left_box
        )

        # RIGHT
        self.right_layout = gui.UIBoxLayout(vertical=True, space_between=20)
        self.stat_panel = StatPanel(
            width=panel_width, height=200, player=self.player,
            config_data=self.config_data
        )

        if self.player is not None:
            self.player.stat_panel = self.stat_panel

        self.lead_panel = LeadPanel(
            width=panel_width, height=800, player=self.player
        )

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

    def generate_level(self) -> None:
        """Advance to the next level, or show the end view if none remain.

        If all configured levels have been completed, switches to the
        victory ``EndView``. Otherwise, builds a new ``Map`` for the
        next level, creates the player on the first level or
        repositions the existing player and resets the ghosts on
        subsequent levels, increments ``index_level``, and restarts
        the stats panel's timer.

        Returns:
            None
        """
        if self.index_level == len(self.config_data.level):
            win = EndView(self.main_menu_view,
                          self.config_data,
                          self.player,
                          self.sc,
                          defeat=False)
            self.window.show_view(win)
            return
        self.map = Map(self.config_data, self.index_level,
                       (self.window.width, self.window.height))
        self.map.generate_maze()
        if self.index_level == 0:
            self.player = Player(self.map, self.config_data)
        elif self.player is not None:
            self.player.map = self.map
            self.player.cell_pos = ([round(self.map.size[0] / 2) - 1,
                                    round(self.map.size[1] / 2) - 1])
            x, y = self.player.cell_pos
            self.player.pos = list(self.player.map.grid[y][x])
            self.player.speed = self.player.map.cell // 16
            self.ghost_manager.reset_ghost(self.map)
        self.index_level += 1
        if self.stat_panel is not None:
            self.stat_panel.restart_time()

    def on_draw(self) -> None:
        """Render the current frame: map, player, ghosts, and UI.

        Clears the screen, draws the map, player, UI manager
        contents, and ghosts (in that order), draws the pause overlay
        triangle when paused, sets the window caption, and sets the
        background color.

        Returns:
            None
        """
        self.clear()
        if self.map:
            self.map.draw()
        if self.player:
            self.player.draw()
        self.manager.draw()
        self.ghost_manager.draw()
        if self.is_paused:
            self.panel_echap.draw_triangle()
        self.window.set_caption("Pacman - In Game")
        arcade.set_background_color(arcade.color.BLACK)

    def pause_game(self) -> None:
        """Toggle the paused state and show or hide the pause menu.

        When pausing, rebuilds the left-side box layout with the
        escape panel (and cheat panel, if enabled) and adds it to the
        UI manager. When resuming, removes that layout from the UI
        manager.

        Returns:
            None
        """
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.left_box.clear()
            self.left_box.add(self.panel_echap.get_widget())
            if self.config_data.cheats_enabled:
                self.left_box.add(self.panel_cheat.get_widget())
            self.manager.add(self.left_anchor, layer=1)
        else:
            self.manager.remove(self.left_anchor)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle keyboard input for gameplay, pausing, and debug shortcuts.

        Forwards key presses to the cheat panel (if cheats are
        enabled) and to the player. Toggles pause on ``ESCAPE``,
        triggers an instant win on ``F1``, and an instant loss on
        ``F2`` (debug shortcuts). Forwards key presses to the escape
        panel while paused.

        Args:
            symbol (int): The arcade key code that was pressed.
            modifiers (int): Bitwise combination of active modifier
                keys.

        Returns:
            None
        """
        if self.config_data.cheats_enabled:
            self.panel_cheat.on_key_press(symbol, modifiers)
        if self.player:
            self.player.on_key_press(symbol, modifiers)

        if symbol == key.ESCAPE:
            self.pause_game()
            return
        elif symbol == key.F1:
            self.win = EndView(self.main_menu_view, self.config_data,
                               self.player, self.sc, defeat=False)
            self.window.show_view(self.win)
        elif symbol == key.F2:
            self.win = EndView(self.main_menu_view, self.config_data,
                               self.player, self.sc, defeat=True)
            self.window.show_view(self.win)

        if self.is_paused:
            self.panel_echap.on_key_press(symbol, modifiers)

    def on_show_view(self) -> None:
        """Enable the UI manager when this view becomes active.

        Returns:
            None
        """
        self.manager.enable()

    def on_hide_view(self) -> None:
        """Stop the background music and disable the UI manager.

        Called when this view is no longer active (e.g., switching to
        another view).

        Returns:
            None
        """
        if self.music and self.music_player:
            self.music.stop(player=self.music_player)
        self.manager.disable()

    def on_update(self, delta_time: float) -> None:
        """Advance the game state by one frame.

        While paused, only updates the escape panel's labels. While
        running, updates the player and ghosts, checks for the
        player's remaining lives (showing the defeat ``EndView`` if
        zero), updates the stats panel and checks for the level time
        limit (showing a time-out defeat ``EndView`` if reached),
        refreshes the cheat label, and advances to the next level
        when all pac-gums have been collected.

        Args:
            delta_time (float): Time elapsed, in seconds, since the
                last update call.

        Returns:
            None
        """
        if self.is_paused:
            self.panel_echap.update_labels()
            return

        if self.player:
            self.player.update()
            if self.player.lives == 0:
                lose = EndView(self.main_menu_view,
                               self.config_data,
                               self.player,
                               self.sc,
                               defeat=True)
                self.window.show_view(lose)
        self.ghost_manager.update()

        if self.stat_panel:
            self.stat_panel.update_label()
            self.stat_panel.update_timer()
            if (self.stat_panel.get_time_in_sc()
               == self.config_data.lvl_max_time):
                time_lose = EndView(
                    self.main_menu_view,
                    self.config_data,
                    self.player,
                    self.sc,
                    defeat=True,
                    time_elap=True
                )
                self.window.show_view(time_lose)

        if self.config_data.cheats_enabled:
            self.cheat_lbl.text = "Cheats enabled !"
        else:
            self.cheat_lbl.text = ""

        if self.map and len(self.map.pacgums_list) == 0:
            self.generate_level()
            if self.stat_panel:
                self.stat_panel.restart_time()
