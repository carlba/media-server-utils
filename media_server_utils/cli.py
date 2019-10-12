# -*- coding: utf-8 -*-
"""Console script for media_server_utils"""
import sys

import click
from click.testing import CliRunner

from . import core


def is_debugging():
    return not (sys.gettrace() is None)


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('transmission_url')
@click.argument('torrentleech_username', envvar='TORRENTLEECH_USERNAME')
@click.argument('torrentleech_password', envvar='TORRENTLEECH_PASSWORD')
@click.argument('torrentleech_rss_key', envvar='TORRENTLEECH_RSS_KEY')
def add_torrents_from_folder(path, transmission_url, torrentleech_username, torrentleech_password, torrentleech_rss_key):
    """Console script for media_server_utils."""
    core.add_torrents_from_folder(path, transmission_url, torrentleech_username, torrentleech_password, torrentleech_rss_key)
    return 0


if __name__ == "__main__":
    if is_debugging():
        runner = CliRunner()
        runner.invoke(add_torrents_from_folder)
    else:
        add_torrents_from_folder()
