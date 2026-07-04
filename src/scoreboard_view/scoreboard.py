import json
import os
from pathlib import Path
from typing import Dict
import sys


class Scoreboard:
    """Manage the game's saved scoreboard entries on disk."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
        file_path: Path = Path.home() / ".dark_man"
    else:
        file_path: Path = (Path(__file__).parent.parent.parent
                           / "scoreboard.json")

    def __init__(self) -> None:
        """Load existing scoreboard data or create a new file if needed.

        Returns:
            None
        """
        if not os.path.exists(self.file_path):
            print("The scoreboard.json file does not exist. Creating...")
            self.data: Dict[str, int] = {}
            self.save_file()
        else:
            print("The scoreboard.json file has been found. Loading...")
            with open(self.file_path, "r", encoding="utf-8")as f:
                try:
                    data = json.load(f)
                    self.data = self.check_data(data)
                except json.JSONDecodeError:
                    print("Invalid format for scoreboard file...")
                    self.data = {}
                    self.save_file()

    def check_data(self, data_file: dict) -> Dict[str, int]:
        """Validate and clean loaded scoreboard data.

        Args:
            data_file: Raw scoreboard payload loaded from disk.

        Returns:
            A cleaned dictionary of valid player names and scores.
        """
        cleaned_data: Dict[str, int] = {}
        is_modify: bool = False

        for player, score in data_file.items():
            if (self.is_valid_name(player) and isinstance(score, int) and
               score >= 0):
                cleaned_data[player] = score
            else:
                print(f"Invalid entry removed from file: '{player}'"
                      f" with score {score}")
                is_modify = True

        if is_modify:
            self.data = cleaned_data
            self.save_file()
        return cleaned_data

    def is_valid_name(self, name: str) -> bool:
        """Check whether a player name meets the scoreboard rules.

        Args:
            name: The player name to validate.

        Returns:
            True if the name is non-empty, at most 10 characters, and only
            contains letters, spaces, or numbers.
        """
        n_strip = name.strip()
        if n_strip == "":
            return False
        if len(name) > 10:
            return False
        if not all(c.isalpha() or c.isspace() or c.isnumeric() for c in name):
            return False
        return True

    def update_score(self, player: str, score: int) -> None:
        """Add or update a player's score in the scoreboard.

        Args:
            player: The player's name.
            score: The score to save.

        Returns:
            None
        """
        if player in self.data:
            if score > self.data[player]:
                print(f"New record for {player}: {score}")
                self.data[player] = score
        else:
            print(f"New player {player}: {score}")
            self.data[player] = score
        self.save_file()

    def print_scoreboard(self) -> None:
        """Print the scoreboard contents to the console.

        Returns:
            None
        """
        print("------ Scoreboard ------")
        for name, score in self.data.items():
            print(f"- {name}: {score}")

    def save_file(self) -> None:
        """Write the current scoreboard data to disk.

        Returns:
            None
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get_scores(self) -> Dict[str, int]:
        """Return the current scoreboard mapping.

        Returns:
            A dictionary mapping player names to their scores.
        """
        return self.data
