from collections import Counter
import json

stock = {
    "riz": {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}

# 1
print("-----1------")
for nom, info in stock.items():
    print(f"{nom} : {info['prix']} Ar, quantite {info['quantite']}")

# 2
print("-----2------")
total = 0
for info in stock.values():
    total += info["prix"] * info["quantite"]
print(f"Valeur totale du stock : {total} Ar")

# 3
print("-----3------")
ruptures = [nom for nom, info in stock.items() if info["quantite"] == 0]
print(f"Produits en rupture : {ruptures}")

# 4
print("-----4------")
def vendre(stock, produit, quantite):
    info = stock.get(produit)
    if info is None:
        return False, f"Produit inconnu : {produit}"
    if info["quantite"] < quantite:
        return False, f"Stock insuffisant : {info['quantite']} disponible(s)"
    info["quantite"] -= quantite
    return True, f"Vente de {quantite} {produit} reussie"

print(vendre(stock, "riz", 10))      # vente reussie
print(vendre(stock, "sfgdf", 5))    # produit inconnu
print(vendre(stock, "huile", 100))   # quantite trop grande

# 5
print("-----5------")
def ajouter_produit(stock, nom, prix, quantite):
    if nom in stock:
        return False, f"{nom} existe deja"
    stock[nom] = {"prix": prix, "quantite": quantite}
    return True, f"{nom} ajoute"

print(ajouter_produit(stock, "riz", 3200, 10))    # refuse
print(ajouter_produit(stock, "farine", 2800, 20)) # accepte

# 6
print("-----6------")
prix_hausse = {nom: int(info["prix"] * 1.10 + 0.5) for nom, info in stock.items()}
print(prix_hausse)

# 7
print("-----7------")
ventes = ["riz", "sucre", "riz", "huile", "riz"]

compte = {}
for produit in ventes:
    compte[produit] = compte.get(produit, 0) + 1
print(f"Avec get : {compte}")

print(f"Avec Counter : {dict(Counter(ventes))}")

# 8
print("-----8------")
with open("stock.json", "w") as f:
    json.dump(stock, f)

with open("stock.json", "r") as f:
    stock_recharge = json.load(f)

print(f"Dictionnaires egaux : {stock == stock_recharge}")
