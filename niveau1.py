"""
Jeu de Plateforme - Version Améliorée avec Clonage
Bibliothèque: Python Arcade
Contrôles: 
- Flèches/A/D : Déplacement
- Espace : Sauter
- C : Créer un clone à l'emplacement actuel (le personnage revient au début)
- R : Recommencer le niveau
Objectif: Atteindre la porte avant la fin du compte à rebours
"""

import arcade
import math
import random
from typing import Optional, List

# === CONSTANTES DU JEU ===
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Jeu de Plateforme - Aventure avec Clones"

# Constantes de physique
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 18
PLAYER_MOVEMENT_SPEED = 5
PLAYER_MAX_HEALTH = 3

# Propriétés des plateformes
PLATFORM_EDGE_WIDTH = 5

# Couleurs
BACKGROUND_COLOR = arcade.color.LIGHT_STEEL_BLUE
PLATFORM_COLOR = arcade.color.DARK_BROWN
PLATFORM_EDGE_COLOR = arcade.color.DARK_SLATE_GRAY
PLAYER_COLOR = arcade.color.ORANGE_PEEL
PLAYER_CLONE_COLOR = arcade.color.LIGHT_BLUE
DOOR_COLOR = arcade.color.FOREST_GREEN
DOOR_FRAME_COLOR = arcade.color.GOLD
COIN_COLOR = arcade.color.GOLD
ENEMY_COLOR = arcade.color.RED
HEART_COLOR = arcade.color.RED
HEART_EMPTY_COLOR = arcade.color.GRAY

# Temps du compte à rebours
COUNTDOWN_TIME = 45


class Player(arcade.Sprite):
    """Classe pour le personnage joueur avec animation"""
    
    def __init__(self, x=100, y=100, is_clone=False):
        super().__init__()
        
        # Dimensions du personnage
        self.width = 30
        self.height = 50
        self.color = PLAYER_CLONE_COLOR if is_clone else PLAYER_COLOR
        
        # Position
        self.center_x = x
        self.center_y = y
        
        # État du joueur
        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.is_clone = is_clone
        
        # Créer la texture
        self.texture = self._create_player_texture()
        
        # Pour l'animation
        self.jump_offset = 0
        
    def _create_player_texture(self):
        """Créer une texture pour le joueur"""
        # Créer une surface pour dessiner
        image = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        
        # Ajouter un symbole C sur les clones
        if self.is_clone:
            arcade.draw_text(
                "C",
                self.width // 2, self.height // 2 - 8,
                arcade.color.BLACK,
                16,
                anchor_x="center"
            )
        
        return arcade.Texture("player", image.texture.image)
    
    def update_animation(self, delta_time: float = 1/60):
        """Mettre à jour l'animation du joueur"""
        if self.is_invulnerable:
            self.invulnerable_timer -= delta_time
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False
        
        # Effet de rebond lors de la marche
        if abs(self.change_x) > 0.1:
            self.jump_offset = abs(math.sin(self.center_x * 0.1)) * 2
        else:
            self.jump_offset = 0


class Platform(arcade.Sprite):
    """Classe pour les plateformes avec bordures"""
    
    def __init__(self, x, y, width, height, color=PLATFORM_COLOR, has_edges=True):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.color = color
        self.has_edges = has_edges
        
        # Créer la texture
        self.texture = self._create_platform_texture()
    
    def _create_platform_texture(self):
        """Créer une texture avec bordures"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        
        # Ajouter des bordures
        if self.has_edges:
            arcade.draw_rectangle_filled(
                self.width // 2, self.height - PLATFORM_EDGE_WIDTH // 2,
                self.width, PLATFORM_EDGE_WIDTH,
                PLATFORM_EDGE_COLOR
            )
        
        return arcade.Texture("platform", shape.texture.image)


class Door(arcade.Sprite):
    """Classe pour la porte de sortie"""
    
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 70
        self.height = 90
        self.color = DOOR_COLOR
        self.frame_color = DOOR_FRAME_COLOR
        self.pulse = 0
        
        self.texture = self._create_door_texture()
    
    def _create_door_texture(self):
        """Créer une texture pour la porte"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        
        # Cadre
        arcade.draw_rectangle_outline(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.frame_color, 3
        )
        
        # Poignée
        arcade.draw_circle_filled(
            self.width - 15, self.height // 2,
            5, self.frame_color
        )
        
        return arcade.Texture("door", shape.texture.image)
    
    def update_animation(self, delta_time):
        """Animation de la porte"""
        self.pulse += delta_time * 2
        pulse_scale = 1 + math.sin(self.pulse) * 0.02
        self.scale = pulse_scale


