from game_view.ghost.blinky import Blinky
from game_view.ghost.clyde import Clyde
from game_view.ghost.inky import Inky
from game_view.ghost.pinky import Pinky
from game_view.player import Player
from typing import Any


class GhostManager:
    """Manage all four ghosts in the game (Blinky, Clyde, Inky, Pinky).

    Acts as a central access point for the ghosts: it holds the game
    map and the player, and delegates update, draw, and reset
    operations to each individual ghost.

    Attributes:
        map (Any): The current level map/maze.
        player (Player): The player tracked/chased by the ghosts.
        blinky (Blinky): The Blinky ghost instance.
        clyde (Clyde): The Clyde ghost instance.
        inky (Inky): The Inky ghost instance.
        pinky (Pinky): The Pinky ghost instance.
    """

    def __init__(self, map: Any, player: Player) -> None:
        """Initialize the manager and create the four ghosts.

        Args:
            map (Any): The level map/maze.
            player (Player): The player instance.

        Returns:
            None
        """
        self.map = map
        self.player = player

        self.blinky = Blinky(self)
        self.clyde = Clyde(self)
        self.inky = Inky(self)
        self.pinky = Pinky(self)

    def kill_player(self) -> None:
        """Reset all ghosts' positions and kill the player.

        Called when the player collides with a ghost while neither
        invincible nor in super mode.

        Returns:
            None
        """
        self.blinky.init_pos()
        self.clyde.init_pos()
        self.inky.init_pos()
        self.pinky.init_pos()
        self.player.death()

    def reset_ghost(self, map: Any) -> None:
        """Recreate the four ghosts for a new map.

        Args:
            map (Any): The new level map/maze to use.

        Returns:
            None
        """
        self.map = map
        self.blinky = Blinky(self)
        self.clyde = Clyde(self)
        self.inky = Inky(self)
        self.pinky = Pinky(self)

    def draw(self) -> None:
        """Draw all four ghosts on screen.

        Returns:
            None
        """
        self.blinky.draw()
        self.clyde.draw()
        self.pinky.draw()
        self.inky.draw()

    def update(self) -> None:
        """Update the state (position, direction, collisions) of all four ghosts.

        Returns:
            None
        """
        self.blinky.update()
        self.clyde.update()
        self.inky.update()
        self.pinky.update()