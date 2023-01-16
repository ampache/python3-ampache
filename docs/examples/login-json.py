#!/usr/bin/env python3

import sys

import ampache

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
ampache_api = ampache.handshake(ampache_url, encrypted_key, '', 0, '390001', 'json')
print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
     print()
     sys.exit('ERROR: Failed to connect to ' + ampache_url)
