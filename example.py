#!/usr/bin/env python3

import ampache

# user variables
ampache_url   = 'https://music.server'
my_api_key    = 'mysuperapikey'
user          = 'myusername'

print('\n#######################\nTesting the ampache API\n#######################\n')

"""
'handshake'
"""
# processed details
encrypted_key = ampache.encrypt_string(my_api_key, user)
ampache_api   = ampache.handshake(ampache_url, encrypted_key)
print('The ampache handshake for:\n    ', my_api_key, '\n\nReturned the following session key:\n    ', ampache_api)

"""
'ping'
"""
# did all this work?
print('\nif your handshake was correct, ping will return your session key and extend the session.')
print('\nPing returned:\n    ', ampache.ping(ampache_url, ampache_api))

"""
get_indexes
'song'|'album'|'artist'|'playlist'
"""
songs     = ampache.get_indexes(ampache_url, ampache_api, 'song', '', '', '', '', 1)
albums    = ampache.get_indexes(ampache_url, ampache_api, 'album', '', '', '', '', 1)
artists   = ampache.get_indexes(ampache_url, ampache_api, 'artist', '', '', '', '', 1)
playlists = ampache.get_indexes(ampache_url, ampache_api, 'playlist', '', '', '', '', 1)

print('\nget_indexes is good for listing all the ids\n')
print('This server has:', songs.find('total_count').text, 'songs')
print('This server has:', albums.find('total_count').text, 'albums')
print('This server has:', artists.find('total_count').text, 'artists')
print('This server has:', playlists.find('total_count').text, 'playlists\n')

for child in songs:
    if child.tag == 'song':
        single_song = child.attrib['id']
for child in albums:
    if child.tag == 'album':
        single_album = child.attrib['id']
for child in artists:
    if child.tag == 'artist':
        single_artist = child.attrib['id']
for child in playlists:
    if child.tag == 'playlist':
        single_playlist = child.attrib['id']

"""
advanced_search
"""

"""
album
"""
for child in ampache.album(ampache_url, ampache_api, single_album, ''):
    if child.tag == 'album':
        print('searching for an album with this id', single_album)
        print(child.tag, child.attrib)

"""
album_songs
"""
print('\nsearching for songs with this that are in this album', single_album)
for child in ampache.album_songs(ampache_url, ampache_api, single_album, '', 0):
    if child.tag == 'song':
        print(child.tag, child.attrib)
"""
albums
"""

"""
artist
"""

"""
artist_albums
"""

"""
artist_songs
"""

"""
artists
"""

"""
catalog_action
"""

"""
democratic
"""

"""
encrypt_string
"""

"""
flag
"""

"""
followers
"""

"""
following
"""

"""
friends_timeline
"""

"""
last_shouts
"""

"""
localplay
"""

"""
playlist
"""

"""
playlist_add_song
"""

"""
playlist_create
"""

"""
playlist_delete
"""

"""
playlist_edit
"""

"""
playlist_remove_song
"""

"""
playlist_songs
"""

"""
playlists
"""

"""
rate
"""

"""
record_play
"""

"""
scrobble
"""

"""
search_songs
"""

"""
song
"""

"""
songs
"""

"""
stats
"""

"""
tag
"""

"""
tag_albums
"""

"""
tag_artists
"""

"""
tag_songs
"""

"""
tags
"""

"""
time
"""

"""
timeline
"""

"""
toggle_follow
"""

"""
update_from_tags
"""

"""
url_to_song
"""

"""
urllib
"""

"""
user
"""

"""
video
"""

"""
videos
"""

"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
print('    ', ampache.goodbye(ampache_url, ampache_api))


