import requests
import bs4
import re

from bs.hoster import Hoster


class Streamtape(Hoster):

    @property
    def stream(self) -> str | None:
        session = requests.Session()

        if "/e/" in self.url:
            url = self.url.replace("/e/", "/v/")

        res = session.get(url)
        res.raise_for_status()

        norobot_link_pattern = re.compile(
            r"document\.getElementById\('norobotlink'\)\.innerHTML = (.+?);"
        )
        norobot_link_matcher = norobot_link_pattern.search(res.text)

        if norobot_link_matcher:
            norobot_link_content = norobot_link_matcher.group(1)

            token_pattern = re.compile(r"token=([^&']+)")
            token_matcher = token_pattern.search(norobot_link_content)

            if token_matcher:
                token = token_matcher.group(1)

                soup = bs4.BeautifulSoup(res.text, "html.parser")
                div_element = soup.select_one("div#ideoooolink[style='display:none;']")

                if div_element:
                    streamtape = div_element.get_text()
                    full_url = f"https:/{streamtape}&token={token}"

                    return f"{full_url}&dl=1s"
