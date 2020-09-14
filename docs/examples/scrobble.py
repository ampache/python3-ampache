#!/usr/bin/env python3

import ampache
import sys
import time

from multiprocessing import Process

# user variables
ampache_url = 'https://music.server'
ampache_api = 'mysuperapikey'
ampache_user = 'myusername'

"""
encrypt_string
"""
encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

"""
handshake
"""
print('Connecting to:\n    ', ampache_url)
ampache_session = ampache.handshake(ampache_url, encrypted_key)
print('\nThe ampache handshake for:\n    ',
      ampache_api, '\n\nReturned the following session key:\n    ',
      ampache_session)

"""
if you didn't connect you can't do anything
"""
if not ampache_api:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

"""
scrobble
"""
if ampache_session:
    Process(target=ampache.scrobble,
            args=(ampache_url, ampache_session, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
                  '', '', int(time.time()))).start()
