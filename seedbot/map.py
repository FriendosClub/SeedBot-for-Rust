"""Summary
"""
import re
import requests
from bs4 import BeautifulSoup


class Map():
    """Map with details

    Attributes:
        cdn_url (str): Map image host
        features (list): List of map monuments
        img_hi_res (str): High resolution map image
        img_monuments (str): Map image with monuments
        request (requests.models.Response): GET <map URL>
        seed (int): Map seed
        size (int): Map size
    """
    def __init__(self, url, seed, size, timeout=2):
        """Summary

        Args:
            url (str): URL of map
            seed (int): Map seed
            size (int): Map size
            timeout (int, optional): Request timeout
        """
        self.request = requests.get(url, timeout=timeout)
        self.request.raise_for_status()

        self.cdn_url = 'https://assets-rustserversio.netdna-ssl.com'

        self.seed = seed
        self.size = size

        # Variables we populate later
        self.features = self.get_features()
        self.img_hi_res = f"{self.cdn_url}/maps/{self.seed}-{self.size}-Procedural_Map.jpg"
        self.img_monuments = f"{self.cdn_url}/maps/{self.seed}-{self.size}-Procedural_Map-lowres-monuments.jpg"

    def get_features(self):
        """Parses the map page with BeautifulSoup to retrieve a list of features

        Returns:
            list: A list of features such as 'Lighthouse', etc.
        """
        soup = BeautifulSoup(self.request.text, 'html.parser')
        media_content = soup.find("div", class_="media-content")
        features = re.findall(r'\S.*, .*',
                              media_content.text)[0].strip().split(', ')

        # Remove size and map name 'features'
        return features[:-2]
