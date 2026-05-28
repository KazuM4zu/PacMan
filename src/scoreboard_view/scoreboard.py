import json
import os
from pathlib import Path


class Scoreboard:
    file_path = Path(__file__).parent.parent.parent / "scoreboard.json"

    def __init__(self):
        if not os.path.exists(self.file_path):
            print("The scoreboard.json file does not exist. Creating...")
            self.data = {}
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        else:
            print("The scoreboard.json file has been found. Loading...")
            with open(self.file_path, "r", encoding="utf-8")as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}

    def update_score(self, player, score):
        if player in self.data:
            if score > self.data[player]:
                print(f"New record for {player}: {score}")
                self.data[player] = score
        else:
            print(f"New player {player}: {score}")
            self.data[player] = score
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def print_scoreboard(self):
        print("------ Scoreboard ------")
        for name, score in self.data.items():
            print(f"- {name}: {score}")

    def get_scores(self):
        return self.data
