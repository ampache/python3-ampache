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
ampache_api = ampache.handshake(ampache_url, encrypted_key, '', 0, '390001', 'xml')
print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
     print()
     sys.exit('ERROR: Failed to connect to ' + ampache_url)

print('\nPing returned:\n    ', ampache.ping(ampache_url, ampache_api, 'json'))
print()

"""
advanced_search
"""
print('\nadvanced_search\nmetadata, BPM, is greater than, 200\n')
search_rules = [['metadata', 8, 200, 9]]
search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'song', 0, 0, 'xml')
if search_song:
    for child in search_song:
        if child.tag == 'total_count':
            continue
        print(child.tag, child.attrib)
        print(child.find('filename').text)

print("\nadvanced_search\nsearch song year = 1999 and CONTAINS artist 'Prodigy'\n")
search_rules = [['year', 2, 1999], ['artist', 0, 'Prodigy']]
search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'song', 0, 0, 'xml')
if search_song:
    for child in search_song:
        if child.tag == 'total_count':
            continue
        print(child.tag, child.attrib)
        print(child.find('filename').text)
    
"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
print('    ', ampache.goodbye(ampache_url, ampache_api, 'xml'))