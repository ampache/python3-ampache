#!/usr/bin/env python3

import sys

import ampache

# user variables
ampache_url = 'https://develop.ampache.dev'
ampache_api = 'demodemo'
ampache_user = 'demo'

# xml or json supported formats
api_format = 'json'

ampacheConnection = ampache.API()
ampacheConnection.set_format(api_format)

"""
encrypt_string
"""
encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)

"""
handshake
"""
print('Connecting to:\n    ', ampache_url)
src_api = ampache_api
ampache_api = ampacheConnection.handshake(ampache_url, encrypted_key, '', 0, '6.0.0')

print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)
