import arcade
from constants import *
import json
from pathlib import Path
import level_manager

def _create_sprite(size, color, alpha=255):
    texture = arcade.make_soft_square_texture(size, color, outer_alpha=alpha)
    sprite = arcade.Sprite(texture)
    return sprite

class LevelEditorView(arcade.View):
    def __init__(self, level_name, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.level_name = level_name
        self.grid = arcade.SpriteList()
        self.cursor_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.start_list = arcade.SpriteList()
        self.end_list = arcade.SpriteList()
        self.save_message_timer = 0
        self.max_ghosts = 3

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        
        self.grid.clear()
        for x in range(0, self.window.width, 50):
            for y in range(0, self.window.height, 50):
                sprite = _create_sprite(50, arcade.color.GRAY, alpha=100)
                sprite.center_x = x + 25
                sprite.center_y = y + 25
                self.grid.append(sprite)

    def setup(self):
        cursor = _create_sprite(50, arcade.color.WHITE, alpha=100)
        self.cursor_list.append(cursor)

        level_data = level_manager.load_level(self.level_name)
        if level_data:
            self.max_ghosts = level_data.get("max_ghosts", 3)
            for wall_data in level_data["walls"]:
                wall = _create_sprite(50, arcade.color.DARK_GREEN)
                wall.center_x = wall_data["position"][0]
                wall.center_y = wall_data["position"][1]
                self.walls.append(wall)
            
            if "start" in level_data:
                start = _create_sprite(50, arcade.color.BLUE)
                start.center_x = level_data["start"][0]
                start.center_y = level_data["start"][1]
                self.start_list.append(start)

            if "end" in level_data:
                end = _create_sprite(50, arcade.color.GOLD)
                end.center_x = level_data["end"][0]
                end.center_y = level_data["end"][1]
                self.end_list.append(end)

    def on_draw(self):
        self.clear()
        self.grid.draw()
        self.walls.draw()
        self.start_list.draw()
        self.end_list.draw()
        self.cursor_list.draw()
        
        arcade.draw_text(f"Éditeur de niveau: {self.level_name}", 10, self.window.height - 30, arcade.color.WHITE, 20)
        arcade.draw_text("Cliquez pour placer des murs", 10, self.window.height - 60, arcade.color.WHITE, 16)
        arcade.draw_text("Clique-droit pour enlever un mur", 10, self.window.height - 90, arcade.color.WHITE, 16)
        arcade.draw_text("S: Placer le départ", 10, self.window.height - 120, arcade.color.WHITE, 16)
        arcade.draw_text("E: Placer l'arrivée", 10, self.window.height - 150, arcade.color.WHITE, 16)
        arcade.draw_text("Entrée: Sauvegarder", 10, self.window.height - 180, arcade.color.WHITE, 16)
        arcade.draw_text("Échap: Quitter sans sauvegarder", 10, self.window.height - 210, arcade.color.WHITE, 16)
        arcade.draw_text(f"HAUT/BAS: Changer nombre max de fantômes ({self.max_ghosts})", 10, self.window.height - 240, arcade.color.WHITE, 16)

        if self.save_message_timer > 0:
            arcade.draw_text("Sauvegardé !", self.window.width / 2, self.window.height / 2, 
                             arcade.color.GREEN, 40, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_list[0].center_x = (x // 50) * 50 + 25
        self.cursor_list[0].center_y = (y // 50) * 50 + 25

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if len(arcade.get_sprites_at_point(self.cursor_list[0].position, self.walls)) > 0:
                return
            wall = _create_sprite(50, arcade.color.DARK_GREEN)
            wall.center_x = self.cursor_list[0].center_x
            wall.center_y = self.cursor_list[0].center_y
            self.walls.append(wall)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            hit_list = arcade.get_sprites_at_point(self.cursor_list[0].position, self.walls)
            for wall in hit_list:
                wall.remove_from_sprite_lists()

    def on_update(self, delta_time):
        if self.save_message_timer > 0:
            self.save_message_timer -= delta_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            if self.start_list:
                self.start_list[0].position = self.cursor_list[0].position
            else:
                start = _create_sprite(50, arcade.color.BLUE)
                start.position = self.cursor_list[0].position
                self.start_list.append(start)
        elif key == arcade.key.E:
            if self.end_list:
                self.end_list[0].position = self.cursor_list[0].position
            else:
                end = _create_sprite(50, arcade.color.GOLD)
                end.position = self.cursor_list[0].position
                self.end_list.append(end)
        elif key == arcade.key.ENTER:
            self.save_level()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.menu_view)
        elif key == arcade.key.UP:
            self.max_ghosts += 1
        elif key == arcade.key.DOWN:
            self.max_ghosts = max(0, self.max_ghosts - 1)
    
    def save_level(self):
        level_data = {
            "start": [self.start_list[0].center_x, self.start_list[0].center_y] if self.start_list else [100, 100],
            "end": [self.end_list[0].center_x, self.end_list[0].center_y] if self.end_list else [700, 500],
            "max_ghosts": self.max_ghosts,
            "walls": []
        }
        for wall in self.walls:
            level_data["walls"].append({
                "position": [wall.center_x, wall.center_y],
                "size": [wall.width, wall.height]
            })
        
        filepath = Path(f"data/levels/{self.level_name}.json")
        with open(filepath, "w") as f:
            json.dump(level_data, f, indent=4)
        self.save_message_timer = 3.0
