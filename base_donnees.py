# Fichier : base_donnees.py
import sqlite3 # L'outil intégré à Python pour gérer les bases de données

def connecter_bdd():
    # Cette ligne crée un fichier 'scores.db' s'il n'existe pas, ou l'ouvre s'il existe déjà
    connexion = sqlite3.connect("scores.db")
    return connexion

def initialiser_bdd():
    # 1. On ouvre la connexion
    connexion = connecter_bdd()
    curseur = connexion.cursor() # Le curseur, c'est le stylo qui va écrire dans la base
    
    # 2. On écrit notre première requête SQL (Créer la table 'leaderboard' si elle n'existe pas)
    # Elle aura 3 infos : un ID unique, le pseudo (texte), et le temps (nombre entier)
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            temps_secondes INTEGER NOT NULL
        )
    """)
    
    # 3. On sauvegarde et on ferme
    connexion.commit()
    connexion.close()

def sauvegarder_score(pseudo, temps_secondes):
    connexion = connecter_bdd()
    curseur = connexion.cursor()
    
    # On insère une nouvelle ligne dans notre tableau
    curseur.execute("INSERT INTO leaderboard (pseudo, temps_secondes) VALUES (?, ?)", (pseudo, temps_secondes))
    
    connexion.commit()
    connexion.close()

def obtenir_top_5():
    connexion = connecter_bdd()
    curseur = connexion.cursor()
    
    # On demande à la base de données de nous donner les 5 meilleurs temps (triés du plus petit au plus grand)
    curseur.execute("SELECT pseudo, temps_secondes FROM leaderboard ORDER BY temps_secondes ASC LIMIT 5")
    resultats = curseur.fetchall() # On récupère toutes les lignes
    
    connexion.close()
    return resultats # On renvoie la liste à l'interface

# Quand on lance ce fichier pour la toute première fois, on initialise la base !
initialiser_bdd()