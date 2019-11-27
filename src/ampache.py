#!/usr/bin/env python3

""" Copyright (C)2019
Lachlan de Waard <lachlan.00@gmail.com>
---------------------------------------
Ampache XML-Api 400002 for python3
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

import hashlib
import os
import requests
import time
import urllib.parse
import urllib.request

from xml.etree import ElementTree as ET

"""
----------------
HELPER FUNCTIONS
----------------
"""

""" encrypt_string

    This function can be used to encrype your apikey into the accepted format.

    INPUTS
    * ampache_api = (string) apikey
    * user        = (string) username
"""
def encrypt_string(ampache_api, user):
    key = hashlib.sha256(ampache_api.encode()).hexdigest()
    passphrase = user + key
    sha_signature = hashlib.sha256(passphrase.encode()).hexdigest()
    return sha_signature

"""
-------------
API FUNCTIONS
-------------
"""

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
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'ping',
                                   'auth': ampache_api})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read()
    result.close()
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        tree.find('session_expire').text
    except AttributeError:
        return False
    return ampache_api

""" handshake
    MINIMUM_API_VERSION=380001

    This is the function that handles verifying a new handshake
    Takes a timestamp, auth key, and username.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * timestamp   = (integer) UNIXTIME() //optional
    * version     = (string) //optional
"""
def handshake(ampache_url, ampache_api, timestamp=0, version='400001'):
    if timestamp == 0:
        timestamp = int(time.time())
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'handshake',
                                   'auth': ampache_api,
                                   'timestamp': str(timestamp),
                                   'version': version})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    result.close()
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'goodbye',
                                   'auth': ampache_api})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    result.close()
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * client      = (string) //optional
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
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * add         = //optional
    * update      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def get_indexes(ampache_url, ampache_api, type, filter = '', add = '', update = '', offset = 0, limit = 0):
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
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = //optional
    * add         = //optional
    * update      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * include     = //optional
"""
def artists(ampache_url, ampache_api, filter = '', add = None, update = None, offset = 0, limit = 0, include = None):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'artists',
            'auth': ampache_api,
            'filter': filter,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * include     = //optional
"""
def artist(ampache_url, ampache_api, filter, include = None):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'artist',
            'auth': ampache_api,
            'filter': filter,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      =
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artist_albums',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'artist_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * exact       = //optional
    * add         = //optional
    * update      = //optional
    * filter      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * include     = //optional
"""
def albums(ampache_url, ampache_api, exact = '', add = None, update = None, filter = '', offset = 0, limit = 0, include = None):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'albums',
            'auth': ampache_api,
            'exact': exact,
            'add': add,
            'update': update,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * include     = //optional
"""
def album(ampache_url, ampache_api, filter, include = None):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'album',
            'auth': ampache_api,
            'filter': filter,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = (string)
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'album_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = //optional
    * exact       = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def tags(ampache_url, ampache_api, filter = '', exact = '', offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tags',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
"""
def tag(ampache_url, ampache_api, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_artists',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_albums',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'tag_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * exact       = //optional
    * add         = //optional
    * update      = //optional
    * filter      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def songs(ampache_url, ampache_api, exact = '', add = '', update = '', filter = '', offset = 0, limit = 0):
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
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
"""
def song(ampache_url, ampache_api, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'song',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * url         = 
"""
def url_to_song(ampache_url, ampache_api, url):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'url_to_song',
                                   'auth': ampache_api,
                                   'url': url})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * exact       = //optional
    * filter      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def playlists(ampache_url, ampache_api, exact = '', filter = '', offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlists',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
"""
def playlist(ampache_url, ampache_api, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * name        = 
    * type        = 
"""
def playlist_create(ampache_url, ampache_api, name, type):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_create',
                                   'auth': ampache_api,
                                   'name': name,
                                   'type': type})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * name        = 
    * type        = 
    * filter      = 
