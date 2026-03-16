import arcade
from constants import *
from level_editor import LevelEditorView
import re

class TextInputView(arcade.View):
    def __init__(self, editor_menu_view):
        super().__init__()
        self.editor_menu_view = editor_menu_view
        self.text = ""
        self.error_message = ""

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Créer un nouveau niveau", SCREEN_W / 2, SCREEN_H - 50,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        
        arcade.draw_text("Nom du niveau:", SCREEN_W / 2, SCREEN_H / 2 + 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        # Display the text being typed
        arcade.draw_text(self.text, SCREEN_W / 2, SCREEN_H / 2,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        
        # Display blinking cursor
        if len(self.text) < 20: # Limit cursor blink to max length
            if int(arcade.get_window().time) % 2 == 0:
                text_width = len(self.text) * 14 # Approximate width
                arcade.draw_line(SCREEN_W/2 + text_width/2 + 5, SCREEN_H/2 - 5,
                                 SCREEN_W/2 + text_width/2 + 5, SCREEN_H/2 + 25,
                                 arcade.color.WHITE, 2)


        if self.error_message:
            arcade.draw_text(self.error_message, SCREEN_W / 2, SCREEN_H / 2 - 50,
                             arcade.color.RED, font_size=16, anchor_x="center")

        arcade.draw_text("Appuyez sur ENTRÉE pour valider, ÉCHAP pour annuler.",
                         SCREEN_W / 2, 50, arcade.color.GRAY, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.validate_and_start()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.editor_menu_view)
        elif key == arcade.key.BACKSPACE:
            self.text = self.text[:-1]

    def on_text(self, text):
        # Append the character to the text
        if len(self.text) < 20: # Arbitrary limit
            # a-z, 0-9, underscore and hyphen allowed
            if re.match("^[a-zA-Z0-9_-]*$", text):
                self.text += text
    
    def validate_and_start(self):
        level_name = self.text.strip()
        if not level_name:
            self.error_message = "Le nom ne peut pas être vide."
            return
        
        # Simple sanitization
        level_name = re.sub(r'[^a-zA-Z0-9_-]', '', level_name).lower()

        if level_name in ["level1", "level_editor"]:
            self.error_message = "Ce nom de niveau est réservé."
            return

        # All checks passed, clear error and proceed
        self.error_message = ""
        
        # We pass the editor menu view, which the editor will return to
        editor_view = LevelEditorView(level_name, self.editor_menu_view)
        editor_view.setup()
        self.window.show_view(editor_view)
