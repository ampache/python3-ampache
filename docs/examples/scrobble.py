#!/usr/bin/env python3

import sys
import time

import ampache

from multiprocessing import Process

# user variables
ampache_url  = 'https://music.server'
ampache_api  = 'mysuperapikey'
ampache_user = 'myusername'

"""
encrypt_string
"""
encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

"""
handshake
"""
# processed details
print('Connecting to:\n    ', ampache_url)
src_api = ampache_api
ampache_api = ampache.handshake(ampache_url, encrypted_key)
print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
     print()
     sys.exit('ERROR: Failed to connect to ' + ampache_url)

Process(target=ampache.scrobble,
        args=(ampache_url, ampache_api, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
              '', '', '', int(time.time()))).start()
