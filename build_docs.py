#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import sys
import time

from src import ampache

# user variables
url = None
api = None
user = None
try:
    if sys.argv[1]:
        url = sys.argv[1]
    if sys.argv[2]:
        api = sys.argv[2]
    if sys.argv[3]:
        user = sys.argv[3]
except IndexError:
    if os.path.isfile('docs/examples/ampyche.conf'):
        conf = configparser.RawConfigParser()
        conf.read('docs/examples/ampyche.conf')
        if not url:
            url = conf.get('conf', 'ampache_url')
        if not api:
            api = conf.get('conf', 'ampache_apikey')
        if not user:
            user = conf.get('conf', 'ampache_user')

limit = 4
offset = 0
api_version = '5.0.0'
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=60&uid=4&player=api&name=Synthetic%20-%20BrownSmoke.wma'


def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    """TODO
    def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
    get_similar: send artist or song id to get related objects from last.fm
    podcast_episode_delete: delete an existing podcast_episode
    catalogs: get all the catalogs
    catalog: get a catalog by id
    catalog_file: clean, add, verify using the file path (good for scripting)
    """

    """ def set_debug(boolean):
        This function can be used to enable/disable debugging messages
    """
    ampache.set_debug(True)

    # send a bad ping
    ampache.ping(ampache_url, False, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/ping." + api_format):
        shutil.move("docs/" + api_format + "-responses/ping." + api_format,
                    "docs/" + api_format + "-responses/ping (no auth)." + api_format)

    """ def encrypt_string(ampache_api, user)
        This function can be used to encrypt your apikey into the accepted format.
    """
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '5.0.0', api_format = 'xml'):
        This is the function that handles verifying a new handshake
        Takes a timestamp, auth key, and username.
    """
    # bad handshake
    ampache.handshake(ampache_url, 'badkey', False, False, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/handshake." + api_format):
        shutil.move("docs/" + api_format + "-responses/handshake." + api_format,
                    "docs/" + api_format + "-responses/handshake (error)." + api_format)
    # use correct details
    ampache_session = ampache.handshake(ampache_url, encrypted_key, False, False, api_version, api_format)
    if not ampache_session:
        print(encrypted_key)
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ def ping(ampache_url, ampache_api, api_format = 'xml'):
        This can be called without being authenticated, it is useful for determining if what the status
        of the server is, and what version it is running/compatible with
    """
    my_ping = ampache.ping(ampache_url, ampache_session, api_version, api_format)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ def system_update(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """
    ampache.system_update(ampache_url, ampache_session, api_format)

    """ def labels(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.labels(ampache_url, ampache_session, False, False, offset, limit, api_format)

    """ def label(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.label(ampache_url, ampache_session, 1677, api_format)

    """ def label_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.label_artists(ampache_url, ampache_session, 1677, api_format)

    """ def url_to_song(ampache_url, ampache_api, url, api_format = 'xml'):
    """
    ampache.url_to_song(ampache_url, ampache_session, song_url, api_format)

    """ def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    tempusername = 'temp_user'
    ampache.user_create(ampache_url, ampache_session, tempusername, 'supoersecretpassword', 'email@gmail.com', False, False, api_format)
    ampache.user(ampache_url, ampache_session, tempusername, api_format)

    """ def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    ampache.user_update(ampache_url, ampache_session, tempusername, False, False, False, False, False, False, True, False, api_format)
    ampache.user(ampache_url, ampache_session, tempusername, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (disabled)." + api_format)

    """ def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user_delete(ampache_url, ampache_session, tempusername, api_format)

    """ def user(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user(ampache_url, ampache_session, 'missing_user', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (error)." + api_format)

    myuser = ampache.user(ampache_url, ampache_session, 'demo', api_format)
    if api_format == 'xml':
        for child in myuser:
            if child.tag == 'user':
                myuser = child.attrib['id']
    else:
        user_id = myuser['id']

    """ def get_indexes(ampache_url, ampache_api, object_type, filter_str, exact, add, update, include, offset, limit, api_format)):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampache.get_indexes(ampache_url, ampache_session, 'song', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song)." + api_format)
    single_song = ampache.get_id_list(songs, 'song', api_format)[0]

    ampache.get_indexes(ampache_url, ampache_session, 'song', False, False, False, False, True, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song with include)." + api_format)

    albums = ampache.get_indexes(ampache_url, ampache_session, 'album', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album)." + api_format)
    single_album = ampache.get_id_list(albums, 'album', api_format)[0]

    ampache.get_indexes(ampache_url, ampache_session, 'album', False, False, False, False, True, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album with include)." + api_format)
    single_album = ampache.get_id_list(albums, 'album', api_format)[0]

    artists = ampache.get_indexes(ampache_url, ampache_session, 'artist', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist)." + api_format)
    single_artist = ampache.get_id_list(artists, 'artist', api_format)[0]

    ampache.get_indexes(ampache_url, ampache_session, 'artist', False, False, False, False, True, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist with include)." + api_format)
    single_artist = ampache.get_id_list(artists, 'artist', api_format)[0]

    playlists = ampache.get_indexes(ampache_url, ampache_session, 'playlist', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist)." + api_format)
    single_playlist = ampache.get_id_list(playlists, 'playlist', api_format)[0]

    ampache.get_indexes(ampache_url, ampache_session, 'playlist', False, False, False, False, True, offset, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist with include)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'podcast', False, False, False, False, False, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast)." + api_format)

    ampache.get_indexes(ampache_url, ampache_session, 'podcast', False, False, False, False, True, offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast with include)." + api_format)

    """ def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    videos = ampache.videos(ampache_url, ampache_session, False, False, 0, 0, api_format)
    single_video = 1262

    """ def video(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.video(ampache_url, ampache_session, single_video, api_format)

    """ def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['title', 2, 'D']]
    search_song = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'song', offset, limit, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    if api_format == 'xml':
        song_id = search_song[1].attrib['id']
    else:
        print(search_song['song'][0]['title'])
        song_id = search_song['song'][0]['id']
    song_title = "Fasten Your Seatbelt"

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'album', offset, limit, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album['album'][0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', 2, 'Car']]
    search_artist = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'artist', offset, limit, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'artist':
                artist_title = child.find('name').text
    else:
        artist_title = search_artist['artist'][0]['name']

    """ def album(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    ampache.album(ampache_url, ampache_session, single_album, True, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/album." + api_format):
        shutil.move("docs/" + api_format + "-responses/album." + api_format,
                    "docs/" + api_format + "-responses/album (with include)." + api_format)

    album = ampache.album(ampache_url, ampache_session, single_album, False, api_format)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album['album'][0]['name']

    """ def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.album_songs(ampache_url, ampache_session, single_album, offset, limit, api_format)

    """ def albums(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampache.albums(ampache_url, ampache_session, album_title, 1, False, False, 0, 2, True, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/albums." + api_format):
        shutil.move("docs/" + api_format + "-responses/albums." + api_format,
                    "docs/" + api_format + "-responses/albums (with include)." + api_format)

    albums = ampache.albums(ampache_url, ampache_session, album_title, 1, False, False, 0, 10, False, api_format)

    """ def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """

    ampache.stats(ampache_url, ampache_session, 'song', 'random', ampache_user, None, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (song)." + api_format)

    stats = ampache.stats(ampache_url, ampache_session, 'artist', 'random', ampache_user, False, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (artist)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'artist':
                print('\ngetting a random artist using the stats method and found', child.find('name').text)
                single_artist = child.attrib['id']
                print(child.tag, child.attrib)
    else:
        single_artist = stats['artist'][0]['id']

    stats = ampache.stats(ampache_url, ampache_session, 'album', 'random', ampache_user, None, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (album)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'album':
                print('\ngetting a random album using the stats method and found', child.find('name').text)
                single_album = child.attrib['id']
                album_title = child.find('name').text
    else:
        album_title = stats['album'][0]['name']

    """ def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    ampache.artist(ampache_url, ampache_session, single_artist, True, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include songs,albums)." + api_format)
    ampache.artist(ampache_url, ampache_session, single_artist, 'songs', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include songs)." + api_format)
    ampache.artist(ampache_url, ampache_session, single_artist, 'albums', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include albums)." + api_format)
    artist = ampache.artist(ampache_url, ampache_session, single_artist, False, api_format)

    if api_format == 'xml':
        for child in artist:
            if child.tag == 'artist':
                print('\nsearching for an artist with this id', single_artist)

    """ def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_albums(ampache_url, ampache_session, single_artist, offset, limit, api_format)

    """ def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_songs(ampache_url, ampache_session, single_artist, offset, limit, api_format)

    """ def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampache.artists(ampache_url, ampache_session, False, False, False, offset, limit, True, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs,albums)." + api_format)
    ampache.artists(ampache_url, ampache_session, False, False, False, offset, limit, 'songs', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs)." + api_format)
    ampache.artists(ampache_url, ampache_session, False, False, False, offset, limit, 'albums', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include albums)." + api_format)
    ampache.artists(ampache_url, ampache_session, False, False, False, offset, limit, False, api_format)

    """ def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    """
    ampache.catalog_action(ampache_url, ampache_session, 'clean', 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/catalog_action." + api_format):
        shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                    "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    ampache.catalog_action(ampache_url, ampache_session, 'clean_catalog', 2, api_format)

    """ def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'playlist', 70, True, api_format)

    """ def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'playlist', 70, 2, api_format)

    """ def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.record_play(ampache_url, ampache_session, song_id, 4, 'debug', api_format)

    """ def followers(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.followers(ampache_url, ampache_session, ampache_user, api_format)

    """ def following(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.following(ampache_url, ampache_session, ampache_user, api_format)

    """ def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0, api_format = 'xml'):
    """
    ampache.friends_timeline(ampache_url, ampache_session, limit, 0, api_format)

    """ def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    """
    ampache.last_shouts(ampache_url, ampache_session, ampache_user, limit, api_format)

    """ def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.playlists(ampache_url, ampache_session, False, False, offset, limit, api_format)

    """ def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    """
    playlist_create = ampache.playlist_create(ampache_url, ampache_session, 'rename', 'private', api_format)

    if api_format == 'xml':
        for child in playlist_create:
            if child.tag == 'playlist':
                tmp_playlist = child.attrib['id']
        single_playlist = tmp_playlist
    else:
        single_playlist = playlist_create['id']

    """ def playlist_edit(ampache_url, ampache_api, filter, name = False, type = False, api_format = 'xml'):
    """
    ampache.playlist_edit(ampache_url, ampache_session, single_playlist, 'documentation', 'public', api_format)

    """ def playlist_add_song(ampache_url, ampache_api, filter, song, check = 0, api_format = 'xml'):
    """
    ampache.playlist_add_song(ampache_url, ampache_api, single_playlist, 71, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_api, single_playlist, 72, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, single_song, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, single_song, 1, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_add_song." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_add_song." + api_format,
                    "docs/" + api_format + "-responses/playlist_add_song (error)." + api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, single_song, 1, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, single_song, 0, api_format)

    """ def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False, api_format = 'xml'):
    """
    ampache.playlist_remove_song(ampache_url, ampache_session, single_playlist, False, 1, api_format)

    """ def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.playlist(ampache_url, ampache_session, single_playlist, api_format)

    """ def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.playlist_songs(ampache_url, ampache_session, single_playlist, offset, limit, api_format)

    """ def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    #ampache.playlist_delete(ampache_url, ampache_session, single_playlist, api_format)

    """ def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    'song'|'index'|'id'
    """
    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'song', offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (song)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'index', offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (index)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'id', offset, limit, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (id)." + api_format)

    """ def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.scrobble(ampache_url, ampache_session, 'Hear. Life. Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False, int(time.time()), 'debug', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/scrobble." + api_format):
        shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                    "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    ampache.scrobble(ampache_url, ampache_session, 'Sensorisk Deprivation', 'IOK-1', 'Sensorisk Deprivation', False, False, False, int(time.time()), 'debug', api_format)

    """ def record_play(ampache_url, ampache_api, object_id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.record_play(ampache_url, ampache_session, 70, ampache_user, 'debug', api_format)

    """ def rate(ampache_dexesurl, ampache_api, object_type, object_id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'song', 70, 5, api_format)
    ampache.rate(ampache_url, ampache_session, 'song', 70, 0, api_format)

    """ def flag(ampache_url, ampache_api, object_type, object_id, flag, api_format = 'xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'song', 70, True, api_format)
    ampache.flag(ampache_url, ampache_session, 'song', 70, False, api_format)

    """ def get_art(ampache_url, ampache_api, object_id, object_type, destination, api_format = 'xml'):
    """
    ampache.get_art(ampache_url, ampache_session, 70, 'song', (os.path.join(os.getcwd(), 'get_art.jpg')), api_format)
    
    """ def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampache.search_songs(ampache_url, ampache_session, song_title, offset, limit, api_format)

    if api_format == 'xml':
        for child in search_songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def song(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    song = ampache.song(ampache_url, ampache_session, single_song, api_format)

    if api_format == 'xml':
        for child in song:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    songs = ampache.songs(ampache_url, ampache_session, False, False, False, False, offset, limit, api_format)
    if api_format == 'xml':
        for child in songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genres(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampache.genres(ampache_url, ampache_session, 'D', False, offset, limit, api_format)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'genre':
                genre = child.attrib['id']
    else:
        for tag in tags['genre']:
            print(tag)
            tmp_genre = tag['id']
        genre = tmp_genre

    """ def genre(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.genre(ampache_url, ampache_session, genre, api_format)

    """ def genre_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre_albums = ampache.genre_albums(ampache_url, ampache_session, genre, 0, 2, api_format)
    if api_format == 'xml':
        for child in genre_albums:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genre_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre_artists = ampache.genre_artists(ampache_url, ampache_session, genre, 0, 1, api_format)
    if api_format == 'xml':
        for child in genre_artists:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genre_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.genre_songs(ampache_url, ampache_session, genre, 0, 1, api_format)

    """ def licenses(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.licenses(ampache_url, ampache_session, False, False, offset, limit, api_format)

    """ def license(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license(ampache_url, ampache_session, 1, api_format)

    """ def license_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license_songs(ampache_url, ampache_session, 1, api_format)

    """ def labels(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.labels(ampache_url, ampache_session, False, False, offset, limit, api_format)

    """ def label(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.label(ampache_url, ampache_session, 1677, api_format)

    """ def label_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.label_artists(ampache_url, ampache_session, 1677, api_format)

    """ def podcasts(ampache_url, ampache_api, filter_str = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.podcasts(ampache_url, ampache_session, False, False, 0, 4, api_format)

    """ def podcast(ampache_url, ampache_api, filter_str, api_format = 'xml'):
    """
    ampache.podcast(ampache_url, ampache_session, 10, 'episodes', api_format)
    if os.path.isfile("docs/" + api_format + "-responses/podcast." + api_format):
        shutil.move("docs/" + api_format + "-responses/podcast." + api_format,
                    "docs/" + api_format + "-responses/podcast (include episodes)." + api_format)

    ampache.podcast(ampache_url, ampache_session, 10, False, api_format)

    """ def podcast_episodes
    """
    ampache.podcast_episodes(ampache_url, ampache_session, 10, offset, limit, api_format)
    """ def podcast_episode
    """
    ampache.podcast_episode(ampache_url, ampache_session, 6394, api_format)

    """ def podcast_create
    """
    ampache.podcast_create(ampache_url, ampache_session, 'https://www.abc.net.au/radio/programs/trace/feed/8597522/podcast.xml', 7, api_format)

    """ def podcast_edit(ampache_url, ampache_api, filter_str, stream, download, expires, description, api_format)
    """
    ampache.podcast_edit(ampache_url, ampache_session, 10, 1, 1, False, False, api_format)

    """ def podcast_delete
    """
    # ampache.podcast_delete(ampache_url, ampache_session, 56, api_format)

    """ def update_podcast(ampache_url, ampache_api, filter_str, api_format = 'xml'):
    """
    ampache.update_podcast(ampache_url, ampache_session, 10, api_format)

    """ shares
    """
    shares = ampache.shares(ampache_url, ampache_session, False, False, offset, limit, api_format)
    share_id = ampache.get_id_list(shares, 'share', api_format)[0]

    """ share
    """
    ampache.share(ampache_url, ampache_session, share_id, api_format)

    """ share_create
    """
    share_create = ampache.share_create(ampache_url, ampache_session, single_song, 'song', False, False, api_format)
    if api_format == 'xml':
        share_new = share_create[1].attrib['id']
    else:
        share_new = share_create['id']

    """ share_edit
    """
    ampache.share_edit(ampache_url, ampache_session, share_new, 0, 0, False, False, api_format)

    """ share_delete
    """
    ampache.share_delete(ampache_url, ampache_session, share_new, api_format)

    """ def timeline(ampache_url, ampache_api, username, limit = 0, since = 0, api_format = 'xml'):
    """
    ampache.timeline(ampache_url, ampache_session, ampache_user, 10, 0, api_format)

    """ def toggle_follow(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    toggle = 'generic'
    if ampache_user == 'generic':
        toggle = 'user'
    # unfollow and refollow for timeline stuff
    ampache.toggle_follow(ampache_url, ampache_session, toggle, api_format)
    ampache.toggle_follow(ampache_url, ampache_session, toggle, api_format)

    """ def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id, api_format = 'xml'):
    """
    ampache.update_from_tags(ampache_url, ampache_session, 'album', single_album, api_format)

    """ def update_artist_info(ampache_url, ampache_api, id, api_format = 'xml'):
    """
    ampache.update_artist_info(ampache_url, ampache_session, single_artist, api_format)

    """ def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    """
    ampache.update_art(ampache_url, ampache_session, 'artist', single_artist, True, api_format)

    """ def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    """
    ampache.localplay(ampache_url, ampache_session, 'status', False, False, 0, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/localplay." + api_format):
        shutil.move("docs/" + api_format + "-responses/localplay." + api_format,
                    "docs/" + api_format + "-responses/localplay (status)." + api_format)

    ampache.localplay(ampache_url, ampache_session, 'stop', False, False, 0, api_format)

    """ def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    """
    # ampache.democratic(ampache_url, ampache_session)

    """ def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    Close your session when you're done
    """
    # ampache.goodbye(ampache_url, ampache_session, api_format)

    # Clean the files
    self_check(api_format, ampache_url, ampache_api, ampache_session)


def self_check(api_format, ampache_url, ampache_api, ampache_session):
    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files, 'r', encoding="utf-8")
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        newdata = re.sub(url_text, "music.com.au", filedata)
        newdata = re.sub(ampache_api, "eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('auth=[a-z0-9]*', "auth=eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('ssid=[a-z0-9]*', "ssid=cfj3f237d563f479f5223k23189dbb34", newdata)
        newdata = re.sub(ampache_session, "cfj3f237d563f479f5223k23189dbb34", newdata)

        f = open("./docs/" + api_format + "-responses/" + files, 'w', encoding="utf-8")
        f.write(newdata)
        f.close()


build_docs(url, api, user, 'xml')
build_docs(url, api, user, 'json')

