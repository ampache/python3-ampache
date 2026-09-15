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
    conf_files = ['ampache.conf',
                  os.path.join(os.pardir, 'ampache.conf'),
                  'docs/examples/ampyche.conf']
    conf_file = next((path for path in conf_files if os.path.isfile(path)), None)
    if conf_file:
        print('Using config file ' + conf_file)
        conf = configparser.RawConfigParser()
        conf.read(conf_file)
        url = conf.get('conf', 'ampache_url')
        api = conf.get('conf', 'ampache_apikey')
        user = conf.get('conf', 'ampache_user')
    else:
        print()
        sys.exit('Error: docs/examples/ampyche.conf not found and no arguments set')


def object_list(connection, data, attribute):
    """ Return a list of (id, fields) tuples for any api response

        Ampache hands back three different shapes for a list of things, so they are
        all folded into one here:
          * a wrapped list  {'song': [{...}, {...}]}
          * a bare object   {'id': '132', 'title': '...'}  (song, user, bookmark)
          * an index list   {'song': ['132', '133']}
        Nested objects (a song's artist and album) are flattened to their name so
        that fields['artist'] is a string in both json and xml.
    """
    objects = list()
    if data is None:
        return objects
    if connection.AMPACHE_API == 'xml':
        for child in data:
            if child.tag != attribute:
                continue
            fields = dict()
            for field in child:
                if len(field) > 0:
                    # a nested object such as a song's artist, so read its name
                    nested = field.find('name')
                    fields[field.tag] = nested.text if nested is not None else None
                else:
                    fields[field.tag] = field.text
            objects.append((child.attrib.get('id'), fields))
        return objects
    if not isinstance(data, dict):
        return objects
    items = data.get(attribute)
    if items is None:
        # a bare object response carries the object itself
        items = [data] if 'id' in data else None
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list):
        return objects
    for item in items:
        if isinstance(item, (str, int)):
            objects.append((str(item), dict()))
            continue
        if not isinstance(item, dict):
            continue
        fields = {key: (value.get('name') if isinstance(value, dict) else value)
                  for key, value in item.items()}
        item_id = item.get('id')
        objects.append((str(item_id) if item_id is not None else None, fields))
    return objects


def id_list(connection, data, attribute):
    """ Return every id in an api response """
    return [object_id for object_id, fields in object_list(connection, data, attribute) if object_id]


def first_id(connection, data, attribute):
    """ Return the first id in an api response, or None when the server has none """
    found = id_list(connection, data, attribute)
    return found[0] if found else None


def first_value(connection, data, attribute, field):
    """ Return a field from the first object in an api response """
    for object_id, fields in object_list(connection, data, attribute):
        value = fields.get(field)
        if value:
            return value
    return None


def find_id(connection, data, attribute, field, value):
    """ Return the id of the first object whose field matches value """
    for object_id, fields in object_list(connection, data, attribute):
        if str(fields.get(field)) == str(value):
            return object_id
    return None


def resolve(connection, lookup, attribute, candidate, fallback):
    """ Check that a discovered id really resolves before adopting it

        A random stat can name an object that is no longer in the catalog. When that
        happens the fallback is looked up again so its response, and not the error, is
        what ends up in the documentation.
    """
    if candidate and str(candidate) != str(fallback):
        if first_id(connection, lookup(candidate), attribute):
            return candidate
        print('the server offered ' + attribute + ' ' + str(candidate) + ' but it does not resolve, keeping ' + str(fallback))
        lookup(fallback)
    return fallback


def remove_existing(connection, data, attribute, names, delete):
    """ Delete anything an interrupted run left behind

        Ampache rejects a duplicate name, so the objects this script creates have to be
        cleared out before it can create them again.
    """
    for name in names:
        existing = find_id(connection, data, attribute, 'name', name)
        if existing:
            print('removing the leftover ' + attribute + ' "' + name + '" from an earlier run')
            delete(existing)


def pick(items, index):
    """ Cycle through whatever the server has so callers can ask for distinct objects """
    if not items:
        return None
    return items[index % len(items)]


def filter_word(text, fallback='a'):
    """ Turn a real name into a search filter that is guaranteed to match it """
    if not text:
        return fallback
    for word in str(text).split():
        if len(word) > 2:
            return word
    return str(text)[:3] or fallback


