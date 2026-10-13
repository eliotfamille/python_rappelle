notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]

# 1
print("-----1-----")
print(f"Nombre de notes : {len(notes)}")
print(f"Moyenne : {(sum(notes) / len(notes))}")
print(f"Note minimale : {min(notes)}")
print(f"Note maximale : {max(notes)}")

# 2
print("-----2-----")
print(f"Note superieure a 10 : {[n for n in notes if n > 10]}")
print(f"Ajournes : {[n for n in notes if n < 10]}")

# 3
print("-----3-----")
print(f"Note ordre croissant : {sorted(notes)}")
triee = sorted(notes, reverse=True)
print(f"Top 3 : {triee[:3]}")

# 4
print("-----4-----")
NNotes = [min(n + 2, 10) if n < 10 else n for n in notes]   # nouvelle liste
print(f"Nouveau liste : {NNotes}")

# 5
print("-----5-----")
def histogramme(notes):
    n = 0
    while n < 20:
        Etoiles = ['*' for i in notes if i>n and i<=n+4]    # creation des liste *
        print(f"{n}-{n+(4 if n<15 else 5)} \t | \t {len(Etoiles)*'*'}")
        n+=5
histogramme(notes)

# 6
print("-----6-----")
def rang(notes, note):
    tmp = sorted(notes, reverse=True)
    print(f"Rang de {note} : {tmp.index(note)+1}")
rang(notes, 14)

# 7
print("-----7-----")
sup = [15, 6, 18]
notes.extend(sup)
ord = set()
notes = [x for x in notes if x not in ord and not ord.add(x)]
print(notes)
