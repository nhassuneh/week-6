# apputil.py
import requests
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class Genius:
    # Exercise 1
    # Initialize the Genius object and store the access token.
    def __init__(self, access_token):
        self.access_token = access_token
        self.url = "https://api.genius.com"

    
    # Exercise 2
    def get_artist(self, search_term):
        # Search for artist
        search = requests.get(
            f"{self.url}/search",
            headers={"Authorization": f"Bearer {self.access_token}"},
            params={"q": search_term}
        ).json()

        # Get the first artist ID
        artist_id = search["response"]["hits"][0]["result"]["primary_artist"]["id"]

        # Get artist's info
        artist = requests.get(
            f"{self.url}/artists/{artist_id}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        ).json()

        return artist

        #Exercise 3
    def get_artists(self, search_terms):
        # Search for artist
        data = []

        for term in search_terms:
            result = self.get_artist(term)
            if "error" in result:
                data.append({"search_term": term, "artist_name": None, "artist_id": None, "followers_count": None})
                continue

            artist = result["response"]["artist"]
            data.append({
                "search_term": term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(data)


genius = Genius(ACCESS_TOKEN)
print(genius.get_artists(['Rihanna', 'Tycho', 'Seal', 'U2']))   