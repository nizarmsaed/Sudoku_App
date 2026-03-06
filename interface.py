# Fichier : interface.py
import customtkinter as ctk
import copy
from moteur_sudoku import resoudre_sudoku, generer_nouvelle_partie
from base_donnees import sauvegarder_score, obtenir_top_5 # --- NOUVEAU : On appelle l'archiviste ---

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

app = ctk.CTk() 
app.geometry("650x900") # Un peu plus haut
app.title("Sudoku Pro - Édition Spéciale") 

# --- VARIABLES DU JEU ---
temps_ecoule = 0
chrono_actif = False
grille_actuelle = []
grille_solution = []
cases_ui = []

# --- LOGIQUE DU CHRONO ---
def mettre_a_jour_chrono():
    global temps_ecoule, chrono_actif
    if chrono_actif:
        temps_ecoule += 1
        minutes = temps_ecoule // 60
        secondes = temps_ecoule % 60
        label_chrono.configure(text=f"{minutes:02d}:{secondes:02d}")
        app.after(1000, mettre_a_jour_chrono)

def demarrer_chrono():
    global temps_ecoule, chrono_actif
    temps_ecoule = 0 
    chrono_actif = True 
    label_chrono.configure(text="00:00")
    mettre_a_jour_chrono() 

def arreter_chrono():
    global chrono_actif
    chrono_actif = False 

# --- NOUVEAU : ENREGISTREMENT DU SCORE ---
def valider_et_enregistrer(pseudo, temps, difficulte, fenetre):
    if pseudo.strip() == "":
        pseudo = "Anonyme"
    
    # On envoie les données à notre archiviste (base_donnees.py)
    # On stocke le texte "Temps (Difficulté)" ou on adapte la BDD
    sauvegarder_score(f"{pseudo} ({difficulte})", temps)
    fenetre.destroy()
    afficher_leaderboard()

# --- NOUVEAU : AFFICHAGE DU TOP 5 ---
def afficher_leaderboard():
    fenetre_top = ctk.CTkToplevel(app)
    fenetre_top.geometry("400x400")
    fenetre_top.title("🏆 Meilleurs Scores")
    fenetre_top.attributes("-topmost", True)

    ctk.CTkLabel(fenetre_top, text="LEADERBOARD", font=("Arial", 24, "bold")).pack(pady=20)
    
    scores = obtenir_top_5()
    for i, (pseudo, temps) in enumerate(scores):
        min = temps // 60
        sec = temps % 60
        texte = f"{i+1}. {pseudo} : {min:02d}:{sec:02d}"
        ctk.CTkLabel(fenetre_top, text=texte, font=("Arial", 18)).pack(pady=5)

def afficher_victoire():
    arreter_chrono()
    fenetre_victoire = ctk.CTkToplevel(app)
    fenetre_victoire.geometry("400x350")
    fenetre_victoire.title("🏆 Victoire !")
    fenetre_victoire.attributes("-topmost", True) 
    
    diff_actuelle = menu_difficulte.get()
    texte_bravo = f"Félicitations !\nNiveau : {diff_actuelle}\nTemps : {label_chrono.cget('text')}"
    
    ctk.CTkLabel(fenetre_victoire, text=texte_bravo, font=("Arial", 20, "bold"), text_color="#2ECC71").pack(pady=20)
    
    # Saisie du Pseudo
    ctk.CTkLabel(fenetre_victoire, text="Entre ton pseudo :").pack()
    entree_pseudo = ctk.CTkEntry(fenetre_victoire)
    entree_pseudo.pack(pady=10)
    
    btn_save = ctk.CTkButton(fenetre_victoire, text="Enregistrer mon score", 
                             command=lambda: valider_et_enregistrer(entree_pseudo.get(), temps_ecoule, diff_actuelle, fenetre_victoire))
    btn_save.pack(pady=10)

