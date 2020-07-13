#!/usr/bin/env python3

import os
import shutil
import sys
import time

from src import ampache

# user variables
try:
    if sys.argv[1] and sys.argv[2] and sys.argv[2]:
        ampache_url  = sys.argv[1]
        ampache_api  = sys.argv[2]
        ampache_user = sys.argv[3]
except IndexError:
    ampache_url  = 'https://music.server'
    ampache_api  = 'mysuperapikey'
    ampache_user = 'myusername'

limit    = 4
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=164215&uid=2&player=api&name=Hellyeah%20-%20-.mp3'

def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    """TODO
    def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    def update_artist_info(ampache_url, ampache_api, id, api_format = 'xml'):
    def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
    def get_art(ampache_url, ampache_api, id, type, api_format = 'xml'):
    get_similar: send artist or song id to get related objects from last.fm
    shares: get a list of shares you can access
    share: get a share by id
    share_create: create a share
    share_edit: edit an existing share
    share_delete: delete an existing share
    podcasts: get a list of podcasts you can access
    podcast: get a podcast by id
    podcast_episodes: get a list of podcast_episodes you can access
    podcast_episode: get a podcast_episode by id
    podcast_episode_delete: delete an existing podcast_episode
    podcast_create: create a podcast
    podcast_edit: edit an existing podcast
    podcast_delete: delete an existing podcast
    update_podcast: sync and download new episodes
    catalogs: get all the catalogs
    catalog: get a catalog by id
    catalog_file: clean, add, verify using the file path (good for scripting)
    """

    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    original_api = ampache_api
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ handshake
    def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '400004', api_format = 'xml'):
    """
    # processed details
    ampache_api = ampache.handshake(ampache_url, encrypted_key, False, False, '400004', api_format)
    if not ampache_api:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api, api_format = 'xml'):
    """
    # did all this work?
    my_ping = ampache.ping(ampache_url, ampache_api, api_format)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ set_debug
    def set_debug(mybool):
    """
    ampache.set_debug(True)

    """ url_to_song
    def url_to_song(ampache_url, ampache_api, url, api_format = 'xml'):
    """
    url_to_song = ampache.url_to_song(ampache_url, ampache_api, song_url, api_format)

    """ user_create
        def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    tempusername = 'temp_user'
    createuser   = ampache.user_create(ampache_url, ampache_api, tempusername, 'supoersecretpassword', 'email@gmail.com', False, False, api_format)
    tmpuser = ampache.user(ampache_url, ampache_api, tempusername, api_format)

    """ user_edit
        def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    edituser = ampache.user_update(ampache_url, ampache_api, tempusername, False, False, False, False, False, False, True, False, api_format)
    tmpuser = ampache.user(ampache_url, ampache_api, tempusername, api_format)
    shutil.move("docs/" + api_format + "-responses/user." + api_format,
                "docs/" + api_format + "-responses/user (disabled)." + api_format)

    """ user_delete
        def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    deleteuser = ampache.user_delete(ampache_url, ampache_api, tempusername, api_format)

    """ user
    def user(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    myuser = ampache.user(ampache_url, ampache_api, 'missing_user', api_format)
    shutil.move("docs/" + api_format + "-responses/user." + api_format,
                "docs/" + api_format + "-responses/user (error)." + api_format)

    myuser = ampache.user(ampache_url, ampache_api, ampache_user, api_format)

    """ get_indexes
    def get_indexes(ampache_url, ampache_api, type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):

    'song'|'album'|'artist'|'playlist'
    """
    songs     = ampache.get_indexes(ampache_url, ampache_api, 'song', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (song)." + api_format)
    if api_format == 'xml':
        for child in songs:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: songs ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    albums    = ampache.get_indexes(ampache_url, ampache_api, 'album', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (album)." + api_format)
    if api_format == 'xml':
        for child in albums:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: albums ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    artists   = ampache.get_indexes(ampache_url, ampache_api, 'artist', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (artist)." + api_format)
    if api_format == 'xml':
        for child in artists:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: artists ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    playlists = ampache.get_indexes(ampache_url, ampache_api, 'playlist', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (playlist)." + api_format)
    if api_format == 'xml':
        for child in playlists:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: playlists ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

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

    """ advanced_search
    def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['artist', 3, 'Prodigy']]
    search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'song', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (song) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
            song_title = child.find('title').text
    else:
        song_title = search_song[0]['title']

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'album', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (album) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
            album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', limit, 'Prodigy']]
    search_artist = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'artist', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (artist) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
            artist_title = child.find('name').text
    else:
        artist_title = search_artist[0]['name']

    """ album
    def album(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    album = ampache.album(ampache_url, ampache_api, single_album, False, api_format)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                print(child.tag, child.attrib)
                album_title = child.find('name').text
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        album_title = search_album[0]['name']

    """ album_songs
    def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    album_songs = ampache.album_songs(ampache_url, ampache_api, single_album, 0, limit, api_format)
    if api_format == 'xml':
        for child in album_songs:
            if child.tag == 'song':
                print(child.tag, child.attrib)
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ albums
    def albums(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    albums = ampache.albums(ampache_url, ampache_api, album_title, 1, False, False, 0, 10, False, api_format)
    if api_format == 'xml':
        for child in albums:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: albums ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ stats
    def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """

    stats = ampache.stats(ampache_url, ampache_api, 'song', 'random', ampache_user, None, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (song)." + api_format)

    stats = ampache.stats(ampache_url, ampache_api, 'artist', 'random', ampache_user, False, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (artist)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'artist':
                print('\ngetting a random artist using the stats method and found', child.find('name').text)
                single_artist = child.attrib['id']
                print(child.tag, child.attrib)
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        single_artist = stats[0]['id']

    stats = ampache.stats(ampache_url, ampache_api, 'album', 'random', ampache_user, None, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (album)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'album':
                print('\ngetting a random album using the stats method and found', child.find('name').text)
                single_album = child.attrib['id']
                album_title = child.find('name').text
                print(child.tag, child.attrib)
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        album_title = stats[0]['name']

    """ artist
    def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    artist = ampache.artist(ampache_url, ampache_api, single_artist, False, api_format)

    if api_format == 'xml':
        for child in artist:
            if child.tag == 'artist':
                print('\nsearching for an artist with this id', single_artist)
                print(child.tag, child.attrib)
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ artist_albums
    def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_albums = ampache.artist_albums(ampache_url, ampache_api, single_artist, 0, limit, api_format)

    """ artist_songs
    def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_songs = ampache.artist_songs(ampache_url, ampache_api, single_artist, 0, limit, api_format)

    """ artists
    def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    myartists = ampache.artists(ampache_url, ampache_api, False, False, False, 0, limit, False, api_format)

    """ catalog_action
    def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    """
    catalog_action = ampache.catalog_action(ampache_url, ampache_api, 'clean', 2, api_format)
    shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    catalog_action = ampache.catalog_action(ampache_url, ampache_api, 'clean_catalog', 2, api_format)

    """ flag
    def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    """
    ampache.flag(ampache_url, ampache_api, 'playlist', 2069, True, api_format)

    """ rate
    def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_api, 'playlist', 2069, 2, api_format)

    """ record_play
    def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.record_play(ampache_url, ampache_api, 77371, 4, 'AmpacheAPI', api_format)

    """ followers
    def followers(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    followers = ampache.followers(ampache_url, ampache_api, ampache_user, api_format)

    """ following
    def following(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    following = ampache.following(ampache_url, ampache_api, ampache_user, api_format)

    """ friends_timeline
    def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0, api_format = 'xml'):
    """
    friends_timeline = ampache.friends_timeline(ampache_url, ampache_api, limit, 0, api_format)

    """ last_shouts
    def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    """
    last_shouts = ampache.last_shouts(ampache_url, ampache_api, ampache_user, limit, api_format)

    """ playlists
    def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlists = ampache.playlists(ampache_url, ampache_api, False, False, 0, limit, api_format)

    """ playlist
    def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    playlist = ampache.playlist(ampache_url, ampache_api, single_playlist, api_format)

    """ playlist_songs
    def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlist_songs = ampache.playlist_songs(ampache_url, ampache_api, single_playlist, 0, limit, api_format)

    """ playlist_create
    def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    """
    #print(ampache.playlist_create(ampache_url, ampache_api))

    """ playlist_edit
    def playlist_edit(ampache_url, ampache_api, filter, name = False, type = False, api_format = 'xml'):
    """
    #print(ampache.playlist_edit(ampache_url, ampache_api))

    """ playlist_add_song
    def playlist_add_song(ampache_url, ampache_api, filter, song, check = 0, api_format = 'xml'):
    """
    #print(ampache.playlist_add_song(ampache_url, ampache_api))

    """ playlist_remove_song
    def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False, api_format = 'xml'):
    """
    #print(ampache.playlist_remove_song(ampache_url, ampache_api))

    """ playlist_delete
    def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    #print(ampache.playlist_delete(ampache_url, ampache_api))

    """ playlist_generate
    def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    'song'|'index'|'id'
    """
    ampache.playlist_generate(ampache_url, ampache_api, 'random', False, False, False, False, 'song', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (song)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_api, 'random', False, False, False, False, 'index', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (index)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_api, 'random', False, False, False, False, 'id', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (id)." + api_format)

    """ scrobble
    def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    scrobble = ampache.scrobble(ampache_url, ampache_api, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False, int(time.time()), 'AmpaceApi', api_format)
    shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    scrobble = ampache.scrobble(ampache_url, ampache_api, 'Welcome to Planet Sexor', 'Tiga', 'Sexor', False, False, False, int(time.time()), 'test.py', api_format)

    """ search_songs
    def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampache.search_songs(ampache_url, ampache_api, song_title, 0, limit, api_format)

    if api_format == 'xml':
        for child in search_songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ song
    def song(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    song = ampache.song(ampache_url, ampache_api, single_song, api_format)

    if api_format == 'xml':
        for child in song:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ songs
    def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    songs = ampache.songs(ampache_url, ampache_api, False, False, False, False, 0, limit, api_format)
    if api_format == 'xml':
        for child in songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tags
    def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampache.tags(ampache_url, ampache_api, 'Brutal Death Metal', False, 0, limit, api_format)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'total_count':
                print('total_count', child.text)
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: tags ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            print(child.tag, child.attrib)
            genre = child.attrib['id']
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
    else:
        genre = tags[0]['tag']
        for tag in genre:
            print(tag)
            tmp_genre = tag['id']
        genre = tmp_genre

    """ tag
    def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    tag = ampache.tag(ampache_url, ampache_api, genre, api_format)

    """ tag_albums
    def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_albums = ampache.tag_albums(ampache_url, ampache_api, genre, 0, 2, api_format)
    if api_format == 'xml':
        for child in tag_albums:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tag_artists
    def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_artists = ampache.tag_artists(ampache_url, ampache_api, genre, 0, 1, api_format)
    if api_format == 'xml':
        for child in tag_artists:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tag_songs
    def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_songs = ampache.tag_songs(ampache_url, ampache_api, genre, 0, 1, api_format)

    """ licenses
    def licenses(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    licenses = ampache.licenses(ampache_url, ampache_api, False, False, 0, limit, api_format)

    """ license
    def license(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    license = ampache.license(ampache_url, ampache_api, 2, api_format)

    """ license_songs
    def license_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    license_songs = ampache.license_songs(ampache_url, ampache_api, 2, api_format)

    """ timeline
    def timeline(ampache_url, ampache_api, username, limit = 0, since = 0, api_format = 'xml'):
    """
    timeline = ampache.timeline(ampache_url, ampache_api, ampache_user, 10, 0, api_format)

    #if api_format == 'xml':
    #    for child in timeline:
    #        print(child.tag, child.attrib)
    #        for subchildren in child:
    #            print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ toggle_follow
    def toggle_follow(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    toggle = 'generic'
    if ampache_user == 'generic':
        toggle = 'user'
    # unfollow and refollow for timeline stuff
    ampache.toggle_follow(ampache_url, ampache_api, toggle, api_format)
    togglefollow = ampache.toggle_follow(ampache_url, ampache_api, toggle, api_format)

    """ update_from_tags
    def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id, api_format = 'xml'):
    """
    update_from_tags = ampache.update_from_tags(ampache_url, ampache_api, 'album', single_album, api_format)

    """ update_artist_info

    """
    ampache.update_artist_info(ampache_url, ampache_api, single_artist, api_format)

    """ update_art

    """
    ampache.update_art(ampache_url, ampache_api, 'artist', single_artist, True, api_format)
   
    """ update_podcast

    """
    ampache.update_podcast(ampache_url, ampache_api, 10, api_format)
    
    """ video
    def video(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    #print(ampache.video(ampache_url, ampache_api))

    """ videos
    def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    #print(ampache.videos(ampache_url, ampache_api))

    """ localplay
    def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    """
    #print(ampache.localplay(ampache_url, ampache_api))

    """ democratic
    def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    """
    #print(ampache.democratic(ampache_url, ampache_api))

    """ goodbye
    def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    """
    # Close your session when you're done
    goodbye = ampache.goodbye(ampache_url, ampache_api, api_format)

    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files,'r')
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        newdata = filedata.replace(url_text, "music.com.au")
        newdata = newdata.replace(ampache_api, "eeb9f1b6056246a7d563f479f518bb34")
        newdata = newdata.replace(original_api, "cfj3f237d563f479f5223k23189dbb34")

        f = open("./docs/" + api_format + "-responses/" + files,'w')
        f.write(newdata)
        f.close()


build_docs(ampache_url, ampache_api,ampache_user, 'xml')
build_docs(ampache_url, ampache_api,ampache_user, 'json')

