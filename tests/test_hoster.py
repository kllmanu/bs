import pytest

from bs.hoster import Hoster

urls = {
    # Simpsons S01E01
    "doodstream": "https://d0000d.com/d/c44lm0xup99s",
    # Falling Skies S01E01
    "streamtape": "https://streamtape.com/e/WgY832Xl9VIb8kA",
}

doodstream = Hoster.factory(urls["doodstream"])
streamtape = Hoster.factory(urls["streamtape"])


def test_doodstream():
    assert "Simpsons" in doodstream.stream and "download" in doodstream.referer


def test_streamtape():
    print(streamtape.stream)


@pytest.mark.skip(reason="For manually testing the download method")
def test_download():
    doodstream.download("", "test.mp4")
