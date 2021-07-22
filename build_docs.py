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
    ampacheConnection = ampache.API()
    """TODO
    def stream(id, type, destination, api_format = 'xml'):
    def download(id, type, destination, format = 'raw', api_format = 'xml'):
    get_similar: send artist or song id to get related objects from last.fm
    podcast_episode_delete: delete an existing podcast_episode
    catalogs: get all the catalogs
    catalog: get a catalog by id
    catalog_file: clean, add, verify using the file path (good for scripting)
    """

    """ def set_debug(boolean):
        This function can be used to enable/disable debugging messages
    """
    ampacheConnection.set_debug(True)
    ampacheConnection.set_format(api_format)

    # send a bad ping
    ampacheConnection.ping(ampache_url, False, api_version)
    if os.path.isfile("docs/" + api_format + "-responses/ping." + api_format):
        shutil.move("docs/" + api_format + "-responses/ping." + api_format,
                    "docs/" + api_format + "-responses/ping (no auth)." + api_format)

    """ def encrypt_string(ampache_api, user)
        This function can be used to encrypt your apikey into the accepted format.
    """
    encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)

    """ def handshake(user = False, timestamp = False, version = '5.0.0', api_format = 'xml'):
        This is the function that handles verifying a new handshake
        Takes a timestamp, auth key, and username.
    """
    # bad handshake
    ampacheConnection.handshake(ampache_url, 'badkey', False, False, api_version)
    if os.path.isfile("docs/" + api_format + "-responses/handshake." + api_format):
        shutil.move("docs/" + api_format + "-responses/handshake." + api_format,
                    "docs/" + api_format + "-responses/handshake (error)." + api_format)
    # use correct details
    ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key, False, False, api_version)
    if not ampache_session:
        print(encrypted_key)
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ def ping(api_format = 'xml'):
        This can be called without being authenticated, it is useful for determining if what the status
        of the server is, and what version it is running/compatible with
    """
    my_ping = ampacheConnection.ping(ampache_url, ampache_session, api_version)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ def system_update(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """
    ampacheConnection.system_update()

    """ def labels(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.labels(False, False, offset, limit)

    """ def label(filter, api_format = 'xml'):
    """
    ampacheConnection.label(1677)

    """ def label_songs(filter, api_format = 'xml'):
    """
    ampacheConnection.label_artists(1677)

    """ def url_to_song(url, api_format = 'xml'):
    """
    ampacheConnection.url_to_song(song_url)

    """ def user_create(username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    tempusername = 'temp_user'
    ampacheConnection.user_create(tempusername, 'supoersecretpassword', 'email@gmail.com', False, False)
    ampacheConnection.user(tempusername)

    """ def user_update(username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    ampacheConnection.user_update(tempusername, False, False, False, False, False, False, True, False)
    ampacheConnection.user(tempusername)
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (disabled)." + api_format)

    """ def user_delete(username, api_format = 'xml'):
    """
    ampacheConnection.user_delete(tempusername)

    """ def user(username, api_format = 'xml'):
    """
    ampacheConnection.user('missing_user')
    if os.path.isfile("docs/" + api_format + "-responses/user." + api_format):
        shutil.move("docs/" + api_format + "-responses/user." + api_format,
                    "docs/" + api_format + "-responses/user (error)." + api_format)

    myuser = ampacheConnection.user('demo')
    if api_format == 'xml':
        for child in myuser:
            if child.tag == 'user':
                myuser = child.attrib['id']
    else:
        user_id = myuser['id']

    """ def get_indexes(object_type, filter_str, exact, add, update, include, offset, limit)):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampacheConnection.get_indexes('song', False, False, False, False, False, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song)." + api_format)
    single_song = ampacheConnection.get_id_list(songs, 'song')[0]

    ampacheConnection.get_indexes('song', False, False, False, False, True, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (song with include)." + api_format)

    albums = ampacheConnection.get_indexes('album', False, False, False, False, False, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album)." + api_format)
    single_album = ampacheConnection.get_id_list(albums, 'album')[0]

    ampacheConnection.get_indexes('album', False, False, False, False, True, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (album with include)." + api_format)
    single_album = ampacheConnection.get_id_list(albums, 'album')[0]
    single_album = 12

    artists = ampacheConnection.get_indexes('artist', False, False, False, False, False, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist)." + api_format)
    single_artist = ampacheConnection.get_id_list(artists, 'artist')[0]

    ampacheConnection.get_indexes('artist', False, False, False, False, True, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (artist with include)." + api_format)
    single_artist = ampacheConnection.get_id_list(artists, 'artist')[0]

    playlists = ampacheConnection.get_indexes('playlist', False, False, False, False, False, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist)." + api_format)
    single_playlist = ampacheConnection.get_id_list(playlists, 'playlist')[0]

    ampacheConnection.get_indexes('playlist', False, False, False, False, True, offset, 1)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (playlist with include)." + api_format)

    ampacheConnection.get_indexes('podcast', False, False, False, False, False, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast)." + api_format)

    ampacheConnection.get_indexes('podcast', False, False, False, False, True, offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/get_indexes." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                    "docs/" + api_format + "-responses/get_indexes (podcast with include)." + api_format)

    """ def videos(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    videos = ampacheConnection.videos(False, False, 0, 0)
    single_video = 1

    """ def video(filter, api_format = 'xml'):
    """
    ampacheConnection.video(single_video)

    """ def advanced_search(rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['title', 2, 'D']]
    search_song = ampacheConnection.advanced_search(search_rules, 'or', 'song', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    if api_format == 'xml':
        song_id = search_song[1].attrib['id']
    else:
        print(search_song['song'][0]['title'])
        song_id = search_song['song'][0]['id']
    song_title = "Fasten Your Seatbelt"

    search_rules = [['artist', 0, 'Synthetic']]
    search_album = ampacheConnection.advanced_search(search_rules, 'or', 'album', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album['album'][0]['name']

    search_rules = [['artist', 2, 'CARN'], ['artist', 2, 'Synthetic']]
    search_artist = ampacheConnection.advanced_search(search_rules, 'or', 'artist', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'artist':
                artist_title = child.find('name').text
    else:
        artist_title = search_artist['artist'][0]['name']

    """ def album(filter, include = False, api_format = 'xml'):
    """
    ampacheConnection.album(single_album, True)
    if os.path.isfile("docs/" + api_format + "-responses/album." + api_format):
        shutil.move("docs/" + api_format + "-responses/album." + api_format,
                    "docs/" + api_format + "-responses/album (with include)." + api_format)

    album = ampacheConnection.album(single_album, False)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album['album'][0]['name']

    """ def album_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.album_songs(single_album, offset, limit)

    """ def albums(filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampacheConnection.albums(album_title, 1, False, False, 0, 2, True)
    if os.path.isfile("docs/" + api_format + "-responses/albums." + api_format):
        shutil.move("docs/" + api_format + "-responses/albums." + api_format,
                    "docs/" + api_format + "-responses/albums (with include)." + api_format)

    albums = ampacheConnection.albums(album_title, 1, False, False, 0, 10, False)

    """ def stats(type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """

    ampacheConnection.stats('song', 'random', ampache_user, None, 0, 2)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (song)." + api_format)

    stats = ampacheConnection.stats('artist', 'random', ampache_user, False, 0, 2)
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
    single_artist = 2

    stats = ampacheConnection.stats('album', 'random', ampache_user, None, 0, 2)
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

    """ def artist(filter, include = False, api_format = 'xml'):
    """
    ampacheConnection.artist(single_artist, True)
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include songs,albums)." + api_format)
    ampacheConnection.artist(single_artist, 'songs')
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include songs)." + api_format)
    ampacheConnection.artist(single_artist, 'albums')
    if os.path.isfile("docs/" + api_format + "-responses/artist." + api_format):
        shutil.move("docs/" + api_format + "-responses/artist." + api_format,
                    "docs/" + api_format + "-responses/artist (with include albums)." + api_format)
    artist = ampacheConnection.artist(single_artist, False)

    if api_format == 'xml':
        for child in artist:
            if child.tag == 'artist':
                print('\nsearching for an artist with this id', single_artist)

    """ def artist_albums(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.artist_albums(single_artist, offset, limit)

    """ def artist_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.artist_songs(single_artist, offset, limit)

    """ def artists(filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampacheConnection.artists(False, False, False, offset, limit, True)
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs,albums)." + api_format)
    ampacheConnection.artists(False, False, False, offset, limit, 'songs')
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs)." + api_format)
    ampacheConnection.artists(False, False, False, offset, limit, 'albums')
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include albums)." + api_format)
    ampacheConnection.artists(False, False, False, offset, limit, False)

    """ def catalog_action(task, catalog, api_format = 'xml'):
    """
    ampacheConnection.catalog_action('clean', 2)
    if os.path.isfile("docs/" + api_format + "-responses/catalog_action." + api_format):
        shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                    "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    ampacheConnection.catalog_action('clean_catalog', 2)

    """ def flag(type, id, flag, api_format = 'xml'):
    """
    ampacheConnection.flag('playlist', 2, True)

    """ def rate(type, id, rating, api_format = 'xml'):
    """
    ampacheConnection.rate('playlist', 2, 2)

    """ def record_play(id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampacheConnection.record_play(song_id, 4, 'debug')

    """ def followers(username, api_format = 'xml'):
    """
    ampacheConnection.followers(ampache_user)

    """ def following(username, api_format = 'xml'):
    """
    ampacheConnection.following(ampache_user)

    """ def friends_timeline(limit = 0, since = 0, api_format = 'xml'):
    """
    ampacheConnection.friends_timeline(limit, 0)

    """ def last_shouts(username, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.last_shouts(ampache_user, limit)

    """ def playlists(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.playlists(False, False, offset, limit)

    """ def playlist_create(name, type, api_format = 'xml'):
    """
    playlist_create = ampacheConnection.playlist_create('rename', 'private')

    if api_format == 'xml':
        for child in playlist_create:
            if child.tag == 'playlist':
                tmp_playlist = child.attrib['id']
        single_playlist = tmp_playlist
    else:
        single_playlist = playlist_create['id']

    """ def playlist_edit(filter, name = False, type = False, api_format = 'xml'):
    """
    ampacheConnection.playlist_edit(single_playlist, 'documentation', 'public')

    """ def playlist_add_song(filter, song, check = 0, api_format = 'xml'):
    """
    ampacheConnection.playlist_add_song(single_playlist, 71, 0)
    ampacheConnection.playlist_add_song(single_playlist, 72, 0)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 0)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 1)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_add_song." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_add_song." + api_format,
                    "docs/" + api_format + "-responses/playlist_add_song (error)." + api_format)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 1)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 0)

    """ def playlist_remove_song(filter, song = False, track = False, api_format = 'xml'):
    """
    ampacheConnection.playlist_remove_song(single_playlist, False, 1)

    """ def playlist(filter, api_format = 'xml'):
    """
    ampacheConnection.playlist(single_playlist)

    """ def playlist_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.playlist_songs(single_playlist, offset, limit)

    """ def playlist_delete(filter, api_format = 'xml'):
    """
    ampacheConnection.playlist_delete(single_playlist)

    """ def playlist_generate(mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    'song'|'index'|'id'
    """
    ampacheConnection.playlist_generate('random', False, False, False, False, 'song', offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (song)." + api_format)

    ampacheConnection.playlist_generate('random', False, False, False, False, 'index', offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (index)." + api_format)

    ampacheConnection.playlist_generate('random', False, False, False, False, 'id', offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_generate." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                    "docs/" + api_format + "-responses/playlist_generate (id)." + api_format)

    """ def scrobble(title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampacheConnection.scrobble('Hear. Life. Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False,
                               int(time.time()), 'debug')
    if os.path.isfile("docs/" + api_format + "-responses/scrobble." + api_format):
        shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                    "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    ampacheConnection.scrobble('Sensorisk Deprivation', 'IOK-1', 'Sensorisk Deprivation', False, False, False,
                               int(time.time()), 'debug')

    """ def record_play(object_id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampacheConnection.record_play(93, ampache_user, 'debug')

    """ def rate(ampache_dexesurl, ampache_api, object_type, object_id, rating, api_format = 'xml'):
    """
    ampacheConnection.rate('song', 93, 5)
    ampacheConnection.rate('song', 93, 0)

    """ def flag(object_type, object_id, flag, api_format = 'xml'):
    """
    ampacheConnection.flag('song', 93, True)
    ampacheConnection.flag('song', 93, False)

    """ def get_art(object_id, object_type, destination, api_format = 'xml'):
    """
    ampacheConnection.get_art(93, 'song', (os.path.join(os.getcwd(), 'get_art.jpg')))

    """ def search_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampacheConnection.search_songs(song_title, offset, limit)

    if api_format == 'xml':
        for child in search_songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def song(filter, api_format = 'xml'):
    """
    song = ampacheConnection.song(single_song)

    if api_format == 'xml':
        for child in song:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def songs(filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    songs = ampacheConnection.songs(False, False, False, False, offset, limit)
    if api_format == 'xml':
        for child in songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genres(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampacheConnection.genres('D', False, offset, limit)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'genre':
                genre = child.attrib['id']
    else:
        for tag in tags['genre']:
            print(tag)
            tmp_genre = tag['id']
        genre = tmp_genre

    """ def genre(filter, api_format = 'xml'):
    """
    ampacheConnection.genre(genre)

    """ def genre_albums(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre_albums = ampacheConnection.genre_albums(genre, 0, 2)
    if api_format == 'xml':
        for child in genre_albums:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genre_artists(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre_artists = ampacheConnection.genre_artists(genre, 0, 1)
    if api_format == 'xml':
        for child in genre_artists:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def genre_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.genre_songs(genre, 0, 1)

    """ def licenses(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.licenses(False, False, offset, limit)

    """ def license(filter, api_format = 'xml'):
    """
    ampacheConnection.license(1)

    """ def license_songs(filter, api_format = 'xml'):
    """
    ampacheConnection.license_songs(1)

    """ def labels(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.labels(False, False, offset, limit)

    """ def label(filter, api_format = 'xml'):
    """
    ampacheConnection.label(2)

    """ def label_songs(filter, api_format = 'xml'):
    """
    ampacheConnection.label_artists(2)


    """ def podcast(filter_str, api_format = 'xml'):
    """
    ampacheConnection.podcast(1, 'episodes')
    if os.path.isfile("docs/" + api_format + "-responses/podcast." + api_format):
        shutil.move("docs/" + api_format + "-responses/podcast." + api_format,
                    "docs/" + api_format + "-responses/podcast (include episodes)." + api_format)

    ampacheConnection.podcast(1, False)

    """ def podcast_episodes
    """
    ampacheConnection.podcast_episodes(1, offset, limit)
    """ def podcast_episode
    """
    ampacheConnection.podcast_episode(47)

    """ def podcast_create
    """
    ampacheConnection.podcast_create('https://www.abc.net.au/radio/programs/trace/feed/8597522/podcast.xml', 3)

    """ def podcast_edit(filter_str, stream, download, expires, description)
    """
    ampacheConnection.podcast_edit(1)

    """ def podcast_delete
    """
    podcasts = ampacheConnection.podcasts('Trace', 1)
    podcast_id = ampacheConnection.get_id_list(podcasts, 'podcast')[0]
    ampacheConnection.podcast_delete(3)

    """ def podcasts(filter_str = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.podcasts(False, False, 0, 4)

    """ def update_podcast(filter_str, api_format = 'xml'):
    """
    ampacheConnection.update_podcast(1)

    """ shares
    """
    shares = ampacheConnection.shares(False, False, offset, limit)
    share_id = ampacheConnection.get_id_list(shares, 'share')[0]

    """ share
    """
    ampacheConnection.share(share_id)

    """ share_create
    """
    share_create = ampacheConnection.share_create(single_song, 'song', False, False)
    if api_format == 'xml':
        share_new = share_create[1].attrib['id']
    else:
        share_new = share_create['id']

    """ share_edit
    """
    ampacheConnection.share_edit(share_new, 0, 0, False, False)

    """ share_delete
    """
    ampacheConnection.share_delete(share_new)

    """ def timeline(username, limit = 0, since = 0, api_format = 'xml'):
    """
    ampacheConnection.timeline(ampache_user, 10, 0)

    """ def toggle_follow(username, api_format = 'xml'):
    """
    toggle = 'generic'
    if ampache_user == 'generic':
        toggle = 'user'
    # unfollow and refollow for timeline stuff
    ampacheConnection.toggle_follow(toggle)
    ampacheConnection.toggle_follow(toggle)

    """ def update_from_tags(ampache_type, ampache_id, api_format = 'xml'):
    """
    ampacheConnection.update_from_tags('album', 6)

    """ def update_artist_info(id, api_format = 'xml'):
    """
    ampacheConnection.update_artist_info(26)

    """ def update_art(ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    """
    ampacheConnection.update_art('artist', 26, True)

    """ def localplay(command, api_format = 'xml'):
    """
    ampacheConnection.localplay('status', False, False, 0)
    if os.path.isfile("docs/" + api_format + "-responses/localplay." + api_format):
        shutil.move("docs/" + api_format + "-responses/localplay." + api_format,
                    "docs/" + api_format + "-responses/localplay (status)." + api_format)

    ampacheConnection.localplay('stop', False, False, 0)

    """ def democratic(method, action, oid, api_format = 'xml'):
    """
    # ampacheConnection.democratic()

    """ def goodbye(api_format = 'xml'):
    Close your session when you're done
    """
    # ampacheConnection.goodbye()

    # Clean the files
    self_check(api_format, ampache_url, ampache_api, ampache_session)


def self_check(api_format, ampache_url, ampache_api, ampache_session):
    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files, 'r', encoding="utf-8")
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        url_json = url_text.replace("/", "\\/")
        newdata = re.sub(url_text, "music.com.au", filedata)
        newdata = re.sub(url_text.replace("/", "\\/"), "music.com.au", newdata)
        newdata = re.sub(ampache_api, "eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('auth=[a-z0-9]*', "auth=eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('ssid=[a-z0-9]*', "ssid=cfj3f237d563f479f5223k23189dbb34", newdata)
        newdata = re.sub(ampache_session, "cfj3f237d563f479f5223k23189dbb34", newdata)

        f = open("./docs/" + api_format + "-responses/" + files, 'w', encoding="utf-8")
        f.write(newdata)
        f.close()


build_docs(url, api, user, 'json')
build_docs(url, api, user, 'xml')
