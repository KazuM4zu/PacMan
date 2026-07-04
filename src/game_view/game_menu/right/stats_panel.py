import arcade
import arcade.gui as gui
from arcade.clock import GLOBAL_CLOCK
from src.game_view.game_menu.panel import PanelInterface


class StatPanel(PanelInterface):
    """Show the player's score, lives, level, and remaining time."""

    def setup_ui(self) -> None:
        """Create the statistics labels and place them in the layout.

        Returns:
            None
        """
        self.start_time: float = GLOBAL_CLOCK.time
        box = gui.UIBoxLayout(vertical=True, space_between=20)

        title = gui.UILabel(
            text="==== STATS ====",
            font_name="Press Start 2P",
            font_size=14,
            text_color=arcade.color.YELLOW
        )
        box.add(title)

        self.score_label = gui.UILabel(
            text="Score: 0000",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.score_label)

        self.live_label = gui.UILabel(
            text=f"Lifes : {self.player.lives}",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.live_label)

        self.level_label = gui.UILabel(
            text="Level: 0",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.level_label)

        self.timer_label = gui.UILabel(
            text=f"Timer: {self.config_data.lvl_max_time}:00",
            font_name="Press Start 2P",
            font_size=12
        )
        box.add(self.timer_label)

        self.layout.add(
            child=box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

    def update_label(self) -> None:
        """Refresh the score and life information shown in the panel.

        Returns:
            None
        """
        self.score_label.text = f"Score: {self.player.score:04d}"
        self.live_label.text = f"Lifes: {self.player.lives}"

    def update_timer(self) -> None:
        """Refresh the displayed countdown timer.

        Returns:
            None
        """
        elaps = GLOBAL_CLOCK.time_since(self.start_time)

        time_remaining = self.config_data.lvl_max_time - elaps
        sec = int(time_remaining)
        ms = int((time_remaining - sec) * 100)
        self.timer_label.text = f"Timer: {sec}:{ms:02d}"

    def get_time_in_sc(self) -> int:
        """Return the elapsed time since the statistics panel started.

        Returns:
            Elapsed seconds as an integer.
        """
        return int(GLOBAL_CLOCK.time_since(self.start_time))

    def restart_time(self) -> None:
        """Reset the panel timer to the current clock value.

        Returns:
            None
        """
        self.start_time = GLOBAL_CLOCK.time
