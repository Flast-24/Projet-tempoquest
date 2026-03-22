import arcade
from constants import *
from text_input_view import TextInputView
from select_level_to_edit_view import SelectLevelToEditView

class EditorMenuView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.options = ["Créer un nouveau niveau", "Modifier un niveau existant"]
        self.selected_index = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Éditeur de Niveaux", SCREEN_W / 2, SCREEN_H - 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        for i, option in enumerate(self.options):
            y = SCREEN_H - 200 - (i * 60)
            color = arcade.color.YELLOW if i == self.selected_index else arcade.color.WHITE
            arcade.draw_text(option, SCREEN_W / 2, y, color, font_size=30, anchor_x="center")
        
        arcade.draw_text("Utilisez HAUT/BAS pour naviguer, ENTRÉE pour choisir, ÉCHAP pour revenir.",
                         SCREEN_W / 2, 100, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == arcade.key.ENTER:
            if self.selected_index == 0:
                # "Créer" selected
                text_input_view = TextInputView(self)
                self.window.show_view(text_input_view)
            elif self.selected_index == 1:
                # "Modifier" selected
                select_edit_view = SelectLevelToEditView(self)
                self.window.show_view(select_edit_view)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.menu_view)
