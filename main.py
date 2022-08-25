import requests
from bs4 import BeautifulSoup
from datetime import *
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

while True:
    try:
        string = input("Input a day you want to jump to in YYYY-MM-DD format (Nothing before 1958): ")
        moment = datetime.strptime(string, '%Y-%m-%d')
        if moment < datetime(1958, 1, 1) or moment > datetime.today():
            raise ValueError
        break
    except ValueError:
        print("Make sure your date is in the right format and that its not too far back or too far forward")


moment = datetime.strftime(moment, "%Y-%m-%d")
URL = f"https://www.billboard.com/charts/hot-100/{moment}"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
song_list = [song.getText().strip() for song in soup.select("li h3#title-of-a-story")]
artist_list = [artist.getText().strip().replace(' Featuring', ',') for artist in soup.select("li h3#title-of-a-story + span")]


scope = "playlist-modify-private playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


user_id = sp.me()['id']
uri_list = []

for song, artist in zip(song_list, artist_list):
    search_info = f"track:{song} artist:{artist}"
    song_info = sp.search(search_info, limit=1, type="track", market="US")
    if song_info['tracks']['items']:
        uri_list.append(song_info['tracks']['items'][0]['uri'])

play_id = sp.user_playlist_create(user=user_id, name=f"{moment} Billboard 100", public=False, description="Python Project")['id']
sp.user_playlist_add_tracks(user=user_id, playlist_id=play_id, tracks=uri_list)











