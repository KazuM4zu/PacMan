import arcade
import arcade.gui as gui
from typing import Dict, Any
from scoreboard_view.scoreboard import Scoreboard
from scoreboard_view.scoreview import ScoreView


class EndView(arcade.View):
    """Display the game result, allow score saving,
    and navigate back to menu."""

    def __init__(
        self,
        main_menu_view: Any,
        config_data: Any,
        player: Any,
        scoreboard: Scoreboard,
        defeat: bool = True,
        time_elap: bool = False
    ) -> None:
        """Initialize the end view and build its UI.

        Args:
            main_menu_view: Reference to the main menu view.
            config_data: Configuration data for the game.
            player: Player instance containing the final score.
            scoreboard: Scoreboard used to save the score.
            defeat: Whether the player lost the game.
            time_elap: Whether the game ended because the timer expired.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.EERIE_BLACK)

        arcade.load_font("assets/font/PressStart2P-Regular.ttf")

        self.defeat: bool = defeat
        self.main_menu_view: Any = main_menu_view
        self.config_data: Any = config_data
        self.player: Any = player
        self.sc: Scoreboard = scoreboard
        self.time_elap: bool = time_elap

        self.manager = gui.UIManager()
        self.manager.enable()

        self.music = arcade.load_sound("assets/sound/music/loser.mp3",
                                       streaming=True)
        self.music_player = arcade.play_sound(
            self.music,
            volume=self.config_data.volume / 100,
            loop=True
        )

        button_style: Dict[str, gui.UIFlatButton.UIStyle] = {
                "normal": gui.UIFlatButton.UIStyle(
                    font_name="Press Start 2P",
                    font_size=15,
                    font_color=arcade.color.WHITE,
                    bg=arcade.color.DARK_SLATE_GRAY,
                    border=arcade.color.WHITE,
                    border_width=2,
                ),
                "hover": gui.UIFlatButton.UIStyle(
                    font_name="Press Start 2P",
                    font_size=15,
                    font_color=arcade.color.EERIE_BLACK,
                    bg=arcade.color.WHITE,
                    border=arcade.color.WHITE,
                    border_width=2,
                ),
                "press": gui.UIFlatButton.UIStyle(
                    font_name="Press Start 2P",
                    font_size=15,
                    font_color=arcade.color.EERIE_BLACK,
                    bg=arcade.color.GRAY,
                    border=arcade.color.WHITE,
                    border_width=2,
                )
            }

        box_layout = gui.UIBoxLayout(
            vertical=True,
            space_between=15
        )
        txt: str = ""
        if self.defeat:
            if self.time_elap:
                txt = "Time elapsed, you lose !"
            else:
                txt = "You lose !"
            color = arcade.color.RED_DEVIL
        else:
            txt = "You win !"
            color = arcade.color.YELLOW

        title = gui.UILabel(
            text=txt,
            width=150,
            font_name="Press Start 2P",
            font_size=20,
            text_color=color
        )
        box_layout.add(title.with_padding(bottom=15))

        box_layout.add(
            gui.UILabel(
                text=f"Your score was {self.player.score}.",
                width=150,
                font_name="Press Start 2P",
                font_size=20
            )
        )
        if self.player.score > 0:
            box_layout.add(
                gui.UILabel(
                    text="Please enter your username to save your score.",
                    width=150,
                    font_name="Press Start 2P",
                    font_size=20
                )
            )

            self.username = gui.UIInputText(
                width=150,
                font_name="Press Start 2P"
            )
            box_layout.add(self.username)
            self.error_msg = gui.UILabel(
                text="",
                font_name="Press Start 2P",
                font_size=10,
                text_color=arcade.color.RED_DEVIL
            )
            box_layout.add(self.error_msg)

            self.save_button = gui.UIFlatButton(
                text="Save and exit",
                height=40,
                width=300,
                style=button_style
            )
            box_layout.add(self.save_button)
            setattr(self.save_button, "on_click", self.on_save)

        self.exit_button = gui.UIFlatButton(
            text="Do not save and exit",
            height=60,
            width=450,
            style=button_style
        )
        box_layout.add(self.exit_button)
        setattr(self.exit_button, "on_click", self.on_exit)

        anchor = gui.UIAnchorLayout()
        anchor.add(
            child=box_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

    def on_draw(self) -> None:
        """Draw the end view UI to the screen.

        Returns:
            None
        """
        self.clear()
        self.manager.draw()

    def on_exit(self, event: gui.UIOnClickEvent) -> None:
        """Return to the main menu and stop end-view music.

        Args:
            event: The click event for the exit button.

        Returns:
            None
        """
        if self.music and self.music_player:
            self.music.stop(player=self.music_player)
        from menu_view.menu_view import MenuView
        mv = MenuView(self.config_data)
        self.window.show_view(mv)

    def is_alnum_space(self, s: str) -> bool:
        """Check whether a string contains only letters, numbers, or spaces.

        Args:
            s: The string to validate.

        Returns:
            True if the string contains only alphanumeric
            characters and spaces.
        """
        return all(c.isalpha() or c.isspace() or c.isnumeric() for c in s)

    def on_save(self, event: gui.UIOnClickEvent) -> None:
        """Validate the username and save the score if it is valid.

        Args:
            event: The click event for the save button.

        Returns:
            None
        """
        username_str: str = self.username.text.strip()
        if username_str == "":
            self.error_msg.text = "The username cannot be empty !"
        elif not self.is_alnum_space(username_str):
            self.error_msg.text = ("The username can only contain"
                                   " alphanumeric characters and spaces.")
        elif len(username_str) > 10:
            self.error_msg.text = "The username must not exceed 10 characters."
        else:
            self.sc.update_score(username_str, self.player.score)
            if self.music and self.music_player:
                self.music.stop(player=self.music_player)
            from menu_view.menu_view import MenuView
            mv = MenuView(self.config_data)
            self.scoreboard_view = ScoreView(self.sc, mv,
                                             self.config_data)
            self.window.show_view(self.scoreboard_view)

    def on_show_view(self) -> None:
        """Enable the UI manager when the view becomes active.

        Returns:
            None
        """
        self.manager.enable()

    def on_hide_view(self) -> None:
        """Disable the UI manager when the view is no longer active.

        Returns:
            None
        """
        self.manager.disable()
