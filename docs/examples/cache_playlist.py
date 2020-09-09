#!/usr/bin/env python3

import os
import sys
import ampache

# user variables
url = 'https://music.server'
api = 'mysuperapikey'
user = 'myusername'
smart_list = 142
my_limit = 4
my_transcode = 'ogg'
my_destin = '/tmp'


def cache_playlist(ampache_url, ampache_api, ampache_user, api_format, smartlist, destination, transcode, limit):
    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ handshake
    def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '420000', api_format = 'xml'):
    # processed details
    """
    ampache_session = ampache.handshake(ampache_url, encrypted_key, False, False, '420000', api_format)
    if not ampache_session:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api, api_format = 'xml'):
    # did all this work?
    """
    my_ping = ampache.ping(ampache_url, ampache_session, api_format)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ set_debug
    def set_debug(mybool):
    """
    ampache.set_debug(False)

    """ advanced_search
    def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, random = 0, api_format = 'xml'):
    """
    list_songs = list()
    search_rules = [['smartplaylist', 0, smartlist]]
    search_song = ampache.advanced_search(ampache_url, ampache_session, search_rules, 'or', 'song', 0, limit, 1, api_format)

    for child in search_song:
        if api_format == 'xml':
            if child.tag == 'song':
                list_songs.append([child.attrib['id'], os.path.basename(os.path.splitext(child.find('filename').text)[0] + '.' + transcode)])
        else:
            list_songs.append([child['id'], os.path.basename(os.path.splitext(child['filename'])[0] + '.' + transcode)])

    print(list_songs)
    
    """ download
    def download(ampache_url, ampache_api, object_id, object_type, destination, file_format='raw', api_format='xml'):
    """
    for object_id in list_songs:
        if not os.path.isfile(os.path.join(destination, object_id[1])):
            ampache.download(ampache_url, ampache_session, object_id[0], 'song', os.path.join(destination, object_id[1]), transcode, api_format)
        else:
            print('File exists')

    """ goodbye
    def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    Close your session when you're done
    """
    ampache.goodbye(ampache_url, ampache_session, api_format)


cache_playlist(url, api, user, 'xml', smart_list, my_destin, my_transcode, my_limit)
cache_playlist(url, api, user, 'json', smart_list, my_destin, my_transcode, my_limit)
