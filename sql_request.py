import sqlite3

# Quelques exemples de requêtes : 
# SELECT * FROM pokemons ORDER BY special_attack DESC -> ça permet de trier les pkmn par attaque spéciale dans l'ordre décroissant
# SELECT name, special_attack FROM pokemons ORDER BY special_attack DESC -> c'est la même commande mais cette fois on affiche que le nom et l'attaque spé. plutôt que toutes les colonnes
# SELECT * FROM pokemons WHERE name LIKE '%Alola%' -> permet d'afficher toutes les pokemon qui ont la forme de Alola, on aurait pu choisir Galar, Mega, etc...
# SELECT * FROM pokemons WHERE LOWER(type1) = 'fire' OR LOWER(type2) = 'water' -> permet d'afficher les pkmn selon leur type (ici LOWER permet de rendre insensible à la casse le type)


conn = sqlite3.connect('pokemon_db.sqlite')
cur = conn.cursor()
#Ici, il faudra juste remplacer ce qu'il y a entre parenthèses par une des requêtes ci-dessus ou n'importe quelle requête SQL classique
cur.execute("SELECT * FROM pokemons WHERE (LOWER(type1) = 'fire' AND LOWER(type2) = 'water') OR (LOWER(type2) = 'fire' AND LOWER(type1) = 'WATER')")
rows = cur.fetchall()

for row in rows:
    print(row)
    
#(len(rows))