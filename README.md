# bs

![](./header.png)

## Features

- [fuzzy find](https://github.com/junegunn/fzf) and download series, seasons and episodes using [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **solves captchas** with the help of [Anti Captcha](https://getcaptchasolution.com/f3w2accaul) API
- runs totally unattended (retries on error)
- skips already downloaded files
- supports multiple hosters (with fallback)
- organizes downloads in `series/S01E02_name-of-the-episode.mp4` style

## Setup

1. Install [poetry](https://python-poetry.org/), [fzf](https://github.com/junegunn/fzf) and [yt-dlp](https://github.com/yt-dlp/yt-dlp)
2. Clone the repo and run `poetry install` in the project root
3. Run `poetry run bs` to start the downloader

## Supported hosters

- ✅ VOE
- ✅ Vidoza
- ✅ Doodstream
- ❌ Streamtape (see [this guide](https://github.com/ChristopherProject/Streamtape-Video-Downloader))
- ❌ Vidmoly (bypass with [vidmoly-bot](https://github.com/Z3NTL3/vidmoly-bot))

## Settings

Export [environment variables](https://wiki.archlinux.org/title/Environment_variables) for global settings:

- `ANTICAPTCHA_KEY` (required): in order to use `bs` you've to register an [anticaptcha](https://getcaptchasolution.com/f3w2accaul) account for yourself and obtain the api key from the settings
- `YTDLP_OPTIONS`: pass additional options to download episodes with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- `BS_DIR`: set the downloads directory prefix (must be an absolute path without variables)
- `BS_LANG`: set your preferred language (defaults to `de`)

### Example config

exported from my `~/.bash_profile`

```
export ANTICAPTCHA_KEY="...."
export YTDLP_OPTIONS="{}"
export BS_DIR="/home/manu/tmp"
export BS_LANG="de"
```

## Todo

- [x] error handling
- [ ] language selection
- [x] support doodstream
- [ ] support streamtape
- [ ] support vidmoly
- [ ] add tests (should have been doing TDD straight from the beginning)
