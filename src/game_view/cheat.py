from .player import Player
from abc import ABC, abstractmethod
from typing import Any


class Cheat(ABC):
    """Abstract base class defining cheat operations.

    The methods in this class mutate player state or trigger game-level
    actions such as advancing to the next level.
    """

    @staticmethod
    @abstractmethod
    def add_points(p: Player) -> None:
        """Increase the player's score by 10.

        Args:
            p: The player whose score should be increased.
        """
        p.score += 10

    @staticmethod
    @abstractmethod
    def add_life(p: Player) -> None:
        """Increase the player's life count by 1.

        Args:
            p: The player whose lives should be increased.
        """
        p.lives += 1

    @staticmethod
    @abstractmethod
    def remove_life(p: Player) -> None:
        """Decrease the player's life count by 1 when possible.

        Args:
            p: The player whose lives should be decreased.
        """
        if p.lives > 0:
            p.lives -= 1

    @staticmethod
    @abstractmethod
    def remove_points(p: Player) -> None:
        """Decrease the player's score by 10 when possible.

        Args:
            p: The player whose score should be decreased.
        """
        if p.score >= 10:
            p.score -= 10

    @staticmethod
    @abstractmethod
    def set_invicible(p: Player) -> None:
        """Toggle the player's invincibility state.

        Args:
            p: The player whose invincibility status should be toggled.
        """
        if not p.invicible:
            p.invicible = True
        else:
            p.invicible = False

    @staticmethod
    @abstractmethod
    def freeze_minotaurs(p: Player) -> None:
        """Toggle the player's freeze state.

        Args:
            p: The player whose freeze state should be toggled.
        """
        if not p.freeze:
            p.freeze = True
        else:
            p.freeze = False

    @staticmethod
    @abstractmethod
    def next_level(g: Any) -> None:
        """Generate the next level for the given game view.

        Args:
            g: The game view or controller that should generate the next level.
        """
        g.generate_level()
