# Fichier : interface.py
import customtkinter as ctk
import copy # --- NOUVEAU 1 : L'outil pour cloner notre grille ---

from moteur_sudoku import resoudre_sudoku, generer_nouvelle_partie

# --- CONFIGURATION DU DESIGN ---
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

app = ctk.CTk() 
app.geometry("650x800") # Un peu plus large pour nos 3 boutons
app.title("Sudoku Pro - Édition Spéciale") 
app.iconbitmap("icone.ico")

titre = ctk.CTkLabel(app, text="Sudoku", font=("Arial", 28, "bold"))
titre.pack(pady=20) 

# --- LE VIDEUR (Validation) ---
def valider_saisie(texte_futur):
    if texte_futur == "": return True
    if len(texte_futur) == 1 and texte_futur.isdigit() and texte_futur != "0": return True
    return False

validation_cmd = (app.register(valider_saisie), '%P')

cadre_grille = ctk.CTkFrame(app, fg_color="transparent")
cadre_grille.pack(pady=10)

cases_ui = []

# --- VARIABLES GLOBALES (Le jeu et son corrigé) ---
grille_actuelle = []
grille_solution = []

# --- DESSIN DES 81 CASES ---
for ligne in range(9):
    ligne_ui = []
    for colonne in range(9):
        case = ctk.CTkEntry(
            cadre_grille, 
            width=50, height=50, 
            font=("Arial", 24, "bold"), justify="center", corner_radius=0,
            validate="key", validatecommand=validation_cmd
        )
        
        marge_droite = 3 if colonne % 3 == 2 and colonne != 8 else 1
        marge_bas = 3 if ligne % 3 == 2 and ligne != 8 else 1
        case.grid(row=ligne, column=colonne, padx=(1, marge_droite), pady=(1, marge_bas))
        
        # --- NOUVEAU 2 : Petit bonus UX - Quand on tape un chiffre, il se met en blanc (pour effacer le rouge d'une erreur précédente) ---
        case.bind("<KeyRelease>", lambda event, c=case: c.configure(text_color="white") if c.cget("state") == "normal" else None)
        
        ligne_ui.append(case)
    cases_ui.append(ligne_ui)


def afficher_grille(grille_a_afficher):
    for ligne in range(9):
        for colonne in range(9):
            case = cases_ui[ligne][colonne]
            valeur = grille_a_afficher[ligne][colonne]
            
            case.configure(state="normal", text_color="white")
            case.delete(0, "end")
            
            if valeur != 0:
                case.insert(0, str(valeur))
                case.configure(text_color="#3B8ED0", state="readonly")


def preparer_nouvelle_partie():
    global grille_actuelle, grille_solution
    
    # 1. On génère la grille pour le joueur
    grille_actuelle = generer_nouvelle_partie()
    
    # 2. On fait un clone (Deep Copy) pour l'ordinateur
    grille_solution = copy.deepcopy(grille_actuelle)
    
    # 3. L'ordinateur résout son clone en secret (Le Corrigé)
    resoudre_sudoku(grille_solution)
    
    # 4. On affiche la grille à trous au joueur
    afficher_grille(grille_actuelle)


# --- NOUVEAU 3 : La fonction de Vérification ---
def clic_verifier():
    for ligne in range(9):
        for colonne in range(9):
            case = cases_ui[ligne][colonne]
            
            # On ne vérifie que les cases que le joueur peut modifier
            if case.cget("state") == "normal":
                texte_joueur = case.get() # On lit ce que le joueur a tapé
                
                # Si la case n'est pas vide
                if texte_joueur != "":
                    chiffre_joueur = int(texte_joueur)
                    chiffre_solution = grille_solution[ligne][colonne]
                    
                    # On compare avec le corrigé secret !
                    if chiffre_joueur == chiffre_solution:
                        case.configure(text_color="#2ECC71") # Vrai = Vert
                    else:
                        case.configure(text_color="#E74C3C") # Faux = Rouge


def clic_resoudre():
    for ligne in range(9):
        for colonne in range(9):
            valeur = grille_solution[ligne][colonne] # On utilise directement notre corrigé !
            case = cases_ui[ligne][colonne] 
            
            if case.cget("state") == "normal":
                case.delete(0, "end") 
                case.insert(0, str(valeur)) 
                case.configure(state="readonly", text_color="#2ECC71") 

# On prépare la toute première partie au lancement
preparer_nouvelle_partie()

# --- LES 3 BOUTONS ---
cadre_boutons = ctk.CTkFrame(app, fg_color="transparent")
cadre_boutons.pack(pady=20)

bouton_nouveau = ctk.CTkButton(cadre_boutons, text="Nouvelle Partie 🔄", font=("Arial", 16, "bold"), fg_color="#E67E22", hover_color="#D35400", command=preparer_nouvelle_partie)
bouton_nouveau.grid(row=0, column=0, padx=5) 

# LE NOUVEAU BOUTON !
bouton_verifier = ctk.CTkButton(cadre_boutons, text="Vérifier 🔍", font=("Arial", 16, "bold"), fg_color="#8E44AD", hover_color="#9B59B6", command=clic_verifier)
bouton_verifier.grid(row=0, column=1, padx=5)

bouton_resoudre = ctk.CTkButton(cadre_boutons, text="Résoudre (IA) 🤖", font=("Arial", 16, "bold"), command=clic_resoudre)
bouton_resoudre.grid(row=0, column=2, padx=5)

# --- LANCEMENT ---
app.mainloop()