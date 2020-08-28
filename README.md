# Python-WCS-Projet-1

Aventure sur l'île au Python (part 1) (Python Isle Adventure (part 1))

Version : Python 3.8.3

Objectif : une correction possible du projet 1

Lancement de l'application : 
    - idéalement via le fichier IsleAdventure.bat

Documentation (dossier Documents) :
    - Change log
    - Lien vers le Trello
    - Diagramme de flux (drawio)
    - Support de présentation PowerPoint
    - Sujet du projet (équivalent du cahier des charges)    

Fichiers Python :
    - Point d'entrée à la racine : IsleAdventure1.py
    - Dossier Program Files
        - Game.py : programme principal
        - Variables.py : variables partagées
        - Challenge1.py : code du défi 1 (Nombre mystérieux)
        - Challenge2.py : code du défi 2 (Code César)
        - Challenge3.py : code du défi 3 (Multi FizzBuzz)
        - Sous-dossier Utilities
            - Utilities.py : utilitaires divers dont :
                - GetUserInput (demande de données à l'utilisateur)
                - Lecture/écriture de fichiers text et json
            - RichConsole.py : diverses fonctions pour une expérience utilisateur enrichie sur la console dont principalement la méthode Print

Fichiers de configuration (dossier Resources) :
    - Paramètres globaux du jeu : GameData.json
    - Vues (affichage) du jeu : Views
    - Les cartes (taille maximum 100x50) : fichier par défaut Maps
    - Éléments pouvant composer une carte : MapElements.json
    - Objets pouvant être trouvés : Objects.json
    - Données des personnages (dont le joueur) : Characters.json
    - Textes du jeu : Messages-xx.json (xx est le code langue, par défaut fr)

Fichiers de sauvegarde :
    - Dossier Saves avec :
        - L'historique des parties terminées : WallOfHeroes
        - Un sous-dossier par nom de joueur avec :
            - Les cartes : Maps.json 
            - Les éléments des cartes : MapElements.json
            - Les objets : Objects.json
            - Les personnages (dont le joueur) : Characters.json