import arcade
from pathlib import Path
from constants import *
from level_editor import LevelEditorView

class SelectLevelToEditView(arcade.View):
    def __init__(self, editor_menu_view):
        super().__init__()
        self.editor_menu_view = editor_menu_view
        self.levels = []
        self.selected_index = 0
        self.message = ""

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.scan_levels()

    def scan_levels(self):
        level_files = Path("levels").glob("*.json")
        self.levels = sorted([f.stem for f in level_files if f.stem not in ["level1", "level_editor"]])
        if not self.levels:
            self.message = "Aucun niveau personnalisé trouvé."

    def on_draw(self):
        self.clear()
        arcade.draw_text("Modifier un niveau existant", SCREEN_W / 2, SCREEN_H - 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        if self.message:
            arcade.draw_text(self.message, SCREEN_W / 2, SCREEN_H / 2,
                             arcade.color.WHITE, font_size=30, anchor_x="center")
        else:
            for i, level_name in enumerate(self.levels):
                y = SCREEN_H - 200 - (i * 60)
                color = arcade.color.YELLOW if i == self.selected_index else arcade.color.WHITE
                arcade.draw_text(level_name, SCREEN_W / 2, y, color, font_size=30, anchor_x="center")
        
        arcade.draw_text("Utilisez HAUT/BAS pour naviguer, ENTRÉE pour choisir, ÉCHAP pour revenir.",
                         SCREEN_W / 2, 100, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.editor_menu_view)
            return

        if not self.levels:
            return

        if key == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.levels)
        elif key == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.levels)
        elif key == arcade.key.ENTER:
            level_to_edit = self.levels[self.selected_index]
            editor_view = LevelEditorView(level_to_edit, self.editor_menu_view)
            editor_view.setup()
            self.window.show_view(editor_view)
