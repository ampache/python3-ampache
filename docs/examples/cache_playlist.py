#!/usr/bin/env python3

import os
import sys
import ampache

# user variables
url = 'https://develop.ampache.dev'
api = 'demodemo'
user = 'demo'
smart_list = 21
my_limit = 4
my_transcode = 'raw'
my_destin = '/tmp'


def cache_playlist(ampache_url, ampache_api, ampache_user, api_format, smartlist, destination, transcode, limit):
    ampacheConnection = ampache.API()
    ampacheConnection.set_format(api_format)
    """ encrypt_string
    def encrypt_string(ampache_api, user):
    """
    encrypted_key = ampacheConnection.encrypt_string(ampache_api, ampache_user)

    """ handshake
    def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '6.0.0'):
    # processed details
    """
    ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key, '', 0, '6.0.0')
    if not ampache_session:
        print()
        sys.exit('ERROR: Failed to connect to ' + ampache_url)

    """ ping
    def ping(ampache_url, ampache_api):
    # did all this work?
    """
    my_ping = ampacheConnection.ping(ampache_url, ampache_session)
    if not my_ping:
        print()
        sys.exit('ERROR: Failed to ping ' + ampache_url)

    """ set_debug
    def set_debug(mybool):
    """
    ampacheConnection.set_debug(False)

    """ advanced_search
    def advanced_search(ampache_url, ampache_api, rules, operator = 'and',
                        type = 'song', offset = 0, limit = 0, random = 0):
    """
    list_songs = list()
    search_rules = [['smartplaylist', 0, smartlist]]
    search_song = ampacheConnection.advanced_search(search_rules, 'or', 'song', 0, limit, 1)

    if api_format == 'xml':
        for child in search_song:
            if child.tag == 'song':
                list_songs.append([child.attrib['id'], os.path.basename(child.find('filename').text)])
    else:
         for child in search_song['song']:
            print('list')
            print(child)
            list_songs.append([child['id'], os.path.basename(child['filename'])])

    print(list_songs)
    
    """ download
    def download(ampache_url, ampache_api, object_id, object_type, destination, file_format='raw'):
    """
    for object_id in list_songs:
        if not os.path.isfile(os.path.join(destination, object_id[1])):
            ampacheConnection.download(object_id[0], 'song', os.path.join(destination, object_id[1]), transcode)
        else:
            print('File exists')

    """ goodbye
    def goodbye(ampache_url, ampache_api):
    Close your session when you're done
    """
    ampacheConnection.goodbye()


cache_playlist(url, api, user, 'xml', smart_list, my_destin, my_transcode, my_limit)
cache_playlist(url, api, user, 'json', smart_list, my_destin, my_transcode, my_limit)
