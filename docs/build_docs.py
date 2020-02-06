#!/usr/bin/env python3

import shutil
import sys
import time

import ampache

# user variables
if sys.argv[1] and sys.argv[2] and sys.argv[2]:
    ampache_url  = sys.argv[1]
    ampache_api  = sys.argv[2]
    ampache_user = sys.argv[3]
else:
    ampache_url  = 'https://music.server'
    ampache_api  = 'mysuperapikey'
    ampache_user = 'myusername'

def build_docs(ampache_url, ampache_api, ampache_user, api_format):
    """TODO
    def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    def update_artist_info(ampache_url, ampache_api, id, api_format = 'xml'):
    def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
    def get_art(ampache_url, ampache_api, id, type, api_format = 'xml'):
    def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False, api_format = 'xml'):
    def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    def localplay(ampache_url, ampache_api, username, api_format = 'xml'):
    def democratic(ampache_url, ampache_api, username, api_format = 'xml'):
    """

    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
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
    #print(ampache.url_to_song(ampache_url, ampache_api))

    """ get_indexes
    def get_indexes(ampache_url, ampache_api, type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):

    'song'|'album'|'artist'|'playlist'
    """
    songs     = ampache.get_indexes(ampache_url, ampache_api, 'song', '', '', '', '', 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/get_indexes." + api_format,
                "../docs/" + api_format + "-responses/get_indexes-songs." + api_format)

    albums    = ampache.get_indexes(ampache_url, ampache_api, 'album', '', '', '', '', 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/get_indexes." + api_format,
                "../docs/" + api_format + "-responses/get_indexes-albums." + api_format)

    artists   = ampache.get_indexes(ampache_url, ampache_api, 'artist', '', '', '', '', 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/get_indexes." + api_format,
                "../docs/" + api_format + "-responses/get_indexes-artists." + api_format)

    playlists = ampache.get_indexes(ampache_url, ampache_api, 'playlist', '', '', '', '', 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/get_indexes." + api_format,
                "../docs/" + api_format + "-responses/get_indexes-playlists." + api_format)

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

    """ user
    def user(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    myuser = ampache.user(ampache_url, ampache_api, ampache_user, api_format)

    """ advanced_search
    def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    """
    search_rules = [['favorite', 0, '%'], ['artist', 3, 'Prodigy']]
    search_song = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'song', 0, 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/advanced_search." + api_format,
                "../docs/" + api_format + "-responses/advanced_search-song." + api_format)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'total_count':
                continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
            song_title = child.find('title').text
    else:
        song_title = search_song[0]['title']

    search_rules = [['favorite', 0, '%'], ['artist', 0, 'Men']]
    search_album = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'album', 0, 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/advanced_search." + api_format,
                "../docs/" + api_format + "-responses/advanced_search-album." + api_format)

    if api_format == 'xml':
        for child in search_album:
            if child.tag == 'total_count':
                continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))
            album_title = child.find('name').text
    else:
        album_title = search_album[0]['name']

    search_rules = [['favorite', 0, '%'], ['artist', 4, 'Prodigy']]
    search_artist = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'artist', 0, 4, api_format)
    shutil.move("../docs/" + api_format + "-responses/advanced_search." + api_format,
                "../docs/" + api_format + "-responses/advanced_search-artist." + api_format)

    if api_format == 'xml':
        for child in search_artist:
            if child.tag == 'total_count':
                print('total_count', search_artist.find('total_count').text)
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
    album_songs = ampache.album_songs(ampache_url, ampache_api, single_album, 0, 0, api_format)
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
                continue
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ stats
    def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    stats = ampache.stats(ampache_url, ampache_api, 'artist', 'random', ampache_user, False, 0, 2, api_format)
    shutil.move("../docs/" + api_format + "-responses/stats." + api_format,
                "../docs/" + api_format + "-responses/stats-artist." + api_format)

    if api_format == 'xml':
        for child in stats:
            if child.tag == 'artist':
                print('\ngetting a random artist using the stats method and found', child.find('name').text)
                single_artist = child.attrib['id']
                print(child.tag, child.attrib)
                for subchildren in child:
                    print(str(subchildren.tag) + ': ' + str(subchildren.text))
    stats = ampache.stats(ampache_url, ampache_api, 'album', 'random', ampache_user, None, 0, 2, api_format)
    shutil.move("../docs/" + api_format + "-responses/stats." + api_format,
                "../docs/" + api_format + "-responses/stats-album." + api_format)

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
        album_title = search_album[0]['name']

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
    artist_albums = ampache.artist_albums(ampache_url, ampache_api, single_artist, 0, 0, api_format)

    """ artist_songs
    def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    artist_songs = ampache.artist_songs(ampache_url, ampache_api, single_artist, 0, 0, api_format)

    """ artists
    def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    """
    myartists = ampache.artists(ampache_url, ampache_api, False, False, False, 0, 0, False, api_format)

    """ catalog_action
    def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    """
    catalog_action = ampache.catalog_action(ampache_url, ampache_api, 'clean', 2, api_format)
    shutil.move("../docs/" + api_format + "-responses/catalog_action." + api_format,
                "../docs/" + api_format + "-responses/catalog_action-error." + api_format)

    catalog_action = ampache.catalog_action(ampache_url, ampache_api, 'clean_catalog', 2, api_format)
    shutil.move("../docs/" + api_format + "-responses/catalog_action." + api_format,
                "../docs/" + api_format + "-responses/catalog_action-clean_catalog." + api_format)

    """ flag
    def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    """
    #print(ampache.flag(ampache_url, ampache_api))

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
    friends_timeline = ampache.friends_timeline(ampache_url, ampache_api, 0, 0, api_format)

    """ last_shouts
    def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    """
    last_shouts = ampache.last_shouts(ampache_url, ampache_api, ampache_user, 0, api_format)

    """ playlists
    def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlists = ampache.playlists(ampache_url, ampache_api, False, False, 0, 0, api_format)

    """ playlist
    def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    """
    playlist = ampache.playlist(ampache_url, ampache_api, single_playlist, api_format)

    """ playlist_songs
    def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    playlist_songs = ampache.playlist_songs(ampache_url, ampache_api, single_playlist, 0, 0, api_format)

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

    """ rate
    def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    """
    #print(ampache.rate(ampache_url, ampache_api))

    """ record_play
    def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    """
    #print(ampache.record_play(ampache_url, ampache_api))

    """ scrobble
    def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    """
    scrobble = ampache.scrobble(ampache_url, ampache_api, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Sub Atari Knives', False, False, False, int(time.time()), 'AmpaceApi', api_format)
    shutil.move("../docs/" + api_format + "-responses/scrobble." + api_format,
                "../docs/" + api_format + "-responses/scrobble-error." + api_format)

    scrobble = ampache.scrobble(ampache_url, ampache_api, 'Welcome to Planet Sexor', 'Tiga', 'Sexor', False, False, False, int(time.time()), 'test.py', api_format)

    """ search_songs
    def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    """
    search_songs = ampache.search_songs(ampache_url, ampache_api, song_title, 0, 0, api_format)

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
    songs = ampache.songs(ampache_url, ampache_api, False, False, False, False, 0, 0, api_format)
    if api_format == 'xml':
        for child in songs:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ tags
    def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    """
    genre = ''
    tags = ampache.tags(ampache_url, ampache_api, 'Brutal Death Metal', '1', 0, 4, api_format)
    if api_format == 'xml':
        for child in tags:
            if child.tag == 'total_count':
                print('total_count', search_artist.find('total_count').text)
                continue
            print(child.tag, child.attrib)
            genre = child.attrib['id']
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

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

    """ timeline
    def timeline(ampache_url, ampache_api, username, limit = 0, since = 0, api_format = 'xml'):
    """
    timeline = ampache.timeline(ampache_url, ampache_api, ampache_user, 10, 0, api_format)

    if api_format == 'xml':
        for child in timeline:
            print(child.tag, child.attrib)
            for subchildren in child:
                print(str(subchildren.tag) + ': ' + str(subchildren.text))

    """ toggle_follow
    def toggle_follow(ampache_url, ampache_api, username, api_format = 'xml'):
    """
    #print(ampache.toggle_follow(ampache_url, ampache_api))

    """ update_from_tags
    def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id, api_format = 'xml'):
    """
    update_from_tags = ampache.update_from_tags(ampache_url, ampache_api, 'album', single_album, api_format)

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


build_docs(ampache_url, ampache_api,ampache_user, 'xml')
build_docs(ampache_url, ampache_api,ampache_user, 'json')