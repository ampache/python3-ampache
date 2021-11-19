#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import sys
import time

# pip3 install --user ampache==4.4.0
import ampache

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
api_version = '390000'
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=60&uid=4&player=api&name=Synthetic%20-%20BrownSmoke.wma'


def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    """TODO
    def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
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
    ampache.handshake(ampache_url, 'badkey', False, False, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/handshake." + api_format):
        shutil.move("docs/" + api_format + "-responses/handshake." + api_format,
                    "docs/" + api_format + "-responses/handshake (error)." + api_format)
    # use correct details
    ampache_session = ampache.handshake(ampache_url, encrypted_key, False, False, api_version, api_format)
    if not ampache_session:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api=False, version='443000', api_format='xml'):
    """
    ampache.ping(ampache_url, False, api_version, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/ping." + api_format):
        shutil.move("docs/" + api_format + "-responses/ping." + api_format,
                    "docs/" + api_format + "-responses/ping (no auth)." + api_format)
    # did all this work?
    my_ping = ampache.ping(ampache_url, ampache_session, api_version, api_format)
    if not my_ping:
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ url_to_song
    def url_to_song(ampache_url, ampache_api, url, api_format = 'xml'):
    """
    ampache.url_to_song(ampache_url, ampache_session, song_url, api_format)

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

    single_song = 57

    """ videos
    def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.videos(ampache_url, ampache_session, False, False, 0, 0, api_format)
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

    song_title = 'Sensorisk Deprivation'

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'album', 0, limit, 0,
                                           api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    album_title = ' CARNÚN - MALKUTH'

    search_rules = [['favorite', 0, '%'], ['artist', 2, 'Car']]
    search_artist = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'artist', 0, limit, 0,
                                            api_format)
    if os.path.isfile("docs/" + api_format + "-responses/advanced_search." + api_format):
        shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                    "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    artist_title = 'CARNÚN'

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
    ampache.albums(ampache_url, ampache_session, album_title, 1, False, False, 0, 10, False, api_format)

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

    single_artist = 2

    ampache.stats(ampache_url, ampache_session, 'album', 'random', ampache_user, None, 0, 2, api_format)
    if os.path.isfile("docs/" + api_format + "-responses/stats." + api_format):
        shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                    "docs/" + api_format + "-responses/stats (album)." + api_format)

    """ artist
    def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    ampache.artist(ampache_url, ampache_session, single_artist, False, api_format)

    """ artist_albums
    def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_albums(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ artist_songs
    def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_songs(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ artists
    def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampache.artists(ampache_url, ampache_session, False, False, False, 0, limit, False, api_format)

    """ rate
    def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'playlist', 2, 2, api_format)

    """ followers
    def followers(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.followers(ampache_url, ampache_session, ampache_user, api_format)

    """ following
    def following(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.following(ampache_url, ampache_session, ampache_user, api_format)

    """ friends_timeline
    def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0, api_format = 'xml'):
    """
    ampache.friends_timeline(ampache_url, ampache_session, limit, 0, api_format)

    """ last_shouts
    def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    """
    ampache.last_shouts(ampache_url, ampache_session, ampache_user, limit, api_format)

    """ playlists
    def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.playlists(ampache_url, ampache_session, False, False, 0, limit, api_format)

    """ playlist_create
    def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    """
    playlist_create = ampache.playlist_create(ampache_url, ampache_session, 'rename', 'private', api_format)

    for child in playlist_create:
        if child.tag == 'playlist':
            single_playlist = child.attrib['id']

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
    ampache.playlist(ampache_url, ampache_session, single_playlist, api_format)

    """ playlist_songs
    def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.playlist_songs(ampache_url, ampache_session, single_playlist, 0, limit, api_format)

    """ playlist_delete
    def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    #ampache.playlist_delete(ampache_url, ampache_session, single_playlist, api_format)

    """ rate
    def rate(ampache_url, ampache_api, object_type, object_id, rating, api_format='xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'song', 70, 5, api_format)
    ampache.rate(ampache_url, ampache_session, 'song', 70, 0, api_format)

    """ search_songs
    def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.search_songs(ampache_url, ampache_session, song_title, 0, limit, api_format)

    """ song
    def song(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.song(ampache_url, ampache_session, single_song, api_format)

    """ songs
    def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.songs(ampache_url, ampache_session, False, False, False, False, 0, limit, api_format)

    """ tags
    def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = 4
    tags = ampache.tags(ampache_url, ampache_session, 'Da', False, 0, limit, api_format)

    """ tag
    def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.tag(ampache_url, ampache_session, genre, api_format)

    """ tag_albums
    def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.tag_albums(ampache_url, ampache_session, genre, 0, 2, api_format)

    """ tag_artists
    def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.tag_artists(ampache_url, ampache_session, genre, 0, 1, api_format)

    """ tag_songs
    def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.tag_songs(ampache_url, ampache_session, genre, 0, 1, api_format)

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

    """ localplay
    def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    """
    ampache.localplay(ampache_url, ampache_session, 'stop', api_format)

    """ democratic
    def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    """
    ampache.democratic(ampache_url, ampache_session, 'vote', single_song, api_format)

    # Clean the files
    self_check(api_format, ampache_url, ampache_session, original_api)


def self_check(api_format, ampache_url, ampache_api, ampache_session):
    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files, 'r', encoding="utf-8")
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        newdata = re.sub(url_text, "music.com.au", filedata)
        newdata = re.sub(ampache_api, "eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub(ampache_session, "cfj3f237d563f479f5223k23189dbb34", newdata)
        newdata = re.sub('auth=[a-z0-9]*', "auth=eeb9f1b6056246a7d563f479f518bb34", newdata)
        newdata = re.sub('ssid=[a-z0-9]*', "ssid=cfj3f237d563f479f5223k23189dbb34", newdata)

        f = open("./docs/" + api_format + "-responses/" + files, 'w', encoding="utf-8")
        f.write(newdata)
        f.close()


build_docs(url, api, user, 'xml')
