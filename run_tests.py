#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import sys
import time

from src import ampache

from xml.etree import ElementTree as ET

# Test colors for printing
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# user variables
url = 'https://music.server'
api = 'mysuperapikey'
user = 'myusername'
try:
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        url = sys.argv[1]
        api = sys.argv[2]
        user = sys.argv[3]
except IndexError:
    if os.path.isfile('docs/examples/ampyche.conf'):
        conf = configparser.RawConfigParser()
        conf.read('docs/examples/ampyche.conf')
        url = conf.get('conf', 'ampache_url')
        user = conf.get('conf', 'ampache_user')
        api = conf.get('conf', 'ampache_apikey')

limit = 4
offset = 0
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=60&uid=4&player=api&name=Synthetic%20-%20BrownSmoke.wma'
tempusername = 'temp_user'
    

def run_tests(ampache_url, ampache_api, ampache_user, api_format):

    print(f"{HEADER}\n################\nRUN PYTHON TESTS\n################\n{ENDC}")
    print("Testing: " + api_format)

    ampacheConnection = ampache.API()
    ampacheConnection.set_format(api_format)
    """TODO
    def update_art(ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    def update_artist_info(id, api_format = 'xml'):
    def stream(id, type, destination, api_format = 'xml'):
    def download(id, type, destination, format = 'raw', api_format = 'xml'):
    def get_art(id, type, api_format = 'xml'):
    """

    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)
    if encrypted_key:
        print(f"ampacheConnection.encrypted_key: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:\n" + encrypted_key)
    else:
        sys.exit(f"\nampache.encrypted_key:     {FAIL}FAIL{ENDC}")

    """ handshake
    def handshake(user = False, timestamp = False, version = '420000', api_format = 'xml'):
    """
    # processed details
    ampache_api = ampacheConnection.handshake(ampache_url, encrypted_key, False, False, '420000')
    if ampache_api:
        print(f"ampacheConnection.handshake: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:\n" + ampache_api)
    else:
        print(f"ampacheConnection.handshake: {FAIL}FAIL{ENDC}")
        sys.exit(f"\n{FAIL}ERROR:{ENDC} Failed to connect to " + ampache_url)

    """ ping
    def ping(api_format = 'xml'):
    """
    # did all this work?
    my_ping = ampacheConnection.ping(ampache_url, ampache_api)
    if my_ping:
        print(f"ampacheConnection.ping: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:\n" + my_ping)
    else:
        print(f"ampacheConnection.ping: {FAIL}FAIL{ENDC}")
        sys.exit(f"\n{FAIL}ERROR:{ENDC} Failed to ping " + ampache_url)

    """ set_debug
    def set_debug(mybool):
    """
    set_debug = ampacheConnection.set_debug(False)

    """ url_to_song
    def url_to_song(url, api_format = 'xml'):
    """
    song_id     = False
    url_to_song = ampacheConnection.url_to_song(song_url)

    if api_format == 'xml':
        song_id = ET.tostring(url_to_song).decode()
    else:
        song_id = url_to_song

    if url_to_song and song_id:
        print(f"ampacheConnection.url_to_song: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:")
        #print(song_id)
    else:
        print(f"ampacheConnection.url_to_song: {FAIL}FAIL{ENDC}")

    """ user_create
    def user_create(username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    failed  = False
    message = ''
    # delete them first if they exists
    ampacheConnection.user_delete(tempusername)
    createuser   = ampacheConnection.user_create(tempusername, 'supoersecretpassword', 'email@gmail.com', False, False)
    if api_format == 'xml':
        for child in createuser:
            if child.tag == 'error':
                failed = True
                message = child.text
            if child.tag == 'success':
                message = child.text
    else:
        if 'error' in createuser:
            failed = True
            try:
                message = createuser['error']['message']
            except TypeError:
                message = createuser['error']
        if 'success' in createuser:
            try:
                message = createuser['success']['message']
            except TypeError:
                message = createuser['success']

    if createuser and not failed:
        print(f"ampacheConnection.user_create: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:")
        #print(message)
    else:
        if message == 'User does not have access to this function':
            print(f"ampacheConnection.user_create: {WARNING}WARNING{ENDC}")
        else:
            sys.exit(f"ampacheConnection.user_create: {FAIL}FAIL{ENDC}")
        print("returned:")
        print(message + "\n")

    """ user_edit
    def user_update(username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    failed = False
    message = ''
    edituser = ampacheConnection.user_update(tempusername, False, False, False, False, False, False, True, False)
    if api_format == 'xml':
        for child in edituser:
            if child.tag == 'error':
                failed = True
                message = child.text
            if child.tag == 'success':
                message = child.text
    else:
        if 'error' in edituser:
            failed = True
            try:
                message = edituser['error']['message']
            except TypeError:
                message = edituser['error']
        if 'success' in edituser:
            try:
                message = edituser['success']['message']
            except TypeError:
                message = edituser['success']

    if edituser and not failed:
        print(f"ampacheConnection.user_update: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:")
        #print(message)
    else:
        if message == 'User does not have access to this function':
            print(f"ampacheConnection.user_create: {WARNING}WARNING{ENDC}")
        else:
            print(f"ampacheConnection.user_create: {FAIL}FAIL{ENDC}")
        print("returned:")
        print(message + "\n")

    """ user_delete
    def user_delete(username, api_format = 'xml'):
    """
    failed = False
    message = ''
    deleteuser = ampacheConnection.user_delete(tempusername)
    if api_format == 'xml':
        for child in deleteuser:
            if child.tag == 'error':
                failed = True
                message = child.text
            if child.tag == 'success':
                message = child.text
    else:
        if 'error' in deleteuser:
            failed = True
            try:
                message = deleteuser['error']['message']
            except TypeError:
                message = deleteuser['error']
        if 'success' in deleteuser:
            try:
                message = deleteuser['success']['message']
            except TypeError:
                message = deleteuser['success']

    if deleteuser and not failed:
        print(f"ampacheConnection.user_delete: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:")
        #print(message)
    else:
        if message == 'User does not have access to this function':
            print(f"ampacheConnection.user_create: {WARNING}WARNING{ENDC}")
        else:
            print(f"ampacheConnection.user_create: {FAIL}FAIL{ENDC}")
        print("returned:")
        print(message + "\n")

    """ user
    def user(username, api_format = 'xml'):
    """
    myuser = ampacheConnection.user('missing_user')
    myuser = ampacheConnection.user(ampache_user)

    if api_format == 'xml':
        user_id = ET.tostring(myuser).decode()
    else:
        user_id = myuser

    if myuser:
        print(f"ampacheConnection.user: {OKGREEN}PASS{ENDC}")
        #print("\nreturned:")
        #print(user_id)
    else:
        sys.exit(f"\nampache.user: {FAIL}FAIL{ENDC}")

    """ get_indexes
    def get_indexes(type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):

    'song'|'album'|'artist'|'playlist'
    """
    
    songs     = ampacheConnection.get_indexes('song', False, False, False, False, False, offset, limit)
    if api_format == 'xml':
        tmpcount = songs.findall('song')
        #if len(tmpcount) > int(limit):
        #    print(f"ampacheConnection.get_indexes: {FAIL}FAIL{ENDC}")
        #    sys.exit(f"\n{FAIL}ERROR:{ENDC} songs " + str(len(tmpcount)) + ' found more items than the limit ' + str(limit))

    albums    = ampacheConnection.get_indexes('album', False, False, False, False, False, offset, limit)
    if api_format == 'xml':
        tmpcount = albums.findall('album')
        #if len(tmpcount) > int(limit):
        #    print(f"ampacheConnection.get_indexes: {FAIL}FAIL{ENDC}")
        #    sys.exit(f"\n{FAIL}ERROR:{ENDC} albums " + str(len(tmpcount)) + ' found more items than the limit ' + str(limit))

    artists   = ampacheConnection.get_indexes('artist', False, False, False, False, False, offset, limit)
    if api_format == 'xml':
        tmpcount = ampacheConnection.get_object_list(artists, 'artist')
        #if len(tmpcount) > int(limit):
        #    print(f"ampacheConnection.get_indexes: {FAIL}FAIL{ENDC}")
        #    sys.exit(f"\n{FAIL}ERROR:{ENDC} artists " + str(len(tmpcount)) + ' found more items than the limit ' + str(limit))

    playlists = ampacheConnection.get_indexes('playlist', False, False, False, False, False, offset, limit)
    if api_format == 'xml':
        tmpcount = playlists.findall('playlist')
        #if len(tmpcount) > int(limit):
        #    print(f"ampacheConnection.get_indexes: {FAIL}FAIL{ENDC}")
        #    sys.exit(f"\n{FAIL}ERROR:{ENDC} playlists " + str(len(tmpcount)) + ' found more items than the limit ' + str(limit))


    if api_format == 'xml':
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
    else:
        single_song     = songs[0]['id']
        single_album    = albums[0]['id']
        single_artist   = artists[0]['id']
        single_playlist = playlists[0]['id']

    if single_song and single_album and single_artist and single_playlist:
        print(f"ampacheConnection.get_indexes: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.get_indexes: {FAIL}FAIL{ENDC}")

    """ advanced_search
    def advanced_search(rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['title', 2, 'Dance']]
    search_song = ampacheConnection.advanced_search(search_rules, 'or', 'song', 0, 4)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'total_count':
                    continue
            #    #if int(child.text) > int(limit):
            #    #    print(f"ampacheConnection.advanced_search: {FAIL}FAIL{ENDC}")
            #    #    sys.exit(f"\n{FAIL}ERROR:{ENDC} advanced_search (song) " + child.text + ' found more items than the limit ' + str(limit))
            #    #else:
            #    #    continue
            #print(child.tag, child.attrib)
            #for subchildren in child:
            #    #print(str(subchildren.tag) + ': ' + str(subchildren.text))
            song_title = child.find('title').text
    else:
        song_title = search_song[0]['title']

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Car']]
    search_album = ampacheConnection.advanced_search(search_rules, 'or', 'album', 0, 4)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'total_count':
                    continue
            #    if int(child.text) > int(limit):
            #        print(f"ampacheConnection.advanced_search: {FAIL}FAIL{ENDC}")
            #        sys.exit(f"\n{FAIL}ERROR:{ENDC} advanced_search (album) " + child.text + ' found more items than the limit ' + str(limit))
            #    else:
            #        continue
            #print(child.tag, child.attrib)
            #for subchildren in child:
            #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
            album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', 4, 'Prodigy']]
    search_artist = ampacheConnection.advanced_search(search_rules, 'or', 'artist', 0, 4)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'total_count':
                    continue
            #    if int(child.text) > int(limit):
            #        print(f"ampacheConnection.advanced_search: {FAIL}FAIL{ENDC}")
            #        sys.exit(f"{FAIL}ERROR:{ENDC} advanced_search (artist) " + child.text + ' found more items than the limit ' + str(limit))
            #    else:
            #        continue
            #print(child.tag, child.attrib)
            #for subchildren in child:
            #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
            artist_title = child.find('name').text
    else:
        artist_title = search_artist[0]['name']

    if search_song and search_album and search_artist and song_title and album_title and artist_title:
        print(f"ampacheConnection.get_indexes: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.get_indexes: {FAIL}FAIL{ENDC}")

    """ album
    def album(filter, include = False, api_format = 'xml'):
    """
    album = ampacheConnection.album(single_album, False)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                #print(child.tag, child.attrib)
                album_title = child.find('name').text
                #for subchildren in child:
                #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        album_title = search_album[0]['name']

    if album_title:
        print(f"ampacheConnection.album: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.album: {FAIL}FAIL{ENDC}")

    """ album_songs
    def album_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    album_songs = ampacheConnection.album_songs(single_album, 0, 0)
    #if api_format == 'xml':
    #    #for child in album_songs:
    #    #    #if child.tag == 'song':
    #    #    #    #print(child.tag, child.attrib)
    #    #    #    #for subchildren in child:
    #    #    #    #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    if album_songs:
        print(f"ampacheConnection.album_songs: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.album_songs: {FAIL}FAIL{ENDC}")

    """ albums
    def albums(filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    albums = ampacheConnection.albums(album_title, 1, False, False, 0, 10, False)
    #if api_format == 'xml':
    #    for child in albums:
    #        #if child.tag == 'total_count':
    #        #    if int(child.text) > int(limit):
    #        #        print(f"ampacheConnection.albums: {FAIL}FAIL{ENDC}")
    #        #        sys.exit(f"{FAIL}ERROR:{ENDC} albums " + child.text + ' found more items than the limit ' + str(limit))
    #        #    else:
    #        #        continue
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    if albums:
        print(f"ampacheConnection.albums: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.albums: {FAIL}FAIL{ENDC}")

    """ stats
    def stats(type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    stats = ampacheConnection.stats('artist', 'newest', ampache_user, False, 0, limit)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'artist':
                #print('\ngetting a random artist using the stats method and found', child.find('name').text)
                single_artist = child.attrib['id']
                #print(child.tag, child.attrib)
                #for subchildren in child:
                #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        single_artist = stats[0]['id']
    stats = ampacheConnection.stats('album', 'random', ampache_user, None, 0, limit)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'album':
                #print('\ngetting a random album using the stats method and found', child.find('name').text)
                single_album = child.attrib['id']
                album_title = child.find('name').text
                #print(child.tag, child.attrib)
                #for subchildren in child:
                #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        single_album = stats[0]['id']
        album_title  = stats[0]['name']

    if single_artist and single_album and album_title:
        print(f"ampacheConnection.stats: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.stats: {FAIL}FAIL{ENDC}")

    """ artist
    def artist(filter, include = False, api_format = 'xml'):
    """
    artist = ampacheConnection.artist(single_artist, False)

    #if api_format == 'xml':
    #    for child in artist:
    #        if child.tag == 'artist':
    #            #print('\nsearching for an artist with this id', single_artist)
    #            #print(child.tag, child.attrib)
    #            #for subchildren in child:
    #            #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    if artist:
        print(f"ampacheConnection.artist: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.artist: {FAIL}FAIL{ENDC}")

    """ artist_albums
    def artist_albums(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_albums = ampacheConnection.artist_albums(single_artist, 0, 0)

    if artist_albums:
        print(f"ampacheConnection.artist_albums: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.artist_albums: {FAIL}FAIL{ENDC}")

    """ artist_songs
    def artist_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_songs = ampacheConnection.artist_songs(single_artist, 0, 0)

    if artist_songs:
        print(f"ampacheConnection.artist_songs: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.artist_songs: {FAIL}FAIL{ENDC}")

    """ artists
    def artists(filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    myartists = ampacheConnection.artists(False, False, False, 0, 0, False)

    if myartists:
        print(f"ampacheConnection.artists: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.artists: {FAIL}FAIL{ENDC}")

    """ catalog_action
    def catalog_action(task, catalog, api_format = 'xml'):
    """
    catalog_action = ampacheConnection.catalog_action('clean', 1)
    catalog_action = ampacheConnection.catalog_action('clean_catalog', 1)

    if catalog_action:
        print(f"ampacheConnection.catalog_action: {OKGREEN}PASS{ENDC}")
    else:
        sys.exit(f"\nampache.catalog_action: {FAIL}FAIL{ENDC}")

    """ flag
    def flag(type, id, flag, api_format = 'xml'):
    """
    #print(ampacheConnection.flag(ampache_url, ampache_api))

    """ followers
    def followers(username, api_format = 'xml'):
    """
    followers = ampacheConnection.followers(ampache_user)

    """ following
    def following(username, api_format = 'xml'):
    """
    following = ampacheConnection.following(ampache_user)

    """ friends_timeline
    def friends_timeline(limit = 0, since = 0, api_format = 'xml'):
    """
    friends_timeline = ampacheConnection.friends_timeline(0, 0)

    """ last_shouts
    def last_shouts(username, limit = 0, api_format = 'xml'):
    """
    last_shouts = ampacheConnection.last_shouts(ampache_user, 0)

    """ playlists
    def playlists(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlists = ampacheConnection.playlists(False, False, 0, 0)

    """ playlist
    def playlist(filter, api_format = 'xml'):
    """
    playlist = ampacheConnection.playlist(single_playlist)

    """ playlist_songs
    def playlist_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlist_songs = ampacheConnection.playlist_songs(single_playlist, 0, 0)

    """ playlist_create
    def playlist_create(name, type, api_format = 'xml'):
    """
    #print(ampacheConnection.playlist_create(ampache_url, ampache_api))

    """ playlist_edit
    def playlist_edit(filter, name = False, type = False, api_format = 'xml'):
    """
    #print(ampacheConnection.playlist_edit(ampache_url, ampache_api))

    """ playlist_add_song
    def playlist_add_song(filter, song, check = 0, api_format = 'xml'):
    """
    #print(ampacheConnection.playlist_add_song(ampache_url, ampache_api))

    """ playlist_remove_song
    def playlist_remove_song(filter, song = False, track = False, api_format = 'xml'):
    """
    #print(ampacheConnection.playlist_remove_song(ampache_url, ampache_api))

    """ playlist_delete
    def playlist_delete(filter, api_format = 'xml'):
    """
    #print(ampacheConnection.playlist_delete(ampache_url, ampache_api))

    """ playlist_generate
    def playlist_generate(mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.playlist_generate('random', False, False, False, False, 'song', 0, limit)

    ampacheConnection.playlist_generate('random', False, False, False, False, 'index', 0, limit)

    ampacheConnection.playlist_generate('random', False, False, False, False, 'id', 0, limit)

    """ rate
    def rate(type, id, rating, api_format = 'xml'):
    """
    #print(ampacheConnection.rate(ampache_url, ampache_api))

    """ record_play
    def record_play(id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    #print(ampacheConnection.record_play(ampache_url, ampache_api))

    """ scrobble
    def scrobble(title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    scrobble = ampacheConnection.scrobble('Hear.Life.Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False, int(time.time()), 'AmpaceApi')
    scrobble = ampacheConnection.scrobble('Welcome to Planet Sexor', 'Tiga', 'Sexor', False, False, False, int(time.time()), 'test.py')

    """ search_songs
    def search_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampacheConnection.search_songs(song_title, 0, 0)

    #if api_format == 'xml':
    #    for child in search_songs:
    #        print(child.tag, child.attrib)
    #        for subchildren in child:
    #            print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ song
    def song(filter, api_format = 'xml'):
    """
    song = ampacheConnection.song(single_song)

    #if api_format == 'xml':
    #    for child in song:
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ songs
    def songs(filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    songs = ampacheConnection.songs(False, False, False, False, 0, 0)
    #if api_format == 'xml':
    #    for child in songs:
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tags
    def tags(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampacheConnection.tags('Brutal Death Metal', '1', 0, 4)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print(f"ampacheConnection.tags: {FAIL}FAIL{ENDC}")
                    sys.exit(f"\n{FAIL}ERROR:{ENDC} tags " + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            #print(child.tag, child.attrib)
            genre = child.attrib['id']
            #for subchildren in child:
            #    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        genre = tags[0]['tag']['id']

    """ tag
    def tag(filter, api_format = 'xml'):
    """
    tag = ampacheConnection.tag(genre)


    """ tag_albums
    def tag_albums(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_albums = ampacheConnection.tag_albums(genre, 0, limit)
    #if api_format == 'xml':
    #    for child in tag_albums:
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tag_artists
    def tag_artists(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_artists = ampacheConnection.tag_artists(genre, 0, 1)
    #if api_format == 'xml':
    #    for child in tag_artists:
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tag_songs
    def tag_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_songs = ampacheConnection.tag_songs(genre, 0, 1)

    """ timeline
    def timeline(username, limit = 0, since = 0, api_format = 'xml'):
    """
    timeline = ampacheConnection.timeline(ampache_user, 10, 0)

    #if api_format == 'xml':
    #    for child in timeline:
    #        #print(child.tag, child.attrib)
    #        #for subchildren in child:
    #        #    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ toggle_follow
    def toggle_follow(username, api_format = 'xml'):
    """
    toggle = 'generic'
    if ampache_user == 'generic':
        toggle = 'user'
    #togglefollow = ampacheConnection.toggle_follow(toggle))

    """ update_from_tags
    def update_from_tags(ampache_type, ampache_id, api_format = 'xml'):
    """
    update_from_tags = ampacheConnection.update_from_tags('album', single_album)

    """ video
    def video(filter, api_format = 'xml'):
    """
    #print(ampacheConnection.video(ampache_url, ampache_api))

    """ videos
    def videos(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    #print(ampacheConnection.videos(ampache_url, ampache_api))

    """ localplay
    def localplay(command, api_format = 'xml'):
    """
    #print(ampacheConnection.localplay(ampache_url, ampache_api))

    """ democratic
    def democratic(method, action, oid, api_format = 'xml'):
    """
    #print(ampacheConnection.democratic(ampache_url, ampache_api))

    """ goodbye
    def goodbye(api_format = 'xml'):
    """
    # Close your session when you're done
    goodbye = ampacheConnection.goodbye(api_format)


run_tests(url, api, user, 'xml')
run_tests(url, api, user, 'json')

