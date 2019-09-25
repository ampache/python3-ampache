#!/usr/bin/env python3

""" Copyright (C)2019
Lachlan de Waard <lachlan.00@gmail.com>
---------------------------------------
Ampache XML-Api v400001 for python3
---------------------------------------

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.    
    
 This program is distributed in the hope that it will be useful,    
 but WITHOUT ANY WARRANTY; without even the implied warranty of    
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the    
 GNU General Public License for more details.    

 You should have received a copy of the GNU General Public License    
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import urllib.parse
import urllib.request

from xml.etree import ElementTree as ET

""" ping
    MINIMUM_API_VERSION=380001

    This can be called without being authenticated, it is useful for determining if what the status
    of the server is, and what version it is running/compatible with

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
"""
def ping(ampache_url, ampache_api):
    """ Request Ampache ping auth """
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'ping',
                                   'auth': ampache_api})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    result.close()
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('auth').text
    except AttributeError:
        token = False
    return token

""" handshake
    MINIMUM_API_VERSION=380001

    This is the function that handles verifying a new handshake
    Takes a timestamp, auth key, and username.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * user        = (string)
    * timestamp   = (integer) UNIXTIME() //optional
    * version     = (string) //optional)
"""
def handshake(ampache_url, ampache_api, user, timestamp=0, version='400001'):
    if not ampache_url or not ampache_api or not user:
        return False
    if timestamp == 0:
        timestamp = int(time.time())
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'handshake',
                                   'user': user,
                                   'auth': ampache_api,
                                   'timestamp': str(timestamp),
                                   'version': version})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    result.close()
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('auth').text
    except AttributeError:
        token = False
    return token

""" goodbye
    MINIMUM_API_VERSION=400001

    Destroy session for ampache_api auth key.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
"""
def goodbye(ampache_url, ampache_api):
    """ Request Ampache destroy an api session """
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'goodbye',
                                   'auth': ampache_api})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    result.close()
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" scrobble
    MINIMUM_API_VERSION=400001

    Search for a song using text info and then record a play if found.
    This allows other sources to record play history to ampache

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * title       = (string)
    * artist      = (string)
    * album       = (string)
    * MBtitle     = (string) //optional
    * MBartist    = (string) //optional
    * MBalbum     = (string) //optional
    * time        = (integer) UNIXTIME() //optional
    * client      = (string) //optional)
"""
def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle='', MBartist='', MBalbum='', time='', client = 'AmpacheAPI'):
    if not ampache_url or not ampache_api or not title or not artist or not album:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'scrobble',
                                   'auth': ampache_api,
                                   'client': client,
                                   'date': str(time),
                                   'song': title,
                                   'album': album,
                                   'artist': artist,
                                   'songmbid': MBtitle,
                                   'albummbid': MBalbum,
                                   'artistmdib': MBartist})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" get_indexes
    MINIMUM_API_VERSION=400001

    This takes a collection of inputs and returns ID + name for the object type

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'song'|'album'|'artist'|'playlist'
    * filter      = (string) //optional
    * add
    * update
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def get_indexes(ampache_url, ampache_api, type, filter = '', add = '', update = '', offset = '', limit = ''):
    if not ampache_url or not ampache_api or not type:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'get_indexes',
                                   'auth': ampache_api,
                                   'type': type,
                                   'filter': filter,
                                   'add': add,
                                   'update': update,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" artists
    MINIMUM_API_VERSION=380001

    This takes a collection of inputs and returns artist objects. This function is deprecated!

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * add
    * update
    * offset
    * limit
    * include
"""
def artists(ampache_url, ampache_api, filter, add, update, offset, limit, include):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artists',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'add': add,
                                   'update': update,
                                   'offset': str(offset),
                                   'limit': str(limit),
                                   'include': include})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" artist
    MINIMUM_API_VERSION=380001

    This returns a single artist based on the UID of said artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * include
"""
def artist(ampache_url, ampache_api, filter, include):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artist',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'include': include})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" artist_albums
    MINIMUM_API_VERSION=380001

    This returns the albums of an artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def artist_albums(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artist_albums',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" artist_songs
    MINIMUM_API_VERSION=380001

    This returns the songs of the specified artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def artist_songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artist_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" albums
    MINIMUM_API_VERSION=380001

    This returns albums based on the provided search filters

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * exact
    * add
    * update
    * filter
    * offset
    * limit
    * include
"""
def albums(ampache_url, ampache_api, exact, add, update, filter, offset, limit, include):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'albums',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'add': add,
                                   'update': update,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit),
                                   'include': include})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" album
    MINIMUM_API_VERSION=380001

    This returns a single album based on the UID provided

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * include
"""
def album(ampache_url, ampache_api, filter, include):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'album',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'include': include})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" album_songs
    MINIMUM_API_VERSION=380001

    This returns the songs of a specified album

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def album_songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'album_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" tags
    MINIMUM_API_VERSION=380001

    This returns the tags (Genres) based on the specified filter

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * exact
    * filter
    * offset
    * limit
