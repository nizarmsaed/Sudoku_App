# Fichier : moteur_sudoku.py
# Fichier : moteur_sudoku.py
import random # Outil mathématique pour le hasard

# --- 1. LES RÈGLES DU JEU (Inchangées) ---
def est_valide(grille, ligne, colonne, chiffre):
    for i in range(9):
        if grille[ligne][i] == chiffre: return False
    for i in range(9):
        if grille[i][colonne] == chiffre: return False
    debut_ligne = (ligne // 3) * 3
    debut_colonne = (colonne // 3) * 3
    for i in range(3):
        for j in range(3):
            if grille[debut_ligne + i][debut_colonne + j] == chiffre: return False
    return True

def trouver_case_vide(grille):
    for ligne in range(9):
        for colonne in range(9):
            if grille[ligne][colonne] == 0:
                return (ligne, colonne)
    return None

# --- 2. NOTRE IA CLASSIQUE (Pour le bouton Résoudre) ---
def resoudre_sudoku(grille):
    case_vide = trouver_case_vide(grille)
    if not case_vide: return True 
    ligne, colonne = case_vide

    for chiffre in range(1, 10):
        if est_valide(grille, ligne, colonne, chiffre):
            grille[ligne][colonne] = chiffre
            if resoudre_sudoku(grille): return True
            grille[ligne][colonne] = 0
    return False

# --- NOUVEAU : 3. LE GÉNÉRATEUR DE PARTIES ---
def remplir_grille_aleatoirement(grille):
    case_vide = trouver_case_vide(grille)
    if not case_vide: return True
    ligne, colonne = case_vide

    # L'astuce est ici : on crée une liste de 1 à 9, et on la mélange !
    chiffres = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(chiffres) 

    for chiffre in chiffres:
        if est_valide(grille, ligne, colonne, chiffre):
            grille[ligne][colonne] = chiffre
            if remplir_grille_aleatoirement(grille): return True
            grille[ligne][colonne] = 0
    return False

# NOUVELLE VERSION (Ce qu'il faut mettre)
def generer_nouvelle_partie(nb_trous): # <-- On a ajouté nb_trous ici
    nouvelle_grille = [[0 for _ in range(9)] for _ in range(9)]
    remplir_grille_aleatoirement(nouvelle_grille)
    
    trous_a_faire = nb_trous # <-- On dit que trous_a_faire est égal à nb_trous
    while trous_a_faire > 0:
        l = random.randint(0, 8) 
        c = random.randint(0, 8) 
        if nouvelle_grille[l][c] != 0:
            nouvelle_grille[l][c] = 0 
            trous_a_faire -= 1
            
    return nouvelle_grille

