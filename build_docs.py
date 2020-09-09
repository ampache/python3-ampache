#!/usr/bin/env python3

import os
import shutil
import sys
import time

from src import ampache

# user variables
try:
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        ampache_url  = sys.argv[1]
        ampache_api  = sys.argv[2]
        ampache_user = sys.argv[3]
except IndexError:
    ampache_url  = 'https://music.server'
    ampache_api  = 'mysuperapikey'
    ampache_user = 'myusername'

limit = 4
song_url = 'https://music.com.au/play/index.php?ssid=eeb9f1b6056246a7d563f479f518bb34&type=song&oid=164215&uid=2&player=api&name=Hellyeah%20-%20-.mp3'


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

    """ def encrypt_string(ampache_api, user)
        This function can be used to encrypt your apikey into the accepted format.
    """
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '400004', api_format = 'xml'):
        This is the function that handles verifying a new handshake
        Takes a timestamp, auth key, and username.
    """
    ampache_session = ampache.handshake(ampache_url, encrypted_key, False, False, '400004', api_format)
    if not ampache_session:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ def ping(ampache_url, ampache_api, api_format = 'xml'):
        This can be called without being authenticated, it is useful for determining if what the status
        of the server is, and what version it is running/compatible with
    """
    my_ping = ampache.ping(ampache_url, ampache_session, api_format)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ def set_debug(boolean):
        This function can be used to enable/disable debugging messages
    """
    ampache.set_debug(True)

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
    shutil.move("docs/" + api_format + "-responses/user." + api_format,
                "docs/" + api_format + "-responses/user (disabled)." + api_format)

    """ def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user_delete(ampache_url, ampache_session, tempusername, api_format)

    """ def user(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    ampache.user(ampache_url, ampache_session, 'missing_user', api_format)
    shutil.move("docs/" + api_format + "-responses/user." + api_format,
                "docs/" + api_format + "-responses/user (error)." + api_format)

    myuser = ampache.user(ampache_url, ampache_session, ampache_user, api_format)
    if api_format == 'xml':
        for child in myuser:
            if child.tag == 'user':
                user_id = child.attrib['id']
    else:
        user_id = myuser['user']['id']

    """ def get_indexes(ampache_url, ampache_api, type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):

    'song'|'album'|'artist'|'playlist'
    """
    songs = ampache.get_indexes(ampache_url, ampache_session, 'song', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (song)." + api_format)
    if api_format == 'xml':
        for child in songs:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: songs ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    albums = ampache.get_indexes(ampache_url, ampache_session, 'album', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (album)." + api_format)
    if api_format == 'xml':
        for child in albums:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: albums ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    artists = ampache.get_indexes(ampache_url, ampache_session, 'artist', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (artist)." + api_format)
    if api_format == 'xml':
        for child in artists:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: artists ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    playlists = ampache.get_indexes(ampache_url, ampache_session, 'playlist', False, False, False, 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/get_indexes." + api_format,
                "docs/" + api_format + "-responses/get_indexes (playlist)." + api_format)
    if api_format == 'xml':
        for child in playlists:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: playlists ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    """ def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    videos = ampache.videos(ampache_url, ampache_session, False, False, 0, 0, api_format)

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
        # for child in playlists:
        #     if child.tag == 'playlist':
        #         single_playlist = child.attrib['id']
        for child in videos:
            if child.tag == 'video':
                single_video = child.attrib['id']
    else:
        single_song = songs[0]['id']
        single_album = albums[0]['id']
        single_artist = artists[0]['id']
        # single_playlist = playlists[0]['id']
        single_video = videos[0]['id']

    """ def video(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.video(ampache_url, ampache_session, single_video, api_format)

    """ def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['artist', 3, 'Prodigy']]
    search_song = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'song', 0, limit, 0, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (song)." + api_format)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (song) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            song_title = child.find('title').text
    else:
        song_title = search_song[0]['title']

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'album', 0, limit, 0, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (album)." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (album) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', limit, 'Prodigy']]
    search_artist = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'artist', 0, limit, 0, api_format)
    shutil.move("docs/" + api_format + "-responses/advanced_search." + api_format,
                "docs/" + api_format + "-responses/advanced_search (artist)." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: advanced_search (artist) ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue
            artist_title = child.find('name').text
    else:
        artist_title = search_artist[0]['name']

    """ def album(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    album = ampache.album(ampache_url, ampache_session, single_album, False, api_format)

    if api_format == 'xml':
        for child in album:
            if child.tag == 'album':
                album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    """ def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.album_songs(ampache_url, ampache_session, single_album, 0, limit, api_format)

    """ def albums(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    albums = ampache.albums(ampache_url, ampache_session, album_title, 1, False, False, 0, 10, False, api_format)
    if api_format == 'xml':
        for child in albums:
            if child.tag == 'total_count':
                if int(child.text) > int(limit):
                    print()
                    sys.exit('ERROR: albums ' + child.text + ' found more items than the limit ' + str(limit))
                else:
                    continue

    """ def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """

    ampache.stats(ampache_url, ampache_session, 'song', 'random', ampache_user, None, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (song)." + api_format)

    stats = ampache.stats(ampache_url, ampache_session, 'artist', 'random', ampache_user, False, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (artist)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'artist':
                print('\ngetting a random artist using the stats method and found', child.find('name').text)
                single_artist = child.attrib['id']
                print(child.tag, child.attrib)
    else:
        single_artist = stats[0]['id']

    stats = ampache.stats(ampache_url, ampache_session, 'album', 'random', ampache_user, None, 0, 2, api_format)
    shutil.move("docs/" + api_format + "-responses/stats." + api_format,
                "docs/" + api_format + "-responses/stats (album)." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'album':
                print('\ngetting a random album using the stats method and found', child.find('name').text)
                single_album = child.attrib['id']
                album_title = child.find('name').text
    else:
        album_title = stats[0]['name']

    """ def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    """
    artist = ampache.artist(ampache_url, ampache_session, single_artist, False, api_format)

    if api_format == 'xml':
        for child in artist:
            if child.tag == 'artist':
                print('\nsearching for an artist with this id', single_artist)

    """ def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_albums(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.artist_songs(ampache_url, ampache_session, single_artist, 0, limit, api_format)

    """ def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    ampache.artists(ampache_url, ampache_session, False, False, False, 0, limit, False, api_format)

    """ def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    """
    ampache.catalog_action(ampache_url, ampache_session, 'clean', 2, api_format)
    shutil.move("docs/" + api_format + "-responses/catalog_action." + api_format,
                "docs/" + api_format + "-responses/catalog_action (error)." + api_format)

    ampache.catalog_action(ampache_url, ampache_session, 'clean_catalog', 2, api_format)

    """ def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'playlist', 2069, True, api_format)

    """ def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'playlist', 2069, 2, api_format)

    """ def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.record_play(ampache_url, ampache_session, 77371, user_id, 'AmpacheAPI', api_format)

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
    ampache.playlists(ampache_url, ampache_session, False, False, 0, limit, api_format)

    """ def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    """
    playlist_create = ampache.playlist_create(ampache_url, ampache_session, 'rename', 'private', api_format)
    
    if api_format == 'xml':
        tmp_playlist = playlist_create[1].attrib
        single_playlist = tmp_playlist['id']
    else:
        single_playlist = playlist_create[0]['id']

    """ def playlist_edit(ampache_url, ampache_api, filter, name = False, type = False, api_format = 'xml'):
    """
    ampache.playlist_edit(ampache_url, ampache_session, single_playlist, 'documentation', 'public', api_format)

    """ def playlist_add_song(ampache_url, ampache_api, filter, song, check = 0, api_format = 'xml'):
    """
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 77371, 0, api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 77371, 1, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_add_song." + api_format,
                "docs/" + api_format + "-responses/playlist_add_song (error)." + api_format)
    ampache.playlist_add_song(ampache_url, ampache_session, single_playlist, 77371, 0, api_format)

    """ def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False, api_format = 'xml'):
    """
    ampache.playlist_remove_song(ampache_url, ampache_session, single_playlist, False, 1, api_format)

    """ def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.playlist(ampache_url, ampache_session, single_playlist, api_format)

    """ def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.playlist_songs(ampache_url, ampache_session, single_playlist, 0, limit, api_format)

    """ def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.playlist_delete(ampache_url, ampache_session, single_playlist, api_format)

    """ def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    'song'|'index'|'id'
    """
    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'song', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (song)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'index', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (index)." + api_format)

    ampache.playlist_generate(ampache_url, ampache_session, 'random', False, False, False, False, 'id', 0, limit, api_format)
    shutil.move("docs/" + api_format + "-responses/playlist_generate." + api_format,
                "docs/" + api_format + "-responses/playlist_generate (id)." + api_format)

    """ def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    ampache.scrobble(ampache_url, ampache_session, 'Hear. Life. Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False, int(time.time()), 'AmpaceApi', api_format)
    shutil.move("docs/" + api_format + "-responses/scrobble." + api_format,
                "docs/" + api_format + "-responses/scrobble (error)." + api_format)

    ampache.scrobble(ampache_url, ampache_session, 'Welcome to Planet Sexor', 'Tiga', 'Sexor', False, False, False, int(time.time()), 'test.py', api_format)

    """ def record_play(ampache_url, ampache_api, object_id, user, client='AmpacheAPI', api_format='xml'):
    """
    ampache.record_play(ampache_url, ampache_session, 164527, ampache_user, 'AmpaceApi', api_format)

    """ def rate(ampache_url, ampache_api, object_type, object_id, rating, api_format='xml'):
    """
    ampache.rate(ampache_url, ampache_session, 'song', 164527, 5, api_format)
    ampache.rate(ampache_url, ampache_session, 'song', 164527, 0, api_format)

    """ def flag(ampache_url, ampache_api, object_type, object_id, flag, api_format='xml'):
    """
    ampache.flag(ampache_url, ampache_session, 'song', 164527, True, api_format)
    ampache.flag(ampache_url, ampache_session, 'song', 164527, False, api_format)

    """ def get_art(ampache_url, ampache_api, object_id, object_type, destination, api_format='xml'):
    """
    ampache.get_art(ampache_url, ampache_session, 164527, 'song', (os.path.join(os.getcwd(), 'get_art.jpg')), api_format)
    
    """ def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampache.search_songs(ampache_url, ampache_session, song_title, 0, limit, api_format)

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
    songs = ampache.songs(ampache_url, ampache_session, False, False, False, False, 0, limit, api_format)
    if api_format == 'xml':
        for child in songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampache.tags(ampache_url, ampache_session, 'Brutal Death Metal', False, 0, limit, api_format)
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

    """ def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.tag(ampache_url, ampache_session, genre, api_format)

    """ def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_albums = ampache.tag_albums(ampache_url, ampache_session, genre, 0, 2, api_format)
    if api_format == 'xml':
        for child in tag_albums:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    tag_artists = ampache.tag_artists(ampache_url, ampache_session, genre, 0, 1, api_format)
    if api_format == 'xml':
        for child in tag_artists:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.tag_songs(ampache_url, ampache_session, genre, 0, 1, api_format)

    """ def licenses(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    ampache.licenses(ampache_url, ampache_session, False, False, 0, limit, api_format)

    """ def license(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license(ampache_url, ampache_session, 2, api_format)

    """ def license_songs(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    ampache.license_songs(ampache_url, ampache_session, 2, api_format)

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

    """ update_podcast
    """
    ampache.update_podcast(ampache_url, ampache_session, 10, api_format)

    """ def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    """
    ampache.localplay(ampache_url, ampache_session, 'status', False, False, 0, api_format)
    shutil.move("docs/" + api_format + "-responses/localplay." + api_format,
                "docs/" + api_format + "-responses/localplay (status)." + api_format)

    ampache.localplay(ampache_url, ampache_session, 'stop', False, False, 0, api_format)

    """ def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    """
    #print(ampache.democratic(ampache_url, ampache_session))

    """ def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    Close your session when you're done
    """
    ampache.goodbye(ampache_url, ampache_session, api_format)

    print("Checking files in " + api_format + " for private strings")
    for files in os.listdir("./docs/" + api_format + "-responses/"):
        f = open("./docs/" + api_format + "-responses/" + files, 'r', encoding="utf-8")
        filedata = f.read()
        f.close()

        url_text = ampache_url.replace("https://", "")
        newdata = filedata.replace(url_text, "music.com.au")
        newdata = newdata.replace(ampache_api, "eeb9f1b6056246a7d563f479f518bb34")
        newdata = newdata.replace(ampache_session, "cfj3f237d563f479f5223k23189dbb34")

        f = open("./docs/" + api_format + "-responses/" + files, 'w', encoding="utf-8")
        f.write(newdata)
        f.close()


build_docs(url, api, user, 'xml')
build_docs(url, api, user, 'json')
