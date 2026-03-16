import arcade
from constants import *

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)
        self.center_x = 100
        self.center_y = 100
