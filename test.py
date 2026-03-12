import arcade
from main import MonJeu, GRAVITY, JUMP_SPEED, MOVE_SPEED # On importe la classe de base et les constantes
import level_manager

# --- Constantes ---
# On peut réutiliser les constantes de main.py ou en définir de nouvelles
TILE_SIZE = level_manager.TILE_SIZE

class GameWithLevels(MonJeu):
    """
    Classe principale du jeu, héritant de MonJeu pour en étendre les fonctionnalités
    avec un système de niveaux.
    """
    def __init__(self):
        super().__init__()
        
        self.current_level = 1
        self.exit_list = None

    def setup(self):
        """
        Configure le jeu pour le niveau actuel.
        Cette méthode est appelée à chaque début de niveau.
        """
        # 1. Charger le niveau
        level_data = level_manager.load_level(self.current_level)
        if not level_data:
            # Si aucun niveau n'est trouvé, on peut afficher un message et quitter
            print(f"Niveau {self.current_level} introuvable. Fin du jeu.")
            arcade.exit()
            return

        # 2. Créer les SpriteLists
        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        # 3. Parser les données du niveau pour créer les murs et le joueur
        for y, row in enumerate(level_data):
            for x, char in enumerate(row):
                # Calcule la position du carré dans le jeu
                center_x = x * TILE_SIZE + TILE_SIZE / 2
                center_y = (len(level_data) - 1 - y) * TILE_SIZE + TILE_SIZE / 2

                if char == 'X':
                    wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.DARK_GREEN)
                    wall.center_x = center_x
                    wall.center_y = center_y
                    self.walls.append(wall)
                elif char == 'P':
                    # Créer le joueur
                    self.player = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE) # Un peu plus petit pour passer les portes
                    self.player.center_x = center_x
                    self.player.center_y = center_y
                    self.player_list.append(self.player)
                elif char == 'E':
                    # Créer la sortie
                    exit_sprite = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.GOLD)
                    exit_sprite.center_x = center_x
                    exit_sprite.center_y = center_y
                    self.exit_list.append(exit_sprite)
        
        # S'assurer que le joueur a bien été créé (s'il n'y avait pas de 'P' dans le niveau)
        if not self.player:
            self.player = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE)
            self.player.center_x = 100
            self.player.center_y = 100
            self.player_list.append(self.player)


        # 4. Créer le moteur physique
        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.walls, GRAVITY)
        
        # 5. Réinitialiser l'historique pour le voyage dans le temps
        self.history = []

    def on_draw(self):
        """ Surcharge de on_draw pour dessiner les nouveaux éléments. """
        super().on_draw() # Appelle la méthode on_draw du parent (main.py)
        self.exit_list.draw() # Ajoute le dessin de la sortie

    def on_update(self, delta_time):
        """ Logique de mise à jour du jeu. """
        super().on_update(delta_time) # Appelle la méthode du parent
        
        # Vérifier si le joueur a atteint la sortie
        if arcade.check_for_collision_with_list(self.player, self.exit_list):
            print("Niveau terminé !")
            self.current_level += 1
            self.setup() # Charge le niveau suivant

# --- Code principal pour lancer le jeu ---
if __name__ == "__main__":
    window = GameWithLevels()
    window.setup()
    arcade.run()
