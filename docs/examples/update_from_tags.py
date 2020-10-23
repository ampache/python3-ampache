#!/usr/bin/env python3

import ampache
import configparser
import os
import sys
import time

from multiprocessing import Process

# user variables
url = 'https://music.server'
api = 'mysuperapikey'
user = 'myusername'
if os.path.isfile('ampyche.conf'):
    conf = configparser.RawConfigParser()
    conf.read('ampyche.conf')
    url = conf.get('conf', 'ampache_url')
    user = conf.get('conf', 'ampache_user')
    api = conf.get('conf', 'ampache_apikey')
else:
    try:
        if sys.argv[1] and sys.argv[2] and sys.argv[3]:
            url = sys.argv[1]
            api = sys.argv[2]
            user = sys.argv[3]
    except IndexError:
        sys.exit('ERROR: get your arguments correct')

limit = 4
offset = 0
api_version = '5.0.0'
api_format = 'json'
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=164215&uid=2&player=api&name=Hellyeah%20-%20-.mp3'


"""
encrypt_string
"""
encrypted_key = ampache.encrypt_string(api, user)

"""
handshake
"""
print('Connecting to:\n    ', url)
ampache_session = ampache.handshake(url, encrypted_key)
print('\nThe ampache handshake for:\n    ',
      api, '\n\nReturned the following session key:\n    ',
      ampache_session)

"""
if you didn't connect you can't do anything
"""
if not ampache_session:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

#list to update
artist_list = [9,10,13,14,15,16,18,19,20]

"""
update_from_tags
"""
if ampache_session:
    for artist in artist_list:
        print(artist)
        ampache.update_from_tags(url, ampache_session, 'artist', artist, api_format)