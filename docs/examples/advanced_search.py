#!/usr/bin/env python3

import ampache
import sys

# user variables
ampache_url = 'https://develop.ampache.dev'
ampache_api = 'demodemo'
ampache_user = 'demo'

"""
encrypt_string
"""
ampacheConnection = ampache.API()
encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)

"""
handshake
"""
print('Connecting to:\n    ', ampache_url)
src_api = ampache_api
ampache_api = ampacheConnection.handshake(ampache_url, encrypted_key, False, False, '420000')

print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

print('\nPing returned:\n    ', ampacheConnection.ping(ampache_url, ampache_api))
print()

"""
advanced_search
"""
print("\nadvanced_search\nsearch song year = 2009 or CONTAINS artist 'Pro'\n")
search_rules = [['year', 2, 2009], ['artist', 0, 'Pro']]
search_song = ampacheConnection.advanced_search(search_rules, 'or', 'song', 0, 0)
for child in search_song:
    if child.tag == 'total_count':
        continue
    print(child.tag, child.attrib)
    print(child.find('filename').text)
    
"""
Close your session when you're done
"""
print('\nWhen you are finished it\'s a good idea to kill your session')
ampacheConnection.goodbye()