class Coin(arcade.Sprite):
    """Classe pour les pièces"""
    
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 20
        self.height = 20
        self.color = COIN_COLOR
        self.rotation_speed = 5
        
        self.texture = self._create_coin_texture()
    
    def _create_coin_texture(self):
        """Créer une texture pour la pièce"""
        shape = arcade.create_ellipse_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        
        arcade.draw_text(
            "$",
            self.width // 2, self.height // 2 - 8,
            arcade.color.BLACK,
            16,
            anchor_x="center"
        )
        
        return arcade.Texture("coin", shape.texture.image)
    
    def update_animation(self, delta_time):
        """Faire tourner la pièce"""
        self.angle += self.rotation_speed


class Enemy(arcade.Sprite):
    """Classe pour les ennemis mobiles"""
    
    def __init__(self, x, y, move_range=100):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 30
        self.height = 30
        self.color = ENEMY_COLOR
        
        # Mouvement
        self.start_x = x
        self.move_range = move_range
        self.move_speed = 2
        self.direction = 1
        
        self.texture = self._create_enemy_texture()
    
    def _create_enemy_texture(self):
        """Créer une texture pour l'ennemi"""
        shape = arcade.create_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            self.color
        )
        
        # Yeux
        arcade.draw_circle_filled(
            self.width // 3, self.height * 0.6,
            4, arcade.color.WHITE
        )
        arcade.draw_circle_filled(
            self.width * 2 // 3, self.height * 0.6,
            4, arcade.color.WHITE
        )
        
        return arcade.Texture("enemy", shape.texture.image)
    
    def update(self):
        """Mettre à jour le mouvement"""
        self.center_x += self.move_speed * self.direction
        
        if abs(self.center_x - self.start_x) > self.move_range:
            self.direction *= -1


