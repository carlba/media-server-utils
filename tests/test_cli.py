# -*- coding: utf-8 -*-
from click.testing import CliRunner

from media_server_utils.cli import add_torrents_from_folder


def test_main_returns_correct_output():
    runner = CliRunner()
    result = runner.invoke(add_torrents_from_folder)