def verifier_victoire(event=None):
    for ligne in range(9):
        for colonne in range(9):
            case = cases_ui[ligne][colonne]
            texte = case.get()
            if texte == "" or int(texte) != grille_solution[ligne][colonne]:
                return 
    afficher_victoire()

# --- INTERFACE ET DESSIN ---
titre = ctk.CTkLabel(app, text="Sudoku Pro", font=("Arial", 28, "bold"))
titre.pack(pady=(20, 5)) 

label_chrono = ctk.CTkLabel(app, text="00:00", font=("Arial", 24, "bold"), text_color="#F1C40F")
label_chrono.pack(pady=(0, 10))

# LE VIDEUR
def valider_saisie(texte_futur):
    if texte_futur == "": return True
    if len(texte_futur) == 1 and texte_futur.isdigit() and texte_futur != "0": return True
    return False
validation_cmd = (app.register(valider_saisie), '%P')

cadre_grille = ctk.CTkFrame(app, fg_color="transparent")
cadre_grille.pack(pady=10)

for ligne in range(9):
    ligne_ui = []
    for colonne in range(9):
        case = ctk.CTkEntry(cadre_grille, width=50, height=50, font=("Arial", 24, "bold"), 
                            justify="center", corner_radius=0, validate="key", validatecommand=validation_cmd)
        marge_droite = 3 if colonne % 3 == 2 and colonne != 8 else 1
        marge_bas = 3 if ligne % 3 == 2 and ligne != 8 else 1
        case.grid(row=ligne, column=colonne, padx=(1, marge_droite), pady=(1, marge_bas))
        case.bind("<KeyRelease>", lambda event, c=case: (c.configure(text_color="white") if c.cget("state") == "normal" else None, verifier_victoire()))
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

# CONTROLES
cadre_controles = ctk.CTkFrame(app, fg_color="transparent")
cadre_controles.pack(pady=10)

menu_difficulte = ctk.CTkOptionMenu(cadre_controles, values=["Facile", "Moyen", "Difficile"], font=("Arial", 16))
menu_difficulte.grid(row=0, column=0, padx=10)
menu_difficulte.set("Moyen")

def preparer_nouvelle_partie():
    global grille_actuelle, grille_solution
    arreter_chrono()
    choix = menu_difficulte.get()
    nb_trous = 30 if choix == "Facile" else 45 if choix == "Moyen" else 55
    grille_actuelle = generer_nouvelle_partie(nb_trous)
    grille_solution = copy.deepcopy(grille_actuelle)
    resoudre_sudoku(grille_solution)
    afficher_grille(grille_actuelle)
    demarrer_chrono()

bouton_nouveau = ctk.CTkButton(cadre_controles, text="Nouveau", font=("Arial", 16, "bold"), fg_color="#E67E22", command=preparer_nouvelle_partie)
bouton_nouveau.grid(row=0, column=1, padx=10) 

cadre_boutons_bas = ctk.CTkFrame(app, fg_color="transparent")
cadre_boutons_bas.pack(pady=10)

ctk.CTkButton(cadre_boutons_bas, text="Vérifier", command=lambda: [ (case.configure(text_color="#2ECC71" if case.get() and int(case.get()) == grille_solution[l][c] else "#E74C3C") if case.cget("state") == "normal" and case.get() else None) for l, ligne in enumerate(cases_ui) for c, case in enumerate(ligne) ]).grid(row=0, column=0, padx=5)

ctk.CTkButton(cadre_boutons_bas, text="IA", command=lambda: [ (case.delete(0, "end"), case.insert(0, str(grille_solution[l][c])), case.configure(state="readonly", text_color="#2ECC71"), arreter_chrono()) for l, ligne in enumerate(cases_ui) for c, case in enumerate(ligne) if case.cget("state") == "normal" ]).grid(row=0, column=1, padx=5)

ctk.CTkButton(cadre_boutons_bas, text="Scores 🏆", fg_color="#273c75", command=afficher_leaderboard).grid(row=0, column=2, padx=5)

preparer_nouvelle_partie()
app.mainloop()