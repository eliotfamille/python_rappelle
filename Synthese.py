import json
from datetime import datetime

etudiants = {
    "L3-001": {
        "nom": "Rakoto",
        "prenom": "Soa",
        "notes": {"Python": [15, 14], "Reseaux": [12]},
    },
    "L3-002": {
        "nom": "Rabe",
        "prenom": "Andry",
        "notes": {"Python": [9, 13], "Reseaux": [11, 10]},
    },
}

historique = []  # (date, fonction, args)
fichier = "carnet.json"


# Decorateurs
def journaliser(func):
    # note l'appel dans historique (apres succes)
    def enveloppe(*args):
        resultat = func(*args)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historique.append((date, func.__name__, args))
        return resultat
    return enveloppe


def note_valide(func):
    # refuse note hors 0-20
    def enveloppe(matricule, matiere, note):
        if not 0 <= note <= 20:
            raise ValueError(f"Note invalide : {note} (doit etre entre 0 et 20)")
        return func(matricule, matiere, note)
    return enveloppe


def etudiant_existe(func):
    # verifie le 1er argument (matricule)
    def enveloppe(matricule, *args):
        if matricule not in etudiants:
            raise ValueError(f"Matricule inconnu : {matricule}")
        return func(matricule, *args)
    return enveloppe


# Fonctions
@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    if matricule in etudiants:
        raise ValueError(f"Matricule deja existant : {matricule}")
    etudiants[matricule] = {"nom": nom, "prenom": prenom, "notes": {}}
    return f"Etudiant {prenom} {nom} ajoute"


# ordre : existe -> valide -> journalise (refus non journalises)
@etudiant_existe
@note_valide
@journaliser
def ajouter_note(matricule, matiere, note):
    # setdefault : cree la liste si matiere absente
    etudiants[matricule]["notes"].setdefault(matiere, []).append(note)
    return f"Note {note} ajoutee en {matiere}"


@etudiant_existe
def moyenne_matiere(matricule, matiere):
    notes = etudiants[matricule]["notes"].get(matiere)
    if not notes:
        raise ValueError(f"Aucune note en {matiere}")
    return sum(notes) / len(notes)


@etudiant_existe
def moyenne_generale(matricule):
    # moyenne des moyennes par matiere
    moyennes = [moyenne_matiere(matricule, m) for m in etudiants[matricule]["notes"]]
    return sum(moyennes) / len(moyennes) if moyennes else 0


def classement():
    # liste de (nom complet, moyenne), tri decroissant
    liste = [
        (f"{e['prenom']} {e['nom']}", moyenne_generale(matricule))
        for matricule, e in etudiants.items()
    ]
    return sorted(liste, key=lambda t: t[1], reverse=True)


def majors():
    # meilleurs[matiere] = (meilleure moyenne, nom)
    meilleurs = {}
    for matricule, e in etudiants.items():
        for matiere in e["notes"]:
            moyenne = moyenne_matiere(matricule, matiere)
            if matiere not in meilleurs or moyenne > meilleurs[matiere][0]:
                meilleurs[matiere] = (moyenne, f"{e['prenom']} {e['nom']}")
    # garde seulement matiere -> nom
    return {matiere: nom for matiere, (moyenne, nom) in meilleurs.items()}


@etudiant_existe
def bulletin(matricule):
    e = etudiants[matricule]
    print(f"Bulletin de {e['prenom']} {e['nom']} ({matricule})")
    for matiere, notes in e["notes"].items():
        print(f"  {matiere} : {notes} -> moyenne {moyenne_matiere(matricule, matiere):.2f}")
    print(f"  Moyenne generale : {moyenne_generale(matricule):.2f}")


def sauvegarder(fichier):
    with open(fichier, "w") as f:
        json.dump(etudiants, f)


def charger(fichier):
    try:
        with open(fichier, "r") as f:
            donnees = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Fichier introuvable : {fichier}")
    # clear et update : garde le meme dict (les fonctions le referencent)
    etudiants.clear()
    etudiants.update(donnees)


# chargement au demarrage (ignore si fichier absent)
try:
    charger(fichier)
except ValueError:
    pass

while True:
    print("\n----- MENU -----")
    print("1. Ajouter un etudiant\t\t2. Ajouter une note")
    print("3. Afficher un bulletin\t\t4. Afficher le classement")
    print("5. Afficher les majors\t\t6. Afficher l'historique")
    print("7. Sauvegarder\t\t\t8. Quitter")
    choix = input("Choix : ")

    # un seul try : toutes les erreurs ValueError affichees ici
    try:
        match choix:
            case "1":
                matricule = input("Matricule : ")
                nom = input("Nom : ")
                prenom = input("Prenom : ")
                print(ajouter_etudiant(matricule, nom, prenom))
            case "2":
                matricule = input("Matricule : ")
                matiere = input("Matiere : ")
                note = float(input("Note : "))  # float() leve ValueError si texte
                print(ajouter_note(matricule, matiere, note))
            case "3":
                bulletin(input("Matricule : "))
            case "4":
                for i, (nom, moyenne) in enumerate(classement(), 1):
                    print(f"{i}. {nom:<15} {moyenne:.2f}")
            case "5":
                for matiere, nom in majors().items():
                    print(f"{matiere} : {nom}")
            case "6":
                for date, nom_fonction, arguments in historique:
                    print(f"{date} | {nom_fonction} | {arguments}")
            case "7":
                sauvegarder(fichier)
                print("Carnet sauvegarde")
            case "8":
                break
            case _:
                print("Choix invalide")
    except ValueError as e:
        print(f"Erreur : {e}")
