import requests
import bs4
import time

from bs.hoster import Hoster


class Doodstream(Hoster):

    @property
    def stream(self) -> str | None:
        session = requests.Session()

        res = session.get(self.url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        download = soup.select_one('a[href^="/download/"]')["href"]
        self.referer = f"https://d0000d.com{download}"

        time.sleep(5)

        res = session.get(self.referer)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        link = soup.select_one("a")["href"]

        return link
