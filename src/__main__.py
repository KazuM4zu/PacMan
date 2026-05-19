from menu import MenuView
import menu
import arcade

if __name__ == "__main__":
    try:
        window = arcade.Window(menu.WINDOW_HEIGHT, menu.WINDOW_WIDTH,
                               "Pacman - Menu", resizable=True)
        menu_view = MenuView()
        window.show_view(menu_view)
        arcade.run()
    except BaseException as e:
        print(e)