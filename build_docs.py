#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import sys
import time

from src import ampache

# user variables
url = 'https://demo.ampache.dev'
api = 'demo'
user = 'demodemo'
limit = 4
offset = 0
api_version = '444000'
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=60&uid=4&player=api&name=Synthetic%20-%20BrownSmoke.wma'
try:
    if sys.argv[1]:
        url = sys.argv[1]
    if sys.argv[2]:
        api = sys.argv[2]
    if sys.argv[3]:
        user = sys.argv[3]
except IndexError:
    if os.path.isfile(os.path.join(os.pardir, 'ampache.conf')):
        conf = configparser.RawConfigParser()
        conf.read(os.path.join(os.pardir, 'ampache.conf'))
        url = conf.get('conf', 'ampache_url')
        api = conf.get('conf', 'ampache_apikey')
        user = conf.get('conf', 'ampache_user')
    elif os.path.isfile('docs/examples/ampyche.conf'):
        conf = configparser.RawConfigParser()
        conf.read('docs/examples/ampyche.conf')
        url = conf.get('conf', 'ampache_url')
        api = conf.get('conf', 'ampache_apikey')
        user = conf.get('conf', 'ampache_user')
    else:
        print()
        sys.exit('Error: docs/examples/ampyche.conf not found and no arguments set')


