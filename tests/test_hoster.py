import pytest

from bs.hoster import Hoster

urls = {
    # Stargate SG-1 S01E01
    "voe": "https://voe.sx/llnp6fblsl2w",
    # Der gefährlichste Job Alaska's S20E01
    "vidoza": "https://vidoza.net/embed-71earzhda3ma.html",
    # Simpsons S01E01
    "doodstream": "https://d0000d.com/d/c44lm0xup99s",
    # Falling Skies S01E01
    "streamtape": "https://streamtape.com/e/WgY832Xl9VIb8kA",
}

voe = Hoster.factory(urls["voe"])
vidoza = Hoster.factory(urls["vidoza"])
doodstream = Hoster.factory(urls["doodstream"])
streamtape = Hoster.factory(urls["streamtape"])


def test_voe():
    assert "m3u8" in voe.stream


def test_vidoza():
    assert vidoza.url == vidoza.stream


def test_doodstream():
    assert "Simpsons" in doodstream.stream


def test_streamtape():
    assert "get_video" in streamtape.stream


def test_download():
    doodstream.download("/tmp", "bs", "test.mp4")
