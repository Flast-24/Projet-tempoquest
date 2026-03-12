"""
Sprite Collect Coins

A simple game demonstrating an easy way to create and use sprites.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the
command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.4
COIN_COUNT = 50

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Sprite Collect Coins Example"


class GameView(arcade.View):

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Create a variable to hold the player sprite
        self.player_sprite = None

        # Variables to hold the score and the Text object displaying it
        self.score = 0
        self.score_display = None

        # Hide the mouse cursor while it's over the window
        self.window.set_mouse_visible(False)

        self.background_color = arcade.color.AMAZON

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Reset the score and the score display
        self.score = 0
        self.score_display = arcade.Text(
            text="Score: 0", x=10, y=20,
            color=arcade.color.WHITE, font_size=14)

        # Set up the player
        # Character image from kenney.nl
        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img, scale=SPRITE_SCALING_PLAYER)
        self.player_sprite.position = 50, 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 scale=SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(WINDOW_WIDTH)
            coin.center_y = random.randrange(WINDOW_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """

        # Clear the screen to only show the background color
        self.clear()

        # Draw the sprites
        self.coin_list.draw()
        self.player_list.draw()

        # Draw the score Text object on the screen
        self.score_display.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the player sprite to place its center on the mouse x, y  (40lignes restantes)
        



"ici je met le code que j'ai crée pendant les vacances"

"""
Jeu de Plateforme - Niveau 1
Bibliothèque: Python Arcade
Contrôles: Flèches directionnelles + Espace pour sauter
Objectif: Atteindre la porte avant la fin du compte à rebours (30 secondes)
"""

import arcade
import math

# === CONSTANTES DU JEU ===
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Jeu de Plateforme - Niveau 1"

# Constantes de physique
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20
PLAYER_MOVEMENT_SPEED = 5

# Couleurs
BACKGROUND_COLOR = arcade.color.LIGHT_SLATE_GRAY
PLATFORM_COLOR = arcade.color.DARK_GRAY
PLAYER_COLOR = arcade.color.SAND_BROWN
DOOR_COLOR = arcade.color.DARK_GREEN
CLOCK_COLOR = arcade.color.BLACK

# Temps du compte à rebours
COUNTDOWN_TIME = 30


class Player(arcade.Sprite):
    """Classe pour le personnage joueur (bonhomme bâton)"""
    
    def __init__(self):
        super().__init__()
        
        # Dimensions du personnage
        self.width = 30
        self.height = 50
        self.color = PLAYER_COLOR
        
        # Position initiale (en bas à gauche)
        self.center_x = 100
        self.center_y = 100
        
        # Créer la forme visuelle
        self.texture = self._create_player_texture()
    
    def _create_player_texture(self):
        """Créer une texture simple pour le joueur"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        texture = arcade.Texture("player", shape.texture.image)
        return texture


class Platform(arcade.Sprite):
    """Classe pour les plateformes/obstacles"""
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.color = PLATFORM_COLOR
        
        # Créer la texture
        self.texture = self._create_platform_texture()
    
    def _create_platform_texture(self):
        """Créer une texture pour la plateforme"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        texture = arcade.Texture("platform", shape.texture.image)
        return texture


