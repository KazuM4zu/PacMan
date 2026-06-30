from game_view.ghost.blinky import Blinky
from game_view.ghost.clyde import Clyde
from game_view.ghost.inky import Inky
from game_view.ghost.pinky import Pinky
from game_view.player import Player
from typing import Any


class GhostManager:
    def __init__(self, map: Any, player: Player) -> None:
        self.map = map
        self.player = player

        self.blinky = Blinky(self)
        self.clyde = Clyde(self)
        self.inky = Inky(self)
        self.pinky = Pinky(self)

    def kill_player(self) -> None:
        self.blinky.init_pos()
        self.clyde.init_pos()
        self.inky.init_pos()
        self.pinky.init_pos()
        self.player.death()

    def reset_ghost(self, map: Any) -> None:
        self.map = map
        self.blinky = Blinky(self)
        self.clyde = Clyde(self)
        self.inky = Inky(self)
        self.pinky = Pinky(self)

    def draw(self) -> None:
        self.blinky.draw()
        self.clyde.draw()
        self.pinky.draw()
        self.inky.draw()

    def update(self) -> None:
        self.blinky.update()
        self.clyde.update()
        self.inky.update()
        self.pinky.update()
