from .player import Player
from abc import ABC, abstractmethod


class Cheat(ABC):
    @abstractmethod
    def add_points(p: Player) -> None:
        p.score += 10

    @abstractmethod
    def add_life(p: Player) -> None:
        p.lives += 1

    @abstractmethod
    def remove_life(p: Player) -> None:
        if p.lives > 0:
            p.lives -= 1

    @abstractmethod
    def remove_points(p: Player) -> None:
        if p.score >= 10:
            p.score -= 10

    @abstractmethod
    def set_invicible(p: Player):
        if not p.invicible:
            p.invicible = True
        else:
            p.invicible = False

    @abstractmethod
    def freeze_minotaurs(p: Player):
        if not p.freeze:
            p.freeze = True
        else:
            p.freeze = False

    @abstractmethod
    def next_level(g):
        g.generate_level()