def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    ampacheConnection = ampache.API()
    skipped = list()
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
    live_streams = ampacheConnection.live_streams(False, False, offset, limit)
    single_live_stream = first_id(ampacheConnection, live_streams, 'live_stream')

    """ def live_stream(filter, api_format = 'xml'):
    """
    if single_live_stream:
        ampacheConnection.live_stream(single_live_stream)
    else:
        skipped.append('live_stream (no live streams on this server)')

    """ def labels(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    labels = ampacheConnection.labels(False, False, offset, limit)
    single_label = first_id(ampacheConnection, labels, 'label')

    """ def label(filter, api_format = 'xml'):
    """
    """ def label_songs(filter, api_format = 'xml'):
    """
    if single_label:
        ampacheConnection.label(single_label)
        ampacheConnection.label_artists(filter_id=single_label)
    else:
        skipped.append('label, label_artists (no labels on this server)')

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

    myuser = ampacheConnection.user(ampache_user)
    user_id = first_id(ampacheConnection, myuser, 'user')
    if not user_id:
        sys.exit('ERROR: could not read the user id for ' + ampache_user)
    print('\nbuilding docs as user ' + ampache_user + ' (id ' + str(user_id) + ')')

    """ def index(object_type, filter_str, exact, add, update, include, offset, limit)):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampacheConnection.index(object_type='song', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (song)." + api_format)
    song_ids = id_list(ampacheConnection, songs, 'song')
    if not song_ids:
        sys.exit('ERROR: no songs found on ' + ampache_url + ', the docs need a catalog with data in it')
    single_song = pick(song_ids, 0)

    ampacheConnection.index(object_type='song', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (song with include)." + api_format)

    albums = ampacheConnection.index(object_type='album', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (album)." + api_format)
    album_ids = id_list(ampacheConnection, albums, 'album')
    if not album_ids:
        sys.exit('ERROR: no albums found on ' + ampache_url + ', the docs need a catalog with data in it')
    single_album = pick(album_ids, 0)

    ampacheConnection.index(object_type='album', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (album with include)." + api_format)

    artists = ampacheConnection.index(object_type='artist', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (artist)." + api_format)
    artist_ids = id_list(ampacheConnection, artists, 'artist')
    if not artist_ids:
        sys.exit('ERROR: no artists found on ' + ampache_url + ', the docs need a catalog with data in it')
    single_artist = pick(artist_ids, 0)

    ampacheConnection.index(object_type='artist', filter_str=False, exact=False, add=False, update=False, include=True, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (artist with include)." + api_format)

    playlists = ampacheConnection.index(object_type='playlist', filter_str=False, exact=False, add=False, update=False, include=False, offset=offset, limit=limit)
    if os.path.isfile("docs/" + api_format + "-responses/index." + api_format):
        shutil.move("docs/" + api_format + "-responses/index." + api_format,
                    "docs/" + api_format + "-responses/index (playlist)." + api_format)
    playlist_ids = id_list(ampacheConnection, playlists, 'playlist')
    # the playlist index also carries smartlists as 'smart_<id>', which most methods reject
    real_playlist_ids = [playlist for playlist in playlist_ids if str(playlist).isdigit()]
    single_playlist = pick(real_playlist_ids, 0)

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

    """ Read the names off real objects so every filter below matches something.
        Nothing here is specific to a catalog, so the docs build on any server with data.
    """
    song = ampacheConnection.song(single_song)
    song_title = first_value(ampacheConnection, song, 'song', 'title')
    song_artist = first_value(ampacheConnection, song, 'song', 'artist')
    song_album = first_value(ampacheConnection, song, 'song', 'album')
    song_stream = first_value(ampacheConnection, song, 'song', 'url')
    print('using the song "' + str(song_title) + '" by "' + str(song_artist) + '" on "' + str(song_album) + '"')

    artist = ampacheConnection.artist(single_artist, False)
    artist_title = first_value(ampacheConnection, artist, 'artist', 'name')

    album = ampacheConnection.album(single_album, False)
    album_title = first_value(ampacheConnection, album, 'album', 'name')

    # filters that are guaranteed to return the object they came from
    song_filter = filter_word(song_title)
    artist_filter = filter_word(artist_title)

    """ def url_to_song(url, api_format = 'xml'):
    """
    ampacheConnection.url_to_song(song_stream if song_stream else song_url)

    """ def videos(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    videos = ampacheConnection.videos(False, False, 0, 0)
    single_video = first_id(ampacheConnection, videos, 'video')

    """ def video(filter, api_format = 'xml'):
    """
    if single_video:
        ampacheConnection.video(single_video)
    else:
        skipped.append('video (no videos on this server)')

    """ def advanced_search(rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['title', 2, song_filter]]
    search_song = ampacheConnection.advanced_search(search_rules, 'or', 'song', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    song_id = first_id(ampacheConnection, search_song, 'song')
    if not song_id:
        song_id = single_song

    search_rules = [['artist', 0, artist_filter]]
    search_album = ampacheConnection.advanced_search(search_rules, 'or', 'album', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    found_album = first_value(ampacheConnection, search_album, 'album', 'name')
    if found_album:
        album_title = found_album

    search_rules = [['artist', 2, artist_filter]]
    search_artist = ampacheConnection.advanced_search(search_rules, 'or', 'artist', offset, limit, 0)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    found_artist = first_value(ampacheConnection, search_artist, 'artist', 'name')
    if found_artist:
        artist_title = found_artist

    search_rules = [['favorite', 0, '%'], ['title', 2, song_filter]]
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/search_group%20\(all\).json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/search_group%20\(all\).xml)]]
    ampacheConnection.search_group(search_rules, 'or', 'all', offset, limit, 0)
    if os.path.isfile("docs/" + "search_group." + api_format):
        shutil.move("docs/" + "search_group." + api_format,
                    "docs/" + "search_group (all)." + api_format)

    search_rules = [['artist', 0, artist_filter]]
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/search_group%20\(music\).json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/search_group%20\(music\).xml)]]
    ampacheConnection.search_group(search_rules, 'or', 'music', offset, limit, 0)
    if os.path.isfile("docs/" + "search_group." + api_format):
        shutil.move("docs/" + "search_group." + api_format,
                    "docs/" + "search_group (music)." + api_format)

    search_rules = [['title', 2, song_filter]]
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
    found_album = first_value(ampacheConnection, album, 'album', 'name')
    if found_album:
        album_title = found_album

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

    random_artist = resolve(ampacheConnection, lambda filter_id: ampacheConnection.artist(filter_id, False),
                            'artist', first_id(ampacheConnection, stats, 'artist'), single_artist)
    if str(random_artist) != str(single_artist):
        print('\ngetting a random artist using the stats method and found',
              first_value(ampacheConnection, stats, 'artist', 'name'))
        single_artist = random_artist
        artist_title = first_value(ampacheConnection, stats, 'artist', 'name') or artist_title

    stats = ampacheConnection.stats('album', 'random', ampache_user, None, 0, 2)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (album)." + api_format)

    random_album = resolve(ampacheConnection, lambda filter_id: ampacheConnection.album(filter_id, False),
                           'album', first_id(ampacheConnection, stats, 'album'), single_album)
    if str(random_album) != str(single_album):
        print('\ngetting a random album using the stats method and found',
              first_value(ampacheConnection, stats, 'album', 'name'))
        single_album = random_album
        album_title = first_value(ampacheConnection, stats, 'album', 'name') or album_title

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

    """ catalogs: get all the catalogs
    """
    catalogs = ampacheConnection.catalogs()
    catalog_ids = id_list(ampacheConnection, catalogs, 'catalog')
    single_catalog = pick(catalog_ids, 0)
    podcast_catalog = find_id(ampacheConnection, catalogs, 'catalog', 'gather_types', 'podcast')

    """ def catalog_action(task, catalog, api_format = 'xml'):
    'clean' is not a task name, so this documents the error response
    """
    ampacheConnection.catalog_action('clean', single_catalog)
    if os.path.isfile("docs/" + api_format + "-responses/catalog_action." + api_format):
        shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                    "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    #ampacheConnection.catalog_action('clean_catalog', single_catalog)

    ampacheConnection.bookmark_create(pick(song_ids, 1), 'song', 0, 'client1')

    ampacheConnection.bookmark_create(pick(song_ids, 2), 'song', 10, 'client')
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmarks.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmarks.xml)
    bookmarks = ampacheConnection.bookmarks(False, True)
    if os.path.isfile("docs/" + api_format + "-responses/bookmarks." + api_format):
        shutil.move("docs/" + api_format + "-responses/bookmarks." + api_format,
                    "docs/" + api_format + "-responses/bookmarks (with include)." + api_format)
    ampacheConnection.bookmarks()
    single_bookmark = first_id(ampacheConnection, bookmarks, 'bookmark')

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark.xml)
    if single_bookmark:
        ampacheConnection.bookmark(single_bookmark)
        if os.path.isfile("docs/" + api_format + "-responses/bookmark." + api_format):
            shutil.move("docs/" + api_format + "-responses/bookmark." + api_format,
                        "docs/" + api_format + "-responses/bookmark (with include)." + api_format)
        ampacheConnection.bookmark(single_bookmark)
    else:
        skipped.append('bookmark (no bookmarks on this server)')

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_create.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_create.xml)
    ampacheConnection.bookmark_create(single_song, 'song')
    ampacheConnection.get_bookmark(single_song, 'song', 1)
    if os.path.isfile("docs/" + api_format + "-responses/get_bookmark." + api_format):
        shutil.move("docs/" + api_format + "-responses/get_bookmark." + api_format,
                    "docs/" + api_format + "-responses/get_bookmark (with include)." + api_format)
    mybookmark = first_id(ampacheConnection, ampacheConnection.get_bookmark(single_song, 'song'), 'bookmark')

    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_edit.json)
    # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_edit.xml)
    if mybookmark:
        ampacheConnection.bookmark_edit(mybookmark, 'bookmark', 10)

        # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/json-responses/bookmark_delete)
        # (https://raw.githubusercontent.com/ampache/python3-ampache/api6/docs/xml-responses/bookmark_delete)
        ampacheConnection.bookmark_delete(mybookmark, 'bookmark')
    else:
        skipped.append('bookmark_edit, bookmark_delete (could not read back the new bookmark)')

    """ def flag(type, id, flag, api_format = 'xml'):
    """
    if single_playlist:
        ampacheConnection.flag('playlist', single_playlist, True)

        """ def rate(type, id, rating, api_format = 'xml'):
        """
        ampacheConnection.rate('playlist', single_playlist, 2)
    else:
        skipped.append('flag, rate on a playlist (no playlists on this server)')

    """ def record_play(id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampacheConnection.record_play(song_id, user_id, 'debug')

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

    remove_existing(ampacheConnection, ampacheConnection.playlists(False, False, 0, 0), 'playlist',
                    ('rename', 'documentation'), ampacheConnection.playlist_delete)

    """ def playlists(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampacheConnection.playlists(False, False, offset, limit)

    """ def playlist_create(name, type, api_format = 'xml'):
    """
    playlist_create = ampacheConnection.playlist_create('rename', 'private')
    single_playlist = first_id(ampacheConnection, playlist_create, 'playlist')
    if not single_playlist:
        sys.exit('ERROR: could not create a playlist on ' + ampache_url)

    """ def playlist_edit(filter, name = False, type = False, api_format = 'xml'):
    """
    ampacheConnection.playlist_edit(single_playlist, 'documentation', 'public')

    """ def playlist_add_song(filter, song, check = 0, api_format = 'xml'):
    """
    ampacheConnection.playlist_add_song(single_playlist, pick(song_ids, 1), 0)
    ampacheConnection.playlist_add_song(single_playlist, pick(song_ids, 2), 0)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 0)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 1)
    if os.path.isfile("docs/" + api_format + "-responses/playlist_add_song." + api_format):
        shutil.move("docs/" + api_format + "-responses/playlist_add_song." + api_format,
                    "docs/" + api_format + "-responses/playlist_add_song (error)." + api_format)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 1)
    ampacheConnection.playlist_add_song(single_playlist, single_song, 0)

    """ def playlist_remove_song(filter, song = False, track = False, api_format = 'xml'):
        playlist_add_song is deprecated and adds nothing, so fill the playlist with the
        current method first or there is no track 1 to remove
    """
    ampacheConnection.playlist_add(single_playlist, single_song, 'song')
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
    # a song that does not exist, so this documents the error response
    ampacheConnection.scrobble('Hear. Life. Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False,
                               int(time.time()), 'debug')
    if os.path.isfile("docs/" + api_format + "-responses/scrobble." + api_format):
        shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                    "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    ampacheConnection.scrobble(song_title, song_artist, song_album, False, False, False,
                               int(time.time()), 'debug')

    """ def record_play(object_id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampacheConnection.record_play(single_song, ampache_user, 'debug')

    """ def rate(ampache_dexesurl, ampache_api, object_type, object_id, rating, api_format = 'xml'):
    """
    ampacheConnection.rate('song', single_song, 5)
    ampacheConnection.rate('song', single_song, 0)

    """ def flag(object_type, object_id, flag, api_format = 'xml'):
    """
    ampacheConnection.flag('song', single_song, True)
    ampacheConnection.flag('song', single_song, False)

    """ def get_art(object_id, object_type, destination, api_format = 'xml'):
    """
    ampacheConnection.get_art(single_song, 'song', (os.path.join(os.getcwd(), 'get_art.jpg')))

    """ def search_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampacheConnection.search_songs(song_filter, offset, limit)

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
    # read a real genre name first so the documented filter matches something
    genre_name = first_value(ampacheConnection, ampacheConnection.genres(False, False, offset, limit),
                             'genre', 'name')
    tags = ampacheConnection.genres(filter_word(genre_name), False, offset, limit)
    genre = first_id(ampacheConnection, tags, 'genre')

    if genre:
        """ def genre(filter, api_format = 'xml'):
        """
        ampacheConnection.genre(genre)

        """ def genre_albums(filter, offset = 0, limit = 0, api_format = 'xml'):
        """
        ampacheConnection.genre_albums(genre, 0, 2)

        """ def genre_artists(filter, offset = 0, limit = 0, api_format = 'xml'):
        """
        ampacheConnection.genre_artists(genre, 0, 1)

        """ def genre_songs(filter, offset = 0, limit = 0, api_format = 'xml'):
        """
        ampacheConnection.genre_songs(genre, 0, 1)
    else:
        skipped.append('genre, genre_albums, genre_artists, genre_songs (no genres on this server)')

    """ def licenses(filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    licenses = ampacheConnection.licenses(False, False, offset, limit)
    single_license = first_id(ampacheConnection, licenses, 'license')

    """ def license(filter, api_format = 'xml'):
    """
    """ def license_songs(filter, api_format = 'xml'):
    """
    if single_license:
        ampacheConnection.license(single_license)
        ampacheConnection.license_songs(filter_id=single_license)
    else:
        skipped.append('license, license_songs (no licenses on this server)')


    """ def podcast_create
        Needs a catalog that gathers podcasts, so it only runs where one exists
    """
    podcast_new = None
    if podcast_catalog:
        podcast_create = ampacheConnection.podcast_create(
            'https://www.abc.net.au/radio/programs/trace/feed/8597522/podcast.xml', podcast_catalog)
        podcast_new = first_id(ampacheConnection, podcast_create, 'podcast')
    else:
        skipped.append('podcast_create (no podcast catalog on this server)')

    """ def podcasts(filter_str = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    podcasts = ampacheConnection.podcasts(filter_str=False, exact=False, offset=0, limit=4)
    single_podcast = first_id(ampacheConnection, podcasts, 'podcast')

    if single_podcast:
        """ def podcast(filter_str, api_format = 'xml'):
        """
        ampacheConnection.podcast(single_podcast, 'episodes')
        if os.path.isfile("docs/" + api_format + "-responses/podcast." + api_format):
            shutil.move("docs/" + api_format + "-responses/podcast." + api_format,
                        "docs/" + api_format + "-responses/podcast (include episodes)." + api_format)

        ampacheConnection.podcast(single_podcast, False)

        """ def podcast_episodes
        """
        episodes = ampacheConnection.podcast_episodes(single_podcast, offset, limit)

        """ def podcast_episode
        """
        single_episode = first_id(ampacheConnection, episodes, 'podcast_episode')
        if single_episode:
            ampacheConnection.podcast_episode(single_episode)
        else:
            skipped.append('podcast_episode (this podcast has no episodes)')

        """ def podcast_edit(filter_str, stream, download, expires, description)
        """
        ampacheConnection.podcast_edit(single_podcast)

        """ def update_podcast(filter_str, api_format = 'xml'):
        """
        ampacheConnection.update_podcast(single_podcast)
    else:
        skipped.append('podcast, podcast_episodes, podcast_episode, podcast_edit, update_podcast'
                       ' (no podcasts on this server)')

    """ def podcast_delete
        Only ever removes the podcast this run created
    """
    if podcast_new:
        ampacheConnection.podcast_delete(podcast_new)
    else:
        skipped.append('podcast_delete (nothing was created to delete)')

    """ share_create
    """
    share_create = ampacheConnection.share_create(single_song, 'song', False, False)
    share_new = first_id(ampacheConnection, share_create, 'share')

    """ shares
    """
    shares = ampacheConnection.shares(False, False, offset, limit)
    share_id = first_id(ampacheConnection, shares, 'share')

    """ share
    """
    if share_id:
        ampacheConnection.share(share_id)
    else:
        skipped.append('share (no shares on this server)')

    """ share_edit
    """
    """ share_delete
    """
    if share_new:
        ampacheConnection.share_edit(share_new, 0, 0, False, False)
        ampacheConnection.share_delete(share_new)
    else:
        skipped.append('share_edit, share_delete (could not create a share)')

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
    ampacheConnection.update_from_tags('album', single_album)

    """ def update_artist_info(id, api_format = 'xml'):
    """
    ampacheConnection.update_artist_info(single_artist)

    """ def update_art(ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    """
    ampacheConnection.update_art('artist', single_artist, True)

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
    if single_catalog:
        ampacheConnection.catalog(single_catalog)
    else:
        skipped.append('catalog (no catalogs on this server)')

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
    disk_list = id_list(ampacheConnection, album_disks, 'album_disk')

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
    else:
        skipped.append('album_disk, album_disk_songs (this album has no disks)')

    """ def folders(filter_str, exact, add, update, offset, limit, sort, cond):
    MINIMUM_API_VERSION=8.0.0
    """
    folders = ampacheConnection.folders('/', False, False, False, offset, limit)

    """ def folder(filter_id, add, update, offset, limit, sort, cond):
    MINIMUM_API_VERSION=8.0.0
    -1 is the root folder when the server has no folder objects to walk
    """
    single_folder = first_id(ampacheConnection, folders, 'folder')
    ampacheConnection.folder(single_folder if single_folder else -1, False, False, offset, limit)

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
    ampacheConnection.search([['title', 2, song_filter]], 'or', 'song', offset, limit, 0)

    """ def search_group(rules, operator, object_type, offset, limit, random):
    """
    ampacheConnection.search_group([['title', 2, song_filter]], 'or', 'all', offset, limit, 0)

    """ def search_rules(filter_str):
    """
    ampacheConnection.search_rules('song')

    """ def smartlists(filter_str, exact, offset, limit, include, sort, cond, add, update):
    """
    smartlists = ampacheConnection.smartlists(False, False, offset, limit)
    # smartlists come back under the 'playlist' key with 'smart_' prefixed ids
    smartlist_ids = id_list(ampacheConnection, smartlists, 'playlist')

    """ def smartlist(filter_id):
    """
    if smartlist_ids:
        ampacheConnection.smartlist(smartlist_ids[0])

        """ def smartlist_songs(filter_id, random, offset, limit):
        """
        ampacheConnection.smartlist_songs(smartlist_ids[0], False, offset, limit)
    else:
        skipped.append('smartlist, smartlist_songs (no smartlists on this server)')

    """ def user_playlists(filter_str, exact, offset, limit, sort, cond, include, add, update):
    """
    ampacheConnection.user_playlists(False, False, offset, limit)

    """ def user_smartlists(filter_str, exact, offset, limit, sort, cond, include, add, update):
    """
    ampacheConnection.user_smartlists(False, False, offset, limit)

    """ a real playlist id, since the playlist index also carries smartlists as 'smart_<id>'
        The documentation playlist was deleted above, so make one when the server has none
    """
    real_playlists = id_list(ampacheConnection,
                             ampacheConnection.user_playlists(False, False, offset, limit), 'playlist')
    real_playlist = pick([playlist for playlist in real_playlists if str(playlist).isdigit()], 0)
    if not real_playlist:
        real_playlist = first_id(ampacheConnection,
                                 ampacheConnection.playlist_create('documentation', 'private'), 'playlist')

    if real_playlist:
        """ def playlist_hash(filter_id):
        """
        ampacheConnection.playlist_hash(real_playlist)

        # the song has to be on the playlist before playlist_remove can take it off again
        ampacheConnection.playlist_add(real_playlist, single_song, 'song')

        """ def playlist_add(filter_id, object_id, object_type):
        MINIMUM_API_VERSION=6.3.0
        """
        ampacheConnection.playlist_add(real_playlist, single_album, 'album')

        """ def playlist_remove(filter_id, object_id, object_type, track, clear):
        MINIMUM_API_VERSION=8.0.0
        Replaces playlist_remove_song and is object_type aware
        """
        ampacheConnection.playlist_remove(real_playlist, single_song, 'song')
    else:
        skipped.append('playlist_hash, playlist_add, playlist_remove (no playlist available)')

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

    """ preferences
    A preference Ampache ships with can not be deleted, so this cycles one of its own
    """
    ampacheConnection.preference_create('example_preference', 'boolean', 0, 'interface', 'Example preference')
    ampacheConnection.preference_edit('example_preference', 1)
    ampacheConnection.preference_delete('example_preference')


    """ collections
    MINIMUM_API_VERSION=8.0.0
    A collection curates objects of any type, so the whole lifecycle is exercised here
    """
    remove_existing(ampacheConnection, ampacheConnection.collections(), 'collection',
                    ('Example Collection', 'Example Collection (edited)'), ampacheConnection.collection_delete)

    collection_create = ampacheConnection.collection_create('Example Collection', 'private')
    collection_new = first_id(ampacheConnection, collection_create, 'collection')

    ampacheConnection.collections()

    ampacheConnection.collections('album')
    if os.path.isfile("docs/" + api_format + "-responses/collections." + api_format):
        shutil.move("docs/" + api_format + "-responses/collections." + api_format,
                    "docs/" + api_format + "-responses/collections (album)." + api_format)

    if collection_new:
        ampacheConnection.collection(collection_new)

        ampacheConnection.collection_add(collection_new, single_album, 'album')
        ampacheConnection.collection_add(collection_new, single_song, 'song')

        ampacheConnection.collection_items(collection_new, offset, limit)

        ampacheConnection.collection_edit(collection_new, 'Example Collection (edited)', 'public')

        ampacheConnection.collection_remove(collection_new, single_song, 'song')

        ampacheConnection.collection_delete(collection_new)
    else:
        skipped.append('collection and friends (could not create a collection)')

    """ playlist folders
    MINIMUM_API_VERSION=8.0.0
    A playlist folder files playlists, smartlists and collections into a tree
    """
    remove_existing(ampacheConnection, ampacheConnection.playlist_folders(0, 0), 'playlist_folder',
                    ('Example Folder', 'Example Folder (edited)'), ampacheConnection.playlist_folder_delete)

    folder_create = ampacheConnection.playlist_folder_create('Example Folder')
    folder_new = first_id(ampacheConnection, folder_create, 'playlist_folder')

    ampacheConnection.playlist_folders(offset, limit)

    if folder_new:
        ampacheConnection.playlist_folder(folder_new)

        if real_playlist:
            ampacheConnection.playlist_folder_add(real_playlist, 'playlist', folder_new)

        ampacheConnection.playlist_folder_items(folder_new, offset, limit)

        ampacheConnection.playlist_folder_items('/', offset, limit)
        if os.path.isfile("docs/" + api_format + "-responses/playlist_folder_items." + api_format):
            shutil.move("docs/" + api_format + "-responses/playlist_folder_items." + api_format,
                        "docs/" + api_format + "-responses/playlist_folder_items (root)." + api_format)

        ampacheConnection.playlist_folder_edit(folder_new, 'Example Folder (edited)')

        if real_playlist:
            ampacheConnection.playlist_folder_remove(real_playlist, 'playlist')

        ampacheConnection.playlist_folder_delete(folder_new)
    else:
        skipped.append('playlist_folder and friends (could not create a playlist folder)')

    """ def goodbye(api_format = 'xml'):
    Close your session when you're done
    """
    # ampacheConnection.goodbye()

    if skipped:
        print('\n' + api_format + ': the server had no data for these methods, so they were skipped')
        for note in skipped:
            print('  * ' + note)

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
        newdata = re.sub(r"CDATA\[/media/", "CDATA[/mnt/files-music/ampache-test/", newdata)
        newdata = re.sub(r"\\/media\\/", r"\\/mnt\\/files-music\\/ampache-test\\/", newdata)
        newdata = re.sub(url_text.replace("/", r"\\/"), "music.com.au", newdata)
        newdata = re.sub("http://music.com.au", "https://music.com.au", newdata)
        newdata = re.sub(r"http:\\/\\/music.com.au", r"https:\\/\\/music.com.au", newdata)
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
