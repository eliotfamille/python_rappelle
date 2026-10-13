import math
from collections import namedtuple

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

# 1
print("-----1------")
for nom, lat, lon in villes:
    print(f"{nom} : {lat}, {lon}")

# 2
print("-----2------")
nord = max(villes, key=lambda v: v[1])
print(f"La plus au nord : {nord[0]}")

# 3
print("-----3------")
def bornes(villes):
    lat = [v[1] for v in villes]
    lon = [v[2] for v in villes]
    return min(lat), max(lat), min(lon), max(lon)

lat_min, lat_max, lon_min, lon_max = bornes(villes)
print(f"Latitude : {lat_min} a {lat_max}")
print(f"Longitude : {lon_min} a {lon_max}")

# 4
print("-----4------")
def distance(p1, p2):
    return math.dist(p1, p2)

print(f"Antananarivo - Toamasina : {distance(villes[0][1:], villes[1][1:]):.2f}°")

# 5
print("-----5------")
distances = {}
for i in range(len(villes)):
    for j in range(i + 1, len(villes)):
        a, b = villes[i], villes[j]
        distances[(a[0], b[0])] = distance(a[1:], b[1:])
print(f"Nombre de paire : {len(distances)}")

# 6
print("-----6------")
try:
    villes[0][1] = -19.0
except TypeError as e:
    print(f"Impossible de modifier un tuple : {e}")

# Corriger : creer un nouveau tuple et remplacer l'ancien dans la liste
nom, lat, lon = villes[0]
villes[0] = (nom, -19.0, lon)
print(f"Corrige : {villes[0]}")

# 7
print("-----7------")
Ville = namedtuple("Ville", ["nom", "latitude", "longitude"])
villes = [Ville(*v) for v in villes]

def haversine(v1, v2):
    R = 6371  # rayon en km
    phi1, phi2 = math.radians(v1.latitude), math.radians(v2.latitude)
    dphi = phi2 - phi1
    dlam = math.radians(v2.longitude - v1.longitude)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

for i in range(len(villes)):
    for j in range(i + 1, len(villes)):
        a, b = villes[i], villes[j]
        print(f"{a.nom} - {b.nom} : {haversine(a, b):.1f} km")
