from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

import os
import sys

from bs.burning_series import BurningSeries
from bs.anticaptcha import decaptcha
from bs.hoster import Hoster
from bs.util import select, green, blue, magenta


def run() -> None:
    bs = BurningSeries()
    fzf = FzfPrompt()

    series = bs.series
    selected = fzf.prompt(series, "--exact --reverse")
    series = select(series, selected)[0]

    seasons = bs.seasons(series)
    selected = fzf.prompt(seasons, "--multi --reverse --bind 'ctrl-t:toggle-all'")
    seasons = select(seasons, selected)

    episodes = bs.episodes(seasons)

    # select episodes
    question = "Do you want to select all the episodes? (Y/n): "
    prompt = input(question).strip().lower()

    if prompt == "n":
        selected = fzf.prompt(episodes, "--multi --reverse --bind 'ctrl-t:toggle-all'")
        episodes = select(episodes, selected)

    # confirmation
    question = f"Start downloading {len(episodes)} episode(s) from {len(seasons)} season(s)? (Y/n): "
    prompt = input(question).strip().lower()

    if prompt == "n":
        sys.exit(0)

    for episode in episodes:
        filtered_hosts = []

        for host in episode.hosters:
            if not "Vidmoly" in host:
                filtered_hosts.append(host)

        for host in filtered_hosts:

            if episode.exists(series):
                print(f"{green(episode.filename)} already exists.")
                break

            url = None

            while not url:
                print(f"Trying to get the video link for {blue(host)}")
                [token, lid] = bs.get_token_lid(host)

                print(f"Solving captcha...")
                ticket = decaptcha(host)

                print(f"Embedding link id...")
                url = bs.embed(token, lid, ticket)

            print(f"Downloading {green(episode.filename)} from {magenta(url)}\n")
            video = Hoster.factory(url)
            video.download(series.folder, episode.filename)
            print()


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