"""
def tags(ampache_url, , exact, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tags',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" tag
    MINIMUM_API_VERSION=380001

    This returns a single tag based on UID

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
"""
def tag(ampache_url, ampache_api, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" tag_artists
    MINIMUM_API_VERSION=380001

    This returns the artists associated with the tag in question as defined by the UID

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def tag_artists(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_artists',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token
""" tag_albums

    MINIMUM_API_VERSION=380001

    This returns the albums associated with the tag in question

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def tag_albums(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_albums',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" tag_songs
    MINIMUM_API_VERSION=380001

    returns the songs for this tag

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def tag_songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" songs
    MINIMUM_API_VERSION=380001

    Returns songs based on the specified filter

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * exact
    * add
    * update
    * filter
    * offset
    * limit
"""
def songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'songs',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'add': add,
                                   'update': update,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" song
    MINIMUM_API_VERSION=380001

    returns a single song

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
"""
def song(ampache_url, ampache_api, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'song',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" url_to_song
    MINIMUM_API_VERSION=380001

    This takes a url and returns the song object in question

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * url
"""
def url_to_song(ampache_url, ampache_api, url):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'url_to_song',
                                   'auth': ampache_api,
                                   'url': url})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlists
    MINIMUM_API_VERSION=380001

    This returns playlists based on the specified filter

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * exact
    * add
    * update
    * filter
    * offset
    * limit
"""
def playlists(ampache_url, ampache_api, add, update, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlists',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'add': add,
                                   'update': update,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist
    MINIMUM_API_VERSION=380001

    This returns a single playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
"""
def playlist(ampache_url, ampache_api, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_songs
    MINIMUM_API_VERSION=380001

    This returns the songs for a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def playlist_songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_create
    MINIMUM_API_VERSION=380001

    This create a new playlist and return it

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * name
    * type
"""
def playlist_create(ampache_url, ampache_api, name, type):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_create',
                                   'auth': ampache_api,
                                   'name': name,
                                   'type': type})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_edit
    MINIMUM_API_VERSION=400001

    This modifies name and type of a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * name
    * type
    * filter
"""
def playlist_edit(ampache_url, ampache_api, name, type, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_edit',
                                   'auth': ampache_api,
                                   'name': name,
                                   'type': type,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_delete
    MINIMUM_API_VERSION=380001

    This deletes a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
"""
def playlist_delete(ampache_url, ampache_api, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_delete',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_add_song
    MINIMUM_API_VERSION=380001

    This adds a song to a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * song
    * filter
"""
def playlist_add_song(ampache_url, ampache_api, song, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_add_song',
                                   'auth': ampache_api,
                                   'song': song,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" playlist_remove_song
    MINIMUM_API_VERSION=380001
    CHANGED_IN_API_VERSION=400001

    This remove a song from a playlist. Previous versions required 'track' instead of 'song'.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * song
    * filter
"""
def playlist_remove_song(ampache_url, ampache_api, song, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_remove_song',
                                   'auth': ampache_api,
                                   'song': song,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" search_songs
    MINIMUM_API_VERSION=380001

    This searches the songs and returns... songs

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
    * offset
    * limit
"""
def search_songs(ampache_url, ampache_api, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'search_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" advanced_search
    MINIMUM_API_VERSION=380001

    Perform an advanced search given passed rules

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    //FIXME what are the rules on this?
    * type
    * offset
    * limit'
"""
def advanced_search(ampache_url, ampache_api, type, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'advanced_search',
                                   'auth': ampache_api,
                                   'type': type,
                                   'offset': offset,
                                   'limit': limit})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" videos
    MINIMUM_API_VERSION=380001

    This returns video objects!

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * exact
    * filter
    * offset
    * limit

"""
def videos(ampache_url, ampache_api, exact, filter, offset, limit):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'videos',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" video
    MINIMUM_API_VERSION=380001

    This returns a single video

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter
"""
def video(ampache_url, ampache_api, filter):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'video',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" localplay
    MINIMUM_API_VERSION=380001

    This is for controlling localplay

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * command
"""
def localplay(ampache_url, ampache_api, command):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'localplay',
                                   'auth': ampache_api,
                                   'command': command})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" democratic
    MINIMUM_API_VERSION=380001

    This is for controlling democratic play

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * method
    * action
    * oid
"""
def democratic(ampache_url, ampache_api, method, action, oid):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'democratic',
                                   'auth': ampache_api,
                                   'methon': method,
                                   'action': action,
                                   'oid': oid})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" stats
    MINIMUM_API_VERSION=380001
    CHANGED_IN_API_VERSION=400001

    This gets library stats for different object types. When filter is null get some random items instead

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type = (string) 'song'|'album'|'artist'
    * filter = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|null
    * offset = (integer) //optional
    * limit = (integer) //optional
    * user_id = (integer) //optional
    * username = (string) //optional
"""
def stats(ampache_url, ampache_api, type, filter, offset, limit, user_id, username):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'stats',
                                   'auth': ampache_api,
                                   'type': type,
                                   'filter': filter,
                                   'offset': offset,
                                   'limit': limit,
                                   'user_id': user_id,
                                   'username': username})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" user
    MINIMUM_API_VERSION=380001

    This get an user public information

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username
"""
def user(ampache_url, ampache_api, username):
    if not ampache_url or not ampache_api or not username:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'user',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" followers
    MINIMUM_API_VERSION=380001

    This get an user followers

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username
"""
def followers(ampache_url, ampache_api, username):
    if not ampache_url or not ampache_api or not username:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'followers',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" following
    MINIMUM_API_VERSION=380001

    This get the user list followed by an user

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username
"""
def following(ampache_url, ampache_api, username):
    if not ampache_url or not ampache_api or not username:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'following',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" toggle_follow
    MINIMUM_API_VERSION=380001

    This follow/unfollow an user

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username
"""
def toggle_follow(ampache_url, ampache_api, username):
    if not ampache_url or not ampache_api or not username:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'toggle_follow',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" last_shouts
    MINIMUM_API_VERSION=380001

    This get the latest posted shouts

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username
    * limit
