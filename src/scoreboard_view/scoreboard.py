import json
import os
from pathlib import Path
from typing import Dict


class Scoreboard:
    file_path: Path = Path(__file__).parent.parent.parent / "scoreboard.json"

    def __init__(self) -> None:
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
        n_strip = name.strip()
        if n_strip == "":
            return False
        if len(name) > 10:
            return False
        if not all(c.isalpha() or c.isspace() or c.isnumeric() for c in name):
            return False
        return True

    def update_score(self, player: str, score: int) -> None:
        if player in self.data:
            if score > self.data[player]:
                print(f"New record for {player}: {score}")
                self.data[player] = score
        else:
            print(f"New player {player}: {score}")
            self.data[player] = score
        self.save_file()

    def print_scoreboard(self) -> None:
        print("------ Scoreboard ------")
        for name, score in self.data.items():
            print(f"- {name}: {score}")

    def save_file(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get_scores(self) -> Dict[str, int]:
        return self.data
