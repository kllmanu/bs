from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

from bs.burning_series import BurningSeries
from bs.anticaptcha import decaptcha
from bs.hoster import Hoster
from bs.util import select, green, blue, magenta


def main() -> None:
    bs = BurningSeries()
    fzf = FzfPrompt()

    series = bs.series
    selected = fzf.prompt(series, "--exact --reverse")
    series = select(series, selected)[0]

    seasons = bs.seasons(series)
    selected = fzf.prompt(seasons, "--multi --reverse --bind 'ctrl-t:toggle-all'")
    seasons = select(seasons, selected)

    episodes = bs.episodes(seasons)

    all = input("Do you want to download all the episodes? (Y/n): ").strip().lower()

    if all == "n":
        selected = fzf.prompt(episodes, "--multi --reverse --bind 'ctrl-t:toggle-all'")
        episodes = select(episodes, selected)

    for episode in episodes:

        supported_hosts = ("VOE", "Vidoza")
        filtered_hosts = [host for host in episode.hosters if host in supported_hosts]

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


if __name__ == "__main__":
    getenv("ANTICAPTCHA_KEY") or exit("ANTICAPTCHA_KEY is not set.")
    main()
