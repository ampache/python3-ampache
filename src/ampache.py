#!/usr/bin/env python3

"""
Copyright (C)2020 Ampache.org
---------------------------------------
Ampache XML-Api 400004 for python3
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
import json
import os
import requests
import time
import urllib.parse
import urllib.request

from xml.etree import ElementTree as ET

# used for printing results
AMPACHE_DEBUG = False

"""
----------------
HELPER FUNCTIONS
----------------
"""

""" set_debug

    This function can be used to enable/disable debugging messages

    INPUTS
    * bool = (boolean) Enable/disable debug messages
"""
def set_debug(mybool):
    global AMPACHE_DEBUG
    AMPACHE_DEBUG = mybool

""" write_xml

    This function can be used to write your xml responses to a file.

    INPUTS
    * xmlstr   = (xml) xml to write to file
    * filename = (string) path and filename (e.g. './ampache.xml')
"""
def write_xml(xmlstr, filename):
    if xmlstr:
        text_file = open(filename, "w")
        text_file.write(ET.tostring(xmlstr).decode())
        text_file.close()

""" write_json

    This function can be used to write your json responses to a file.

    INPUTS
    * json_data = (json) json to write to file
    * filename  = (string) path and filename (e.g. './ampache.json')
"""
def write_json(json_data, filename):
    if json_data:
        text_file = open(filename, "w")
        text_file.write(json.dumps(json_data))
        text_file.close()

""" encrypt_string

    This function can be used to encrypt your apikey into the accepted format.

    INPUTS
    * ampache_api = (string) apikey
    * user        = (string) username
"""
def encrypt_string(ampache_api, user):
    key = hashlib.sha256(ampache_api.encode()).hexdigest()
    passphrase = user + key
    sha_signature = hashlib.sha256(passphrase.encode()).hexdigest()
    return sha_signature

""" fetch_url

    This function is used to fetch the string results using urllib

    INPUTS
    * full_url = (string) url to fetch
"""
def fetch_url(full_url, api_format, method):
    try:
        result = urllib.request.urlopen(full_url)
    except urllib.error.URLError:
        return False
    except urllib.error.HTTPError:
        return False
    ampache_response = result.read()
    result.close()
    if AMPACHE_DEBUG:
        url_response = ampache_response.decode('utf-8')
        print(url_response)
        print(full_url)
        text_file = open(api_format + "-responses/" + method + "." + api_format, "w")
        text_file.write(url_response)
        text_file.close()
    return ampache_response

"""
-------------
API FUNCTIONS
-------------
"""

""" handshake
    MINIMUM_API_VERSION=380001

    This is the function that handles verifying a new handshake
    Takes a timestamp, auth key, and username.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * user        = (string) //optional
    * timestamp   = (integer) UNIXTIME() //optional
    * version     = (string) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def handshake(ampache_url, ampache_api, user = False, timestamp = False, version = '400004', api_format = 'xml'):
    if timestamp == 0:
        timestamp = int(time.time())
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'handshake',
            'auth': ampache_api,
            'user': user,
            'timestamp': str(timestamp),
            'version': version}
    if not user:
        data.pop('user')
    if not timestamp:
        data.pop('timestamp')
    if not version:
        data.pop('version')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'handshake')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        if 'auth' in json_data:
            return json_data['auth']
        else:
            return False
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        try:
            token = tree.find('auth').text
        except AttributeError:
            token = False
        return token

""" ping
    MINIMUM_API_VERSION=380001

    This can be called without being authenticated, it is useful for determining if what the status
    of the server is, and what version it is running/compatible with

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string) session auth key //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def ping(ampache_url, ampache_api, api_format = 'xml'):
    """ Request Ampache ping auth """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'ping',
            'auth': ampache_api}
    if not ampache_api:
        data.pop('auth')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'ping')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        if 'session_expire' in json_data:
            return ampache_api
        else:
            return False
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        try:
            tree.find('session_expire').text
        except AttributeError:
            return False
        return ampache_api

""" goodbye
    MINIMUM_API_VERSION=400001

    Destroy session for ampache_api auth key.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * api_format  = (string) 'xml'|'json' //optional
