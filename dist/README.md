# 🧩 Sudoku Pro - Édition Spéciale

Bienvenue dans **Sudoku Pro**, un jeu de Sudoku moderne et complet développé entièrement en Python. 
Ce projet intègre une interface graphique élégante ainsi qu'une véritable Intelligence Artificielle capable de générer et de résoudre des grilles à l'infini !

## ✨ Fonctionnalités Principales

* **🎲 Rejouabilité Infinie :** Génération procédurale de nouvelles grilles à chaque partie.
* **🤖 Solveur IA Intégré :** Un algorithme de *Backtracking* capable de résoudre n'importe quelle grille en une fraction de seconde.
* **🛡️ Sécurité des Saisies :** Validation en temps réel empêchant le joueur de taper des lettres ou des caractères invalides.
* **🔍 Système de Vérification :** Un bouton pour comparer ses réponses avec le corrigé secret de l'ordinateur (Vert = Correct, Rouge = Erreur).
* **🎨 Interface Moderne :** Design sombre et épuré propulsé par `CustomTkinter`.

## 🛠️ Technologies Utilisées

* **Langage :** Python 3
* **Interface Graphique :** CustomTkinter
* **Algorithmique :** Backtracking (Récursivité), Tableaux 2D, Deep Copy
* **Déploiement :** PyInstaller (Génération d'exécutable autonome)

## 🚀 Comment y jouer ?

### Option 1 : Jouer directement (Windows)
Si vous possédez le fichier `Sudoku_Pro.exe`, double-cliquez simplement dessus pour lancer le jeu. Aucune installation n'est requise !

### Option 2 : Lancer depuis le code source
Si vous souhaitez explorer le code et lancer le jeu depuis votre terminal :

1. Clonez ce dépôt sur votre machine.
2. Créez un environnement virtuel et installez les dépendances :
   ```bash
   pip install customtkinter