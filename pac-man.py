import arcade
import sys
import os

from src.menu_view.menu_view import MenuView
from src.config import check_config_file

if __name__ == "__main__":
    """Load configuration, create the game window, and start the main menu."""
    sys.setrecursionlimit(100000000)
    config_file = "config.json"
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
        if len(sys.argv) == 2:
            config_file = os.path.abspath(sys.argv[1])

    elif len(sys.argv) == 2:
        config_file = sys.argv[1]
    if len(sys.argv) > 2:
        print("Usage: uv run src/ <config_file> or"
              " make run CONFIG=<config_file>")
        sys.exit(1)

    try:
        config_data = check_config_file(config_file)
    except Exception as e:
        print(f"Config error: {e}")
        sys.exit(1)

    try:
        window = arcade.Window(1280, 720,
                               "Pacman - Menu",
                               fullscreen=True)
        menu_view = MenuView(config_data)
        window.show_view(menu_view)
        arcade.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
