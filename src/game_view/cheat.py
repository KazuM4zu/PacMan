from .player import Player
from abc import abstractmethod, ABC


class Cheat(ABC):
    @abstractmethod
    def add_points(p: Player) -> None:
        p.score += 10

    @abstractmethod
    def add_life(p: Player) -> None:
        p.lives += 1

    @abstractmethod
    def remove_points(p: Player) -> None:
        if p.score >= 10:
            p.score -= 10

    @abstractmethod
    def set_invicible():
        pass

    @abstractmethod
    def freeze_minotaurs():
        pass
