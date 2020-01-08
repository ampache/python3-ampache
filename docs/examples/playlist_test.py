#!/usr/bin/env python3

import sys

import ampache

# user variables
ampache_url  = 'https://music.server'
ampache_api  = 'mysuperapikey'
ampache_user = 'myusername'

print('\n#######################\nTesting the ampache API\n#######################\n')

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

"""
ping
"""
# did all this work?
my_ping = ampache.ping(ampache_url, ampache_api)
print('\nif your handshake was correct, ping will return your session key and extend the session.')
print('\nPing returned:\n    ', my_ping)
if not my_ping:
     print()
     sys.exit('ERROR: Failed to ping ' + ampache_url)

"""
playlists
"""
#playlists = ampache.playlists(ampache_url, ampache_api)

"""
playlist_create
"""
playlist_create = (ampache.playlist_create(ampache_url, ampache_api, 'python-test', 'private'))
if playlist_create:
    for child in playlist_create:
        if child.tag == 'playlist':
            single_playlist = child.attrib['id']
print('\nplaylist_create created the following id:\n    ', single_playlist)

"""
playlist
"""
#playlist = ampache.playlists(ampache_url, ampache_api, 'python-test', 'private')
#if playlist:
    #for child in playlist:
        #print(child.tag, child.attrib)
        #if child.tag == 'playlist':
        #    single_playlist = child.attrib['id']
        #for subchildren in child:
        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
playlist_add_song
"""
songs = ampache.get_indexes(ampache_url, ampache_api, 'song', '', '', '', '', 10)
for child in songs:
    if child.tag == 'song':
        print(ampache.playlist_add_song(ampache_url, ampache_api, single_playlist, child.attrib['id'], 1))
        print(ampache.playlist_add_song(ampache_url, ampache_api, single_playlist, child.attrib['id'], 1))

"""
playlist_songs
"""
playlist_songs = ampache.playlist_songs(ampache_url, ampache_api, single_playlist)

"""
playlist_remove_song
"""
for child in playlist_songs:
    if child.tag == 'song':
        print(ampache.playlist_remove_song(ampache_url, ampache_api, single_playlist, child.attrib['id']))

"""
playlist_edit
"""
print(ampache.playlist_edit(ampache_url, ampache_api, single_playlist, 'generic', 'public'))


"""
playlist_delete
"""
print(ampache.playlist_delete(ampache_url, ampache_api, single_playlist))

"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
print('    ', ampache.goodbye(ampache_url, ampache_api))

