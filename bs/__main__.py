from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv

load_dotenv()

import os

from bs.burning_series import BurningSeries
from bs.anticaptcha import decaptcha
from bs.models import Hoster


def select(items, selected) -> list:
    """Retrieve the original object after selection."""

    # Create a mapping from string representation to object
    repr_to_obj = {repr(item): item for item in items}

    # Get the original object(s)
    selected_objects = [repr_to_obj[s] for s in selected]

    return selected_objects


def main() -> None:
    bs = BurningSeries()
    fzf = FzfPrompt()

    series = bs.series
    selected = fzf.prompt(series, "--exact --reverse")
    series = select(series, selected)

    seasons = bs.seasons(series[0])
    selected = fzf.prompt(seasons, "--multi --reverse --bind 'ctrl-t:toggle-all'")
    seasons = select(seasons, selected)

    episodes = bs.episodes(seasons)

    all = input("Do you want to download all the episodes? (Y/n): ").strip().lower()

    if all == "n":
        selected = fzf.prompt(episodes, "--multi --reverse --bind 'ctrl-t:toggle-all'")
        episodes = select(episodes, selected)

    if not os.path.exists(series[0].folder):
        os.mkdir(series[0].folder)

    for episode in episodes:
        if os.path.exists(episode.filename):
            continue

        for host in episode.hosters:
            [token, lid] = bs.get_token_lid(host)
            ticket = decaptcha(host)
            url = bs.embed(token, lid, ticket)

            video = Hoster.factory(url)
            video.download(series[0].folder, episode.filename)


if __name__ == "__main__":
    main()
