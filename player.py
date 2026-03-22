import arcade
from constants import *

class Player(arcade.Sprite):
    def __init__(self):
        # Le paramètre `scale` permet d'ajuster la taille du sprite.
        super().__init__("assets/images/Block_Texture.png", scale=1)
        self.center_x = 100
        self.center_y = 100
