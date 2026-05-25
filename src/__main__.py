from front.menu import MenuView
from back.config import check_config_file
import arcade

if __name__ == "__main__":
    # try:
    config_data = check_config_file("config.json")
    window = arcade.Window(1280, 720,
                            "Pacman - Menu",
                            fullscreen=True)
    menu_view = MenuView(config_data)
    window.show_view(menu_view)
    arcade.run()
    # except BaseException as e:
    #     print(e)
