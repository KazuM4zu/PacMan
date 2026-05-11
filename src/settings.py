import arcade
import arcade.gui as gui


class SettingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        back_button = gui.UIFlatButton(text="Back", width=50)

        @back_button.event("on_click")
        def on_click_back_button(event):
            from menu import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)

        on_text = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_on.png"
        )
        off_text = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_off.png"
        )

        toggle_label = gui.UILabel(text="Full Screen")
        toggle = gui.UITextureToggle(
            on_texture=on_text, off_texture=off_text, width=20, height=20
        )

        toggle_group = gui.UIBoxLayout(vertical=False, space_between=5)
        toggle_group.add(toggle)
        toggle_group.add(toggle_label)

        self.top_grid = gui.UIGridLayout(
            column_count=3, row_count=1, horizontal_spacing=100
        )
        self.top_grid.add(back_button, column=0, row=0)

        self.top_anchor = self.manager.add(gui.UIAnchorLayout())
        self.top_anchor.add(
            anchor_x="left",
            anchor_y="top",
            child=self.top_grid,
        )
        self.mid_anchor = self.manager.add(gui.UIAnchorLayout())
        self.mid_anchor.add(
            anchor_x="left",
            anchor_y="center_y",
            child=toggle_group
        )

    def on_show_view(self):
        self.window.set_caption("Pacman - Settings")
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()



class SettingsSubMenu(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
    def __init__(self, menu_view):
        super().__init__(size_hint=(1, 1))
        self.menu_view = menu_view

        self.frame = self.add(gui.UIAnchorLayout(width=350, height=450, size_hint=None))

        self.frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7, right=7, bottom=7, top=7,
                texture=arcade.load_texture(
                    ":resources:gui_basic_assets/window/dark_blue_gray_panel.png"
                ),
            )
        )

        self.widget_layout = gui.UIBoxLayout(space_between=30)

        title_label = gui.UILabel(text="SETTINGS", font_size=20)
        self.widget_layout.add(title_label)

        on_text = arcade.load_texture(":resources:gui_basic_assets/simple_checkbox/circle_on.png")
        off_text = arcade.load_texture(":resources:gui_basic_assets/simple_checkbox/circle_off.png")

        toggle_label = gui.UILabel(text="Full Screen")
        self.toggle = gui.UITextureToggle(
            on_texture=on_text, off_texture=off_text, width=20, height=20
        )

        toggle_group = gui.UIBoxLayout(vertical=False, space_between=10)
        toggle_group.add(self.toggle)
        toggle_group.add(toggle_label)
        self.widget_layout.add(toggle_group)

        back_button = gui.UIFlatButton(text="Back", width=200)
        self.widget_layout.add(back_button)

        @back_button.event("on_click")
        def on_click_back_button(event):
            self.parent.remove(self)
            self.menu_view.settings_menu = None

        self.frame.add(child=self.widget_layout, anchor_x="center_x", anchor_y="center_y")