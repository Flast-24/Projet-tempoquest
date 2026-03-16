import arcade

class Ghost(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)
        self.center_x = x
        self.center_y = y
