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
>>> print(dir(xml.etree.ElementTree.Element))
['__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'attrib', 'clear', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 'text']
"""
myuser = ampache.user(ampache_url, ampache_api, ampache_user)
print('\ndata for my user account details:')
for child in myuser:
    print(child.tag, child.attrib)
    #print('\nusername    ', child.find('username').text)
    #print('create_date ', child.find('create_date').text)
    #print('last_seen   ', child.find('last_seen').text)
    #print('website     ', child.find('website').text)
    #print('state       ', child.find('state').text)
    #print('city        ', child.find('city').text)
    #print('fullname    ', child.find('fullname').text)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
advanced_search

    MINIMUM_API_VERSION=380001

    Perform an advanced search given passed rules
    the rules can occur multiple times and are joined by the operator item.
    
    Refer to the wiki for firther information
    https://github.com/ampache/ampache/wiki/XML-methods

"""
print()
search_rules = [['favorite', 0, '%'], ['artist', 3, 'Prodigy']]
search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'song', 0, 0)
for child in search_song:
    if child.tag == 'total_count':
        continue
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
    song_title = child.find('title').text

print()
search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
search_album = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'album', 0, 1)
for child in search_album:
    if child.tag == 'total_count':
        continue
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
    album_title = child.find('name').text

print()
search_rules = [['favorite', 0, '%'], ['artist', 4, 'Prodigy']]
search_artist = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'and', 'artist', 0, 1)
for child in search_artist:
    if child.tag == 'total_count':
        print('total_count', search_artist.find('total_count').text)
        continue
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
    artist_title = child.find('name').text

"""
album
"""
for child in ampache.album(ampache_url, ampache_api, single_album, ''):
    if child.tag == 'album':
        print(child.tag, child.attrib)
        album_title = child.find('name').text
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
album_songs
"""
print('\nsearching for songs that are in this album', single_album)
for child in ampache.album_songs(ampache_url, ampache_api, single_album, '', 0):
    if child.tag == 'song':
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
albums
"""
print('\nSearching for albums called', album_title)
albums = ampache.albums(ampache_url, ampache_api, 1, 0, 0, album_title, '', 0, 0)
for child in albums:
    if child.tag == 'total_count':
        continue
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
stats
"""
for child in ampache.stats(ampache_url, ampache_api, 'artist', '', ampache_user, None, 0, 1):
    if child.tag == 'artist':
        print('\ngetting a random artist using the stats method and found', child.find('name').text)
        single_artist = child.attrib['id']
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))
for child in ampache.stats(ampache_url, ampache_api, 'album', '', ampache_user, None, 0, 1):
    if child.tag == 'artist':
        print('\ngetting a random album using the stats method and found', child.find('name').text)
        single_album = child.attrib['id']
        album_title = child.find('name').text
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
artist
"""
for child in ampache.artist(ampache_url, ampache_api, single_artist):
    if child.tag == 'artist':
        print('\nsearching for an artist with this id', single_artist)
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
artist_albums
"""
print('\nsearching for albums that are in this artist', single_artist)
for child in ampache.artist_albums(ampache_url, ampache_api, single_artist, None, 0):
    if child.tag == 'album':
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
artist_songs
"""
print('\nsearching for songs that are in this artist', single_artist)
for child in ampache.artist_songs(ampache_url, ampache_api, single_artist, '', 0):
    if child.tag == 'song':
        print(child.tag, child.attrib)
        for subchildren in child:
            print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
artists
"""
myartists = ampache.artists(ampache_url, ampache_api)
for child in myartists:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

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
followers = ampache.followers(ampache_url, ampache_api, ampache_user)

for child in followers:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
following
"""
following = ampache.following(ampache_url, ampache_api, ampache_user)

for child in following:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
friends_timeline
"""
friends_timeline = ampache.friends_timeline(ampache_url, ampache_api)

for child in friends_timeline:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
last_shouts
"""
last_shouts = ampache.last_shouts(ampache_url, ampache_api, ampache_user)

for child in last_shouts:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
localplay
"""
#print(ampache.localplay(ampache_url, ampache_api))

"""
playlists
"""
playlists = ampache.playlists(ampache_url, ampache_api)

for child in playlists:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
playlist
"""
playlist = ampache.playlist(ampache_url, ampache_api, single_playlist)

for child in playlist:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
playlist_songs
"""
playlist_songs = ampache.playlist_songs(ampache_url, ampache_api, single_playlist)

for child in playlist_songs:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
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
search_songs = ampache.search_songs(ampache_url, ampache_api, song_title)

for child in search_songs:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
song
"""
song = ampache.song(ampache_url, ampache_api, song_title)

for child in song:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
songs
"""
songs = ampache.songs(ampache_url, ampache_api)

for child in songs:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
tags
"""
genre = ''
tags = ampache.tags(ampache_url, ampache_api, 'Brutal Death Metal', 'exact', 0, 1)
print('\nLooking for the tag Brutal Death Metal')

for child in tags:
    if child.tag == 'total_count':
        print('total_count', search_artist.find('total_count').text)
        continue
    print(child.tag, child.attrib)
    genre = child.attrib['id']
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
tag_albums
"""
tag_albums = ampache.tag_albums(ampache_url, ampache_api, genre, 0, 1)
for child in tag_albums:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
tag_artists
"""
tag_artists = ampache.tag_artists(ampache_url, ampache_api, genre, 0, 1)
for child in tag_artists:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))

"""
tag_songs
"""
print(ampache.tag_songs(ampache_url, ampache_api, genre, 0, 1))

"""
timeline
"""
print("\nampache.timeline for username:", ampache_user)
timeline = ampache.timeline(ampache_url, ampache_api, ampache_user, 10, 10)

for child in timeline:
    print(child.tag, child.attrib)
    for subchildren in child:
        print(str(subchildren.tag) + ': ' + str(subchildren.text))
"""
toggle_follow
"""
#print(ampache.toggle_follow(ampache_url, ampache_api))

"""
update_from_tags
"""
print("\nampache.update from tags is verifying the album", album_title)
print(ampache.update_from_tags(ampache_url, ampache_api, 'album', single_album))

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

