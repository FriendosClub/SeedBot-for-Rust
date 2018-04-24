# SeedBot for Rust - CURL PoC

Simple proof-of-concept written as a shell script.

## Notes

- **NB:** This PoC doesn't handle automatic logins. You'll have to navigate to [beancan.io](https://beancan.io), log in, then save your `cookies.txt` to this folder using a tool like [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg).
- You **must** wait for the map to generate before visiting the final URL, otherwise beancan will always display a 404 error. Not sure why.
- Values passed to `beancan_gen_map` aren't strictly validated since this is only a proof-of-concept

## Usage

**Generate a map**

```
usage: beancan_gen_map seed world_size

positional arguments:
  seed           Integer 1 <= seed <= 2147483647 OR -1 for random seed
  world_size     Integer 1000 <= world_size <= 6000
```

**Post map details to a webhook**

```
usage: seedbot.py [-h] [-v] beancan_url webhook_url

positional arguments:
  beancan_url    URL of the generated map
  webhook_url    Discord webhook URL

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print debug info
```
