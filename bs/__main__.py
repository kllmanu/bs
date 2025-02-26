from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv

load_dotenv()

import os
import sys

from bs.burning_series import BurningSeries
from bs.anti_captcha import AntiCaptcha
from bs.hoster import Hoster
from bs.util import select, green, blue, magenta

ANTICAPTCHA_KEY = os.getenv("ANTICAPTCHA_KEY")
WEBSITE_KEY = "6Ldd07ogAAAAACktG1QNsMTcUWuwcwtkneCnPDOL"
LANGUAGE = os.getenv("BS_LANG", "de")
DIR = os.getenv("BS_DIR", "")


def run() -> None:
    bs = BurningSeries(LANGUAGE, DIR)
    ac = AntiCaptcha(ANTICAPTCHA_KEY, WEBSITE_KEY)
    fzf = FzfPrompt()

    # select series
    series = bs.series()
    selected = fzf.prompt(series, "--exact --reverse")
    series = select(series, selected)[0]

    # select seasons
    seasons = bs.seasons(series)
    selected = fzf.prompt(seasons, "--multi --reverse --bind 'ctrl-t:toggle-all'")
    seasons = select(seasons, selected)

    # select episodes
    episodes = bs.episodes(series, seasons)
    question = "Do you want to select all the episodes? (Y/n): "
    prompt = input(question).strip().lower()

    if prompt == "n":
        selected = fzf.prompt(episodes, "--multi --reverse --bind 'ctrl-t:toggle-all'")
        episodes = select(episodes, selected)

    # confirm download
    question = f"Start downloading {len(episodes)} episode(s) from {len(seasons)} season(s)? (Y/n): "
    prompt = input(question).strip().lower()

    if prompt == "n":
        sys.exit(0)

    for episode in episodes:
        if episode.exists():
            print(f"{green(episode.filename)} already exists.")
            continue

        for host in episode.filtered_hosts:

            url = None

            while not url:
                print(f"Trying to get the video link for {blue(host)}")
                [token, lid] = bs.get_token_lid(host)

                print(f"Solving captcha...")
                ticket = ac.solve(host)

                print(f"Embedding link id...")
                url = bs.embed(token, lid, ticket)

            print(f"Downloading {green(episode.filename)} from {magenta(url)}\n")
            video = Hoster.factory(url)
            video.download(DIR, series.folder, episode.filename)
            print()

            if episode.exists():
                break


def main() -> None:
    if "ANTICAPTCHA_KEY" not in os.environ:
        print("Please set the ANTICAPTCHA_KEY environment variable.")
        sys.exit(1)

    try:
        run()
    except (IndexError, KeyboardInterrupt):
        sys.exit(0)


if __name__ == "__main__":
    main()
