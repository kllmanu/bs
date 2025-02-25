from bs import dns_override
import requests

from bs4 import BeautifulSoup

from bs.burning_series.series import Series
from bs.burning_series.season import Season
from bs.burning_series.episode import Episode


class BurningSeries:

    def __init__(self):
        self.session = requests.Session()

    def bsto(self, url: str) -> str:
        """Get the content of a bs.to page."""

        if url.startswith("https://bs.to"):
            res = self.session.get(url)
        else:
            res = self.session.get(f"https://bs.to/{url}")

        soup = BeautifulSoup(res.text, "html.parser")

        return soup

    @property
    def series(self) -> list[Series]:
        """Parse all the series from the bs.to homepage."""

        soup = self.bsto("andere-serien")
        ahrefs = soup.find("div", id="seriesContainer").find_all("a")
        series = []

        for a in ahrefs:
            series.append(Series(a["href"], a["title"]))

        return series

    def seasons(self, series: Series) -> list[Season]:
        """Parse all the seasons of a series."""

        soup = self.bsto(series.url + "/de")

        ahrefs = soup.find("div", class_="seasons").find_all("a")
        seasons = []

        for a in ahrefs:
            season = Season(a["href"], a.text)
            seasons.append(season)

        return seasons

    def episodes(self, season: list[Season]) -> list[Episode]:
        """Parse all the episodes of all the seasons."""

        episodes = []

        for season in season:
            soup = self.bsto(season.url)
            rows = soup.find("table", class_="episodes").find_all("tr")

            for row in rows:
                hoster = row.select("td:nth-child(3) a")

                if not hoster:
                    continue

                ahref = row.select_one("td:nth-child(1) a")
                episode = Episode(
                    ahref["href"], ahref["title"], season.title, ahref.text
                )

                for host in hoster:
                    episode.add_hoster(host["href"])

                episodes.append(episode)

        return episodes

    def get_token_lid(self, url: str) -> str:
        """Get security token and the host's link id of an episode."""

        soup = self.bsto(url)

        meta = soup.find("meta", attrs={"name": "security_token"})
        player = soup.find("div", class_="hoster-player")

        return [meta["content"], player["data-lid"]]

    def embed(self, token: str, lid: str, ticket: str) -> str | None:
        """Get the video link of an episode."""

        url = "https://bs.to/ajax/embed.php"
        data = {"token": token, "LID": lid, "ticket": ticket}

        res = self.session.post(url, data=data)
        res.raise_for_status()

        if not res.json()["success"]:
            # raise Exception("Failed to get the video link.")
            return None

        return res.json()["link"]
