#!/usr/bin/env python3

import ampache
import sys
import time

from multiprocessing import Process

# user variables
ampache_url = 'https://develop.ampache.dev'
ampache_api = 'demodemo'
ampache_user = 'demo'

ampacheConnection = ampache.API()

"""
encrypt_string
"""
encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)


"""
handshake
"""
print('Connecting to:\n    ', ampache_url)
ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key)
print('\nThe ampache handshake for:\n    ',
      ampache_api, '\n\nReturned the following session key:\n    ',
      ampache_session)

"""
if you didn't connect you can't do anything
"""
if not ampache_session:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

"""
scrobble
"""
if ampache_session:
    Process(target=ampacheConnection.scrobble,
            args=('Beneath The Cold Clay', 'Crust', '...and a Dirge Becomes an Anthem',
                  '', '', '', int(time.time()))).start()
