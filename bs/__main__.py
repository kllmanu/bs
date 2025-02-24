from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv
from time import sleep

load_dotenv()

from bs.burning_series import BurningSeries
from bs.anticaptcha import decaptcha
from bs.models import Hoster


def blue(text) -> str:
    """Return the text in blue color."""
    return f"\033[1;34m{text}\033[0m"


def green(text) -> str:
    """Return the text in green color."""
    return f"\033[1;32m{text}\033[0m"


def magenta(text) -> str:
    """Return the text in magenta color."""
    return f"\033[1;35m{text}\033[0m"


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

        # todo: fix hoster selection
        filtered_hosts = [
            host for host in episode.hosters if "VOE" in host or "Vidoza" in host
        ]

        for host in filtered_hosts:

            if episode.exists(series):
                print(f"{green(episode.filename)} already exists.")
                continue

            [token, lid] = bs.get_token_lid(host)

            print(f"Solving captcha for {blue(host)}")
            ticket = decaptcha(host)

            print(f"Embedding link id {lid}")
            url = bs.embed(token, lid, ticket)

            print(f"Downloading {green(episode.filename)} from {magenta(url)}")
            video = Hoster.factory(url)
            video.download(series.folder, episode.filename)

            print("Cooling down 5 mins...")
            sleep(300)


if __name__ == "__main__":
    main()
