import arcade
from constants import *
from select_level_view import SelectLevelView
from editor_menu_view import EditorMenuView

class MyWindow(arcade.Window):
    def __init__(self, width, height, title, fullscreen, resizable):
        super().__init__(width, height, title, fullscreen=fullscreen, resizable=resizable)
        self.game_width = width
        self.game_height = height
        self.set_vsync(True)
        # Force an initial resize event
        self.on_resize(self.width, self.height)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        
        game_aspect_ratio = self.game_width / self.game_height
        window_aspect_ratio = width / height
        
        if window_aspect_ratio > game_aspect_ratio:
            # Window is wider
            view_width = int(game_aspect_ratio * height)
            view_height = height
            x_offset = (width - view_width) // 2
            y_offset = 0
        else:
            # Window is taller
            view_width = width
            view_height = int(width / game_aspect_ratio)
            x_offset = 0
            y_offset = (height - view_height) // 2
            
        self.ctx.viewport = (x_offset, y_offset, view_width, view_height)
        self.ctx.projection_2d = 0, self.game_width, 0, self.game_height

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.help_visible = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        if self.help_visible:
            arcade.draw_text("Aide", SCREEN_W / 2, SCREEN_H - 100,
                             arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text("F: Plein écran", SCREEN_W / 2, SCREEN_H / 2 + 100,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("Flèches directionnelles: Déplacer le personnage", SCREEN_W / 2, SCREEN_H / 2 + 50,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("T: Recommencer le niveau", SCREEN_W / 2, SCREEN_H / 2,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("R: Recréer un personnage", SCREEN_W / 2, SCREEN_H / 2 - 50,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("Appuyez sur A pour revenir au menu principal", SCREEN_W / 2, 100,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
        else:
            arcade.draw_text("Menu Principal", SCREEN_W / 2, SCREEN_H / 2,
                             arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text("Appuyez sur J pour Jouer", SCREEN_W / 2, SCREEN_H / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Appuyez sur E pour l'Éditeur de niveaux", SCREEN_W / 2, SCREEN_H / 2 - 125,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Appuyez sur A pour afficher l'aide", SCREEN_W / 2, SCREEN_H / 2 - 175,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
            arcade.draw_text("Appuyez sur Q pour Quitter", SCREEN_W / 2, SCREEN_H / 2 - 225,
                             arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.help_visible = False
            select_view = SelectLevelView(self)
            self.window.show_view(select_view)
        elif key == arcade.key.E:
            self.help_visible = False
            editor_menu = EditorMenuView(self)
            self.window.show_view(editor_menu)
        elif key == arcade.key.A:
            self.help_visible = not self.help_visible
        elif key == arcade.key.Q:
            self.window.close()

def main():
    window = MyWindow(SCREEN_W, SCREEN_H, "Jeu Temporel", fullscreen=False, resizable=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
