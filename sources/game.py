import arcade
from constants import *
from player import Player
from ghost import Ghost
import level_manager

def _create_sprite(size, color, alpha=255):
    texture = arcade.make_soft_square_texture(size, color, outer_alpha=alpha)
    sprite = arcade.Sprite(texture)
    return sprite

class GameView(arcade.View):
    def __init__(self, level_name, menu_view):
        super().__init__()
        self.level_name = level_name
        self.menu_view = menu_view
        self.player = None
        self.player_list = None
        self.walls = None
        self.goal_list = None
        self.physics = None
        self.ghosts = arcade.SpriteList()
        self.level_data = None
        self.win = False
        self.level_found = True
        self.max_ghosts = 0
        self.ghosts_left = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.ghosts.clear()
        self.level_data = level_manager.load_level(self.level_name)
        
        if not self.level_data:
            self.level_found = False
            return

        self.max_ghosts = self.level_data.get("max_ghosts", 3)
        self.ghosts_left = self.max_ghosts

        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        texture_path = "data/assets/images/Block_Texture.png"
        texture_size = 50

        for wall_data in self.level_data["walls"]:
            wall_width = int(wall_data["size"][0])
            wall_height = int(wall_data["size"][1])
            center_x = wall_data["position"][0]
            center_y = wall_data["position"][1]

            start_x = center_x - wall_width / 2
            start_y = center_y - wall_height / 2

            num_tiles_x = wall_width // texture_size
            num_tiles_y = wall_height // texture_size

            for i in range(num_tiles_x):
                for j in range(num_tiles_y):
                    wall = arcade.Sprite(texture_path)
                    wall.center_x = start_x + (i * texture_size) + (texture_size / 2)
                    wall.center_y = start_y + (j * texture_size) + (texture_size / 2)
                    self.walls.append(wall)

        self.player = Player()
        self.player.center_x = self.level_data["start"][0]
        self.player.center_y = self.level_data["start"][1]
        self.player_list.append(self.player)
        
        self.goal_list = arcade.SpriteList()
        goal = _create_sprite(50, arcade.color.GOLD)
        goal.center_x = self.level_data["end"][0]
        goal.center_y = self.level_data["end"][1]
        self.goal_list.append(goal)

        self.physics = arcade.PhysicsEnginePlatformer(self.player, [self.walls, self.ghosts], GRAVITY)
        
        self.win = False

    def on_draw(self):
        self.clear()
        
        if not self.level_found:
            arcade.draw_text("Niveau non trouvé.", SCREEN_W / 2, SCREEN_H / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_text("Appuyez sur Entrée pour retourner au menu.", SCREEN_W / 2, SCREEN_H / 2 - 50, arcade.color.WHITE, font_size=20, anchor_x="center")
            return

        self.walls.draw()
        self.ghosts.draw()
        self.goal_list.draw()
        self.player_list.draw()
        
        arcade.draw_text(f"R: Créer fantôme ({self.ghosts_left}/{self.max_ghosts} restants)", 10, SCREEN_H - 20, arcade.color.WHITE)
        arcade.draw_text("T: Recommencer", 10, SCREEN_H - 40, arcade.color.WHITE)
        arcade.draw_text("Échap: Quitter", 10, SCREEN_H - 60, arcade.color.WHITE)
        
        if self.win:
            arcade.draw_text("Vous avez gagné!", SCREEN_W / 2, SCREEN_H / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_text("Appuyez sur Entrée pour recommencer ou Échap pour quitter.", SCREEN_W / 2, SCREEN_H / 2 - 50, arcade.color.WHITE, font_size=20, anchor_x="center")


    def on_update(self, delta_time):
        if not self.level_found:
            return
        if not self.win:
            self.physics.update()

            if self.player.center_y < 0:
                self.setup()
                return

            if arcade.check_for_collision_with_list(self.player, self.goal_list):
                self.win = True

    def on_key_press(self, key, modifiers):
        if not self.level_found:
            if key == arcade.key.ENTER:
                self.window.show_view(self.menu_view)
            return

        if self.win:
            if key == arcade.key.ENTER:
                self.setup()
            elif key == arcade.key.ESCAPE:
                self.window.show_view(self.menu_view)
            return

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu_view)
        elif key == arcade.key.T:
            self.setup()

        elif key == arcade.key.UP and self.physics.can_jump():
            self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVE_SPEED
            
        elif key == arcade.key.R:
            if self.ghosts_left > 0:
                ghost = Ghost(self.player.center_x, self.player.center_y)
                self.ghosts.append(ghost)
                self.ghosts_left -= 1
                
                self.player.center_x = self.level_data["start"][0]
                self.player.center_y = self.level_data["start"][1]
                self.player.change_x = 0
                self.player.change_y = 0

    def on_key_release(self, key, modifiers):
        if not self.level_found:
            return
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
