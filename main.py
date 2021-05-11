import requests

from bs4 import BeautifulSoup
from collections import namedtuple

Song = namedtuple("Song", ["artist", "title"])


def get_songs(url):
    song_list = []

    response = requests.get(url)
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

    return song_list


wiki_urls = [
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_from_1958_to_1969",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_1970s",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_1980s",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_1990s",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_2000s",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_2010s",
    "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_2020s"
]

number_ones = [song for url in wiki_urls for song in get_songs(url)]

print(number_ones)
print(len(number_ones))