"""
def last_shouts(ampache_url, ampache_api, username, limit = ''):
    if not ampache_url or not ampache_api or not username:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'last_shouts',
                                   'auth': ampache_api,
                                   'username': username,
                                   'limit': limit})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" rate
    MINIMUM_API_VERSION=380001

    This rates a library item

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'song'|'album'|'artist'
    * id          = (integer) $object_id
    * rating      = (integer) 0|1|2|3|4|5
"""
def rate(ampache_url, ampache_api, type, id, rating):
    if not ampache_url or not ampache_api or not type or not id or not rating:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'rate',
                                   'auth': ampache_api,
                                   'type': type,
                                   'id': id,
                                   'rating': rating})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" flag
    MINIMUM_API_VERSION=400001

    This flags a library item as a favorite

    Setting flag to true (1) will set the flag
    Setting flag to false (0) will remove the flag

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'song'|'album'|'artist'
    * id          = (integer) $object_id
    * flag        = (bool) 0|1
"""
def flag(ampache_url, ampache_api, type, id, flag):
    if not ampache_url or not ampache_api or not type or not id or not flag:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'flag',
                                   'auth': ampache_api,
                                   'type': type,
                                   'id': id,
                                   'flag': flag})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" record_play
    MINIMUM_API_VERSION=400001

    Take a song_id and update the object_count and user_activity table with a play. This allows other sources to record play history to ampache

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id = (integer) $object_id
    * user = (integer) $user_id
    * client = (string) $agent (optional)
"""
def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI'):
    if not ampache_url or not ampache_api or not id or not user:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'record_play',
                                   'auth': ampache_api,
                                   'id': id,
                                   'user': user,
                                   'client': client})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" timeline
    MINIMUM_API_VERSION=380001

    This get a user timeline

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username = (string)
    * limit = (integer) // optional
    * since = (integer) UNIXTIME() //optional
"""
def timeline(ampache_url, ampache_api, username, limit = '', since = ''):
    if not ampache_url or not ampache_api or not user:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'timeline',
                                   'auth': ampache_api,
                                   'username': username,
                                   'limit': limit,
                                   'since': since})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" friends_timeline
    MINIMUM_API_VERSION=380001

    This get current user friends timeline

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * limit = (integer)
    * since = (integer) UNIXTIME()
"""
def friends_timeline(ampache_url, ampache_api, limit = '', since = ''):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'friends_timeline',
                                   'auth': ampache_api,
                                   'limit': limit,
                                   'since': since})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" catalog_action
    MINIMUM_API_VERSION=400001

    Kick off a catalog update or clean for the selected catalog

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * task = (string) 'add_to_catalog'|'clean_catalog'
    * catalog = (integer) $catalog_id
"""
def catalog_action(ampache_url, ampache_api, task, catalog):
    if not ampache_url or not ampache_api:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'catalog_action',
                                   'auth': ampache_api,
                                   'task': task,
                                   'catalog': catalog})
    full_url = ampache_url + '?' + data
    result = urllib.request.urlopen(full_url)
    ampache_response = result.read().decode('utf-8')
    tree = ET.fromstring(ampache_response)
    try:
        token = tree.find('success').text
    except AttributeError:
        token = False
    if token:
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token