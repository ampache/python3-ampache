#!/usr/bin/env python3

import os
import shutil
import sys
import time
import ampache

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

try:
    if sys.argv[4]:
        smartlist = sys.argv[4]
except IndexError:
    smartlist    = 142

limit     = 4
transcode = 'ogg'
destin    = '/tmp'

def cache_playlist(ampache_url, ampache_api, ampache_user, api_format, smartlist, destination, transcode):


    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    original_api  = ampache_api
    encrypted_key = ampache.encrypt_string(ampache_api, ampache_user)

    """ handshake
    def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '400004', api_format = 'xml'):
    # processed details
    """
    ampache_api = ampache.handshake(ampache_url, encrypted_key, '', 0, '400004', api_format)
    if not ampache_api:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api, api_format = 'xml'):
    # did all this work?
    """
    my_ping = ampache.ping(ampache_url, ampache_api, api_format)
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
    list_songs   = list()
    search_rules = [['smartplaylist', 0, '142']]
    search_song  = ampache.advanced_search(ampache_url, ampache_api, search_rules, 'or', 'song', 0, limit, 1, api_format)

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
            ampache.download(ampache_url, ampache_api, object_id[0], 'song', os.path.join(destination, object_id[1]), transcode, api_format)
        else:
            print('File exists')

    """ goodbye
    def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    # Close your session when you're done
    """
    goodbye = ampache.goodbye(ampache_url, ampache_api, api_format)

cache_playlist(ampache_url, ampache_api,ampache_user, 'xml', smartlist, destin, transcode)
cache_playlist(ampache_url, ampache_api,ampache_user, 'json', smartlist, destin, transcode)

