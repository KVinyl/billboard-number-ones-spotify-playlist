import os
import requests
import spotipy

from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import date
from spotipy.oauth2 import SpotifyOAuth

Song = namedtuple("Song", ["number", "artist", "title", "year"])

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']


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
            song_list.append(Song(
                number=int(cells[0].text),
                artist=cells[2].text.strip(),
                title=cells[3].text.split('"')[1],
                year=int(cells[1].text.split(",")[-1])
            ))
        except (IndexError, ValueError):
            pass

    return song_list


def get_data_urls(year):
    urls = ["https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_from_1958_to_1969"]
    current_decade = int(f"{year//10}0")
    for decade in range(1970, current_decade+1, 10):
        urls.append(f"https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_the_{decade}s")

    return urls


def get_uri(song, sp):
    result = sp.search(f'track:"{song.title}" artist:"{song.artist}"', limit=1)
    try:
        return result['tracks']['items'][0]['uri']
    except IndexError:
        return None


def main():
    current_year = date.today().year
    data_urls = get_data_urls(current_year)

    number_ones = [song for url in data_urls for song in get_songs(url)]

    # for i, song in enumerate(number_ones, 1):
    #     print(i, song)

    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                                scope="playlist-modify-private", cache_path="token.txt")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_id = sp.current_user()['id']

    song_uris = [get_uri(song, sp) for song in number_ones]
    print(f"Songs found in Spotify search: {sum(x is not None for x in song_uris)}/{len(song_uris)}")


if __name__ == "__main__":
    main()
