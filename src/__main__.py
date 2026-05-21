from front.menu import MenuView
from back.config import check_config_file
import arcade

if __name__ == "__main__":
    try:
        config_data = check_config_file("config.json")
        window = arcade.Window(config_data.win_size[0],
                               config_data.win_size[1],
                               "Pacman - Menu", resizable=True)
        menu_view = MenuView()
        window.show_view(menu_view)
        arcade.run()
    except BaseException as e:
        print(e)
