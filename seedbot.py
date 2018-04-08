#!/usr/bin/env python3

import json
import requests
from bs4 import BeautifulSoup
from dhooks.webhook import Webhook


class Map():

    """Object for managing map generation

    Attributes:
        laravel_session (str): Cookie for beancan.io
        map_size (int): Map size. 1000 <= x <= 6000
    """

    def __init__(self, config: dict):
        """Default constructor

        Args:
            config (dict): JSON object generated from `config.json`
        """
        self.laravel_session = config['laravel_session']
        self.map_size = config['map_size']


if __name__ == '__main__':
    with open('cfg/config.json') as cfg_file:
        cfg = json.load(cfg_file)

    # Debugging
    print(f"Map size: {cfg['map_size']}")
