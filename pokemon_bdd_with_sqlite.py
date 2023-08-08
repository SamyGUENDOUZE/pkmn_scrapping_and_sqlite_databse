import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('pokemon_db.sqlite')
        # print(sqlite3.version) # pas obligatoire
    except Error as e:
        print(e)
    
    if conn:
        return conn

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS pokemons (
                                        id integer PRIMARY KEY,
                                        pokedex_number integer NOT NULL,
                                        name text NOT NULL,
                                        type1 text,
                                        type2 text,
                                        hp integer,
                                        attack integer,
                                        defense integer,
                                        special_attack integer,
                                        special_defense integer,
                                        speed integer
                                    ); '''
        conn.execute(sql)
    except Error as e:
        print(e)

def insert_pokemon(conn, pokemon):
    sql = ''' INSERT INTO pokemons(pokedex_number, name, type1, type2, hp, attack, defense, special_attack, special_defense, speed)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pokemon)
    return cur.lastrowid


connection = create_connection()
create_table(connection)

all_pokemon_url = "https://pokemondb.net/pokedex/all"
request = Request(all_pokemon_url,headers = {'User-Agent': 'Mozilla/5.0'})
page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode("utf-8")
soup = BeautifulSoup(page_html, "html.parser")

pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

for pokemon in pokemon_rows[0:len(pokemon_rows)]: 
    pokemon_data = pokemon.find_all("td")
    pokedex_number = int(pokemon_data[0]["data-sort-value"])
    name = pokemon_data[1].find_all("a")[0].getText()
    if pokemon_data[1].find_all("small"):
        name = name + " (" + pokemon_data[1].find_all("small")[0].getText() + ")"
    details_uri = pokemon_data[1].find_all("a")[0]["href"] #variable qui peut nous servir si on veut rajouter davantage de détails sur chaque pokemon
    type1 = pokemon_data[2].find_all("a")[0].getText() 
    try:
        type2 = pokemon_data[2].find_all("a")[1].getText()
    except IndexError: 
        type2 = None  # C'est mieux de mettre None qu'une chaîne de caractère vide
    hp = int(pokemon_data[4].getText())
    attack = int(pokemon_data[5].getText())
    defense = int(pokemon_data[6].getText())
    special_attack = int(pokemon_data[7].getText())
    special_defense = int(pokemon_data[8].getText())
    speed = int(pokemon_data[9].getText())

    pokemon_info = (pokedex_number, name, type1, type2, hp, attack, defense, special_attack, special_defense, speed)

    insert_pokemon(connection, pokemon_info)

connection.commit()
connection.close()