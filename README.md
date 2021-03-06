# SeedBot for Rust

Generate Rust maps and post photos of them to a Discord channel via webhook.

## About

SeedBot for Rust is an experiment with Discord Webhooks and BeautifulSoup. The script generates a Rust map with [beancan.io](https://beancan.io/map-generate), then sends a message to a Discord text channel using Discord's webhook functionality.

Theoretically (and once the project is finished), one could use a tool like `cron` to run the script on an interval (i.e. hourly).

## Setup

1. Clone repository.
2. Clone dependencies with `git submodule init`.
3. Copy `cfg/config-example.json` to `config.json` and enter your info (see [below](#configuration) for help).
4. Run `seedbot.py` using a scheduler (e.g. [cron](https://debian-administration.org/article/56/Command_scheduling_with_cron)) or by hand.

## Configuration

The configuration file is pretty self-explanatory. Here's an explanation anyway:

- `webhook_url`: Webhook for a Discord text channel.
  - See [this article](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more info about creating a webhook.
- `beancan_email` and `beancan_password`: Login information for a [beancan.io](https://beancan.io) account.
- `map_size`: How large of a map you'd like to generate.
  - Min. 1000, max 6000.
- `timeout`: How long to wait before HTTP requests are terminated.

## Roadmap

Completed | Feature
--------- | -------
:white_check_mark: | Basic webhook functionality
:white_check_mark: | Read beancan.io login info and map size from `config.json`
:white_check_mark: | Generate map on beancan.io
:white_check_mark: | Retrieve and parse map data with BeautifulSoup
:white_check_mark: | Format map data ~~as a rich embed~~ and post via webhook
:x: | Implement basic error handling
:x: | Implement retry backoff in case of an error
:x: | Add ability to filter by monuments (Airport, Harbor, Launch Site, etc.)
:x: | Test and finalize error handling
:x: | Finalize documentation
