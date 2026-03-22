import json
import arcade
from pathlib import Path

def load_level(level_name):
    level_file = Path(f"data/levels/{level_name}.json")
    if not level_file.exists():
        return None
    with open(level_file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # The file is empty or malformed
            return None

def create_walls_from_data(level_data):
    walls = arcade.SpriteList()
    for wall_data in level_data["walls"]:
        wall = arcade.SpriteSolidColor(
            int(wall_data["size"][0]),
            int(wall_data["size"][1]),
            arcade.color.DARK_GREEN
        )
        wall.center_x = wall_data["position"][0]
        wall.center_y = wall_data["position"][1]
        walls.append(wall)
    return walls
