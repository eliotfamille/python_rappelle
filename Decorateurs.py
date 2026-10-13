import time
from functools import wraps, lru_cache

# 1
print("-----1------")
def chronometrer(func):
    @wraps(func)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"{func.__name__} a pris {fin - debut:.2f} s")
        return resultat
    return enveloppe

@chronometrer
def lente():
    time.sleep(1)

lente()

# 2
print("-----2------")
def majuscules(func):
    @wraps(func)
    def enveloppe(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return enveloppe

@majuscules
def dire_bonjour():
    return "bonjour"

print(dire_bonjour())

# 3
print("-----3------")
def compter_appels(func):
    @wraps(func)
    def enveloppe(*args, **kwargs):
        enveloppe.appels += 1
        return func(*args, **kwargs)
    enveloppe.appels = 0
    return enveloppe

@compter_appels
def saluer():
    return "salut"

saluer()
saluer()
saluer()
print(f"Nombre d'appels : {saluer.appels}")

# 4
print("-----4------")
def verifier_positifs(func):
    @wraps(func)
    def enveloppe(*args, **kwargs):
        for valeur in list(args) + list(kwargs.values()):
            if isinstance(valeur, (int, float)) and valeur < 0:
                raise ValueError(f"Argument negatif : {valeur}")
        return func(*args, **kwargs)
    return enveloppe

@verifier_positifs
def surface(longueur, largeur):
    return longueur * largeur

print(surface(3, 4))
try:
    surface(3, -4)
except ValueError as e:
    print(f"Erreur : {e}")

# 5
print("-----5------")
def chronometrer(unite="s"):
    def decorateur(func):
        @wraps(func)
        def enveloppe(*args, **kwargs):
            debut = time.perf_counter()
            resultat = func(*args, **kwargs)
            duree = time.perf_counter() - debut
            if unite == "ms":
                print(f"{func.__name__} a pris {duree * 1000:.2f} ms")
            else:
                print(f"{func.__name__} a pris {duree:.2f} s")
            return resultat
        return enveloppe
    return decorateur

@chronometrer(unite="ms")
def lente_ms():
    time.sleep(1)

lente_ms()

# 6
print("-----6------")
def memoriser(func):
    cache = {}
    @wraps(func)
    def enveloppe(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return enveloppe

# Sans memoisation
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Sans memoriser :")
print(chronometrer("ms")(fibonacci)(30))

# Avec memoriser
@memoriser
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Avec memoriser :")
print(chronometrer("ms")(fibonacci)(30))

# Avec lru_cache
@lru_cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Avec lru_cache :")
print(chronometrer("ms")(fibonacci)(30))

# 7
print("-----7------")
@chronometrer("ms")
@compter_appels
def f_a():
    return 1

@compter_appels
@chronometrer("ms")
def f_b():
    return 1

for _ in range(3):
    f_a()
    f_b()

print(f"f_a.appels = {f_a.appels}")
print(f"f_b.appels = {f_b.appels}")

# 8
print("-----8------")
class MiniFlask:
    def __init__(self):
        self.routes = {}
        self.gestionnaire_404 = None

    def route(self, url):
        def decorateur(func):
            if url in self.routes:
                raise ValueError(f"URL deja enregistree : {url}")
            self.routes[url] = func
            return func
        return decorateur

    def erreur_404(self, func):
        self.gestionnaire_404 = func
        return func

    def lister_routes(self):
        for url in self.routes:
            print(url)

    def repondre(self, url):
        func = self.routes.get(url)
        if func is None:
            if self.gestionnaire_404 is None:
                return "404"
            return self.gestionnaire_404()
        return func()

app = MiniFlask()

@app.route("/")
def accueil():
    return "Page d'accueil"

@app.route("/contact")
def contact():
    return "Page contact"

@app.erreur_404
def introuvable():
    return "Page introuvable"

try:
    @app.route("/")
    def doublon():
        return "doublon"
except ValueError as e:
    print(f"Erreur : {e}")

app.lister_routes()
print(app.repondre("/"))
print(app.repondre("/inconnue"))
