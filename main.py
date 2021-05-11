import requests

from bs4 import BeautifulSoup
from collections import namedtuple

Song = namedtuple("Song", ["artist", "title"])
song_list = []

url_2010s = "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_2010s"

response = requests.get(url_2010s)
response.raise_for_status()
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

table = soup.find(class_="wikitable")
rows = table.find_all("tr")

for row in rows[1:]:
    cells = row.find_all("td")
    try:
        song_list.append(Song(artist=cells[2].text.strip(), title=cells[3].text.split('"')[1]))
    except IndexError:
        pass

print(song_list)
print(len(song_list))