"""
def goodbye(ampache_url, ampache_api, api_format = 'xml'):
    """ Request Ampache destroy an api session """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'goodbye',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'goodbye')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" url_to_song
    MINIMUM_API_VERSION=380001

    This takes a url and returns the song object in question

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * url         = (string) Full Ampache URL from server, translates back into a song XML
    * api_format  = (string) 'xml'|'json' //optional
"""
def url_to_song(ampache_url, ampache_api, url, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'url_to_song',
            'auth': ampache_api,
            'url': url}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'url_to_song')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * api_format  = (string) 'xml'|'json' //optional
"""
def get_indexes(ampache_url, ampache_api, type, filter = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'get_indexes',
            'auth': ampache_api,
            'type': type,
            'filter': filter,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter:
        data.pop('filter')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'get_indexes')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" artists
    MINIMUM_API_VERSION=380001

    This takes a collection of inputs and returns artist objects.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = //optional
    * add         = //optional
    * update      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * include     = //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def artists(ampache_url, ampache_api, filter = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artists',
            'auth': ampache_api,
            'filter': filter,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not filter:
        data.pop('filter')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artists')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" artist
    MINIMUM_API_VERSION=380001

    This returns a single artist based on the UID of said artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $artist_id
    * include     = //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def artist(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist',
            'auth': ampache_api,
            'filter': filter,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" artist_albums
    MINIMUM_API_VERSION=380001

    This returns the albums of an artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      =
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def artist_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist_albums',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist_albums')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" artist_songs
    MINIMUM_API_VERSION=380001

    This returns the songs of the specified artist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def artist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist_songs',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist_songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" albums
    MINIMUM_API_VERSION=380001

    This returns albums based on the provided search filters

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = //optional
    * exact       = //optional
    * add         = //optional
    * update      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * include     = //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def albums(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, include = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'albums',
            'auth': ampache_api,
            'filter': filter,
            'exact': exact,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not filter:
        data.pop('filter')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'albums')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" album
    MINIMUM_API_VERSION=380001

    This returns a single album based on the UID provided

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $album_id
    * include     = //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def album(ampache_url, ampache_api, filter, include = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'album',
            'auth': ampache_api,
            'filter': filter,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'album')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" album_songs
    MINIMUM_API_VERSION=380001

    This returns the songs of a specified album

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (string)
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def album_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'album_songs',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'album_songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * api_format  = (string) 'xml'|'json' //optional
"""
def tags(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'tags',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'tags')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" tag
    MINIMUM_API_VERSION=380001

    This returns a single tag based on UID

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $genre_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def tag(ampache_url, ampache_api, filter, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'tag',
            'auth': ampache_api,
            'filter': filter}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'tag')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" tag_artists
    MINIMUM_API_VERSION=380001

    This returns the artists associated with the tag in question as defined by the UID

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def tag_artists(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'tag_artists',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'tag_artists')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" tag_albums

    MINIMUM_API_VERSION=380001

    This returns the albums associated with the tag in question

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def tag_albums(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'tag_albums',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'tag_albums')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" tag_songs
    MINIMUM_API_VERSION=380001

    returns the songs for this tag

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def tag_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'tag_songs',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'tag_songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" songs
    MINIMUM_API_VERSION=380001

    Returns songs based on the specified filter

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = //optional
    * exact       = //optional
    * add         = //optional
    * update      = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def songs(ampache_url, ampache_api, filter = False, exact = False, add = False, update = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'songs',
            'auth': ampache_api,
            'exact': exact,
            'add': add,
            'update': update,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" song
    MINIMUM_API_VERSION=380001

    returns a single song

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def song(ampache_url, ampache_api, filter, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'song',
            'auth': ampache_api,
            'filter': filter}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'song')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlists
    MINIMUM_API_VERSION=380001

    This returns playlists based on the specified filter

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = //optional
    * exact       = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlists(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlists',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlists')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlist
    MINIMUM_API_VERSION=380001

    This returns a single playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist(ampache_url, ampache_api, filter, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist',
            'auth': ampache_api,
            'filter': filter}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlist_songs
    MINIMUM_API_VERSION=380001

    This returns the songs for a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_songs',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlist_create
    MINIMUM_API_VERSION=380001

    This create a new playlist and return it

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * name        = (string)
    * type        = (string)
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_create(ampache_url, ampache_api, name, type, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_create',
            'auth': ampache_api,
            'name': name,
            'type': type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_create')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        try:
            token = tree.find('playlist').text
        except AttributeError:
            token = False
        if token:
            return tree
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
    * filter      = (integer)
    * name        = 
    * type        = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_edit(ampache_url, ampache_api, filter, name = False, type = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_edit',
            'auth': ampache_api,
            'filter': filter,
            'name': name,
            'type': type}
    if not name:
        data.pop('name')
    if not type:
        data.pop('type')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_edit')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlist_delete
    MINIMUM_API_VERSION=380001

    This deletes a playlist

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $playlist_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_delete(ampache_url, ampache_api, filter, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_delete',
            'auth': ampache_api,
            'filter': filter}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_delete')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" playlist_add_song
    MINIMUM_API_VERSION=380001
    CHANGED_IN_API_VERSION=400003

    This adds a song to a playlist.
    Added duplicate checks in 400003

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $playlist_id
    * song        = (integer) $song_id
    * check       = (boolean|integer) (True,False | 0|1) Check for duplicates //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_add_song(ampache_url, ampache_api, filter, song, check = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(check):
        check = 1
    else:
        check = 0
    data = {'action': 'playlist_add_song',
            'auth': ampache_api,
            'song': song,
            'filter': filter,
            'check': check}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_add_song')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_remove_song(ampache_url, ampache_api, filter, song = False, track = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'

    data = {'action': 'playlist_remove_song',
            'auth': ampache_api,
            'filter': filter,
            'song': song,
            'track': track}
    if not song:
        data.pop('song')
    if not track:
        data.pop('track')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_remove_song')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * api_format  = (string) 'xml'|'json' //optional
"""
def playlist_generate(ampache_url, ampache_api, mode = 'random', filter = False, album = False, artist = False, flag = False, format = 'song', offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
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
    ampache_response = fetch_url(full_url, api_format, 'playlist_generate')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" search_songs
    MINIMUM_API_VERSION=380001

    This searches the songs and returns... songs

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = 
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def search_songs(ampache_url, ampache_api, filter, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'search_songs',
            'auth': ampache_api,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'search_songs')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    
    rule_1_subtype
      * integer code of metadata search items
      * NEEDS EXTENSION IN PYTHON + API

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input], [rule_2,rule_2_operator,rule_2_input], [etc]]
    * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
    * type        = (string)  //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def advanced_search(ampache_url, ampache_api, rules, operator = 'and', type = 'song', offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
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
        if item[0] == 'metadata':
            data['rule_' + str(count) + '_subtype'] = item[3]
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'advanced_search')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" videos
    MINIMUM_API_VERSION=380001

    This returns video objects!

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = //optional
    * exact       = //optional
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional

"""
def videos(ampache_url, ampache_api, filter = False, exact = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'videos',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'videos')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" video
    MINIMUM_API_VERSION=380001

    This returns a single video

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * filter      = (integer) $video_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def video(ampache_url, ampache_api, filter, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'video',
            'auth': ampache_api,
            'filter': filter}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'video')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" localplay
    MINIMUM_API_VERSION=380001

    This is for controlling localplay

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * command     = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def localplay(ampache_url, ampache_api, command, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'localplay',
            'auth': ampache_api,
            'command': command}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'localplay')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" democratic
    MINIMUM_API_VERSION=380001

    This is for controlling democratic play

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * method      = 
    * action      = 
    * oid         = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def democratic(ampache_url, ampache_api, method, action, oid, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'democratic',
            'auth': ampache_api,
            'method': method,
            'action': action,
            'oid': oid}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'democratic')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" stats
    MINIMUM_API_VERSION=380001
    CHANGED_IN_API_VERSION=400001

    This gets library stats for different object types. When filter is null get some random items instead

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'song'|'album'|'artist'
    * filter      = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|'random'
    * offset      = (integer) //optional
    * limit       = (integer) //optional
    * user_id     = (integer) //optional
    * username    = (string) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def stats(ampache_url, ampache_api, type, filter = 'random', username = False, user_id = False, offset = 0, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
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
    ampache_response = fetch_url(full_url, api_format, 'stats')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" user
    MINIMUM_API_VERSION=380001

    This get an user public information

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def user(ampache_url, ampache_api, username, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'user',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" followers
    MINIMUM_API_VERSION=380001

    This get an user followers

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def followers(ampache_url, ampache_api, username, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'followers',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'followers')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" following
    MINIMUM_API_VERSION=380001

    This get the user list followed by an user

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def following(ampache_url, ampache_api, username, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'following',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'following')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" toggle_follow
    MINIMUM_API_VERSION=380001

    This follow/unfollow an user

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = 
    * api_format  = (string) 'xml'|'json' //optional
"""
def toggle_follow(ampache_url, ampache_api, username, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'toggle_follow',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'toggle_follow')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" last_shouts
    MINIMUM_API_VERSION=380001

    This get the latest posted shouts

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = 
    * limit       = (integer) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def last_shouts(ampache_url, ampache_api, username, limit = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'last_shouts',
            'auth': ampache_api,
            'username': username,
            'limit': limit}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'last_shouts')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" rate
    MINIMUM_API_VERSION=380001

    This rates a library item

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'song'|'album'|'artist'
    * id          = (integer) $object_id
    * rating      = (integer) 0|1|2|3|4|5
    * api_format  = (string) 'xml'|'json' //optional
"""
def rate(ampache_url, ampache_api, type, id, rating, api_format = 'xml'):
    if (rating < 0 or rating > 5) or not (type == 'song' or type == 'album' or type == 'artist'):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'rate',
            'auth': ampache_api,
            'type': type,
            'id': id,
            'rating': rating}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'rate')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * flag        = (boolean|integer) (True,False | 0|1)
    * api_format  = (string) 'xml'|'json' //optional
