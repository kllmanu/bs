import requests

import re
import base64

from bs.hoster import Hoster


class VOE(Hoster):

    @property
    def stream(self) -> str | None:
        res = requests.get(self.url)

        # check for redirect first
        redirect = r"window\.location\.href\s*=\s*'(https?://[^\']+)'"
        match = re.search(redirect, res.text)

        if match:
            res = requests.get(match.group(1))

            hls = r"'hls':\s*'([^']+)'"
            match = re.search(hls, res.text)

            if match:
                return base64.b64decode(match.group(1)).decode("utf-8")
