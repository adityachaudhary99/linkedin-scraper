import requests
import os

class PostScraper:
    def __init__(self, key):
        self.api_url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile-posts"
        self.headers = {
            "x-rapidapi-key": key,
            "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com"
        }

    def get_posts(self, linkedin_url):
        response = requests.get(self.api_url, headers=self.headers, params={"linkedin_url": linkedin_url, "type": "posts"})
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
