import arcade

TILE_SIZE = 44

def load_level(level_num):
    """
    Charge un niveau depuis un fichier .txt.

    Args:
        level_num (int): Le numéro du niveau à charger.

    Returns:
        list: Une liste de chaînes de caractères représentant le niveau.
              Retourne None si le fichier n'est pas trouvé.
    """
    filename = f"levels/level{level_num}.txt"
    try:
        with open(filename, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None
