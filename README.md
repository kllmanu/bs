# bs

![](./header.png)

## Features

- download series, seasons and episodes using [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **solves captchas** with the help of [Anti Captcha](https://getcaptchasolution.com/f3w2accaul) API
- runs totally unattended (retries on error)
- skips already downloaded files
- supports multiple hosters (with fallback)
- organizes downloads in `series/S{##}E{##}_{title}.mp4` style

## Setup

1. Install [poetry](https://python-poetry.org/), [fzf](https://github.com/junegunn/fzf) and [yt-dlp](https://github.com/yt-dlp/yt-dlp)
2. Clone the repo and run `poetry install` in the project root
3. Run `poetry run bs` to start the downloader

## Supported hosters

- ✅ VOE
- ✅ Vidoza
- ✅ Doodstream
- ✅ Streamtape (thanks to [this guide](https://github.com/ChristopherProject/Streamtape-Video-Downloader))
- ❌ Vidmoly (bypass with [vidmoly-bot](https://github.com/Z3NTL3/vidmoly-bot))

## Anticaptcha

In order to speed up things it makes sense to increase the **maximum bid** in your anticaptcha account. I've set it to $10 for 1000 captchas (twice the default setting) and I recommend you to do the same.

## Settings

Export [environment variables](https://wiki.archlinux.org/title/Environment_variables) for global settings:

- `ANTICAPTCHA_KEY` (required): register an [anticaptcha](https://getcaptchasolution.com/f3w2accaul) account and obtain the api key from the settings
- `BS_DIR`: set the download directory prefix (must be an absolute path without variables)
- `BS_LANG`: set your preferred language (defaults to `de`)

### Example config

exported from my `~/.bash_profile`

```
export ANTICAPTCHA_KEY="...."
export BS_DIR="/home/manu/tmp"
export BS_LANG="de"
```

## Todo

- [x] error handling
- [x] language selection
- [x] support doodstream
- [x] support streamtape
- [ ] support vidmoly
- [ ] add tests (should have been doing TDD straight from the beginning)
