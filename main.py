import requests
from pprint import pprint

# Задача 1. Кто самый умный супергерой?

response = requests.get('https://akabab.github.io/superhero-api/api/' + '/all.json')

heroes = {
    'Hulk': 0,
    'Captain America': 0,
    'Thanos': 0
}

for hero in response.json():
    name = hero.get('name')
    if name in heroes:
        heroes[name] = hero.get('powerstats', {}).get('intelligence', 0)

heroes_sorted = list(sorted(heroes.items(), key=lambda x: x[1]))
print(heroes_sorted[-1])



