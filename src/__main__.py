import arcade
import sys

from menu_view.menu_view import MenuView
from config import check_config_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run src/ <config_file> or"
              " make run CONFIG=<config_file>")
        sys.exit(1)
    try:
        config_data = check_config_file(sys.argv[1])
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
