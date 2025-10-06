# apputil.py
import requests
import pandas as pd

ACCESS_TOKEN = "Amx61v9fOXuPCVZI1aq5P9vsJxnJsM3HK8csA9f1gwSYqFlz6mFVeBvNBSzqnQK_"

class Genius:
    # Exercise 1
    # Initialize the Genius object and store the access token.
    def __init__(self, access_token):
        """
        Initialize the Genius API client with an access token.
        
        Args:
            access_token (str): The Genius API access token for authentication.
        """
        self.access_token = access_token
        self.url = "https://api.genius.com"

    
    # Exercise 2
    def get_artist(self, search_term):
        """
        Retrieve artist information for a given search term.
        
        Args:
            search_term (str): The artist name to search for.
            
        Returns:
            dict: A dictionary containing the artist's information from the Genius API.
            
        Note:
            This method performs a search and returns the first matching artist's details.
        """
        # Search for the artist
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
        """
        Retrieve information for multiple artists.
        
        Args:
            search_terms (list): A list of artist names to search for.
            
        Returns:
            pandas.DataFrame: A DataFrame containing the following columns:
                - search_term: The original search term
                - artist_name: The artist's name (if found)
                - artist_id: The artist's Genius ID (if found)
                - followers_count: Number of followers for the artist (if available)
                
        Note:
            If an artist cannot be found, the corresponding row will have None values
            for artist_name, artist_id, and followers_count.
        """
        data = []

        # Search for each artist
        for term in search_terms:
            result = self.get_artist(term)
            if "error" in result:
                data.append({"search_term": term, "artist_name": None, "artist_id": None, "followers_count": None})
                continue
            # Get the artist's info
            artist = result["response"]["artist"]
            # Append the artist's info to the data list
            data.append({
                "search_term": term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(data)


genius = Genius(ACCESS_TOKEN)
print(genius.get_artists(['Rihanna', 'Tycho', 'Seal', 'U2']))   