import arcade
from constants import *
from level_editor import LevelEditorView
import re
from pathlib import Path

class RenameLevelView(arcade.View):
    def __init__(self, select_level_view, old_name):
        super().__init__()
        self.select_level_view = select_level_view
        self.old_name = old_name
        self.text = old_name
        self.error_message = ""

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Renommer le niveau", SCREEN_W / 2, SCREEN_H - 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        
        arcade.draw_text(f"Nouveau nom pour '{self.old_name}':", SCREEN_W / 2, SCREEN_H / 2 + 100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

        arcade.draw_text(self.text, SCREEN_W / 2, SCREEN_H / 2,
                         arcade.color.WHITE, font_size=35, anchor_x="center")
        
        if len(self.text) < 20:
            if int(arcade.get_window().time) % 2 == 0:
                text_width = len(self.text) * 20
                arcade.draw_line(SCREEN_W/2 + text_width/2 + 5, SCREEN_H/2 - 5,
                                 SCREEN_W/2 + text_width/2 + 5, SCREEN_H/2 + 25,
                                 arcade.color.WHITE, 2)


        if self.error_message:
            arcade.draw_text(self.error_message, SCREEN_W / 2, SCREEN_H / 2 - 100,
                             arcade.color.RED, font_size=25, anchor_x="center")

        arcade.draw_text("Appuyez sur ENTRÉE pour valider, ÉCHAP pour annuler.",
                         SCREEN_W / 2, 100, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.validate_and_rename()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.select_level_view)
        elif key == arcade.key.BACKSPACE:
            self.text = self.text[:-1]

    def on_text(self, text):
        if len(self.text) < 20:
            if re.match("^[a-zA-Z0-9_ -]*$", text):
                self.text += text
    
    def validate_and_rename(self):
        new_name = self.text.strip()
        if not new_name:
            self.error_message = "Le nom ne peut pas être vide."
            return
        
        new_name = re.sub(r'[^a-zA-Z0-9_ -]', '', new_name).lower()

        if new_name in ["level1", "level_editor"]:
            self.error_message = "Ce nom de niveau est réservé."
            return

        old_path = Path(f"data/levels/{self.old_name}.json")
        new_path = Path(f"data/levels/{new_name}.json")

        if new_path.exists():
            self.error_message = f"Le niveau '{new_name}' existe déjà."
            return

        try:
            old_path.rename(new_path)
        except OSError as e:
            self.error_message = f"Erreur lors du renommage: {e}"
            return

        self.error_message = ""
        
        self.select_level_view.scan_levels()
        self.window.show_view(self.select_level_view)