def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    """TODO
    def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
    get_similar: send artist or song id to get related objects from last.fm
    share_create: create a share
    share_edit: edit an existing share
    share_delete: delete an existing share
    podcast_episode_delete: delete an existing podcast_episode
    podcast_create: create a podcast
    podcast_edit: edit an existing podcast
    podcast_delete: delete an existing podcast
    catalogs: get all the catalogs
    catalog: get a catalog by id
    catalog_file: clean, add, verify using the file path (good for scripting)
    """

    """ set_debug
    def set_debug(mybool):
    """
    ampache.set_debug(True)

    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    original_api = ampache_api
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ handshake
    def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = api_version, api_format = 'xml'):
    """
    # bad handshake
    ampache.handshake(ampache_url, 'badkey', '', 0, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/handshake." + api_format):
        shutil.move("docs/" + api_format + "-responses/handshake." + api_format,
                    "docs/" + api_format + "-responses/handshake (error)." + api_format)
    # use correct details
    ampache_session = ampache.handshake(ampache_url, encrypted_key, '', 0, api_version, api_format)
    if not ampache_session:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api, api_format = 'xml'):
    """
    ampache.ping(ampache_url, False, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/ping." + api_format):
        shutil.move("docs/" + api_format + "-responses/ping." + api_format,
                    "docs/" + api_format + "-responses/ping (No Auth)." + api_format)
    # did all this work?
    my_ping = ampache.ping(ampache_url, ampache_session, api_version, api_format)
    if not my_ping:
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ url_to_song
    def url_to_song(ampache_url, ampache_api, url, api_format = 'xml'):
    """
    ampache.url_to_song(ampache_url, ampache_session, song_url, api_format)

    """ user_create
        def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    tempusername = 'temp_user'
    ampache.user_create(ampache_url, ampache_session, tempusername, 'supoersecretpassword', 'email@gmail.com',
                        False, False, api_format)
    ampache.user(ampache_url, ampache_session, tempusername, api_format)

    """ user_edit
        def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    ampache.user_update(ampache_url, ampache_session, tempusername, False, False, False, False, False, False,
                        True, False, api_format)
    ampache.user(ampache_url, ampache_session, tempusername, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (disabled)." + api_format)

    """ user_delete
        def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user_delete(ampache_url, ampache_session, tempusername, api_format)

    """ user
    def user(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user(ampache_url, ampache_session, 'missing_user', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (error)." + api_format)

    myuser = ampache.user(ampache_url, ampache_session, ampache_user, api_format)
    if api_format == 'xml':
        for child in myuser:
            if child.tag == 'user':
                user_id = child.attrib['id']
    else:
        user_id = myuser['user']['id']

    """ get_indexes
    def get_indexes(ampache_url, ampache_api, type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampache.get_indexes(ampache_url, ampache_session, 'song', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'song', False, False, False, False, True, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song with include)." + api_format)
    single_song = 57

    albums = ampache.get_indexes(ampache_url, ampache_session, 'album', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'album', False, False, False, False, True, offset, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album with include)." + api_format)

    artists = ampache.get_indexes(ampache_url, ampache_session, 'artist', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'artist', False, False, False, False, True, offset, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist with include)." + api_format)

    playlists = ampache.get_indexes(ampache_url, ampache_session, 'playlist', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'playlist', False, False, False, False, True, offset, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist with include)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'podcast', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'podcast', False, False, False, False, True, offset, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast with include)." + api_format)

    """ videos
    def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    videos = ampache.videos(ampache_url, ampache_session, False, False, 0, 0, api_format)
    single_video = 1

    """ video
    def video(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.video(ampache_url, ampache_session, single_video, api_format)

    """ advanced_search
    def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['title', 2, 'Dance']]
    search_song = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'song', 0, limit, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'total_count':
                continue
            song_title = child.find('title').text
    else:
        song_title = search_song[0]['title']

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'album', 0, limit, 0,
                                           api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'total_count':
                continue
            album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', 2, 'Car']]
    search_artist = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'artist', 0, limit, 0,
                                            api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'total_count':
                continue
            artist_title = child.find('name').text
    else:
        artist_title = search_artist[0]['name']

    """ album
    def album(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    single_album = 9
    album = ampache.album(ampache_url, ampache_session, single_album, False, api_format)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    """ album_songs
    def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.album_songs(ampache_url, ampache_session, single_album, 0, limit, api_format)

    """ albums
    def albums(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    albums = ampache.albums(ampache_url, ampache_session, album_title, 1, False, False, 0, 10, False, api_format)

    """ stats
    def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.stats(ampache_url, ampache_session, 'song', 'random', ampache_user, None, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (song)." + api_format)

    stats = ampache.stats(ampache_url, ampache_session, 'artist', 'random', ampache_user, False, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (artist)." + api_format)

    single_artist = 19

    stats = ampache.stats(ampache_url, ampache_session, 'album', 'random', ampache_user, None, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (album)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'album':
                single_album = child.attrib['id']
                album_title = child.find('name').text
    else:
        album_title = stats[0]['name']

    """ artist
    def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    artist = ampache.artist(ampache_url, ampache_session, single_artist, False, api_format)

    """ artist_albums
    def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_albums = ampache.artist_albums(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ artist_songs
    def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_songs = ampache.artist_songs(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ artists
    def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    myartists = ampache.artists(ampache_url, ampache_session, False, False, False, 0, limit, False, api_format)

    """ catalog_action
    def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    """
    catalog_action = ampache.catalog_action(ampache_url, ampache_session, 'clean', 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/catalog_action." + api_format):
        shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                    "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    #catalog_action = ampache.catalog_action(ampache_url, ampache_session, 'clean_catalog', 2, api_format)

    """ flag
    def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'playlist', 2, True, api_format)

    """ rate
    def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'playlist', 2, 2, api_format)

    """ record_play
    def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.record_play(ampache_url, ampache_session, 70, user_id, 'AmpacheAPI', api_format)

    """ followers
    def followers(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    followers = ampache.followers(ampache_url, ampache_session, ampache_user, api_format)

    """ following
    def following(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    following = ampache.following(ampache_url, ampache_session, ampache_user, api_format)

    """ friends_timeline
    def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0, api_format = 'xml'):
    """
    friends_timeline = ampache.friends_timeline(ampache_url, ampache_session, limit, 0, api_format)

    """ last_shouts
    def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    """
    last_shouts = ampache.last_shouts(ampache_url, ampache_session, ampache_user, limit, api_format)

    """ playlists
    def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlists = ampache.playlists(ampache_url, ampache_session, False, False, 0, limit, api_format)

    """ playlist_create
    def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    """
    playlist_create = ampache.playlist_create(ampache_url, ampache_session, 'rename', 'private', api_format)

    single_playlist = 2
    if api_format == 'xml':
        for child in playlist_create:
            try:
                if child.tag == 'playlist':
                    tmp_playlist = child.attrib['id']
                    single_playlist = tmp_playlist
            except AttributeError:
                print("child " + child)
                continue
    else:
        print(playlist_create)
        single_playlist = playlist_create[0]['id']

    """ playlist_edit
    def playlist_edit(ampache_url, ampache_api, filter, name = False, type = False, api_format = 'xml'):
    """
    ampache.playlist_edit(ampache_url, ampache_session, single_playlist, 'documentation', 'public', api_format)

    """ playlist_add_song
    def playlist_add_song(ampache_url, ampache_api, filter, song, check = 0, api_format = 'xml'):
    """
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 71, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 72, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 70, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 70, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_add_song." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_add_song." + api_format,
                    "docs/" + api_format + "-responses/playlist_add_song (error)." + api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 70, 0, api_format)

    """ playlist_remove_song
    def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False, api_format = 'xml'):
    """
    ampache.playlist_remove_song(ampache_url, ampache_session, single_playlist, False, 1, api_format)

    """ playlist
    def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    playlist = ampache.playlist(ampache_url, ampache_session, single_playlist, api_format)

    """ playlist_songs
    def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlist_songs = ampache.playlist_songs(ampache_url, ampache_session, single_playlist, 0, limit, api_format)

    """ playlist_delete
    def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.playlist_delete(ampache_url, ampache_session, single_playlist, api_format)

    """ playlist_generate
    def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    'song'|'index'|'id'
    """
    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'song', 0, limit,
                              api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (song)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'index', 0, limit,
                              api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (index)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'id', 0, limit,
                              api_format)
    if os.path.isfile("docs/" + api_format + "-responses/ping." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (id)." + api_format)

    """ scrobble
    def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.scrobble(ampache_url, ampache_session, 'Hear. Life. Spoken', 'Sub Atari Knives', 'Sub Atari Knives',
                     False, False, False, int(time.time()), 'AmpaceApi', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/scrobble." + api_format):
        shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                    "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    ampache.scrobble(ampache_url, ampache_session, 'Sensorisk Deprivation', 'IOK-1', 'Sensorisk Deprivation',
                     False, False, False, int(time.time()), 'test.py', api_format)

    """ record_play
    def record_play(ampache_url, ampache_api, object_id, user, client='AmpacheAPI', api_format='xml'):
    """
    ampache.record_play(ampache_url, ampache_session, 70, ampache_user, 'AmpaceApi', api_format)

    """ rate
    def rate(ampache_url, ampache_api, object_type, object_id, rating, api_format='xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'song', 70, 5, api_format)
    ampache.rate(ampache_url, ampache_session, 'song', 70, 0, api_format)

    """ flag
    def flag(ampache_url, ampache_api, object_type, object_id, flag, api_format='xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'song', 70, True, api_format)
    ampache.flag(ampache_url, ampache_session, 'song', 70, False, api_format)

    """ get_art
    def get_art(ampache_url, ampache_api, object_id, object_type, destination, api_format='xml'):
    """
    ampache.get_art(ampache_url, ampache_session, 70, 'song', (os.path.join(os.getcwd(), 'get_art.jpg')), api_format)

    """ search_songs
    def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampache.search_songs(ampache_url, ampache_session, song_title, 0, limit, api_format)

    """ song
    def song(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    song = ampache.song(ampache_url, ampache_session, single_song, api_format)

    """ songs
    def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    songs = ampache.songs(ampache_url, ampache_session, False, False, False, False, 0, limit, api_format)

    """ tags
    def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampache.tags(ampache_url, ampache_session, 'Da', False, 0, limit, api_format)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'total_count':
                continue
            genre = child.attrib['id']
    else:
        genre = tags[0]['tag']
        for tag in genre:
            tmp_genre = tag['id']
        genre = tmp_genre

    """ tag
    def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.tag(ampache_url, ampache_session, genre, api_format)

    """ tag_albums
    def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_albums = ampache.tag_albums(ampache_url, ampache_session, genre, 0, 2, api_format)

    """ tag_artists
    def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_artists = ampache.tag_artists(ampache_url, ampache_session, genre, 0, 1, api_format)

    """ tag_songs
    def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.tag_songs(ampache_url, ampache_session, genre, 0, 1, api_format)

    """ licenses
    def licenses(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.licenses(ampache_url, ampache_session, False, False, 0, limit, api_format)

    """ license
    def license(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license(ampache_url, ampache_session, 1, api_format)

    """ license_songs
    def license_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license_songs(ampache_url, ampache_session, 1, api_format)

    """ podcast
    def podcast_episodes(ampache_url, ampache_api, filter_str=False, exact=False, offset=0, limit=0, api_format='xml'):
    """
    ampache.podcast(ampache_url, ampache_session, 1, False, False, api_format)

    """ podcast_episodes
    def podcast_episodes(ampache_url, ampache_api, filter_str=False, exact=False, offset=0, limit=0, api_format='xml'):
    """
    ampache.podcast_episodes(ampache_url, ampache_session, 1, offset, limit, api_format)

    """ podcast_episodes
    def podcast_episode(ampache_url, ampache_api, filter_str, offset=0, limit=0, api_format='xml'):
    """
    ampache.podcast_episode(ampache_url, ampache_session, 47, offset, limit, api_format)

    """ podcasts
    def podcasts(ampache_url, ampache_api, filter_str=False, exact=False, offset=0, limit=0, api_format='xml'):
    """
    ampache.podcasts(ampache_url, ampache_session, False, False, 0, 4, api_format)

    """ shares
    """
    shares = ampache.shares(ampache_url, ampache_session, False, False, offset, limit, api_format)
    if api_format == 'xml':
        for child in shares:
            if child.tag == 'share':
                share_id = child.attrib['id']
    else:
        share_id = shares[0]['id']

    """ share
    def share(ampache_url, ampache_api, filter_str, offset=0, limit=0, api_format='xml'):
    """
    ampache.share(ampache_url, ampache_session, share_id, offset, limit, api_format)

    """ share_create
    def share_create(ampache_url, ampache_api, filter_str, object_type, description=False, expires=False, api_format='xml')
    """
    """
    share_create = ampache.share_create(ampache_url, ampache_session, single_song, 'song', False, False, api_format)
    share_new = 1
    if api_format == 'xml':
        for child in share_create:
            try:
                if child.tag == 'share':
                    share_new = child.attrib['id']
            except AttributeError:
                print("child: " + child)
                continue
    else:
        print(share_create)
        share_new = share_create[0]['id']
    """

    """ share_edit
    """
    """
    ampache.share_edit(ampache_url, ampache_session, share_new, 0, 0, False, False, api_format)
    """

    """ share_delete
    """
    """
    ampache.share_delete(ampache_url, ampache_session, share_new, api_format)
    """

    """ timeline
    def timeline(ampache_url, ampache_api, username, limit = 0, since = 0, api_format = 'xml'):
    """
    ampache.timeline(ampache_url, ampache_session, ampache_user, 10, 0, api_format)

    """ toggle_follow
    def toggle_follow(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    toggle = 'generic'
    if ampache_user == 'generic':
        toggle = 'user'
    # unfollow and refollow for timeline stuff
    ampache.toggle_follow(ampache_url, ampache_session, toggle, api_format)
    ampache.toggle_follow(ampache_url, ampache_session, toggle, api_format)

    """ update_from_tags
    def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id, api_format = 'xml'):
    """
    ampache.update_from_tags(ampache_url, ampache_session, 'album', single_album, api_format)

    """ update_artist_info
    def update_artist_info(ampache_url, ampache_api, object_id, api_format='xml')
    """
    ampache.update_artist_info(ampache_url, ampache_session, single_artist, api_format)

    """ update_art
    def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite: bool = False, api_format: str = 'xml')
    """
    ampache.update_art(ampache_url, ampache_session, 'artist', 20, True, api_format)

    """ update_podcast
    def update_podcast(ampache_url, ampache_api, filter_str, api_format='xml'):
    """
    ampache.update_podcast(ampache_url, ampache_session, 1, api_format)

    """ localplay
    def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    """
    ampache.localplay(ampache_url, ampache_session, 'status', False, False, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/localplay." + api_format):
        shutil.move("docs/" + api_format + "-responses/localplay." + api_format,
                    "docs/" + api_format + "-responses/localplay (status)." + api_format)

    ampache.localplay(ampache_url, ampache_session, 'stop', False, False, 0, api_format)

    """ democratic
    def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    """
    # print(ampache.democratic(ampache_url, ampache_api))

    """ goodbye
    def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    """
    # Close your session when you're done
    ampache.goodbye(ampache_url, ampache_session, api_format)

    # Clean the files
    self_check(api_format, ampache_url, ampache_session, original_api)


def self_check(api_format, ampache_url, ampache_api, ampache_session):
    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files, 'r', encoding="utf-8")
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        url_text = ampache_url.replace("http://", "")
        newdata = re.sub(url_text, "music.com.au", filedata)
        newdata = re.sub("CDATA\[\/media\/", "CDATA[/mnt/files-music/ampache-test/", newdata)
        newdata = re.sub("\\\/media\\\/", "\\\/mnt\\\/files-music\\\/ampache-test\\\/", newdata)
        newdata = re.sub(url_text.replace("/", "\\\/"), "music.com.au", newdata)
        newdata = re.sub("http://music.com.au", "https://music.com.au", newdata)
        newdata = re.sub("http:\\\/\\\/music.com.au", "https:\\\/\\\/music.com.au", newdata)
        newdata = re.sub("\"session_expire\": \".*\"", "\"session_expire\": \"2022-08-17T06:21:00+00:00\"", newdata)
        newdata = re.sub("<session_expire>.*</session_expire>", "<session_expire><![CDATA[2022-08-17T04:34:55+00:00]]></session_expire>", newdata)
        newdata = re.sub("\"delete_time\": \".*\"", "\"delete_time\": \"1670202698\"", newdata)
        newdata = re.sub("<delete_time>.*</delete_time>", "<delete_time>1670202698</delete_time>", newdata)
        newdata = re.sub("\"create_date\": \".*\"", "\"create_date\": \"1670202701\"", newdata)
        newdata = re.sub("<create_date>.*</create_date>", "<create_date>1670202701</create_date>", newdata)
        newdata = re.sub("\"creation_date\": \"[0-9]*\"", "\"creation_date\": \"1670202706\"", newdata)
        newdata = re.sub("<creation_date>[0-9]*</creation_date>", "<creation_date>1670202706</creation_date>", newdata)
        newdata = re.sub("\"sync_date\": \".*\"", "\"sync_date\": \"2022-08-17T05:07:11+00:00\"", newdata)
        newdata = re.sub("<sync_date>.*</sync_date>", "<sync_date><![CDATA[2022-08-17T05:07:11+00:00]]></sync_date>", newdata)
        newdata = re.sub(ampache_api, "eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub(ampache_session, "cfj3f237d563f479f5223k23189dbb34", newdata)
        newdata = re.sub('auth=[a-z0-9]*', "auth=eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('ssid=[a-z0-9]*', "ssid=cfj3f237d563f479f5223k23189dbb34", newdata)

        f = open("./docs/" + api_format + "-responses/" + files, 'w', encoding="utf-8")
        f.write(newdata)
        f.close()


build_docs(url, api, user, 'xml')
build_docs(url, api, user, 'json')
