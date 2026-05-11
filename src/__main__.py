from menu import MenuView
import arcade

if __name__ == "__main__":
    try:
        window = arcade.Window(500, 520, "Pacman - Menu")
        menu_view = MenuView()
        window.show_view(menu_view)
        arcade.run()
    except BaseException as e:
        print(e)