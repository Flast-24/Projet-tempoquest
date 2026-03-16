import arcade
from pathlib import Path
from constants import *
from game import GameView

class SelectLevelView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.levels = []
        self.selected_index = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.scan_levels()

    def scan_levels(self):
        self.levels = ["level1"]
        level_files = Path("levels").glob("*.json")
        custom_levels = sorted([f.stem for f in level_files if f.stem not in ["level1", "level_editor"]])
        self.levels.extend(custom_levels)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Sélectionnez un niveau", SCREEN_W / 2, SCREEN_H - 50,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

        for i, level_name in enumerate(self.levels):
            y = SCREEN_H - 150 - (i * 50)
            color = arcade.color.YELLOW if i == self.selected_index else arcade.color.WHITE
            arcade.draw_text(level_name, SCREEN_W / 2, y, color, font_size=24, anchor_x="center")
        
        arcade.draw_text("Utilisez HAUT/BAS pour naviguer, ENTRÉE pour choisir, ÉCHAP pour revenir.",
                         SCREEN_W / 2, 50, arcade.color.GRAY, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.levels)
        elif key == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.levels)
        elif key == arcade.key.ENTER:
            level_to_load = self.levels[self.selected_index]
            game_view = GameView(level_to_load, self.menu_view)
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.menu_view)