"""
def playlist_edit(ampache_url, ampache_api, name, type, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_edit',
                                   'auth': ampache_api,
                                   'name': name,
                                   'type': type,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * filter      = (integer) $playlist_id
"""
def playlist_delete(ampache_url, ampache_api, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_delete',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * song        = (integer) $song_id
    * filter      = (integer) $playlist_id
"""
def playlist_add_song(ampache_url, ampache_api, song, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'playlist_add_song',
                                   'auth': ampache_api,
                                   'song': song,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * filter      = (integer) $playlist_id
    * song        = (integer) $song_id //optional
    * track       = (integer) $playlist_track number //optional
"""
def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False):
    ampache_url = ampache_url + '/server/xml.server.php'

    data = {'action': 'playlist_remove_song',
            'auth': ampache_api,
            'mode': mode,
            'filter': filter,
            'song': song,
            'track': track}
    if not song:
        data.pop('song')
    if not track:
        data.pop('track')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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

""" playlist_generate
    MINIMUM_API_VERSION=400001
    CHANGED_IN_API_VERSION=400002

    Get a list of song XML, indexes or id's based on some simple search criteria =
    'recent' will search for tracks played after 'Popular Threshold' days
    'forgotten' will search for tracks played before 'Popular Threshold' days
    'unplayed' added in 400002 for searching unplayed tracks

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * mode        = (string) 'recent', 'forgotten', 'unplayed', 'random' (default = 'random') //optional
    * filter      = (string) string LIKE matched to song title //optional
    * album       = (integer) $album_id //optional
    * artist      = (integer) $artist_id //optional
    * flag        = (integer) get flagged songs only 0, 1 (default = 0) //optional
    * format      = (string) 'song', 'index','id' (default = 'song') //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'playlist_generate',
            'auth': ampache_api,
            'mode': mode,
            'filter': filter,
            'album': album,
            'artist': artist,
            'flag': flag,
            'format': format,
            'offset': offset,
            'limit': limit}
    if not filter:
        data.pop('filter')
    if not album:
        data.pop('album')
    if not artist:
        data.pop('artist')
    if not flag:
        data.pop('flag')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'search_songs',
                                   'auth': ampache_api,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" advanced_search
    MINIMUM_API_VERSION=380001

    Perform an advanced search given passed rules
    the rules can occur multiple times and are joined by the operator item.
    
    Refer to the wiki for further information
    https://github.com/ampache/ampache/wiki/XML-methods

    rule_1
      * anywhere
      * title
      * favorite
      * name
      * playlist_name
      * album
      * artist
      * composer
      * comment
      * label
      * tag
      * album_tag
      * filename
      * placeformed
      * username
      * year
      * time
      * rating
      * myrating
      * artistrating
      * albumrating
      * played_times
      * bitrate
      * image height
      * image width
      * yearformed
      * played
      * myplayed
      * myplayedartist
      * myplayedalbum
      * last_play
      * added
      * updated
      * catalog
      * playlist
      * licensing
      * smartplaylist
      * metadata

    rule_1_operator
      * 0 contains / is greater than or equal to / before / is true / is / before (x) days ago
      * 1 does not contain / is less than or equal to / after / is false / is not / after (x) days ago
      * 2 starts with / is 
      * 3 ends with / is not 
      * 4 is / is greater than 
      * 5 is not / is less than 
      * 6 sounds like
      * 7 does not sound like

    rule_1_input
      * text
      * integer
      * etc

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input], [rule_2,rule_2_operator,rule_2_input], [etc]]
    * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
    * type        = (string)  //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
"""
def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'advanced_search',
            'auth': ampache_api,
            'operator': operator,
            'type': type,
            'offset': offset,
            'limit': limit}
    count = 0
    # inputs  [rule_1, rule_1_operator, rule_1_input]
    # example ['year', 2, 1999]
    for item in rules:
        count = count + 1
        data['rule_' + str(count)] = item[0]
        data['rule_' + str(count) + '_operator'] = item[1]
        data['rule_' + str(count) + '_input'] = item[2]
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * exact       = //optional
    * filter      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional

"""
def videos(ampache_url, ampache_api, exact = '', filter = '', offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'videos',
                                   'auth': ampache_api,
                                   'exact': exact,
                                   'filter': filter,
                                   'offset': str(offset),
                                   'limit': str(limit)})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * filter      = 
"""
def video(ampache_url, ampache_api, filter):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'video',
                                   'auth': ampache_api,
                                   'filter': filter})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * command     = 
"""
def localplay(ampache_url, ampache_api, command):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'localplay',
                                   'auth': ampache_api,
                                   'command': command})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * method      = 
    * action      = 
    * oid         = 
"""
def democratic(ampache_url, ampache_api, method, action, oid):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'democratic',
                                   'auth': ampache_api,
                                   'method': method,
                                   'action': action,
                                   'oid': oid})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * type        = (string) 'song'|'album'|'artist'
    * filter      = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|null
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * user_id     = (integer) //optional
    * username    = (string) //optional
"""
def stats(ampache_url, ampache_api, type, filter, username = None, user_id = None, offset = 0, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'stats',
            'auth': ampache_api,
            'type': type,
            'filter': filter,
            'offset': offset,
            'limit': limit,
            'user_id': user_id,
            'username': username}
    if not username:
        data.pop('username')
    if not user_id:
        data.pop('user_id')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * username    = 
"""
def user(ampache_url, ampache_api, username):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'user',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * username    = 
"""
def followers(ampache_url, ampache_api, username):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'followers',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * username    = 
"""
def following(ampache_url, ampache_api, username):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'following',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * username    = 
"""
def toggle_follow(ampache_url, ampache_api, username):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'toggle_follow',
                                   'auth': ampache_api,
                                   'username': username})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * username    = 
    * limit       = (integer) //optional
"""
def last_shouts(ampache_url, ampache_api, username, limit = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'last_shouts',
                                   'auth': ampache_api,
                                   'username': username,
                                   'limit': limit})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    if (rating < 0 or rating > 5) or not (type == 'song' or type == 'album' or type == 'artist'):
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'rate',
                                   'auth': ampache_api,
                                   'type': type,
                                   'id': id,
                                   'rating': rating})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    if not (type == 'song' or type == 'album' or type == 'artist'):
        return False
    if bool(flag):
        flag = 1
    else:
        flag = 0
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'flag',
                                   'auth': ampache_api,
                                   'type': type,
                                   'id': id,
                                   'flag': flag})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * id          = (integer) $object_id
    * user        = (integer) $user_id
    * client      = (string) $agent //optional
"""
def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI'):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'record_play',
                                   'auth': ampache_api,
                                   'id': id,
                                   'user': user,
                                   'client': client})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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
    * username    = (string)
    * limit       = (integer) //optional
    * since       = (integer) UNIXTIME() //optional
"""
def timeline(ampache_url, ampache_api, username, limit = 0, since = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'timeline',
                                   'auth': ampache_api,
                                   'username': username,
                                   'limit': limit,
                                   'since': since})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * limit       = (integer) //optional
    * since       = (integer) UNIXTIME() //optional
"""
def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'friends_timeline',
                                   'auth': ampache_api,
                                   'limit': limit,
                                   'since': since})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
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
    * task        = (string) 'add_to_catalog'|'clean_catalog'
    * catalog     = (integer) $catalog_id
"""
def catalog_action(ampache_url, ampache_api, task, catalog):
    if not (task == 'add_to_catalog' or task == 'clean_catalog') or not catalog > 0:
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'catalog_action',
                                   'auth': ampache_api,
                                   'task': task,
                                   'catalog': catalog})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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

""" update_from_tags
    MINIMUM_API_VERSION=400001

    updates a single album,artist,song from the tag data

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'artist'|'album'|'song'
    * id          = (integer) $artist_id, $album_id, $song_id
"""
def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'update_from_tags',
                                   'auth': ampache_api,
                                   'type': ampache_type,
                                   'id': ampache_id})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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

""" update_art
    MINIMUM_API_VERSION=400001

    updates a single album, artist, song looking for art files
    Doesn't overwrite existing art by default.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'artist'|'album'|'song'
    * id          = (integer) $artist_id, $album_id, $song_id
    * overwrite   = (boolean) 0|1 //optional
"""
def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite = False):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'update_art',
            'auth': ampache_api,
            'type': ampache_type,
            'id': ampache_id,
            'overwrite': overwrite}
    if not overwrite:
        data.pop('overwrite')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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

