import requests

from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import date

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


def get_data_urls(year):
    urls = ["https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_from_1958_to_1969"]
    current_decade = int(f"{year//10}0")
    for decade in range(1970, current_decade+1, 10):
        urls.append(f"https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_{decade}s")

    return urls


current_year = date.today().year
data_urls = get_data_urls(current_year)

number_ones = [song for url in data_urls for song in get_songs(url)]

print(number_ones)
print(len(number_ones))
