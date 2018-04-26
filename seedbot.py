#!/usr/bin/env python3

import json
import requests
from bs4 import BeautifulSoup
from random import randint
from seedbot.map import Map
from time import sleep


def debug_print(msg: str):
    # TODO: Only print debug info if command-line flag is set
    for line in msg.splitlines():
        print(f"[DEBUG] {line}")


def get_token(page: str) -> str:
    """Get the Laravel CSRF token for submitting a form

    Args:
        page (str): HTML text response of a request

    Returns:
        str: CSRF token
    """
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find('input', {'name': '_token'}).get('value')


if __name__ == '__main__':
    bc = 'https://beancan.io'

    with open('cfg/config.json') as cfg_file:
        cfg = json.load(cfg_file)

    debug_print("seedbot.py started")

    session = requests.Session()

    debug_print("New session initialized")

    debug_print("Retrieving login CSRF token...")
    r = session.get(f'{bc}/login', timeout=cfg['timeout'])
    login_token = get_token(r.text)
    debug_print(f"Got token {login_token}")

    login_payload = {
        'email': cfg['beancan_email'],
        'password': cfg['beancan_password'],
        '_token': login_token
    }

    debug_print("Logging in...")
    login = session.post(f'{bc}/login', data=login_payload,
                         timeout=cfg['timeout'])

    login.raise_for_status()

    debug_print(f"Logged in as {cfg['beancan_email']}")

    debug_print("Getting map-generate CSRF token...")
    r = session.get(f'{bc}/map-generate', timeout=cfg['timeout'])
    map_token = get_token(r.text)
    debug_print(f"Got token {map_token}")

    map_payload = {
        'seed': randint(1, 2147483647),
        'size': cfg['map_size'],
        'level': 'Procedural Map',
        '_token': map_token
    }

    debug_print("Generating map...")
    debug_print(f"Size: \t{map_payload['size']}")
    debug_print(f"Seed: \t{map_payload['seed']}")

    map_gen = session.post(f'{bc}/map-generate', data=map_payload,
                           timeout=cfg['timeout'])
    map_gen.raise_for_status()

    debug_print(map_gen.url)

    # Check every 10 seconds to see if the map_gen URL redirects to
    #   https://beancan.io. If it does, that means the map is done generating
    debug_print("Waiting for redirect")
    while True:
        sleep(10)
        r = session.get(map_gen.url, timeout=cfg['timeout'])

        debug_print(f"Current URL: {r.url}")

        if 'map-generate' not in r.url:
            debug_print("Redirect detected")
            break

    # We could check redirects but all URLs follow a uniform pattern.
    # Maybe this will need to be updated one day.
    map_url = f"{bc}/maps/{map_payload['seed']}-{map_payload['size']}"

    debug_print(f"Generating map object from {map_url}")

    map = Map(map_url, map_payload['seed'], map_payload['size'],
              timeout=cfg['timeout'])

    debug_print("Map generated")
    debug_print(f"Features: {map.features}")

    # Webhook time!
    content = (":map: **New map generated!**\n\n",
               f"**Seed:** {map.seed}\n",
               f"**Size:** {map.size}\n",
               f"**Features:** {', '.join(map.features)}\n",
               f"**High-res map:** {map.img_hi_res}\n",
               f"**Low-res w/ monuments:** {map.img_monuments}\n")

    webhook_payload = {
        'username': "SeedBot for Rust",
        'avatar_url': "https://i.imgur.com/r5jdE71.png",  # Transparent map icon
        'content': ''.join(content)
    }

    debug_print("Webhook payload:")
    debug_print(json.dumps(webhook_payload, indent=2, sort_keys=True))

    debug_print("Posting map to webhook...")
    w = requests.post(cfg['webhook_url'], json=webhook_payload)
    w.raise_for_status()
    debug_print("Map posted")
