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

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeu de Plateforme - Niveau 1</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
        }
        
        #gameContainer {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3);
            padding: 20px;
        }
        
        canvas {
            display: block;
            border: 3px solid #333;
            border-radius: 5px;
            background: #8B9BB3;
        }
        
        #instructions {
            margin-top: 15px;
            text-align: center;
            color: #333;
        }
        
        #instructions h2 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        #instructions p {
            margin: 5px 0;
            font-size: 14px;
        }
        
        .key {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-weight: bold;
            margin: 0 2px;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="1024" height="768"></canvas>
        <div id="instructions">
            <h2>🎮 Contrôles</h2>
            <p><span class="key">←</span> <span class="key">→</span> Déplacer | <span class="key">ESPACE</span> Sauter | <span class="key">R</span> Recommencer</p>
            <p>⏰ Atteignez la porte verte avant la fin du compte à rebours (30s) !</p>
        </div>
    </div>

    <script>
        // Récupérer le canvas et le contexte
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Constantes du jeu
        const SCREEN_WIDTH = 1024;
        const SCREEN_HEIGHT = 768;
        const GRAVITY = 0.8;
        const PLAYER_JUMP_SPEED = -15;
        const PLAYER_MOVEMENT_SPEED = 5;
        const COUNTDOWN_TIME = 30;
        
        // État du jeu
        let gameState = {
            player: null,
            platforms: [],
            door: null,
            timeLeft: COUNTDOWN_TIME,
            gameOver: false,
            levelComplete: false,
            keys: {
                left: false,
                right: false,
                space: false
            }
        };
        
        // Classe Joueur
        class Player {
            constructor() {
                this.x = 100;
                this.y = 100;
                this.width = 30;
                this.height = 50;
                this.velocityX = 0;
                this.velocityY = 0;
                this.onGround = false;
                this.color = '#D2B48C';
            }
            
            update() {
                // Appliquer la gravité
                this.velocityY += GRAVITY;
                
                // Déplacement horizontal
                if (gameState.keys.left) {
                    this.velocityX = -PLAYER_MOVEMENT_SPEED;
                } else if (gameState.keys.right) {
                    this.velocityX = PLAYER_MOVEMENT_SPEED;
                } else {
                    this.velocityX = 0;
                }
                
                // Mettre à jour la position
                this.x += this.velocityX;
                this.y += this.velocityY;
                
                // Vérifier les collisions avec les plateformes
                this.onGround = false;
                for (let platform of gameState.platforms) {
                    if (this.checkCollision(platform)) {
                        // Collision par le dessus
                        if (this.velocityY > 0 && this.y + this.height - this.velocityY <= platform.y) {
                            this.y = platform.y - this.height;
                            this.velocityY = 0;
                            this.onGround = true;
                        }
                        // Collision par le dessous
                        else if (this.velocityY < 0 && this.y - this.velocityY >= platform.y + platform.height) {
                            this.y = platform.y + platform.height;
                            this.velocityY = 0;
                        }
                        // Collision latérale gauche
                        else if (this.velocityX > 0) {
                            this.x = platform.x - this.width;
                        }
                        // Collision latérale droite
                        else if (this.velocityX < 0) {
                            this.x = platform.x + platform.width;
                        }
                    }
                }
                
                // Limiter aux bords de l'écran
                if (this.x < 0) this.x = 0;
                if (this.x + this.width > SCREEN_WIDTH) this.x = SCREEN_WIDTH - this.width;
            }
            
            checkCollision(rect) {
                return this.x < rect.x + rect.width &&
                       this.x + this.width > rect.x &&
                       this.y < rect.y + rect.height &&
                       this.y + this.height > rect.y;
            }
            
            jump() {
                if (this.onGround) {
                    this.velocityY = PLAYER_JUMP_SPEED;
                    this.onGround = false;
                }
            }
            
            draw() {
                // Corps
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // Contour
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 2;
                ctx.strokeRect(this.x, this.y, this.width, this.height);
                
                // Tête (cercle)
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x + this.width/2, this.y - 10, 10, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                
                // Yeux
                ctx.fillStyle = '#000';
                ctx.beginPath();
                ctx.arc(this.x + this.width/2 - 4, this.y - 12, 2, 0, Math.PI * 2);
                ctx.arc(this.x + this.width/2 + 4, this.y - 12, 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        // Classe Plateforme
        class Platform {
            constructor(x, y, width, height) {
                this.x = x;
                this.y = y;
                this.width = width;
                this.height = height;
                this.color = '#4A4A4A';
            }
            
            draw() {
                // Plateforme
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // Bordure supérieure claire
                ctx.fillStyle = '#6A6A6A';
                ctx.fillRect(this.x, this.y, this.width, 3);
                
                // Contour
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 2;
                ctx.strokeRect(this.x, this.y, this.width, this.height);
            }
        }
        
        // Classe Porte
        class Door {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.width = 60;
                this.height = 80;
                this.color = '#228B22';
            }
            
            draw() {
                // Porte
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // Contour
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 3;
                ctx.strokeRect(this.x, this.y, this.width, this.height);
                
                // Poignée
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.arc(this.x + this.width - 15, this.y + this.height/2, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                
                // Détails (planches)
                ctx.strokeStyle = '#1a6b1a';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(this.x + this.width/2, this.y);
                ctx.lineTo(this.x + this.width/2, this.y + this.height);
                ctx.stroke();
            }
            
            checkCollision(player) {
                return player.x < this.x + this.width &&
                       player.x + player.width > this.x &&
                       player.y < this.y + this.height &&
                       player.y + player.height > this.y;
            }
        }
        
        // Fonction d'initialisation
        function setupGame() {
            // Créer le joueur
            gameState.player = new Player();
            
            // Créer les plateformes
            gameState.platforms = [];
            
            // Sol
            gameState.platforms.push(new Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50));
            
            // Plateforme de départ (bas gauche)
            gameState.platforms.push(new Platform(50, SCREEN_HEIGHT - 150, 150, 20));
            
            // Rampe montante (plusieurs plateformes)
            for (let i = 0; i < 5; i++) {
                let x = 250 + i * 80;
                let y = SCREEN_HEIGHT - 250 - i * 80;
                gameState.platforms.push(new Platform(x, y, 100, 20));
            }
            
            // Plateforme du milieu
            gameState.platforms.push(new Platform(650, SCREEN_HEIGHT - 450, 120, 20));
            
            // Plateforme haute (sous la porte)
            gameState.platforms.push(new Platform(800, SCREEN_HEIGHT - 650, 150, 20));
            
            // Créer la porte
            gameState.door = new Door(820, SCREEN_HEIGHT - 730);
            
            // Réinitialiser les variables
            gameState.timeLeft = COUNTDOWN_TIME;
            gameState.gameOver = false;
            gameState.levelComplete = false;
        }
        
        // Dessiner l'horloge
        function drawClock() {
            const clockX = 80;
            const clockY = 60;
            const radius = 40;
            
            // Cercle de l'horloge
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(clockX, clockY, radius, 0, Math.PI * 2);
            ctx.fillStyle = '#FFF';
            ctx.fill();
            ctx.stroke();
            
            // Aiguille (rotation basée sur le temps restant)
            const angle = (gameState.timeLeft / COUNTDOWN_TIME) * Math.PI * 2 - Math.PI / 2;
            const endX = clockX + 30 * Math.cos(angle);
            const endY = clockY + 30 * Math.sin(angle);
            
            ctx.strokeStyle = '#FF0000';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(clockX, clockY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
            
            // Point central
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(clockX, clockY, 4, 0, Math.PI * 2);
            ctx.fill();
            
            // Texte du temps
            ctx.fillStyle = '#000';
            ctx.font = 'bold 20px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(Math.ceil(gameState.timeLeft) + 's', clockX, clockY + 60);
        }
        
        // Fonction de rendu
        function draw() {
            // Effacer l'écran
            ctx.fillStyle = '#8B9BB3';
            ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
            
            // Dessiner les plateformes
            for (let platform of gameState.platforms) {
                platform.draw();
            }
            
            // Dessiner la porte
            gameState.door.draw();
            
            // Dessiner le joueur
            gameState.player.draw();
            
            // Dessiner l'horloge
            drawClock();
            
            // Messages de fin
            if (gameState.gameOver) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 - 100, 400, 200);
                
                ctx.fillStyle = '#FF0000';
                ctx.font = 'bold 40px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('TEMPS ÉCOULÉ!', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20);
                
                ctx.fillStyle = '#FFF';
                ctx.font = '20px Arial';
                ctx.fillText('Appuyez sur R pour recommencer', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30);
            }
            
            if (gameState.levelComplete) {
                ctx.fillStyle = 'rgba(34, 139, 34, 0.9)';
                ctx.fillRect(SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 - 100, 500, 200);
                
                ctx.fillStyle = '#FFFF00';
                ctx.font = 'bold 40px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('NIVEAU TERMINÉ!', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30);
                
                ctx.fillStyle = '#FFF';
                ctx.font = '18px Arial';
                ctx.fillText('Félicitations! Vous avez atteint la porte!', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10);
                ctx.font = '16px Arial';
                ctx.fillText('Appuyez sur R pour recommencer', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50);
            }
        }
        
        // Boucle de jeu
        let lastTime = 0;
        function gameLoop(currentTime) {
            const deltaTime = (currentTime - lastTime) / 1000;
            lastTime = currentTime;
            
            if (!gameState.gameOver && !gameState.levelComplete) {
                // Mettre à jour le compte à rebours
                gameState.timeLeft -= deltaTime;
                
                // Vérifier si le temps est écoulé
                if (gameState.timeLeft <= 0) {
                    gameState.timeLeft = 0;
                    gameState.gameOver = true;
                }
                
                // Mettre à jour le joueur
                gameState.player.update();
                
                // Vérifier si le joueur touche la porte
                if (gameState.door.checkCollision(gameState.player)) {
                    gameState.levelComplete = true;
                }
                
                // Vérifier si le joueur tombe
                if (gameState.player.y > SCREEN_HEIGHT) {
                    gameState.gameOver = true;
                }
            }
            
            // Dessiner
            draw();
            
            // Continuer la boucle
            requestAnimationFrame(gameLoop);
        }
        
        // Gestion des touches
        document.addEventListener('keydown', (e) => {
            if (e.code === 'KeyR') {
                setupGame();
                return;
            }
            
            if (gameState.gameOver || gameState.levelComplete) return;
            
            if (e.code === 'ArrowLeft') {
                gameState.keys.left = true;
            }
            if (e.code === 'ArrowRight') {
                gameState.keys.right = true;
            }
            if (e.code === 'Space') {
                e.preventDefault();
                gameState.player.jump();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            if (e.code === 'ArrowLeft') {
                gameState.keys.left = false;
            }
            if (e.code === 'ArrowRight') {
                gameState.keys.right = false;
            }
        });
        
        // Démarrer le jeu
        setupGame();
        requestAnimationFrame(gameLoop);
    </script>
</body>
</html>