# Rust SeedBot

Generate Rust maps and post photos of them to a Discord channel via webhook.

## About

Rust SeedBot is an experiment with Discord Webhooks and BeautifulSoup. On an hourly schedule, it generates a Rust map with [beancan.io](https://beancan.io/map-generate) and uses a webhook to post a rich embed including map size, seed, and photo to a Discord text channel.

## Setup

1. Clone repository.
2. Copy `cfg/config-example.json` to `config.json` and enter your info (see [below](#retrieving-laravel_session) for help).
3. Run `seedbot.py` using a scheduling system (e.g. [cron](https://debian-administration.org/article/56/Command_scheduling_with_cron))

## Retrieving `laravel_session`

**TODO**

## Roadmap

Completed | Feature
--------- | -------
:white_check_mark: | Basic webhook functionality
:x: | Read beancan.io cookies and map size from `config.json`
:x: | Generate map on beancan.io [note: probably a POST request]
:x: | Retrieve and parse map data with BeautifulSoup
:x: | Format map data as a rich embed and posting via webhook
:x: | Implement basic error handling
:x: | Implement retry backoff in case of an error
:x: | Add functionality to 'search' for specific monuments (Airport, Lighthouse, etc.)
:x: | Test and finalize error handling
:x: | Finalize documentation
