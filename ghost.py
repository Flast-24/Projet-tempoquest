import arcade

class Ghost(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/Player_Ghost.png", scale=1)
        self.center_x = x
        self.center_y = y
