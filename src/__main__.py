import arcade

from menu_view.menu_view import MenuView
from config import check_config_file

if __name__ == "__main__":
    config_data = check_config_file("config.json")
    window = arcade.Window(1280, 720,
                           "Pacman - Menu",
                           fullscreen=True)
    menu_view = MenuView(config_data)
    window.show_view(menu_view)
    arcade.run()
