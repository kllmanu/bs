from pyfzf.pyfzf import FzfPrompt
from dotenv import load_dotenv

load_dotenv()

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
    selected_series = select(series, selected)

    seasons = bs.seasons(selected_series[0])
    selected = fzf.prompt(seasons, "--multi --reverse")
    selected_seasons = select(seasons, selected)

    episodes = bs.episodes(selected_seasons)

    for episode in episodes:
        for host in episode.hosters:
            [token, lid] = bs.get_token_lid(host)
            ticket = decaptcha(host)
            url = bs.embed(token, lid, ticket)

            video = Hoster.new(url)
            video.download(episode.filename)


if __name__ == "__main__":
    main()