class Door(arcade.Sprite):
    """Classe pour la porte de sortie (objectif du niveau)"""
    
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 60
        self.height = 80
        self.color = DOOR_COLOR
        
        # Créer la texture
        self.texture = self._create_door_texture()
    
    def _create_door_texture(self):
        """Créer une texture pour la porte"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        texture = arcade.Texture("door", shape.texture.image)
        return texture


class GameView(arcade.View):
    """Vue principale du jeu"""
    
    def __init__(self):
        super().__init__()
        
        # Listes de sprites
        self.player_list = None
        self.platform_list = None
        self.door_list = None
        
        # Objets du jeu
        self.player = None
        self.door = None
        
        # Moteur de physique
        self.physics_engine = None
        
        # Compte à rebours
        self.time_left = COUNTDOWN_TIME
        
        # État du jeu
        self.game_over = False
        self.level_complete = False
        
        # Couleur de fond
        arcade.set_background_color(BACKGROUND_COLOR)
    
    def setup(self):
        """Configuration initiale du jeu"""
        
        # Initialiser les listes de sprites
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        
        # === CRÉER LE JOUEUR ===
        self.player = Player()
        self.player_list.append(self.player)
        
        # === CRÉER LES PLATEFORMES ===
        
        # Sol principal
        ground = Platform(SCREEN_WIDTH // 2, 25, SCREEN_WIDTH, 50)
        self.platform_list.append(ground)
        
        # Plateforme de départ (bas gauche)
        platform_start = Platform(150, 100, 150, 20)
        self.platform_list.append(platform_start)
        
        # Rampe montante (chemin en escalier)
        for i in range(5):
            x = 250 + i * 80
            y = 150 + i * 80
            platform = Platform(x, y, 100, 20)
            self.platform_list.append(platform)
        
        # Plateforme du milieu
        platform_middle = Platform(650, 450, 120, 20)
        self.platform_list.append(platform_middle)
        
        # Plateforme haute (sous la porte)
        platform_top = Platform(850, 650, 150, 20)
        self.platform_list.append(platform_top)
        
        # === CRÉER LA PORTE ===
        self.door = Door(850, 710)
        self.door_list.append(self.door)
        
        # === CRÉER LE MOTEUR DE PHYSIQUE ===
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platform_list,
            gravity_constant=GRAVITY
        )
        
        # Réinitialiser les variables
        self.time_left = COUNTDOWN_TIME
        self.game_over = False
        self.level_complete = False
    
    def on_draw(self):
        """Dessiner tous les éléments du jeu"""
        self.clear()
        
        # Dessiner les sprites
        self.platform_list.draw()
        self.door_list.draw()
        self.player_list.draw()
        
        # === DESSINER L'HORLOGE (compte à rebours) ===
        clock_x = 80
        clock_y = SCREEN_HEIGHT - 60
        clock_radius = 40
        
        # Cercle de l'horloge
        arcade.draw_circle_outline(clock_x, clock_y, clock_radius, CLOCK_COLOR, 3)
        arcade.draw_circle_filled(clock_x, clock_y, clock_radius - 2, arcade.color.WHITE)
        
        # Aiguille de l'horloge (rotation basée sur le temps restant)
        angle = (self.time_left / COUNTDOWN_TIME) * 360
        end_x = clock_x + 30 * math.cos(math.radians(angle - 90))
        end_y = clock_y + 30 * math.sin(math.radians(angle - 90))
        arcade.draw_line(clock_x, clock_y, end_x, end_y, arcade.color.RED, 3)
        
        # Point central de l'horloge
        arcade.draw_circle_filled(clock_x, clock_y, 4, CLOCK_COLOR)
        
        # Afficher le temps restant en texte
        time_text = f"{int(self.time_left)}s"
        arcade.draw_text(
            time_text, 
            clock_x, 
            clock_y - 55, 
            CLOCK_COLOR, 
            20, 
            anchor_x="center", 
            bold=True
        )
        
        # === MESSAGES DE FIN DE JEU ===
        
        # Message de défaite (temps écoulé)
        if self.game_over:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                400, 200, 
                arcade.color.BLACK
            )
            arcade.draw_text(
                "TEMPS ÉCOULÉ!", 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
                arcade.color.RED, 
                40, 
                anchor_x="center", 
                bold=True
            )
            arcade.draw_text(
                "Appuyez sur R pour recommencer", 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, 
                arcade.color.WHITE, 
                20, 
                anchor_x="center"
            )
        
        # Message de victoire (niveau terminé)
        if self.level_complete:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                500, 200, 
                arcade.color.DARK_GREEN
            )
            arcade.draw_text(
                "NIVEAU TERMINÉ!", 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
                arcade.color.YELLOW, 
                40, 
                anchor_x="center", 
                bold=True
            )
            arcade.draw_text(
                "Félicitations! Vous avez atteint la porte!", 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, 
                arcade.color.WHITE, 
                18, 
                anchor_x="center"
            )
            arcade.draw_text(
                "Appuyez sur R pour recommencer", 
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, 
                arcade.color.WHITE, 
                16, 
                anchor_x="center"
            )
    
    def on_update(self, delta_time):
        """Mise à jour de la logique du jeu (appelée ~60 fois par seconde)"""
        
        # Ne pas mettre à jour si le jeu est terminé
        if self.game_over or self.level_complete:
            return
        
        # Mettre à jour le compte à rebours
        self.time_left -= delta_time
        
        # Vérifier si le temps est écoulé
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            return
        
        # Mettre à jour la physique (gravité, collisions)
        self.physics_engine.update()
        
        # Vérifier si le joueur touche la porte
        door_hit = arcade.check_for_collision_with_list(self.player, self.door_list)
        if door_hit:
            self.level_complete = True
        
        # Vérifier si le joueur tombe en dehors de l'écran
        if self.player.center_y < 0:
            self.game_over = True
    
    def on_key_press(self, key, modifiers):
        """Gérer les touches pressées"""
        
        # Touche R : Recommencer le jeu
        if key == arcade.key.R:
            self.setup()
            return
        
        # Ne pas permettre de jouer si le jeu est terminé
        if self.game_over or self.level_complete:
            return
        
        # Flèche gauche : Déplacer à gauche
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        
        # Flèche droite : Déplacer à droite
        if key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        
        # Barre espace : Sauter
        if key == arcade.key.SPACE:
            # Vérifier si le joueur est sur une plateforme
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
    
    def on_key_release(self, key, modifiers):
        """Gérer les touches relâchées"""
        
        # Ne pas permettre de jouer si le jeu est terminé
        if self.game_over or self.level_complete:
            return
        
        # Arrêter le déplacement horizontal quand on relâche les flèches
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    """Fonction principale pour lancer le jeu"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()