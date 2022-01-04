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
ampache_api = ampache.handshake(ampache_url, encrypted_key, False, False, '400004', 'json')
print('\nThe ampache handshake for:\n    ', src_api, '\n\nReturned the following session key:\n    ', ampache_api)
if not ampache_api:
     print()
     sys.exit('ERROR: Failed to connect to ' + ampache_url)

"""
ping
"""
# did all this work?
my_ping = ampache.ping(ampache_url, ampache_api, 'json')
print('\nif your handshake was correct, ping will return your session key and extend the session.')
print('\nPing returned:\n    ', my_ping)
if not my_ping:
     print()
     sys.exit('ERROR: Failed to ping ' + ampache_url)
"""
get_indexes
'song'|'album'|'artist'|'playlist'
"""
songs     = ampache.get_indexes(ampache_url, ampache_api, 'song', '', '', '', '', 4, 'json')
albums    = ampache.get_indexes(ampache_url, ampache_api, 'album', '', '', '', '', 4, 'json')
artists   = ampache.get_indexes(ampache_url, ampache_api, 'artist', '', '', '', '', 4, 'json')
playlists = ampache.get_indexes(ampache_url, ampache_api, 'playlist', '', '', '', '', 4, 'json')
input("\nPress Enter to continue...\n")
single_song = 16776
single_album = 54185
single_artist = 605
single_playlist = 2069
print('\nget_indexes is good for listing all the ids\n')
#print('This server has:', songs.find('total_count').text, 'songs')
#print('This server has:', albums.find('total_count').text, 'albums')
#print('This server has:', artists.find('total_count').text, 'artists')
#print('This server has:', playlists.find('total_count').text, 'playlists\n')

#for child in songs:
#    if child.tag == 'song':
#        single_song = child.attrib['id']
#for child in albums:
#    if child.tag == 'album':
#        single_album = child.attrib['id']
#for child in artists:
#    if child.tag == 'artist':
#        single_artist = child.attrib['id']
#for child in playlists:
#    if child.tag == 'playlist':
#        single_playlist = child.attrib['id']

"""
user
"""
myuser = ampache.user(ampache_url, ampache_api, ampache_user, 'json')
# print('\ndata for my user account details:')

input("\nPress Enter to continue...\n")
"""
advanced_search
"""
print()
search_rules = [['favorite', 0, '%'], ['artist', 3, 'Prodigy']]
search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'song', 0, 0, 'json')

input("\nPress Enter to continue...\n")
song_title = 'funky'
print()
search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
search_album = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'album', 0, 1, 'json')

input("\nPress Enter to continue...\n")
print()
search_rules = [['favorite', 0, '%'], ['artist', 4, 'Prodigy']]
search_artist = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'artist', 0, 1, 'json')
input("\nPress Enter to continue...\n")


"""
album
"""
input("\nPress Enter to continue...\n")
ampache.album(ampache_url, ampache_api, single_album, '', 'json')

album_title = 'Fat of the Land'
"""
album_songs
"""
input("\nPress Enter to continue...\n")
ampache.album_songs(ampache_url, ampache_api, single_album, '', 0, 'json')

"""
albums
"""
input("\nPress Enter to continue...\n")
print('\nSearching for albums called', album_title)
albums = ampache.albums(ampache_url, ampache_api, 'Fat', 0, 0, 0, '', 0, 0, 'json')
input("\nPress Enter to continue...\n")

"""
stats
"""
input("\nPress Enter to continue...\n")

ampache.stats(ampache_url, ampache_api, 'artist', '%', ampache_user, None, 0, 3, 'json')
input("\nPress Enter to continue...\n")

ampache.stats(ampache_url, ampache_api, 'album', '%', ampache_user, None, 0, 3, 'json')
input("\nPress Enter to continue...\n")

"""
artist
"""
ampache.artist(ampache_url, ampache_api, single_artist, None, 'json')


"""
artist_albums
"""
# print('\nsearching for albums that are in this artist', single_artist)
input("\nPress Enter to continue...\n")
ampache.artist_albums(ampache_url, ampache_api, single_artist, None, 0, 'json')

"""
artist_songs
"""
# print('\nsearching for songs that are in this artist', single_artist)
input("\nPress Enter to continue...\n")
ampache.artist_songs(ampache_url, ampache_api, single_artist, 0, 5, 'json')


"""
artists
"""
myartists = ampache.artists(ampache_url, ampache_api, '%', None, None, 0, 5, None, 'json')
input("\nPress Enter to continue...\n")


