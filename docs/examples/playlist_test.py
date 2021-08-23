#!/usr/bin/env python3

import sys

import ampache

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
# processed details
print('Connecting to:\n    ', ampache_url)
src_api = ampache_api
ampache_api = ampacheConnection.handshake(ampache_url, encrypted_key)
print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
    print()
    sys.exit('ERROR: Failed to connect to ' + ampache_url)

"""
ping
"""
# did all this work?
my_ping = ampacheConnection.ping(ampache_url, ampache_api)
print('\nif your handshake was correct, ping will return your session key and extend the session.')
print('\nPing returned:\n    ', my_ping)
if not my_ping:
    print()
    sys.exit('ERROR: Failed to ping ' + ampache_url)

"""
playlists
"""
playlists = ampacheConnection.playlists()

"""
playlist_create
"""
playlist_create = (ampacheConnection.playlist_create('python-test', 'private'))
if playlist_create:
    for child in playlist_create:
        if child.tag == 'playlist':
            single_playlist = child.attrib['id']
print('\nplaylist_create created the following id:\n    ', single_playlist)

"""
playlist
"""
playlist = ampacheConnection.playlists('python-test', 'private')
if playlist:
    for child in playlist:
        print(child.tag, child.attrib)
        if child.tag == 'playlist':
            single_playlist = child.attrib['id']
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
playlist_add_song
"""
songs = ampacheConnection.get_indexes('song', False, False, False, False, False, 0, 10)

for child in ampacheConnection.get_id_list(songs, 'song'):
    ampacheConnection.playlist_add_song(single_playlist, child, 1)

"""
playlist_songs
"""
playlist_songs = ampacheConnection.playlist_songs(single_playlist)

"""
playlist_remove_song
"""
for child in ampacheConnection.get_id_list(playlist_songs, 'song'):
    ampacheConnection.playlist_remove_song(single_playlist, child)

"""
playlist_edit
"""


"""
playlist_delete
"""
ampacheConnection.playlist_delete(single_playlist)

"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
ampacheConnection.goodbye()