""" update_artist_info
    MINIMUM_API_VERSION=400001

    Update artist information and fetch similar artists from last.fm
    Make sure lastfm_api_key is set in your configuration file

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (integer) $artist_id
"""
def update_artist_info(ampache_url, ampache_api, id):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'update_artist_info',
                                   'auth': ampache_api,
                                   'id': id})
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
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

""" stream
    MINIMUM_API_VERSION=400001

    stream a song or podcast episode

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (string) $song_id / $podcast_episode_id
    * type        = (string) 'song'|'podcast'
    * destination = (string) full file path
"""
def stream(ampache_url, ampache_api, id, type, destination):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'stream',
                                   'auth': ampache_api,
                                   'id': id,
                                   'type': type})
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True

""" download
    MINIMUM_API_VERSION=400001

    download a song or podcast episode

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (string) $song_id / $podcast_episode_id
    * type        = (string) 'song'|'podcast'
    * destination = (string) full file path
    * format      = (string) 'mp3', 'ogg', etc. ('raw' / original by default)
"""
def download(ampache_url, ampache_api, id, type, destination, format = 'raw'):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'download',
                                   'auth': ampache_api,
                                   'id': id,
                                   'type': type,
                                   'format': format})
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True

""" get_art
    MINIMUM_API_VERSION=400001

    get the binary art for an item

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (string) $song_id / $podcast_episode_id
    * type        = (string) 'song', 'artist', 'album', 'playlist', 'search', 'podcast'
"""
def get_art(ampache_url, ampache_api, id, type):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'get_art',
                                   'auth': ampache_api,
                                   'id': id,
                                   'type': type})
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True

""" user_create
    MINIMUM_API_VERSION=400001

    Create a new user. (Requires the username, password and email.) @param array $input

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = (string) $username
    * password    = (string) hash('sha256', $password))
    * email       = (string) 'user@gmail.com'
    * fullname    = (string) //optional
    * disable     = (boolean) 0|1 //optional
"""
def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'user_create',
            'auth': ampache_api,
            'username': username,
            'password': password,
            'email': email,
            'fullname': fullname,
            'disable': disable}
    if not fullname:
        data.pop('fullname')
    if not disable:
        data.pop('disable')
    if not maxbitrate:
        data.pop('maxbitrate')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" user_update
    MINIMUM_API_VERSION=400001

    Update an existing user. @param array $input

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = (string) $username
    * password    = (string) hash('sha256', $password)) //optional
    * fullname    = (string) //optional
    * email       = (string) 'user@gmail.com' //optional
    * website     = (string) //optional
    * state       = (string) //optional
    * city        = (string) //optional
    * disable     = (boolean) 0|1 //optional
    * maxbitrate  = (string) //optional
"""
def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'stats',
            'auth': ampache_api,
            'username': username,
            'password': password,
            'fullname': fullname,
            'email': email,
            'website': website,
            'state': state,
            'city': city,
            'disable': disable,
            'maxbitrate': maxbitrate}
    if not password:
        data.pop('password')
    if not fullname:
        data.pop('fullname')
    if not email:
        data.pop('email')
    if not website:
        data.pop('website')
    if not state:
        data.pop('state')
    if not city:
        data.pop('city')
    if not disable:
        data.pop('disable')
    if not maxbitrate:
        data.pop('maxbitrate')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token

""" user_delete
    MINIMUM_API_VERSION=400001

    Delete an existing user. @param array $input

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = (string) $username
"""
def user_delete(ampache_url, ampache_api, username):
    ampache_url = ampache_url + '/server/xml.server.php'
    data = {'action': 'stats',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read().decode('utf-8')
    try:
        tree = ET.fromstring(ampache_response)
    except ET.ParseError:
        return False
    try:
        token = tree.tag
    except AttributeError:
        token = False
    if token:
        return tree
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    return token
