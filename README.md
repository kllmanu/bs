# bs

![](./header.png)

a burning series CLI to download series, seasons and episodes from [bs.to](https://bs.to)

## Features

- download entire series or just select some seasons or episodes
- [fuzzy find](https://github.com/junegunn/fzf) series, seasons and episodes
- skips already downloaded files
- **solves captchas** with the help of [Anti Captcha](https://anti-captcha.com/de) API
- runs totally unattended (retries on error)
- organized downloads of files in `series/S01E02_name-of-the-episode.mp4` style
- supports multiple hosters (with fallback)

## Setup

1. Install [poetry](https://python-poetry.org/) and [fzf](https://github.com/junegunn/fzf)
2. Clone the repo and run `poetry install` in the project root

Your `$SHELL` needs to export an environment variable with your [anticaptcha key](https://anti-captcha.com/de):

```
export ANTICAPTCHA_KEY="...."
export YTDLP_OPTIONS="{}"
export BS_DIR="/home/manu/tmp"
```

3. Run `poetry run bs` to start the downloader

## Hoster

Following hosters are supported:

- ✅ VOE
- ✅ Vidoza
- ❌ Doodstream
- ❌ Streamtape (see [this guide](https://github.com/ChristopherProject/Streamtape-Video-Downloader))
- ❌ Vidmoly (bypass with [vidmoly-bot](https://github.com/Z3NTL3/vidmoly-bot))

## Todo

- [x] error handling
- [ ] language selection
- [ ] support doodstream
- [ ] support streamtape
- [ ] support vidmoly
- [ ] add tests (should have been doing TDD straight from the beginning)