"""
def flag(ampache_url, ampache_api, type, id, flag, api_format = 'xml'):
    if bool(flag):
        flag = 1
    else:
        flag = 0
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'flag',
            'auth': ampache_api,
            'type': type,
            'id': id,
            'flag': flag}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'flag')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" record_play
    MINIMUM_API_VERSION=400001

    Take a song_id and update the object_count and user_activity table with a play. This allows other sources to record play history to ampache

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (integer) $object_id
    * user        = (integer) $user_id
    * client      = (string) $agent //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def record_play(ampache_url, ampache_api, id, user, client = 'AmpacheAPI', api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'record_play',
            'auth': ampache_api,
            'id': id,
            'user': user,
            'client': client}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'record_play')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * api_format  = (string) 'xml'|'json' //optional
"""
def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle = False, MBartist = False, MBalbum = False, time = False, client = 'AmpacheAPI', api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'scrobble',
            'auth': ampache_api,
            'client': client,
            'date': str(time),
            'song': title,
            'album': album,
            'artist': artist,
            'songmbid': MBtitle,
            'albummbid': MBalbum,
            'artistmdib': MBartist}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'scrobble')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" timeline
    MINIMUM_API_VERSION=380001

    This get a user timeline

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = (string)
    * limit       = (integer) //optional
    * since       = (integer) UNIXTIME() //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def timeline(ampache_url, ampache_api, username, limit = 0, since = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'timeline',
            'auth': ampache_api,
            'username': username,
            'limit': limit,
            'since': since}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'timeline')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" friends_timeline
    MINIMUM_API_VERSION=380001

    This get current user friends timeline

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * limit       = (integer) //optional
    * since       = (integer) UNIXTIME() //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def friends_timeline(ampache_url, ampache_api, limit = 0, since = 0, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'friends_timeline',
            'auth': ampache_api,
            'limit': limit,
            'since': since}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'friends_timeline')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" catalog_action
    MINIMUM_API_VERSION=400001

    Kick off a catalog update or clean for the selected catalog

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * task        = (string) 'add_to_catalog'|'clean_catalog'
    * catalog     = (integer) $catalog_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def catalog_action(ampache_url, ampache_api, task, catalog, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'catalog_action',
            'auth': ampache_api,
            'task': task,
            'catalog': catalog}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'catalog_action')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" update_from_tags
    MINIMUM_API_VERSION=400001

    updates a single album,artist,song from the tag data

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'artist'|'album'|'song'
    * id          = (integer) $artist_id, $album_id, $song_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def update_from_tags(ampache_url, ampache_api, ampache_type, ampache_id, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'update_from_tags',
            'auth': ampache_api,
            'type': ampache_type,
            'id': ampache_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'update_from_tags')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" update_art
    MINIMUM_API_VERSION=400001

    updates a single album, artist, song looking for art files
    Doesn't overwrite existing art by default.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * type        = (string) 'artist'|'album'|'song'
    * id          = (integer) $artist_id, $album_id, $song_id
    * overwrite   = (boolean|integer) (True,False | 0|1) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def update_art(ampache_url, ampache_api, ampache_type, ampache_id, overwrite = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(overwrite):
        overwrite = 1
    else:
        overwrite = 0
    data = {'action': 'update_art',
            'auth': ampache_api,
            'type': ampache_type,
            'id': ampache_id,
            'overwrite': overwrite}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'update_art')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" update_artist_info
    MINIMUM_API_VERSION=400001

    Update artist information and fetch similar artists from last.fm
    Make sure lastfm_api_key is set in your configuration file

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (integer) $artist_id
    * api_format  = (string) 'xml'|'json' //optional
