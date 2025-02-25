from bs.hoster import Hoster


class Vidoza(Hoster):

    @property
    def stream(self) -> str | None:
        return self.url
