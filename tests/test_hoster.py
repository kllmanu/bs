import pytest

from bs.hoster import Hoster

urls = {
    # Simpsons S01E01
    "doodstream": "https://d0000d.com/d/c44lm0xup99s",
}

doodstream = Hoster.factory(urls["doodstream"])


def test_doodstream():
    assert "Simpsons" in doodstream.stream and "download" in doodstream.referer


@pytest.mark.skip(reason="For manually testing the download method")
def test_download():
    doodstream.download("", "test.mp4")