"""
def update_artist_info(ampache_url, ampache_api, id, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'update_artist_info',
            'auth': ampache_api,
            'id': id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'update_artist_info')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" stream
    MINIMUM_API_VERSION=400001

    stream a song or podcast episode

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * id          = (string) $song_id / $podcast_episode_id
    * type        = (string) 'song'|'podcast'
    * destination = (string) full file path
    * api_format  = (string) 'xml'|'json' //optional
"""
def stream(ampache_url, ampache_api, id, type, destination, api_format = 'xml'):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'stream',
            'auth': ampache_api,
            'id': id,
            'type': type}
    data = urllib.parse.urlencode(data)
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
    * format      = (string) 'mp3', 'ogg', etc. ('raw' / original by default) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def download(ampache_url, ampache_api, id, type, destination, format = 'raw', api_format = 'xml'):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'download',
            'auth': ampache_api,
            'id': id,
            'type': type,
            'format': format}
    data = urllib.parse.urlencode(data)
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
    * api_format  = (string) 'xml'|'json' //optional
"""
def get_art(ampache_url, ampache_api, id, type, api_format = 'xml'):
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'get_art',
            'auth': ampache_api,
            'id': id,
            'type': type}
    data = urllib.parse.urlencode(data)
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
    * disable     = (boolean|integer) (True,False | 0|1) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def user_create(ampache_url, ampache_api, username, password, email, fullname = False, disable = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(disable):
        disable = 1
    else:
        disable = 0
    data = {'action': 'user_create',
            'auth': ampache_api,
            'username': username,
            'password': password,
            'email': email,
            'fullname': fullname,
            'disable': disable}
    if not fullname:
        data.pop('fullname')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user_create')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

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
    * disable     = (boolean|integer) (True,False | 0|1) //optional
    * maxbitrate  = (string) //optional
    * api_format  = (string) 'xml'|'json' //optional
"""
def user_update(ampache_url, ampache_api, username, password = False, fullname = False, email = False, website = False, state = False, city = False, disable = False, maxbitrate = False, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(disable):
        disable = 1
    else:
        disable = 0
    data = {'action': 'user_update',
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
    if not maxbitrate:
        data.pop('maxbitrate')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user_update')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" user_delete
    MINIMUM_API_VERSION=400001

    Delete an existing user. @param array $input

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * username    = (string) $username
    * api_format  = (string) 'xml'|'json' //optional
"""
def user_delete(ampache_url, ampache_api, username, api_format = 'xml'):
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'user_delete',
            'auth': ampache_api,
            'username': username}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user_delete')
    if not ampache_response:
        return False
    # json format
    if api_format  == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ET.fromstring(ampache_response.decode('utf-8'))
        except ET.ParseError:
            return False
        return tree

""" localplay
    MINIMUM_API_VERSION=380001

    NOT IMPLEMENTED
"""
def localplay(ampache_url, ampache_api, username, api_format = 'xml'):
    return False

""" democratic
    MINIMUM_API_VERSION=380001

    NOT IMPLEMENTED
"""
def democratic(ampache_url, ampache_api, username, api_format = 'xml'):
    return False
