#!/usr/bin/env python3

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
print('Connecting to', ampache_url)
ampache_api = ampache.handshake(ampache_url, encrypted_key)
print('\nThe ampache handshake for:\n    ', ampache_api, '\n\nReturned the following session key:\n    ', ampache_api)

"""
ping
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
user
"""
myuser = ampache.user(ampache_url, ampache_api, ampache_user)
print('\ndata for my user account details:')
for child in myuser:
    print(child.tag, child.attrib)
    print('\nusername    ', child.find('username').text)
    print('create_date ', child.find('create_date').text)
    print('last_seen   ', child.find('last_seen').text)
    print('website     ', child.find('website').text)
    print('state       ', child.find('state').text)
    print('city        ', child.find('city').text)
    print('fullname    ', child.find('fullname').text)

"""
advanced_search

THERE ARE ADDITIONAL THINGS THAT I NEED TO WORK OUT ON THIS

THIS IS THE FULL SEARCH QUERY FUNCTION WITH MANY RULES AVAILABLE
"""
search_song = ampache.advanced_search(ampache_url, ampache_api, 'song', 0, 1)
for child in search_song:
    if child.tag == 'total_count':
        continue
    print('\nadvanced search found a song')
    print(child.find('filename').text)
    print(child.find('title').text)
    print(child.find('track').text)
    print(child.find('artist').text)
    song_title = child.find('title').text
search_album = ampache.advanced_search(ampache_url, ampache_api, 'album', 0, 1)
search_artist = ampache.advanced_search(ampache_url, ampache_api, 'artist', 0, 1)

"""
album
"""
for child in ampache.album(ampache_url, ampache_api, single_album, ''):
    if child.tag == 'album':
        print('\nsearching for an album with this id', single_album)
        print(child.tag, child.attrib)
        album_title = child.find('name').text

"""
album_songs
"""
print('\nsearching for songs that are in this album', single_album)
for child in ampache.album_songs(ampache_url, ampache_api, single_album, '', 0):
    if child.tag == 'song':
        print(child.tag, child.attrib)
"""
albums
"""
print('\nSearching for albums called', album_title)
albums = ampache.albums(ampache_url, ampache_api, 1, 0, 0, album_title, 0, 0, '')
for child in albums:
    if child.tag == 'total_count':
        continue
    print('\nadvanced search found an album')
    print('Album title ', child.find('name').text)
    print('Album artist', child.find('artist').text)


"""
stats
"""
for child in ampache.stats(ampache_url, ampache_api, 'artist', '', 0, 1, 0, 0):
    if child.tag == 'artist':
        print('\ngetting a random artist using the stats method and found', child.find('name').text)
        single_artist = child.attrib['id']

"""
artist
"""
for child in ampache.artist(ampache_url, ampache_api, single_artist, ''):
    if child.tag == 'artist':
        print('\nsearching for an artist with this id', single_artist)
        print(child.tag, child.attrib)
"""
artist_albums
"""
print('\nsearching for albums that are in this artist', single_artist)
for child in ampache.artist_albums(ampache_url, ampache_api, single_artist, '', 0):
    if child.tag == 'album':
        print(child.tag, child.attrib)
"""
artist_songs
"""
print('\nsearching for songs that are in this artist', single_artist)
for child in ampache.artist_songs(ampache_url, ampache_api, single_artist, '', 0):
    if child.tag == 'song':
        print(child.tag, child.attrib)
"""
artists
"""
print(ampache.artists(ampache_url, ampache_api))

"""
catalog_action
"""
print("\nampache.catalog_action was sent an intentionally bad task. 'clean' does not exist so return False")
print(ampache.catalog_action(ampache_url, ampache_api, 'clean', 2))
print()

"""
democratic
"""
#print(ampache.democratic(ampache_url, ampache_api))

"""
flag
"""
#print(ampache.flag(ampache_url, ampache_api))

"""
followers
"""
print(ampache.followers(ampache_url, ampache_api, ampache_user))

"""
following
"""
print(ampache.following(ampache_url, ampache_api, ampache_user))

"""
friends_timeline
"""
print(ampache.friends_timeline(ampache_url, ampache_api))

"""
last_shouts
"""
print(ampache.last_shouts(ampache_url, ampache_api, ampache_user))

"""
localplay
"""
#print(ampache.localplay(ampache_url, ampache_api))

"""
playlists
"""
print(ampache.playlists(ampache_url, ampache_api))

"""
playlist
"""
print(ampache.playlist(ampache_url, ampache_api, single_playlist))

"""
playlist_songs
"""
print(ampache.playlist_songs(ampache_url, ampache_api, single_playlist))

"""
playlist_create
"""
#print(ampache.playlist_create(ampache_url, ampache_api))

"""
playlist_edit
"""
#print(ampache.playlist_edit(ampache_url, ampache_api))

"""
playlist_add_song
"""
#print(ampache.playlist_add_song(ampache_url, ampache_api))

"""
playlist_remove_song
"""
#print(ampache.playlist_remove_song(ampache_url, ampache_api))

"""
playlist_delete
"""
#print(ampache.playlist_delete(ampache_url, ampache_api))

"""
rate
"""
#print(ampache.rate(ampache_url, ampache_api))

"""
record_play
"""
#print(ampache.record_play(ampache_url, ampache_api))

"""
scrobble
"""
#print(ampache.scrobble(ampache_url, ampache_api))

"""
search_songs
"""
print(ampache.search_songs(ampache_url, ampache_api, song_title))

"""
song
"""
print(ampache.song(ampache_url, ampache_api, song_title))

"""
songs
"""
print(ampache.songs(ampache_url, ampache_api))

"""
tag
"""
print(ampache.tag(ampache_url, ampache_api, ''))

"""
tag_albums
"""
print(ampache.tag_albums(ampache_url, ampache_api))

"""
tag_artists
"""
print(ampache.tag_artists(ampache_url, ampache_api))

"""
tag_songs
"""
#print(ampache.tag_songs(ampache_url, ampache_api))

"""
tags
"""
print(ampache.tags(ampache_url, ampache_api))

"""
timeline
"""
print(ampache.timeline(ampache_url, ampache_api))

"""
toggle_follow
"""
#print(ampache.toggle_follow(ampache_url, ampache_api))

"""
update_from_tags
"""
#print(ampache.update_from_tags(ampache_url, ampache_api))

"""
url_to_song
"""
#print(ampache.url_to_song(ampache_url, ampache_api))

"""
video
"""
#print(ampache.video(ampache_url, ampache_api))

"""
videos
"""
#print(ampache.videos(ampache_url, ampache_api))

"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
print('    ', ampache.goodbye(ampache_url, ampache_api))
