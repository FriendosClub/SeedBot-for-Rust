#!/usr/bin/env python3.6

import argparse
import json
import re
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("beancan_url", help="URL of the generated map")
parser.add_argument("webhook_url", help="Discord webhook URL")
parser.add_argument("-v", "--verbose", help="Print debug info",
                    action="store_true")

args = parser.parse_args()


def debug(msg: str):
    if args.verbose:
        for line in msg.splitlines():
            print(f"[DEBUG] {line}")
        print("")


r = requests.get(args.beancan_url)
debug(f"Got response {r.status_code} from {args.beancan_url}")

soup = BeautifulSoup(r.text, "html.parser")

# We extract seed and map size from the URL, so all we need to find is
# the list of the map's features
media_content = soup.find_all("div", class_="media-content")[0]
debug(f"media_content text:\n{media_content.text}")

# Extract tag list as a list
# I feel dirty using a pattern like '.*, .*' but it works. ¯\_(ツ)_/¯
tags = re.findall(r'\S.*, .*', media_content.text)[0].strip().split(', ')
debug(f"tags: {tags}")

# If we wanted to be exact, we could find all the images such that
# div.fotorama__thumb.fotorama__loaded.fotorama__loaded--img >
#   img.fotorama__img.src
# However, the CDN URLs are uniform and based only on the seed and map size.

seed_and_size = re.findall(r'(\d+)', r.url)
seed = seed_and_size[0]
size = seed_and_size[1]

debug(f"Seed: {seed}")
debug(f"Size: {size}")

hires_map_url = ("https://assets-rustserversio.netdna-ssl.com/maps/"
                 f"{seed}-{size}-Procedural_Map.jpg")
monuments_url = ("https://assets-rustserversio.netdna-ssl.com/maps/"
                 f"{seed}-{size}-Procedural_Map-lowres-monuments.jpg")

debug(f"high-res map URL: {hires_map_url}")
debug(f"monuments URL: {monuments_url}")

# Construct the data for our webhook POST
content = (":map: **New map generated!**\n\n",
           f"**Seed:** {seed}\n",
           f"**Size:** {size}\n",
           f"**Features:** {', '.join(tags)}\n",
           f"High-res map: {hires_map_url}\n",
           f"Low-res w/ monuments: {monuments_url}\n")

# At this point, discord_hooks.py would come into play
# However, I don't have my rewrite on my workstation,
#   so I'm shelving this for now.
# embed = {
#     'title': f"Procedural Map {seed}",
#     'url': "args.beancan_url",
#     'color': 13517355,                          # Rust logo color
#     # 'footer': {},                             # TODO: Add footer
#     'image': {
#         'url': hires_map_url
#     },
#     'author': {
#         'name': "Rust Seeds Bot",
#         'url': '',                              # TODO: Add Github link
#         'icon_url': "https://i.imgur.com/r5jdE71.png"
#     },
#     'fields': [
#         {
#             'name': 'Seed',
#             'value': seed
#         },
#         {
#             'name': 'Size',
#             'value': size
#         },
#         {
#             'name': 'Features',
#             'value': ', '.join(tags)
#         },
#         {
#             'name': 'High-res image',
#             'value': hires_map_url
#         },
#         {
#             'name': 'Image w/ monuments',
#             'value': monuments_url
#         }
#     ]
# }

webhook_data = {
    'username': "SeedBot for Rust",
    'avatar_url': "https://i.imgur.com/r5jdE71.png",    # Transparent map icon
    'content': ''.join(content)
}

debug(json.dumps(webhook_data))

w = requests.post(args.webhook_url, json=(webhook_data))

debug(f"Got response {w.status_code} POSTing webhook")
