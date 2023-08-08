from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

all_pokemon_url = "https://pokemondb.net/pokedex/all"

request = Request(all_pokemon_url,headers = {'User-Agent': 'Mozilla/5.0'})
page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode("utf-8")

soup = BeautifulSoup(page_html, "html.parser")

#Ici le [0] nous permet d'avoir uniquement le tableau concerné et pas tout les tableaux de la page
pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")
for pokemon in pokemon_rows[0:len(pokemon_rows)]:  #A remplacer par ce que l'on veut si on ne veut pas tous les pokemon
    pokemon_data = pokemon.find_all("td")
    id = pokemon_data[0]["data-sort-value"]  #Ici l'id correspondra au numéro national du pokedex
    name = pokemon_data[1].find_all("a")[0].getText()
    if pokemon_data[1].find_all("small") : 
        name = name + " (" + pokemon_data[1].find_all("small")[0].getText() + ")"
    details_uri = pokemon_data[1].find_all("a")[0]["href"]
    type1 = pokemon_data[2].find_all("a")[0].getText() 
    try:
        type2 = pokemon_data[2].find_all("a")[1].getText()
    except IndexError: 
        type2 = " "
    hp = pokemon_data[4].getText()
    attack = pokemon_data[5].getText()
    defense = pokemon_data[6].getText()
    special_attack = pokemon_data[7].getText()
    special_defense = pokemon_data[8].getText()
    speed = pokemon_data[9].getText()

    print(f"{id} | {name} | {type1} | {type2} | {hp} | {attack} | {defense} | {special_attack} | {special_defense} | {speed} ")