class GameView(arcade.View):
    """Vue principale du jeu"""
    
    def __init__(self):
        super().__init__()
        
        # Listes de sprites
        self.player_list: Optional[arcade.SpriteList] = None
        self.clone_list: Optional[arcade.SpriteList] = None
        self.platform_list: Optional[arcade.SpriteList] = None
        self.door_list: Optional[arcade.SpriteList] = None
        self.coin_list: Optional[arcade.SpriteList] = None
        self.enemy_list: Optional[arcade.SpriteList] = None
        
        # Objets du jeu
        self.player: Optional[Player] = None
        self.door: Optional[Door] = None
        self.clones: List[Player] = []
        
        # Moteur de physique
        self.physics_engine: Optional[arcade.PhysicsEnginePlatformer] = None
        
        # Variables de jeu
        self.time_left = COUNTDOWN_TIME
        self.game_over = False
        self.level_complete = False
        
        # Caméra
        self.camera = None
        
        # Couleur de fond
        arcade.set_background_color(BACKGROUND_COLOR)
    
    def setup(self):
        """Configuration initiale du jeu"""
        
        # Initialiser les listes de sprites
        self.player_list = arcade.SpriteList()
        self.clone_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        # Liste des clones
        self.clones = []
        
        # Initialiser la caméra
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # === CRÉER LE JOUEUR ===
        self.player = Player(100, 100, is_clone=False)
        self.player_list.append(self.player)
        
        # === CRÉER LES PLATEFORMES ===
        self._create_platforms()
        
        # === CRÉER LA PORTE ===
        self.door = Door(850, 710)
        self.door_list.append(self.door)
        
        # === CRÉER LES PIÈCES ===
        self._create_coins()
        
        # === CRÉER LES ENNEMIS ===
        self._create_enemies()
        
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
    
    def _create_platforms(self):
        """Créer toutes les plateformes"""
        
        # Sol principal
        ground = Platform(
            SCREEN_WIDTH // 2, 25,
            SCREEN_WIDTH, 50,
            color=arcade.color.DARK_GREEN
        )
        self.platform_list.append(ground)
        
        # Plateforme de départ
        start_platform = Platform(150, 100, 150, 20)
        self.platform_list.append(start_platform)
        
        # Chemin en escalier
        for i in range(5):
            x = 250 + i * 80
            y = 150 + i * 80
            platform = Platform(x, y, 100, 20)
            self.platform_list.append(platform)
        
        # Plateforme du milieu
        middle_platform = Platform(650, 450, 120, 20)
        self.platform_list.append(middle_platform)
        
        # Plateforme haute
        top_platform = Platform(850, 650, 150, 20)
        self.platform_list.append(top_platform)
        
        # Plateformes supplémentaires
        challenge_platform = Platform(400, 300, 80, 20)
        self.platform_list.append(challenge_platform)
        
        coin_platform = Platform(500, 450, 200, 20)
        self.platform_list.append(coin_platform)
    
    def _create_coins(self):
        """Créer les pièces"""
        coin_positions = [
            (300, 250),
            (400, 350),
            (550, 500),
            (700, 500),
            (800, 700),
            (200, 400),
        ]
        
        for x, y in coin_positions:
            coin = Coin(x, y)
            self.coin_list.append(coin)
    
    def _create_enemies(self):
        """Créer les ennemis"""
        enemy1 = Enemy(650, 470, move_range=100)
        self.enemy_list.append(enemy1)
        
        enemy2 = Enemy(400, 180, move_range=150)
        self.enemy_list.append(enemy2)
    
    def on_draw(self):
        """Dessiner tous les éléments du jeu"""
        self.clear()
        
        # Appliquer la caméra
        self.camera.use()
        
        # Dessiner les sprites
        self.platform_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.door_list.draw()
        self.clone_list.draw()  # Dessiner les clones d'abord
        self.player_list.draw()  # Dessiner le joueur par-dessus
        
        # Réinitialiser la caméra pour l'interface
        self.camera.use(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # === INTERFACE UTILISATEUR ===
        self._draw_ui()
        
        # === MESSAGES DE FIN DE JEU ===
        self._draw_game_over_messages()
        
        # === INSTRUCTIONS ===
        self._draw_instructions()
    
    def _draw_ui(self):
        """Dessiner l'interface utilisateur"""
        
        # Horloge
        clock_x = 80
        clock_y = SCREEN_HEIGHT - 60
        clock_radius = 40
        
        arcade.draw_circle_outline(clock_x, clock_y, clock_radius, arcade.color.BLACK, 3)
        arcade.draw_circle_filled(clock_x, clock_y, clock_radius - 2, arcade.color.WHITE)
        
        # Aiguille
        angle = (self.time_left / COUNTDOWN_TIME) * 360
        end_x = clock_x + 30 * math.cos(math.radians(angle - 90))
        end_y = clock_y + 30 * math.sin(math.radians(angle - 90))
        
        if self.time_left < 10:
            hand_color = arcade.color.RED
        elif self.time_left < 20:
            hand_color = arcade.color.ORANGE
        else:
            hand_color = arcade.color.GREEN
        
        arcade.draw_line(clock_x, clock_y, end_x, end_y, hand_color, 3)
        arcade.draw_circle_filled(clock_x, clock_y, 4, arcade.color.BLACK)
        
        # Texte du temps
        time_text = f"{int(self.time_left)}s"
        arcade.draw_text(
            time_text, clock_x, clock_y - 55,
            arcade.color.BLACK, 20,
            anchor_x="center", bold=True
        )
        
        # Score
        score_text = f"Score: {self.player.score}"
        arcade.draw_text(
            score_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50,
            arcade.color.BLACK, 20,
            bold=True
        )
        
        # Vies
        heart_x = 200
        heart_y = SCREEN_HEIGHT - 50
        
        for i in range(PLAYER_MAX_HEALTH):
            if i < self.player.health:
                arcade.draw_text("❤", heart_x + i * 30, heart_y,
                               HEART_COLOR, 24, font_name="Arial")
            else:
                arcade.draw_text("❤", heart_x + i * 30, heart_y,
                               HEART_EMPTY_COLOR, 24, font_name="Arial")
        
        # Nombre de clones
        clone_text = f"Clones: {len(self.clones)}"
        arcade.draw_text(
            clone_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80,
            arcade.color.BLUE, 16,
            bold=True
        )
    
    def _draw_instructions(self):
        """Dessiner les instructions"""
        instructions = [
            "Flèches/A/D: Déplacement",
            "Espace: Sauter",
            "C: Créer un clone (retour au début)",
            "R: Recommencer"
        ]
        
        y_offset = 30
        for instruction in instructions:
            arcade.draw_text(
                instruction,
                10, y_offset,
                arcade.color.BLACK,
                14,
                anchor_x="left"
            )
            y_offset += 20
    
    def _draw_game_over_messages(self):
        """Dessiner les messages de fin de jeu"""
        
        if self.game_over:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                400, 200,
                arcade.color.BLACK
            )
            
            message = "TEMPS ÉCOULÉ!" if self.time_left <= 0 else "PERDU!"
            arcade.draw_text(
                message,
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
                arcade.color.RED, 40,
                anchor_x="center", bold=True
            )
            
            arcade.draw_text(
                "Appuyez sur R pour recommencer",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                arcade.color.WHITE, 20,
                anchor_x="center"
            )
        
        if self.level_complete:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                500, 250,
                arcade.color.DARK_GREEN
            )
            
            arcade.draw_text(
                "VICTOIRE!",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60,
                arcade.color.GOLD, 48,
                anchor_x="center", bold=True
            )
            
            arcade.draw_text(
                f"Score final: {self.player.score}",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                arcade.color.WHITE, 24,
                anchor_x="center"
            )
            
            arcade.draw_text(
                f"Temps restant: {int(self.time_left)}s",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10,
                arcade.color.WHITE, 24,
                anchor_x="center"
            )
            
            arcade.draw_text(
                f"Clones utilisés: {len(self.clones)}",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40,
                arcade.color.WHITE, 18,
                anchor_x="center"
            )
            
            arcade.draw_text(
                "Appuyez sur R pour rejouer",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70,
                arcade.color.WHITE, 18,
                anchor_x="center"
            )
    
    def on_update(self, delta_time):
        """Mise à jour de la logique du jeu"""
        
        if self.game_over or self.level_complete:
            return
        
        # Mettre à jour le compte à rebours (ne bouge pas pour les clones)
        self.time_left -= delta_time
        
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            return
        
        # Mettre à jour la physique du joueur seulement
        self.physics_engine.update()
        
        # Les clones restent immobiles (pas de mise à jour physique)
        
        # Mettre à jour les animations
        self.player.update_animation(delta_time)
        for clone in self.clones:
            clone.update_animation(delta_time)
        
        if self.door:
            self.door.update_animation(delta_time)
        for coin in self.coin_list:
            coin.update_animation(delta_time)
        
        # Mettre à jour les ennemis
        self.enemy_list.update()
        
        # Vérifier les collisions
        self._check_collisions()
        
        # Mettre à jour la caméra
        self._update_camera()
        
        # Vérifier si le joueur tombe
        if self.player.center_y < -100:
            self._player_hit()
    
    def _update_camera(self):
        """Mettre à jour la caméra pour suivre le joueur"""
        screen_center_x = self.player.center_x - (SCREEN_WIDTH // 2)
        screen_center_y = self.player.center_y - (SCREEN_HEIGHT // 2)
        
        screen_center_x = max(0, min(screen_center_x, SCREEN_WIDTH * 2 - SCREEN_WIDTH))
        screen_center_y = max(0, min(screen_center_y, SCREEN_HEIGHT * 2 - SCREEN_HEIGHT))
        
        self.camera.move_to((screen_center_x, screen_center_y))
    
    def _check_collisions(self):
        """Vérifier toutes les collisions"""
        
        # Collision du joueur avec la porte
        door_hit = arcade.check_for_collision_with_list(self.player, self.door_list)
        if door_hit:
            self.level_complete = True
            self.player.score += int(self.time_left * 10)
        
        # Collision du joueur avec les pièces
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.player.score += 10
        
        # Collision du joueur avec les ennemis
        if not self.player.is_invulnerable:
            enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
            if enemies_hit:
                self._player_hit()
        
        # Vérifier si les clones peuvent aider (optionnel)
        for clone in self.clones:
            # Les clones peuvent aussi collecter des pièces
            coins_hit = arcade.check_for_collision_with_list(clone, self.coin_list)
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.player.score += 5  # Moins de points pour les clones
    
    def _player_hit(self):
        """Gérer quand le joueur est touché"""
        self.player.health -= 1
        self.player.is_invulnerable = True
        self.player.invulnerable_timer = 2.0
        
        if self.player.health > 0:
            # Retour à la position de départ
            self.player.center_x = 100
            self.player.center_y = 100
            self.player.change_x = 0
            self.player.change_y = 0
        else:
            self.game_over = True
    
    def _create_clone(self):
        """Créer un clone à la position actuelle du joueur"""
        if self.game_over or self.level_complete:
            return
        
        # Créer un clone à la position actuelle
        clone = Player(
            x=self.player.center_x,
            y=self.player.center_y,
            is_clone=True
        )
        
        # Le clone reste immobile
        clone.change_x = 0
        clone.change_y = 0
        
        # Ajouter le clone aux listes
        self.clones.append(clone)
        self.clone_list.append(clone)
        
        # Remettre le joueur au début
        self.player.center_x = 100
        self.player.center_y = 100
        self.player.change_x = 0
        self.player.change_y = 0
    
    def on_key_press(self, key, modifiers):
        """Gérer les touches pressées"""
        
        # Touche R : Recommencer
        if key == arcade.key.R:
            self.setup()
            return
        
        # Touche C : Créer un clone
        if key == arcade.key.C:
            self._create_clone()
            return
        
        if self.game_over or self.level_complete:
            return
        
        # Déplacement
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        
        # Saut
        if key == arcade.key.SPACE or key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
    
    def on_key_release(self, key, modifiers):
        """Gérer les touches relâchées"""
        
        if self.game_over or self.level_complete:
            return
        
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or \
           key == arcade.key.A or key == arcade.key.D:
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