# bs

![](./header.png)

a burning series CLI to download series, seasons and episodes from [bs.to](https://bs.to)

## Setup

1. Install [poetry](https://python-poetry.org/) and [fzf](https://github.com/junegunn/fzf)
2. Clone the repo and to your local disk
3. Run `poetry install` in the project root.

Your `$SHELL` needs to export an environment variable with your [anticaptcha key](https://anti-captcha.com/de):

```
export ANTICAPTCHA_KEY="...."
export YTDLP_OPTIONS="{}"
export BS_DIR="/home/manu/tmp"
```

## Todo

- [x] error handling
- [ ] language selection
- [ ] support [streamtape](https://github.com/ChristopherProject/Streamtape-Video-Downloader)
- [ ] bypass cloudflare protected hosters (vidmoly)
- [ ] add tests (should have been doing TDD straight from the beginning)
