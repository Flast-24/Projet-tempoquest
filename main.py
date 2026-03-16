import arcade
from constants import *
from select_level_view import SelectLevelView
from editor_menu_view import EditorMenuView

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Principal", SCREEN_W / 2, SCREEN_H / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Appuyez sur J pour Jouer", SCREEN_W / 2, SCREEN_H / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Appuyez sur E pour l'Éditeur de niveaux", SCREEN_W / 2, SCREEN_H / 2 - 125,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            select_view = SelectLevelView(self)
            self.window.show_view(select_view)
        elif key == arcade.key.E:
            editor_menu = EditorMenuView(self)
            self.window.show_view(editor_menu)

def main():
    window = arcade.Window(SCREEN_W, SCREEN_H, "Jeu Temporel")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
