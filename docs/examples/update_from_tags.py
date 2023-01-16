#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import sys
import time

import ampache

# user variables
ampache_url = 'https://develop.ampache.dev'
ampache_api = 'demodemo'
ampache_user = 'demo'

# xml or json supported formats
api_format = 'json'
api_version = '5.0.0'

"""
handshake
"""
print('Connecting to:\n    ', ampache_url)
ampacheConnection = ampache.API()
ampacheConnection.set_debug(False)
ampacheConnection.set_format(api_format)
encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)
ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key, '', 0, api_version)

if not ampache_api:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

my_list = [1]
# for each artist get their albums and update_from tags to help keep alive while updating
for artist in my_list:
    print("\nArtist:", artist)
    albums = ampacheConnection.artist_albums(artist)
    for child in albums['album']:
        print("-------", child['name'], "-", child['artist']['name'])
        ampacheConnection.ping(ampache_url, ampache_session, api_version)
        ampacheConnection.update_from_tags('album', int(child['id']))

