# Présentation de TempoQuest

---

### Présentation globale du projet

- **Naissance de l'idée :** L'idée de **TempoQuest** est née d'une volonté de créer un jeu de plateforme qui ne soit pas simplement une question de sauts et de réflexes. Après avoir exploré plusieurs concepts, y compris des idées peu concluantes proposées par une IA, l'équipe a eu l'idée d'une mécanique de duplication temporelle. Ce brainstorming a permis de définir une vision unique pour le projet.

- **Problématique initiale :** Comment créer un jeu de plateforme qui incite à la réflexion plutôt qu'à la simple exécution ? Comment une mécanique temporelle peut-elle renouveler le genre ?

- **Objectifs :** L'objectif était de développer un jeu complet basé sur cette mécanique de "fantômes temporels", incluant un personnage jouable, des niveaux complexes, et un éditeur de niveaux fonctionnel pour permettre une créativité étendue.

### Organisation du travail

- **Présentation de l'équipe :**
    - Diennet Teddy
    - Benzaoui Ryad
    - Amar hidoux Raphaël

- **Rôle de chacun et chacune :** Le projet a été développé dans un esprit de collaboration où chaque membre a touché à différents aspects du développement. Cependant, pour structurer le travail, des responsabilités principales ont été esquissées :
    - **Diennet Teddy :** S'est concentré sur la conception des niveaux et les mécaniques de jeu qui y sont associées, tout en assurant le suivi régulier du projet via les comptes rendus.
    - **Benzaoui Ryad :** A pris en charge le développement du personnage principal et de la mécanique de duplication temporelle, qui est au cœur du jeu. Il a également assuré la coordination générale en tant que chef de projet.
    - **Amar hidoux Raphaël :** A géré toute la partie visuelle : création des sprites, design de l'interface utilisateur et gestion du calendrier de production.

- **Répartition des tâches et temps passé :** L'équipe a fonctionné de manière très collaborative, prenant les décisions de conception ensemble. Le développement s'est étalé sur plusieurs semaines, avec une utilisation de GitHub pour la gestion du code source.

### Étapes du projet

1.  **Brainstorming et Conception :** Phase initiale de recherche d'idées, aboutissant à la mécanique de duplication temporelle.
2.  **Développement du Moteur de Base :** Mise en place du personnage, de la physique de base et des interactions avec l'environnement en utilisant la bibliothèque Arcade.
3.  **Implémentation de la Mécanique Centrale :** Développement de la capacité à créer des "fantômes" et du retour au point de départ.
4.  **Création de l'Éditeur de Niveaux :** Un outil crucial qui permet de créer, sauvegarder, modifier, renommer et supprimer des niveaux, stockés en format JSON.
5.  **Conception des Niveaux et Assets :** Création des premiers niveaux de jeu et des sprites pour le personnage et l'environnement.
6.  **Finalisation et Débogage :** Tests, corrections de bugs et améliorations de l'expérience de jeu.

### Validation de l'opérationnalité et du fonctionnement

- **État d'avancement :** Le projet est fonctionnel. Il inclut un menu principal, un sélecteur de niveaux, un éditeur de niveaux complet et plusieurs niveaux jouables.
- **Vérification de l'absence de bugs :** Des tests manuels ont été effectués tout au long du développement, en particulier après l'ajout de nouvelles fonctionnalités comme la gestion des fichiers de niveaux.
- **Difficultés rencontrées et solutions apportées :**
    - **Prise en main de la bibliothèque Arcade :** C'était la première fois que l'équipe utilisait Arcade. Un temps d'adaptation a été nécessaire pour en comprendre le fonctionnement, notamment pour la gestion des "Views" et de la physique.
    - **Développement de l'éditeur de niveaux :** La création d'une interface complète pour l'éditeur (sauvegarde, chargement, modification des noms) a représenté un défi de conception et de logique de programmation non négligeable.
- **Utilisation de l'intelligence artificiel** : Oui, l'intelligence artificielle a été un outil d'assistance tout au long de ce projet, intervenant à la fois sur des aspects de conception et sur des points techniques spécifiques.

- **Conception de la Mécanique de Jeu :** Au départ, plusieurs idées de gameplay ont été explorées. L'IA a été utilisée comme un partenaire de brainstorming pour affiner le concept de "fantôme temporel". C'est cette collaboration qui a mené à la mécanique centrale du jeu : la capacité du joueur à laisser derrière lui un bloc solide (un "fantôme") pour s'en servir comme plateforme, transformant ainsi la résolution des niveaux en un puzzle de création.

- **Optimisation des Contrôles du Joueur :** Pour la base du jeu, notamment le système de personnage qui bouge, nous avons utilisé l'IA pour nous aider à ajuster et à équilibrer les paramètres du moteur physique (gravité, vitesse de déplacement, force du saut). L'objectif était d'obtenir des contrôles qui soient à la fois réactifs, précis et agréables pour le joueur.

- **Structure de l'Éditeur de Niveaux et des Données :** L'IA a fourni une aide précieuse dans la conception de l'éditeur de niveaux. Elle a assisté à la structuration du format de sauvegarde en JSON, en s'assurant que celui-ci soit à la fois simple à lire et capable de stocker toutes les informations nécessaires (positions des murs, points de départ/arrivée, nombre de fantômes autorisés).

- **Logique de la Boucle de Jeu :** L'IA a été consultée pour l'écriture de la structure de base de la boucle de jeu principale, y compris la gestion des différents états (jeu en cours, écran de victoire) et la mise en place de la logique de détection de collision, notamment avec le bloc de fin qui valide la réussite d'un niveau.

### Ouverture

- **Idées d'amélioration :**
    - **Amélioration de l'interface :** L'interface utilisateur pourrait être rendue "responsive" pour s'adapter correctement à toutes les résolutions d'écran et échelles d'affichage, car elle est actuellement optimisée pour une configuration 1080p à 100%.
    - **Nouvelles mécaniques de jeu :** Ajouter des éléments comme des murs traversables, des interrupteurs, ou des ennemis pour enrichir le gameplay.
    - **Améliorer l'utilisation de Git/GitHub :** L'équipe a noté que pour un futur projet, une utilisation plus structurée de Git (branches, pull requests) serait bénéfique.

- **Analyse critique :** Ce projet a été une excellente opportunité d'apprendre à utiliser une nouvelle bibliothèque graphique, de concevoir une mécanique de jeu originale et de gérer un projet de A à Z. La principale leçon est l'importance d'une planification plus rigoureuse et d'une meilleure utilisation des outils collaboratifs comme Git.

- **Démarche d'inclusion :** L'accessibilité n'a pas été une priorité pour cette première version en raison de la complexité et du temps limité. Des améliorations comme la possibilité de reconfigurer les touches ou d'ajouter des modes d'affichage pour les daltoniens seraient des pistes intéressantes pour le futur.
