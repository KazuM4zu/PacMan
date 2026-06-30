from .player import Player
from abc import ABC, abstractmethod
from typing import Any


class Cheat(ABC):
    @staticmethod
    @abstractmethod
    def add_points(p: Player) -> None:
        p.score += 10

    @staticmethod
    @abstractmethod
    def add_life(p: Player) -> None:
        p.lives += 1

    @staticmethod
    @abstractmethod
    def remove_life(p: Player) -> None:
        if p.lives > 0:
            p.lives -= 1

    @staticmethod
    @abstractmethod
    def remove_points(p: Player) -> None:
        if p.score >= 10:
            p.score -= 10

    @staticmethod
    @abstractmethod
    def set_invicible(p: Player) -> None:
        if not p.invicible:
            p.invicible = True
        else:
            p.invicible = False

    @staticmethod
    @abstractmethod
    def freeze_minotaurs(p: Player) -> None:
        if not p.freeze:
            p.freeze = True
        else:
            p.freeze = False

    @staticmethod
    @abstractmethod
    def next_level(g: Any) -> None:
        g.generate_level()
