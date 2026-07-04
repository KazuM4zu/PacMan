import arcade
import arcade.gui as gui
from src.game_view.game_menu.panel import PanelInterface


class LeadPanel(PanelInterface):
    """Render a leaderboard with the highest scores."""

    def setup_ui(self) -> None:
        """Create the leaderboard title and score container.

        Returns:
            None
        """
        self.box = gui.UIBoxLayout(vertical=True, space_between=20)
        title = gui.UILabel(
            text="LeaderBoard",
            align="center",
            font_size=12,
            font_name="Press Start 2P"
        )
        self.box.add(title)

        self.score_box = gui.UIBoxLayout(vertical=True, space_between=10)
        self.box.add(self.score_box)

        self.layout.add(child=self.box,
                        anchor_x="center_x",
                        anchor_y="top",
                        align_y=-20)

    def update_lead(self, data: dict[str, int]) -> None:
        """Refresh the leaderboard with the latest scores.

        Args:
            data: Mapping of player names to their score values.

        Returns:
            None
        """
        self.score_box.clear()

        sorted_score = sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )
        top_sc = sorted_score[:30]
        for index, (name, score) in enumerate(top_sc):
            max_score_length = 6
            score_str = str(score)
            if len(score_str) > max_score_length:
                score_str = f"{score_str[:max_score_length]}..."

            text = f"{index + 1}. {name[:14]:<14} {score_str}"
            color = arcade.color.WHITE
            if index == 0:
                color = arcade.color.GOLD
            elif index == 1:
                color = arcade.color.SILVER
            elif index == 2:
                color = arcade.color.BRONZE

            score_label = gui.UILabel(
                text=text,
                font_name="Press Start 2P",
                font_size=10,
                text_color=color
            )
            self.score_box.add(score_label)
