# -*- coding: utf-8 -*-
"""Main module"""

import json

import requests
import transmissionrpc
from pathlib import Path
from unicodedata import normalize
import guessit


from media_server_utils.utils import load_environment, configure_logging

CATEGORIES = [27, 32]
REQUEST_HEADERS = {'User-Agent': 'curl/7.54.0'}
PROCESSED_FILE = 'processed.json'
processeds = {}

load_environment()
logger = configure_logging('core')


def normalize_unicode(text):
    if isinstance(text, str):
        # Convert to combined form for better search results
        return normalize('NFC', text)
    return text


def login(username: str, password: str):
    data = {'username': username, 'password': password}
    login = requests.post('https://www.torrentleech.org/user/account/login/',
                          data=data, headers=REQUEST_HEADERS, allow_redirects=True)
    if login.url.endswith(u'/user/account/login/'):
        raise Exception('Failed to login')
    return login


def get_filter_url():
    return '/categories/{}'.format(','.join(str(c) for c in CATEGORIES))


def load_processed():
    global processeds
    try:
        with open(PROCESSED_FILE, 'r') as json_file:
            processeds = json.load(json_file)
    except FileNotFoundError as e:
        if e.errno == 2:
            logger.debug(f'No download file exists creating a new one')


def log_error(name, reason, action='no_download'):
    if name not in processeds:
        logger.info(f'Name: {name:75s} Action: {action} Reason: {reason}')
        processeds[name] = {'action': action, 'reason': reason}
        with open(PROCESSED_FILE, 'w') as json_file:
            json.dump(processeds, json_file, indent=4)
    else:
        logger.info(f'Name: {name:75s} Action: {action} Reason: {reason}')


def log_success(name, download_path, output_path, action='download'):
    processeds[name] = {'action': action, 'download_path': download_path}
    logger.info(f'Name: {name:75s} Action: {action} Output Path: {output_path} Download Path: {download_path}')
    with open(PROCESSED_FILE, 'w') as json_file:
        json.dump(processeds, json_file, indent=4)


def add_torrents_from_folder(path: str, transmission_url: str, torrentleech_username: str, torrentleech_password: str, torrentleech_rss_key):
    tc = transmissionrpc.Client(transmission_url, port=9091, user='cada', password='bajskorv')
    load_processed()
    for dirname in Path(path).glob('**'):
        matches = guessit.guessit(dirname.name)
        if matches.get('type') == 'episode' and len(matches.keys()) > 2:
            if any([processed for processed in processeds if processed in str(dirname)]):
                log_error(dirname.name, 'already downloaded as part of '
                                        'a season pack or already downloaded')
                continue

            filter_url = get_filter_url()
            login_request = login(torrentleech_username, torrentleech_password)
            query = normalize_unicode(dirname.name).replace(":", "")

            url = f'https://www.torrentleech.org/torrents/browse/list/query/{query}/{filter_url}'

            results = requests.get(url, headers=REQUEST_HEADERS,
                                   cookies=login_request.cookies).json()

            if results['numFound'] > 0:
                torrent = results['torrentList'][0]
                if not torrent['filename'] == f'{dirname.name}.torrent':
                    log_error(dirname.name, f'Torrent {dirname.name} no download filename '
                                            f'mismatch {torrent["filename"]} '
                                            f'!= {dirname.name}.torrent')
                    continue

                torrent_url = (f'https://www.torrentleech.org/rss/download'
                               f'/{torrent["fid"]}/{torrentleech_rss_key}/{torrent["filename"]}')

                download_path = str(dirname.parent).replace("/Volumes", "")
                tc.add_torrent(torrent_url, download_dir=download_path)
                log_success(dirname.name, download_path, dirname)
            else:
                log_error(dirname.name, 'no search results', action='no_download')
