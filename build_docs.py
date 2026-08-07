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
api_version = '8.0.0'
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
    ampacheConnection = ampache.API()
    """TODO
    def stream(id, type, destination, api_format = 'xml'):
    def download(id, type, destination, format = 'raw', api_format = 'xml'):
    def random(destination, type, filter_id, ...): streams a random object, needs a writable destination
    def upload(file_path, ...): needs a real media file and the allow_upload preference
    podcast_episode_delete: delete an existing podcast_episode
    catalog_file: clean, add, verify using the file path (good for scripting)
    catalog_folder: clean, add, verify using the folder path
    catalog_create: creates a real catalog, so it is left to run_tests.py
    sonic_match: answers 4703 unless a sonic analysis plugin is enabled for the user
    preference_create/preference_delete: both answer 4704 on API8, and create still writes the
        row, so running them leaves a preference behind that delete can not remove
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
    ampacheConnection.handshake(ampache_url, 'badkey', '', 0, api_version)
    if os.path.isfile("docs/" + api_format + "-responses/handshake." + api_format):
        shutil.move("docs/" + api_format + "-responses/handshake." + api_format,
                    "docs/" + api_format + "-responses/handshake (error)." + api_format)
    # use correct details
    ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key, '', 0, api_version)
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

    """ def live_streams(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.live_streams(False, False, offset, limit)

    """ def live_stream(filter, api_format = 'xml'):
    """
    ampacheConnection.live_stream(3)

    """ def labels(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.labels(False, False, offset, limit)

    """ def label(filter, api_format = 'xml'):
    """
    ampacheConnection.label(1677)

    """ def label_songs(filter, api_format = 'xml'):
    """
    ampacheConnection.label_artists(filter_id=1677)

    """ def url_to_song(url, api_format = 'xml'):
    """
    ampacheConnection.url_to_song(song_url)

    """ def user_create(username, password, email, fullname = False, disable = False, api_format = 'xml'):
    """
    tempusername = 'temp_user'
    ampacheConnection.user_create(tempusername, 'supoersecretpassword', 'email@gmail.com', False, False)
    ampacheConnection.user(tempusername)

    """ def user_edit(username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    """
    ampacheConnection.user_edit(username=tempusername, password=False, fullname=False, email=False, website=False, state=False, city=False, disable=True, maxbitrate=False)
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

    """ def index(object_type, filter_str, exact, add, update, include, offset, limit)):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampacheConnection.index(object_type='song', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (song)." + api_format)
    single_song = ampacheConnection.get_id_list(songs, 'song')[0]

    ampacheConnection.index(object_type='song', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (song with include)." + api_format)

    albums = ampacheConnection.index(object_type='album', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (album)." + api_format)
    single_album = ampacheConnection.get_id_list(albums, 'album')[0]

    ampacheConnection.index(object_type='album', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (album with include)." + api_format)
    single_album = ampacheConnection.get_id_list(albums, 'album')[0]
    single_album = 12

    artists = ampacheConnection.index(object_type='artist', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (artist)." + api_format)
    single_artist = ampacheConnection.get_id_list(artists, 'artist')[0]

    ampacheConnection.index(object_type='artist', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (artist with include)." + api_format)
    single_artist = ampacheConnection.get_id_list(artists, 'artist')[0]

    playlists = ampacheConnection.index(object_type='playlist', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (playlist)." + api_format)
    single_playlist = ampacheConnection.get_id_list(playlists, 'playlist')[0]

    ampacheConnection.index(object_type='playlist', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=1)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (playlist with include)." + api_format)

    ampacheConnection.index(object_type='podcast', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (podcast)." + api_format)

    ampacheConnection.index(object_type='podcast', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (podcast with include)." + api_format)

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

    search_rules = [['favorite', 0, '%'], ['title', 2, 'D']]
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/search_group%20\(all\).json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/search_group%20\(all\).xml)]]
    ampacheConnection.search_group(search_rules, 'or', 'all', offset, limit, 0)
    if os.path.isfile("docs/" + "search_group." + api_format):
        shutil.move("docs/" + "search_group." + api_format,
                    "docs/" + "search_group (all)." + api_format)

    search_rules = [['artist', 0, 'Synthetic']]
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/search_group%20\(music\).json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/search_group%20\(music\).xml)]]
    ampacheConnection.search_group(search_rules, 'or', 'music', offset, limit, 0)
    if os.path.isfile("docs/" + "search_group." + api_format):
        shutil.move("docs/" + "search_group." + api_format,
                    "docs/" + "search_group (music)." + api_format)

    search_rules = [['title', 2, 'D']]
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/search_group%20\(podcast\).json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/search_group%20\(podcast\).xml)]]
    ampacheConnection.search_group(search_rules, 'or', 'podcast', offset, limit, 0)
    if os.path.isfile("docs/" + "search_group." + api_format):
        shutil.move("docs/" + "search_group." + api_format,
                    "docs/" + "search_group (podcast)." + api_format)

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
    ampacheConnection.artist_songs(filter_id=single_artist, offset=offset, limit=limit)

    """ def artists(filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampacheConnection.artists(filter_str=False, add=False, update=False, offset=offset, limit=limit, include=True)
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs,albums)." + api_format)
    ampacheConnection.artists(filter_str=False, add=False, update=False, offset=offset, limit=limit, include='songs')
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include songs)." + api_format)
    ampacheConnection.artists(filter_str=False, add=False, update=False, offset=offset, limit=limit, include='albums')
    if os.path.isfile("docs/" + api_format + "-responses/artists." + api_format):
        shutil.move("docs/" + api_format + "-responses/artists." + api_format,
                    "docs/" + api_format + "-responses/artists (with include albums)." + api_format)
    ampacheConnection.artists(filter_str=False, add=False, update=False, offset=offset, limit=limit, include=False)

    """ def catalog_action(task, catalog, api_format = 'xml'):
    """
    ampacheConnection.catalog_action('clean', 2)
    if os.path.isfile("docs/" + api_format + "-responses/catalog_action." + api_format):
        shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                    "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    #ampacheConnection.catalog_action('clean_catalog', 2)

    ampacheConnection.bookmark_create(115, 'song', 0, 'client1')

    ampacheConnection.bookmark_create(64, 'song', 10, 'client')
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmarks.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmarks.xml)
    ampacheConnection.bookmarks(False, True)
    if os.path.isfile("docs/" + api_format + "-responses/bookmarks." + api_format):
        shutil.move("docs/" + api_format + "-responses/bookmarks." + api_format,
                    "docs/" + api_format + "-responses/bookmarks (with include)." + api_format)
    ampacheConnection.bookmarks()

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark.xml)
    ampacheConnection.bookmark(1)
    if os.path.isfile("docs/" + api_format + "-responses/bookmark." + api_format):
        shutil.move("docs/" + api_format + "-responses/bookmark." + api_format,
                    "docs/" + api_format + "-responses/bookmark (with include)." + api_format)
    ampacheConnection.bookmark(1)

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_create.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_create.xml)
    ampacheConnection.bookmark_create(93, 'song')
    ampacheConnection.get_bookmark(93, 'song', 1)
    if os.path.isfile("docs/" + api_format + "-responses/get_bookmark." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_bookmark." + api_format,
                    "docs/" + api_format + "-responses/get_bookmark (with include)." + api_format)
    mybookmark = ampacheConnection.get_bookmark(45, 'song')
    if api_format == 'xml':
        for child in mybookmark:
            if child.tag == 'user':
                mybookmark = child.attrib['id']
    else:
        mybookmark = mybookmark['id']

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_edit.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_edit.xml)
    ampacheConnection.bookmark_edit(mybookmark, 'bookmark', 10)

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_delete)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_delete)
    ampacheConnection.bookmark_delete(mybookmark, 'bookmark')

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
    ampacheConnection.followers(username=ampache_user)

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

    """ def playlist_songs(filter, random, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.playlist_songs(single_playlist, 0, offset, limit)

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
    ampacheConnection.license_songs(filter_id=1)

    """ def labels(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.labels(False, False, offset, limit)

    """ def label(filter, api_format = 'xml'):
    """
    ampacheConnection.label(2)

    """ def label_songs(filter, api_format = 'xml'):
    """
    ampacheConnection.label_artists(filter_id=2)


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
    ampacheConnection.podcast_episode(23)

    """ def podcast_create
    """
    ampacheConnection.podcast_create('https://www.abc.net.au/radio/programs/trace/feed/8597522/podcast.xml', 3)

    """ def podcast_edit(filter_str, stream, download, expires, description)
    """
    ampacheConnection.podcast_edit(1)

    """ def podcast_delete
    """
    podcasts = ampacheConnection.podcasts(filter_str='Trace', exact=1)
    podcast_id = ampacheConnection.get_id_list(podcasts, 'podcast')[0]
    ampacheConnection.podcast_delete(3)

    """ def podcasts(filter_str = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.podcasts(filter_str=False, exact=False, offset=0, limit=4)

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

    """ def localplay_songs():
    """
    ampacheConnection.localplay_songs()

    """ catalogs: get all the catalogs
    """ 
    ampacheConnection.catalogs()
    """ catalog: get a catalog by id
    """ 
    ampacheConnection.catalog(1)

    """ def deleted_songs(offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.deleted_songs()

    """ def deleted_podcast_episodes(offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.deleted_podcast_episodes()

    """ def deleted_videos(offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.deleted_videos()

    """ def democratic(method, action, oid, api_format = 'xml'):
    """
    # ampacheConnection.democratic()

    """ def index(object_type, filter_str, exact, add, update, include, offset, limit, hide_search, sort, cond):
    MINIMUM_API_VERSION=8.0.0 for the album_disk type
    """
    ampacheConnection.index(object_type='album_disk', offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (album_disk)." + api_format)

    """ def list(object_type, filter_str, exact, add, update, offset, limit):
    """
    ampacheConnection.list(object_type='album', offset=offset, limit=limit)

    """ def browse(filter_str, object_type, catalog, add, update, offset, limit):
    """
    ampacheConnection.browse()

    """ def get_similar(object_type, filter_id, offset, limit):
    """
    ampacheConnection.get_similar('song', single_song, offset, limit)

    """ def album_disks(filter_id, include, offset, limit, sort, cond):
    MINIMUM_API_VERSION=8.0.0
    """
    album_disks = ampacheConnection.album_disks(single_album, False, offset, limit)
    disk_list = ampacheConnection.get_id_list(album_disks, 'album_disk')

    """ def album_disk(filter_id, include):
    MINIMUM_API_VERSION=8.0.0
    """
    if disk_list:
        single_disk = disk_list[0]
        ampacheConnection.album_disk(single_disk, False)

        ampacheConnection.album_disk(single_disk, True)
        if os.path.isfile("docs/" + api_format + "-responses/album_disk." + api_format):
            shutil.move("docs/" + api_format + "-responses/album_disk." + api_format,
                        "docs/" + api_format + "-responses/album_disk (with include)." + api_format)

        """ def album_disk_songs(filter_id, offset, limit, sort, cond):
        MINIMUM_API_VERSION=8.0.0
        """
        ampacheConnection.album_disk_songs(single_disk, offset, limit)

    """ def folders(filter_str, exact, add, update, offset, limit, sort, cond):
    MINIMUM_API_VERSION=8.0.0
    """
    ampacheConnection.folders('/', False, False, False, offset, limit)

    """ def folder(filter_id, add, update, offset, limit, sort, cond):
    MINIMUM_API_VERSION=8.0.0
    """
    ampacheConnection.folder(-1, False, False, offset, limit)

    """ def song_tags(filter_id):
    """
    ampacheConnection.song_tags(single_song)

    """ def get_lyrics(filter_id, plugins):
    """
    ampacheConnection.get_lyrics(single_song)

    """ def get_external_metadata(filter_id, object_type):
    """
    ampacheConnection.get_external_metadata(single_artist, 'artist')

    """ def now_playing():
    """
    ampacheConnection.now_playing()

    """ def player(filter_str, object_type, state, play_time, client, offset, limit):
    """
    ampacheConnection.player(single_song, 'song', 'play', 0)
    ampacheConnection.player(single_song, 'song', 'stop', 0)

    """ def search(rules, operator, object_type, offset, limit, random):
    """
    ampacheConnection.search([['title', 2, 'D']], 'or', 'song', offset, limit, 0)

    """ def search_group(rules, operator, object_type, offset, limit, random):
    """
    ampacheConnection.search_group([['title', 2, 'D']], 'or', 'all', offset, limit, 0)

    """ def search_rules(filter_str):
    """
    ampacheConnection.search_rules('song')

    """ def smartlists(filter_str, exact, offset, limit, include, sort, cond, add, update):
    """
    smartlists = ampacheConnection.smartlists(False, False, offset, limit)
    # smartlists come back under the 'playlist' key with 'smart_' prefixed ids
    smartlist_ids = ampacheConnection.get_id_list(smartlists, 'playlist')

    """ def smartlist(filter_id):
    """
    if smartlist_ids:
        ampacheConnection.smartlist(smartlist_ids[0])

        """ def smartlist_songs(filter_id, random, offset, limit):
        """
        ampacheConnection.smartlist_songs(smartlist_ids[0], False, offset, limit)

    """ def user_playlists(filter_str, exact, offset, limit, sort, cond, include, add, update):
    """
    ampacheConnection.user_playlists(False, False, offset, limit)

    """ def user_smartlists(filter_str, exact, offset, limit, sort, cond, include, add, update):
    """
    ampacheConnection.user_smartlists(False, False, offset, limit)

    """ a real playlist id, since the playlist index also carries smartlists as 'smart_<id>'
    """
    real_playlists = ampacheConnection.get_id_list(
        ampacheConnection.user_playlists(False, False, offset, limit), 'playlist')
    real_playlist = real_playlists[0] if real_playlists else single_playlist

    """ def playlist_hash(filter_id):
    """
    ampacheConnection.playlist_hash(real_playlist)

    """ def playlist_add(filter_id, object_id, object_type):
    MINIMUM_API_VERSION=6.3.0
    """
    ampacheConnection.playlist_add(real_playlist, single_album, 'album')

    """ def playlist_remove(filter_id, object_id, object_type, track, clear):
    MINIMUM_API_VERSION=8.0.0
    Replaces playlist_remove_song and is object_type aware
    """
    ampacheConnection.playlist_remove(real_playlist, single_song, 'song')

    """ def users():
    """
    ampacheConnection.users()

    """ def user_preferences():
    """
    ampacheConnection.user_preferences()

    """ def user_preference(filter_str):
    """
    ampacheConnection.user_preference('play_type')

    """ def system_preferences():
    """
    ampacheConnection.system_preferences()

    """ def system_preference(filter_str):
    """
    ampacheConnection.system_preference('lock_songs')


    """ collections
    MINIMUM_API_VERSION=8.0.0
    A collection curates objects of any type, so the whole lifecycle is exercised here
    """
    collection_create = ampacheConnection.collection_create('Example Collection', 'private')
    collection_new = ampacheConnection.get_id_list(collection_create, 'collection')[0]

    ampacheConnection.collections()

    ampacheConnection.collections('album')
    if os.path.isfile("docs/" + api_format + "-responses/collections." + api_format):
        shutil.move("docs/" + api_format + "-responses/collections." + api_format,
                    "docs/" + api_format + "-responses/collections (album)." + api_format)

    ampacheConnection.collection(collection_new)

    ampacheConnection.collection_add(collection_new, single_album, 'album')
    ampacheConnection.collection_add(collection_new, single_song, 'song')

    ampacheConnection.collection_items(collection_new, offset, limit)

    ampacheConnection.collection_edit(collection_new, 'Example Collection (edited)', 'public')

    ampacheConnection.collection_remove(collection_new, single_song, 'song')

    ampacheConnection.collection_delete(collection_new)

    """ playlist folders
    MINIMUM_API_VERSION=8.0.0
    A playlist folder files playlists, smartlists and collections into a tree
    """
    folder_create = ampacheConnection.playlist_folder_create('Example Folder')
    folder_new = ampacheConnection.get_id_list(folder_create, 'playlist_folder')[0]

    ampacheConnection.playlist_folders(offset, limit)

    ampacheConnection.playlist_folder(folder_new)

    ampacheConnection.playlist_folder_add(real_playlist, 'playlist', folder_new)

    ampacheConnection.playlist_folder_items(folder_new, offset, limit)

    ampacheConnection.playlist_folder_items('/', offset, limit)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_folder_items." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_folder_items." + api_format,
                    "docs/" + api_format + "-responses/playlist_folder_items (root)." + api_format)

    ampacheConnection.playlist_folder_edit(folder_new, 'Example Folder (edited)')

    ampacheConnection.playlist_folder_remove(real_playlist, 'playlist')

    ampacheConnection.playlist_folder_delete(folder_new)

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


build_docs(url, api, user, 'json')
build_docs(url, api, user, 'xml')
