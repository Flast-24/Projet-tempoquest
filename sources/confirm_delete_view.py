import arcade
from constants import *
from pathlib import Path

class ConfirmDeleteView(arcade.View):
    def __init__(self, select_level_view, level_to_delete):
        super().__init__()
        self.select_level_view = select_level_view
        self.level_to_delete = level_to_delete

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"Supprimer '{self.level_to_delete}' ?",
                         SCREEN_W / 2, SCREEN_H / 2 + 50,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        
        arcade.draw_text("Cette action est irréversible.",
                         SCREEN_W / 2, SCREEN_H / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Appuyez sur S pour confirmer la suppression.",
                         SCREEN_W / 2, SCREEN_H / 2 - 75,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")
        
        arcade.draw_text("Appuyez sur N ou ÉCHAP pour annuler.",
                         SCREEN_W / 2, SCREEN_H / 2 - 125,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            self.delete_level()
        elif key == arcade.key.N or key == arcade.key.ESCAPE:
            self.window.show_view(self.select_level_view)

    def delete_level(self):
        level_path = Path(f"data/levels/{self.level_to_delete}.json")
        try:
            if level_path.exists():
                level_path.unlink()
        except OSError as e:
            print(f"Error deleting file: {e}")
        
        self.select_level_view.scan_levels()
        self.window.show_view(self.select_level_view)