"""
catalog_action
"""
print("\nampache.catalog_action was sent an intentionally bad task. 'clean' does not exist so return False")
ampache.catalog_action(ampache_url, ampache_api, 'clean', 2, 'json')
print()

"""
democratic
"""
#ampache.democratic(ampache_url, ampache_api)

"""
flag
"""
#ampache.flag(ampache_url, ampache_api)

"""
followers
"""
followers = ampache.followers(ampache_url, ampache_api, ampache_user, 'json')

input("\nPress Enter to continue...\n")

"""
following
"""
following = ampache.following(ampache_url, ampache_api, ampache_user, 'json')

input("\nPress Enter to continue...\n")

"""
friends_timeline
"""
friends_timeline = ampache.friends_timeline(ampache_url, ampache_api, 5, 0, 'json')

input("\nPress Enter to continue...\n")

"""
last_shouts
"""
last_shouts = ampache.last_shouts(ampache_url, ampache_api, ampache_user, 5, 'json')

input("\nPress Enter to continue...\n")

"""
localplay
"""
#ampache.localplay(ampache_url, ampache_api)

"""
playlists
"""
playlists = ampache.playlists(ampache_url, ampache_api, '%', 0, 0, 5, 'json')

input("\nPress Enter to continue...\n")

"""
playlist
"""
playlist = ampache.playlist(ampache_url, ampache_api, single_playlist, 'json')

input("\nPress Enter to continue...\n")

"""
playlist_songs
"""
playlist_songs = ampache.playlist_songs(ampache_url, ampache_api, single_playlist, 0, 5, 'json')

input("\nPress Enter to continue...\n")

"""
playlist_create
"""
#ampache.playlist_create(ampache_url, ampache_api, 'json')

"""
playlist_edit
"""
#ampache.playlist_edit(ampache_url, ampache_api, 'json')

"""
playlist_add_song
"""
#ampache.playlist_add_song(ampache_url, ampache_api, 'json')

"""
playlist_remove_song
"""
#ampache.playlist_remove_song(ampache_url, ampache_api, 'json')

"""
playlist_delete
"""
#ampache.playlist_delete(ampache_url, ampache_api, 'json')

"""
rate
"""
#ampache.rate(ampache_url, ampache_api, 'json')

"""
record_play
"""
#ampache.record_play(ampache_url, ampache_api, 'json')

"""
scrobble
"""
#ampache.scrobble(ampache_url, ampache_api, 'json')

"""
search_songs
"""
search_songs = ampache.search_songs(ampache_url, ampache_api, song_title, '%', 0, 5, 'json')

input("\nPress Enter to continue...\n")

"""
song
"""
song = ampache.song(ampache_url, ampache_api, 16822, 'json')

input("\nPress Enter to continue...\n")

"""
songs
"""
songs = ampache.songs(ampache_url, ampache_api, '%', 0, None, None, 0, 5, 'json')

input("\nPress Enter to continue...\n")


"""
tags
"""
genre = ''
tags = ampache.tags(ampache_url, ampache_api, 'Brutal Death Metal', 'exact', 0, 1, 'json')
print('\nLooking for the tag Brutal Death Metal')

input("\nPress Enter to continue...\n")

"""
tag_albums
"""
tag_albums = ampache.tag_albums(ampache_url, ampache_api, genre, 0, 1, 'json')
input("\nPress Enter to continue...\n")

"""
tag_artists
"""
tag_artists = ampache.tag_artists(ampache_url, ampache_api, genre, 0, 1, 'json')
input("\nPress Enter to continue...\n")

"""
tag_songs
"""
ampache.tag_songs(ampache_url, ampache_api, genre, 0, 1)

input("\nPress Enter to continue...\n")
"""
timeline
"""
print("\nampache.timeline for username:", ampache_user)
timeline = ampache.timeline(ampache_url, ampache_api, ampache_user, 10, 10, 'json')

input("\nPress Enter to continue...\n")

"""
toggle_follow
"""
#ampache.toggle_follow(ampache_url, ampache_api, 'json')

"""
update_from_tags
"""
print("\nampache.update from tags is verifying the album", album_title, 'json')

ampache.update_from_tags(ampache_url, ampache_api, 'album', single_album, 'json')

"""
url_to_song
"""
#ampache.url_to_song(ampache_url, ampache_api, 'json')

"""
video
"""
#ampache.video(ampache_url, ampache_api, 'json')

"""
videos
"""
#ampache.videos(ampache_url, ampache_api, 'json')

"""
goodbye
"""
# Close your session when you're done
print('\nWhen you are finished it\'s a good idea to kill your session')
ampache.goodbye(ampache_url, ampache_api, 'json')

