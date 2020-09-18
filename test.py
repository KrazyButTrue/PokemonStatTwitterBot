import requests

r = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
r_info = r.json()
name = r_info["name"]
print(name)


'@WillieTwitBot “gengar”' "gengar"