#!/usr/bin/env python3


"""
Copyright (C)2020 Ampache.org
-------------------------------------------
Ampache XML and JSON Api 420000 for python3
-------------------------------------------

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

from xml.etree import ElementTree

# used for printing results
AMPACHE_DEBUG = False


"""
----------------
HELPER FUNCTIONS
----------------
"""


def set_debug(mybool: bool):
    """ set_debug

        This function can be used to enable/disable debugging messages

        INPUTS
        * bool = (boolean) Enable/disable debug messages
    """
    global AMPACHE_DEBUG
    AMPACHE_DEBUG = mybool


def get_id_list(data, attribute: str, data_format: str = 'xml'):
    """ get_id_list

        return a list of id's from the data you've got from the api

        INPUTS
        * data        = (mixed) XML or JSON from the API
        * attribute   = (string) attribute you are searching for
        * data_format = (string) 'xml','json'
    """
    id_list = list()
    if data_format == 'xml':
        for child in data:
            if child.tag == attribute:
                id_list.append(child.attrib['id'])
    else:
        try:
            for data_object in data[attribute]:
                id_list.append(data_object['id'])
        except TypeError:
            for data_object in data:
                id_list.append(data_object[0])
    return id_list


def write_xml(xmlstr, filename: str):
    """ write_xml

        This function can be used to write your xml responses to a file.

        INPUTS
        * xmlstr   = (xml) xml to write to file
        * filename = (string) path and filename (e.g. './ampache.xml')
    """
    if xmlstr:
        text_file = open(filename, "w")
        text_file.write(ElementTree.tostring(xmlstr).decode())
        text_file.close()


def write_json(json_data: str, filename: str):
    """ write_json

        This function can be used to write your json responses to a file.

        INPUTS
        * json_data = (json) json to write to file
        * filename  = (string) path and filename (e.g. './ampache.json')
    """
    if json_data:
        text_file = open(filename, "w")
        text_file.write(json.dumps(json_data))
        text_file.close()


def encrypt_string(api_key: str, username: str):
    """ encrypt_string

        This function can be used to encrypt your apikey into the accepted format.

        INPUTS
        * api_key = (string) unencrypted apikey
        * user    = (string) username
    """
    key = hashlib.sha256(api_key.encode()).hexdigest()
    passphrase = username + key
    sha_signature = hashlib.sha256(passphrase.encode()).hexdigest()
    return sha_signature


def fetch_url(full_url: str, api_format: str, method: str):
    """ fetch_url

        This function is used to fetch the string results using urllib

        INPUTS
        * full_url   = (string) url to fetch
        * api_format = (string) 'xml'|'json'
        * method     = (string)
    """
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
        try:
            text_file = open("docs/" + api_format + "-responses/" + method + "." + api_format, "w", encoding="utf-8")
            text_file.write(url_response)
            text_file.close()
        except FileNotFoundError:
            pass
    return ampache_response


"""
-------------
API FUNCTIONS
-------------
"""


def handshake(ampache_url: str, ampache_api: str, ampache_user: str = False,
              timestamp: int = 0, version: str = '5.0.0', api_format: str = 'xml'):
    """ handshake
        MINIMUM_API_VERSION=380001

        This is the function that handles verifying a new handshake
        Takes a timestamp, auth key, and username.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) encrypted apikey
        * user        = (string) username //optional
        * timestamp   = (integer) UNIXTIME() //optional
        * version     = (string) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    if timestamp == 0:
        timestamp = int(time.time())
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'handshake',
            'auth': ampache_api,
            'user': ampache_user,
            'timestamp': str(timestamp),
            'version': version}
    if not ampache_user:
        data.pop('user')
    if not timestamp or not ampache_user:
        data.pop('timestamp')
    if not version:
        data.pop('version')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'handshake')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        if 'auth' in json_data:
            return json_data['auth']
        else:
            return False
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        try:
            token = tree.find('auth').text
        except AttributeError:
            token = False
        return token


def ping(ampache_url: str, ampache_api: str = False, api_format: str = 'xml'):
    """ ping
        MINIMUM_API_VERSION=380001

        This can be called without being authenticated, it is useful for determining if what the status
        of the server is, and what version it is running/compatible with

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        if 'session_expire' in json_data:
            return ampache_api
        else:
            return False
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        try:
            tree.find('session_expire').text
        except AttributeError:
            return False
        return ampache_api


def goodbye(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ goodbye
        MINIMUM_API_VERSION=400001

        Destroy session for ampache_api auth key.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'goodbye',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'goodbye')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def url_to_song(ampache_url: str, ampache_api: str, url, api_format: str = 'xml'):
    """ url_to_song
        MINIMUM_API_VERSION=380001

        This takes a url and returns the song object in question

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * url         = (string) Full Ampache URL from server, translates back into a song XML
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def get_similar(ampache_url: str, ampache_api: str, object_type, filter_id: int,
                offset=0, limit=0, api_format: str = 'xml'):
    """ get_similar
        MINIMUM_API_VERSION=420000

        Return similar artist id's or similar song ids compared to the input filter

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'song'|'album'|'artist'|'playlist'
        * filter_id   = (integer) $artist_id or song_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'get_similar',
            'auth': ampache_api,
            'type': object_type,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'get_similar')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def get_indexes(ampache_url: str, ampache_api: str, object_type,
                filter_str: str = False, exact: int = False, add: int = False, update: int = False,
                include=False, offset=0, limit=0, api_format: str = 'xml'):
    """ get_indexes
        MINIMUM_API_VERSION=400001

        This takes a collection of inputs and returns ID + name for the object type

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'song'|'album'|'artist'|'album_artist'|'playlist'
        * filter_str  = (string) search the name of the object_type //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * add         = (integer) UNIXTIME() //optional
        * update      = (integer) UNIXTIME() //optional
        * include     = (integer) 0,1 include songs if available for that object //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(include):
        include = 1
    else:
        include = 0
    data = {'action': 'get_indexes',
            'auth': ampache_api,
            'type': object_type,
            'filter': filter_str,
            'exact': exact,
            'add': add,
            'update': update,
            'include': include,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'get_indexes')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def artists(ampache_url: str, ampache_api: str, filter_str: str = False,
            add: int = False, update: int = False, offset=0, limit=0, include=False, api_format: str = 'xml'):
    """ artists
        MINIMUM_API_VERSION=380001

        This takes a collection of inputs and returns artist objects.

        INPUTS
        * ampache_url  = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api  = (string) session 'auth' key
        * filter_str   = (string) search the name of an artist //optional
        * add          = (integer) UNIXTIME() //optional
        * update       = (integer) UNIXTIME() //optional
        * offset       = (integer) //optional
        * limit        = (integer) //optional
        * include      = (string) 'albums', 'songs' //optional
        * album_artist = (boolean) 0,1 if true filter for album artists only //optional
        * api_format   = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artists',
            'auth': ampache_api,
            'filter': filter_str,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not filter_str:
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def artist(ampache_url: str, ampache_api: str, filter_id: int, include=False, api_format: str = 'xml'):
    """ artist
        MINIMUM_API_VERSION=380001

        This returns a single artist based on the UID of said artist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $artist_id
        * include     = (string) 'albums', 'songs' //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist',
            'auth': ampache_api,
            'filter': filter_id,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def artist_albums(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ artist_albums
        MINIMUM_API_VERSION=380001

        This returns the albums of an artist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $artist_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist_albums',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist_albums')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def artist_songs(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ artist_songs
        MINIMUM_API_VERSION=380001

        This returns the songs of the specified artist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $artist_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'artist_songs',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'artist_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def albums(ampache_url: str, ampache_api: str, filter_str: str = False,
           exact=False, add: int = False, update: int = False, offset=0, limit=0,
           include=False, api_format: str = 'xml'):
    """ albums
        MINIMUM_API_VERSION=380001

        This returns albums based on the provided search filters

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of an album //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * add         = (integer) UNIXTIME() //optional
        * update      = (integer) UNIXTIME() //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * include     = (string) 'songs' //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'albums',
            'auth': ampache_api,
            'filter': filter_str,
            'exact': exact,
            'add': add,
            'update': update,
            'offset': str(offset),
            'limit': str(limit),
            'include': include}
    if not filter_str:
        data.pop('filter_str')
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def album(ampache_url: str, ampache_api: str, filter_id: int, include=False, api_format: str = 'xml'):
    """ album
        MINIMUM_API_VERSION=380001

        This returns a single album based on the UID provided

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $album_id
        * include     = (string) 'songs' //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'album',
            'auth': ampache_api,
            'filter': filter_id,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    print(full_url)
    ampache_response = fetch_url(full_url, api_format, 'album')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def album_songs(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ album_songs
        MINIMUM_API_VERSION=380001

        This returns the songs of a specified album

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $album_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'album_songs',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'album_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def genres(ampache_url: str, ampache_api: str, filter_str: str = False,
           exact: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ genres
        MINIMUM_API_VERSION=380001

        This returns the genres (Tags) based on the specified filter

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a genre //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'genres',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'genres')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def genre(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ genre
        MINIMUM_API_VERSION=380001

        This returns a single genre based on UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $genre_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'genre',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'genre')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def genre_artists(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ genre_artists
        MINIMUM_API_VERSION=380001

        This returns the artists associated with the genre in question as defined by the UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $genre_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'genre_artists',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'genre_artists')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def genre_albums(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ genre_albums
        MINIMUM_API_VERSION=380001

        This returns the albums associated with the genre in question

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $genre_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'genre_albums',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'genre_albums')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def genre_songs(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ genre_songs
        MINIMUM_API_VERSION=380001

        returns the songs for this genre

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $genre_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'genre_songs',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'genre_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def songs(ampache_url: str, ampache_api: str, filter_str: str = False, exact: int = False,
          add: int = False, update: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ songs
        MINIMUM_API_VERSION=380001

        Returns songs based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a song //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * add         = (integer) UNIXTIME() //optional
        * update      = (integer) UNIXTIME() //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'songs',
            'auth': ampache_api,
            'exact': exact,
            'add': add,
            'update': update,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def song(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ song
        MINIMUM_API_VERSION=380001

        returns a single song

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $song_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'song',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'song')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def song_delete(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ song_delete
        MINIMUM_API_VERSION=5.0.0

        Delete an existing song.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (string) UID of song to delete
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'song_delete',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'song')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlists(ampache_url: str, ampache_api: str, filter_str: str = False,
              exact: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ playlists
        MINIMUM_API_VERSION=380001

        This returns playlists based on the specified filter

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a playlist //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlists',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlists')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ playlist
        MINIMUM_API_VERSION=380001

        This returns a single playlist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id  = (integer) $playlist_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_songs(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ playlist_songs
        MINIMUM_API_VERSION=380001

        This returns the songs for a playlist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $playlist_id
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_songs',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_create(ampache_url: str, ampache_api: str, name, object_type, api_format: str = 'xml'):
    """ playlist_create
        MINIMUM_API_VERSION=380001

        This create a new playlist and return it

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * name        = (string)
        * object_type = (string)
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_create',
            'auth': ampache_api,
            'name': name,
            'type': object_type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_create')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
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


def playlist_edit(ampache_url: str, ampache_api: str, filter_id: int, name=False,
                  object_type=False, api_format: str = 'xml'):
    """ playlist_edit
        MINIMUM_API_VERSION=400001

        This modifies name and type of a playlist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer)
        * name        = (string) playlist name //optional
        * object_type = (string) 'public'|'private'
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_edit',
            'auth': ampache_api,
            'filter': filter_id,
            'name': name,
            'type': object_type}
    if not name:
        data.pop('name')
    if not object_type:
        data.pop('type')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_edit')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_delete(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ playlist_delete
        MINIMUM_API_VERSION=380001

        This deletes a playlist

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $playlist_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_delete',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_delete')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_add_song(ampache_url: str, ampache_api: str, filter_id: int, song_id, check=False,
                      api_format: str = 'xml'):
    """ playlist_add_song
        MINIMUM_API_VERSION=380001
        CHANGED_IN_API_VERSION=400003

        This adds a song to a playlist.
        Added duplicate checks in 400003

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $playlist_id
        * song_id     = (integer) $song_id
        * check       = (boolean|integer) (True,False | 0|1) Check for duplicates //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(check):
        check = 1
    else:
        check = 0
    data = {'action': 'playlist_add_song',
            'auth': ampache_api,
            'song': song_id,
            'filter': filter_id,
            'check': check}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_add_song')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_remove_song(ampache_url: str, ampache_api: str, filter_id: int,
                         song_id=False, track=False, api_format: str = 'xml'):
    """ playlist_remove_song
        MINIMUM_API_VERSION=380001
        CHANGED_IN_API_VERSION=400001

        This removes a song from a playlist. Previous versions required 'track' instead of 'song'.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $playlist_id
        * song_id     = (integer) $song_id //optional
        * track       = (integer) $playlist_track number //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'

    data = {'action': 'playlist_remove_song',
            'auth': ampache_api,
            'filter': filter_id,
            'song': song_id,
            'track': track}
    if not song_id:
        data.pop('song')
    if not track:
        data.pop('track')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_remove_song')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def playlist_generate(ampache_url: str, ampache_api: str, mode='random',
                      filter_str: str = False, album_id=False, artist_id=False, flagged=False,
                      list_format='song', offset=0, limit=0, api_format: str = 'xml'):
    """ playlist_generate
        MINIMUM_API_VERSION=400001
        CHANGED_IN_API_VERSION=400002

        Get a list of song XML, indexes or id's based on some simple search criteria =
        'recent' will search for tracks played after 'Popular Threshold' days
        'forgotten' will search for tracks played before 'Popular Threshold' days
        'unplayed' added in 400002 for searching unplayed tracks

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * mode        = (string) 'recent', 'forgotten', 'unplayed', 'random' (default = 'random') //optional
        * filter_str  = (string) string LIKE matched to song title //optional
        * album_id    = (integer) $album_id //optional
        * artist_id   = (integer) $artist_id //optional
        * flagged     = (integer) get flagged songs only 0, 1 (default=0) //optional
        * list_format = (string) 'song', 'index','id' (default = 'song') //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'playlist_generate',
            'auth': ampache_api,
            'mode': mode,
            'filter': filter_str,
            'album': album_id,
            'artist': artist_id,
            'flag': flagged,
            'format': list_format,
            'offset': offset,
            'limit': limit}
    if not filter_str:
        data.pop('filter')
    if not album_id:
        data.pop('album')
    if not artist_id:
        data.pop('artist')
    if not flagged:
        data.pop('flag')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'playlist_generate')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def shares(ampache_url: str, ampache_api: str, filter_str: str = False,
           exact: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ shares
        MINIMUM_API_VERSION=420000

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a share //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'shares',
            'auth': ampache_api,
            'filter': filter_str,
            'exact': exact,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'shares')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def share(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ share
        MINIMUM_API_VERSION=420000

        Return shares by UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of Share
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'share',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'share')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def share_create(ampache_url: str, ampache_api: str, filter_id: int, object_type,
                 description=False, expires=False, api_format: str = 'xml'):
    """ share_create
        MINIMUM_API_VERSION=420000

        Create a public url that can be used by anyone to stream media.
        Takes the file id with optional description and expires parameters.

       INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $object_id
        * object_type = (string) object_type ('song', 'album', 'artist')
        * description = (string) description (will be filled for you if empty) //optional
        * expires     = (integer) days to keep active //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'share_create',
            'auth': ampache_api,
            'filter': filter_id,
            'type': object_type,
            'description': description,
            'expires': expires}
    if not description:
        data.pop('description')
    if not expires:
        data.pop('expires')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'share_create')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        try:
            token = tree.find('share').text
        except AttributeError:
            token = False
        if token:
            return tree
        try:
            token = tree.find('error').text
        except AttributeError:
            token = False
        return token


def share_edit(ampache_url: str, ampache_api: str, filter_id: int, can_stream=False, can_download=False,
               expires=False, description=False, api_format: str = 'xml'):
    """ share_edit
        MINIMUM_API_VERSION=420000

        Update the description and/or expiration date for an existing share.
        Takes the share id to update with optional description and expires parameters.

        INPUT
        * ampache_url  = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api  = (string) session 'auth' key
        * filter_id    = (integer) UID of Share
        * can_stream   = (boolean) 0,1 //optional
        * can_download = (boolean) 0,1 //optional
        * expires      = (integer) number of whole days before expiry //optional
        * description  = (string) update description //optional
        * api_format   = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'share_edit',
            'auth': ampache_api,
            'filter': filter_id,
            'stream': can_stream,
            'download': can_download,
            'expires': expires,
            'description': description}
    if not can_stream:
        data.pop('stream')
    if not can_download:
        data.pop('download')
    if not expires:
        data.pop('expires')
    if not description:
        data.pop('description')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'share_edit')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def share_delete(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ share_delete
        MINIMUM_API_VERSION=420000

        Delete an existing share.

        INPUT
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of Share to delete
        * api_format  = (string) 'xml'|'json' //optional
     """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'share_delete',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'share_delete')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def catalogs(ampache_url: str, ampache_api: str, filter_str: str = False, offset=0, limit=0, api_format: str = 'xml'):
    """ catalogs
        MINIMUM_API_VERSION=420000

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a catalog //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'catalogs',
            'auth': ampache_api,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'catalogs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def catalog(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ catalog
        MINIMUM_API_VERSION=420000

        Return catalogs by UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of catalog
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'catalog',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'catalog')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def catalog_action(ampache_url: str, ampache_api: str, task, catalog_id, api_format: str = 'xml'):
    """ catalog_action
        MINIMUM_API_VERSION=400001

        Kick off a catalog update or clean for the selected catalog

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * task        = (string) 'add_to_catalog'|'clean_catalog'|'verify_catalog'|'gather_art'
        * catalog_id  = (integer) $catalog_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'catalog_action',
            'auth': ampache_api,
            'task': task,
            'catalog': catalog_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'catalog_action')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def catalog_file(ampache_url: str, ampache_api: str, file, task, catalog_id, api_format: str = 'xml'):
    """ catalog_file
        MINIMUM_API_VERSION=420000

        Perform actions on local catalog files.
        Single file versions of catalog add, clean and verify.
        Make sure you remember to urlencode those file names!

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * file        = (string) urlencode(FULL path to local file)
        * task        = (string) 'add'|'clean'|'verify'|'remove'
        * catalog_id  = (integer) $catalog_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'catalog_file',
            'auth': ampache_api,
            'file': file,
            'task': task,
            'catalog': catalog_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'catalog_action')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcasts(ampache_url: str, ampache_api: str, filter_str: str = False,
             exact: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ podcasts
        MINIMUM_API_VERSION=420000

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a podcast //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcasts',
            'auth': ampache_api,
            'filter': filter_str,
            'exact': exact,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcasts')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast(ampache_url: str, ampache_api: str, filter_id: int, include=False, api_format: str = 'xml'):
    """ podcast
        MINIMUM_API_VERSION=420000

        Return podcasts by UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of Podcast
        * include     = (string) 'episodes' Include episodes with the response //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast',
            'auth': ampache_api,
            'filter': filter_id,
            'include': include}
    if not include:
        data.pop('include')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_create(ampache_url: str, ampache_api: str, url, catalog_id, api_format: str = 'xml'):
    """ podcast_create
        MINIMUM_API_VERSION=420000

        Return podcasts by UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * url         = (string) rss url for podcast
        * catalog_id  = (string) podcast catalog
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_create',
            'auth': ampache_api,
            'url': url,
            'catalog': catalog_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_create')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_edit(ampache_url: str, ampache_api: str, filter_id: int,
                 feed=False, title=False, website=False,
                 description=False, generator=False, copyright_str=False, api_format: str = 'xml'):
    """ podcast_edit
        MINIMUM_API_VERSION=420000

        Update the description and/or expiration date for an existing podcast.
        Takes the podcast id to update with optional description and expires parameters.

        INPUTS
        * ampache_url   = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api   = (string) session 'auth' key
        * filter_id     = (integer) $podcast_id
        * feed          = (string) feed url (xml!) //optional
        * title         = (string) title string //optional
        * website       = (string) source website url //optional
        * description   = (string) //optional
        * generator     = (string) //optional
        * copyright_str = (string) //optional
        * api_format    = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_edit',
            'auth': ampache_api,
            'filter': filter_id,
            'feed': feed,
            'title': title,
            'website': website,
            'description': description,
            'generator': generator,
            'copyright': copyright_str}
    if not feed:
        data.pop('feed')
    if not title:
        data.pop('title')
    if not website:
        data.pop('website')
    if not description:
        data.pop('description')
    if not generator:
        data.pop('generator')
    if not copyright:
        data.pop('copyright')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_edit')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_delete(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ podcast_delete
        MINIMUM_API_VERSION=420000

        Delete an existing podcast.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of podcast to delete
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_delete',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_delete')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_episodes(ampache_url: str, ampache_api: str, filter_id: int, offset=0, limit=0, api_format: str = 'xml'):
    """ podcast_episodes
        MINIMUM_API_VERSION=420000

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (string) UID of podcast
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_episodes',
            'auth': ampache_api,
            'filter': filter_id,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_episodes')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_episode(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ podcast_episode
        MINIMUM_API_VERSION=420000

        Return podcast_episodes by UID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of Podcast
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_episode',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_episode')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def podcast_episode_delete(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ podcast_episode_delete
        MINIMUM_API_VERSION=420000

        Delete an existing podcast_episode.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of podcast_episode to delete
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'podcast_episode_delete',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'podcast_episode')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def update_podcast(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ update_podcast
        MINIMUM_API_VERSION=420000

        Sync and download new podcast episodes

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) UID of Podcast
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'update_podcast',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'update_podcast')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def search_songs(ampache_url: str, ampache_api: str, filter_str, offset=0, limit=0, api_format: str = 'xml'):
    """ search_songs
        MINIMUM_API_VERSION=380001

        This searches the songs and returns... songs

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a song
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'search_songs',
            'auth': ampache_api,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'search_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def advanced_search(ampache_url: str, ampache_api: str, rules,
                    operator='and', object_type='song', offset=0, limit=0, random=0, api_format: str = 'xml'):
    """ advanced_search
        MINIMUM_API_VERSION=380001

        Perform an advanced search given passed rules
        the rules can occur multiple times and are joined by the operator item.

        Refer to the wiki for further information
        http://ampache.org/api/api-advanced-search

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input], [rule_2,rule_2_operator,rule_2_input], [etc]]
        * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
        * object_type = (string)  //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * random      = (integer) 0|1' //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'advanced_search',
            'auth': ampache_api,
            'operator': operator,
            'type': object_type,
            'offset': offset,
            'limit': limit,
            'random': random}
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def videos(ampache_url: str, ampache_api: str, filter_str: str = False,
           exact: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ videos
        MINIMUM_API_VERSION=380001

        This returns video objects!

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a video //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'videos',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'videos')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def video(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ video
        MINIMUM_API_VERSION=380001

        This returns a single video

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $video_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'video',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'video')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def localplay(ampache_url: str, ampache_api: str, command, oid=False, otype=False, clear=0, api_format: str = 'xml'):
    """ localplay
        MINIMUM_API_VERSION=380001
        CHANGED_IN_API_VERSION=5.0.0

        This is for controlling localplay

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * command     = (string) 'next', 'prev', 'stop', 'play', 'pause', 'add', 'volume_up',
                                 'volume_down', 'volume_mute', 'delete_all', 'skip', 'status'
        * oid         = (integer) object_id //optional
        * otype       = (string) 'Song', 'Video', 'Podcast_Episode', 'Channel',
                                 'Broadcast', 'Democratic', 'Live_Stream' //optional
        * clear       = (integer) 0,1 Clear the current playlist before adding //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'localplay',
            'auth': ampache_api,
            'command': command,
            'oid': oid,
            'type': otype,
            'clear': clear}
    if not oid:
        data.pop('oid')
    if not type:
        data.pop('type')
    if not clear:
        data.pop('clear')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'localplay')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def democratic(ampache_url: str, ampache_api: str, method, oid, api_format: str = 'xml'):
    """ democratic
        MINIMUM_API_VERSION=380001

        This is for controlling democratic play

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * oid         = (integer) object_id (song_id|playlist_id)
        * method      = (string) 'vote'|'devote'|'playlist'|'play'
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'democratic',
            'auth': ampache_api,
            'oid': oid,
            'method': method}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'democratic')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def stats(ampache_url: str, ampache_api: str, object_type, filter_str='random',
          username=False, user_id=False, offset=0, limit=0, api_format: str = 'xml'):
    """ stats
        MINIMUM_API_VERSION=380001
        CHANGED_IN_API_VERSION=400001

        This gets library stats for different object types. When filter is null get some random items instead

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'song'|'album'|'artist'
        * filter_str  = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|'random'
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * user_id     = (integer) //optional
        * username    = (string) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'stats',
            'auth': ampache_api,
            'type': object_type,
            'filter': filter_str,
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def users(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ users
        MINIMUM_API_VERSION=5.0.0
    
        Get ids and usernames for your site users
    
        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'users',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def user(ampache_url: str, ampache_api: str, username, api_format: str = 'xml'):
    """ user
        MINIMUM_API_VERSION=380001

        This get an user public information

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    =
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def followers(ampache_url: str, ampache_api: str, username, api_format: str = 'xml'):
    """ followers
        MINIMUM_API_VERSION=380001
    
        This get an user followers
    
        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    = 
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def following(ampache_url: str, ampache_api: str, username, api_format: str = 'xml'):
    """ following
        MINIMUM_API_VERSION=380001

        This get the user list followed by an user

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    =
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def toggle_follow(ampache_url: str, ampache_api: str, username, api_format: str = 'xml'):
    """ toggle_follow
        MINIMUM_API_VERSION=380001

        This follow/unfollow an user

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    =
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def last_shouts(ampache_url: str, ampache_api: str, username, limit=0, api_format: str = 'xml'):
    """ last_shouts
        MINIMUM_API_VERSION=380001

        This get the latest posted shouts

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    =
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def rate(ampache_url: str, ampache_api: str, object_type, object_id, rating, api_format: str = 'xml'):
    """ rate
        MINIMUM_API_VERSION=380001

        This rates a library item

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'song'|'album'|'artist'
        * object_id   = (integer) $object_id
        * rating      = (integer) 0|1|2|3|4|5
        * api_format  = (string) 'xml'|'json' //optional
    """
    if (rating < 0 or rating > 5) or not (object_type == 'song' or object_type == 'album' or object_type == 'artist'):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'rate',
            'auth': ampache_api,
            'type': object_type,
            'id': object_id,
            'rating': rating}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'rate')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def flag(ampache_url: str, ampache_api: str, object_type, object_id, flagbool, api_format: str = 'xml'):
    """ flag
        MINIMUM_API_VERSION=400001

        This flags a library item as a favorite

        Setting flagbool to true (1) will set the flag
        Setting flagbool to false (0) will remove the flag

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'song'|'album'|'artist'
        * object_id   = (integer) $object_id
        * flagbool    = (boolean|integer) (True,False | 0|1)
        * api_format  = (string) 'xml'|'json' //optional
    """
    if bool(flagbool):
        flag_state = 1
    else:
        flag_state = 0
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'flag',
            'auth': ampache_api,
            'type': object_type,
            'id': object_id,
            'flag': flag_state}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'flag')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def record_play(ampache_url: str, ampache_api: str, object_id, user_id, client='AmpacheAPI', api_format: str = 'xml'):
    """ record_play
        MINIMUM_API_VERSION=400001

        Take a song_id and update the object_count and user_activity table with a play.
        This allows other sources to record play history to ampache

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_id   = (integer) $object_id
        * user_id     = (integer) $user_id
        * client      = (string) $agent //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'record_play',
            'auth': ampache_api,
            'id': object_id,
            'user': user_id,
            'client': client}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'record_play')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def scrobble(ampache_url: str, ampache_api: str, title, artist_name, album_name,
             mbtitle=False, mbartist=False, mbalbum=False, stime=False,
             client='AmpacheAPI', api_format: str = 'xml'):
    """ scrobble
        MINIMUM_API_VERSION=400001

        Search for a song using text info and then record a play if found.
        This allows other sources to record play history to ampache

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * title       = (string) song title
        * artist_name = (string) artist name
        * album_name  = (string) album name
        * mbtitle     = (string) song mbid //optional
        * mbartist    = (string) artist mbid //optional
        * mbalbum     = (string) album mbid //optional
        * stime       = (integer) UNIXTIME() //optional
        * client      = (string) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'scrobble',
            'auth': ampache_api,
            'client': client,
            'date': str(stime),
            'song': title,
            'artist': artist_name,
            'album': album_name,
            'songmbid': mbtitle,
            'albummbid': mbalbum,
            'artistmdib': mbartist}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'scrobble')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def timeline(ampache_url: str, ampache_api: str, username, limit=0, since=0, api_format: str = 'xml'):
    """ timeline
        MINIMUM_API_VERSION=380001

        This get a user timeline

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    = (string)
        * limit       = (integer) //optional
        * since       = (integer) UNIXTIME() //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def friends_timeline(ampache_url: str, ampache_api: str, limit=0, since=0, api_format: str = 'xml'):
    """ friends_timeline
        MINIMUM_API_VERSION=380001

        This get current user friends timeline

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * limit       = (integer) //optional
        * since       = (integer) UNIXTIME() //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def update_from_tags(ampache_url: str, ampache_api: str, ampache_type, ampache_id, api_format: str = 'xml'):
    """ update_from_tags
        MINIMUM_API_VERSION=400001

        updates a single album,artist,song from the tag data

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'artist'|'album'|'song'
        * object_id   = (integer) $artist_id, $album_id, $song_id
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def update_art(ampache_url: str, ampache_api: str, ampache_type, ampache_id, overwrite=False, api_format: str = 'xml'):
    """ update_art
        MINIMUM_API_VERSION=400001

        updates a single album, artist, song looking for art files
        Doesn't overwrite existing art by default.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_type = (string) 'artist'|'album'|'song'
        * object_id   = (integer) $artist_id, $album_id, $song_id
        * overwrite   = (boolean|integer) (True,False | 0|1) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def update_artist_info(ampache_url: str, ampache_api: str, object_id, api_format: str = 'xml'):
    """ update_artist_info
        MINIMUM_API_VERSION=400001

        Update artist information and fetch similar artists from last.fm
        Make sure lastfm_api_key is set in your configuration file

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_id   = (integer) $artist_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'update_artist_info',
            'auth': ampache_api,
            'id': object_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'update_artist_info')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def stream(ampache_url: str, ampache_api: str, object_id, object_type, destination, api_format: str = 'xml'):
    """ stream
        MINIMUM_API_VERSION=400001

        stream a song or podcast episode

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_id   = (string) $song_id / $podcast_episode_id
        * object_type = (string) 'song'|'podcast'
        * destination = (string) full file path
        * api_format  = (string) 'xml'|'json' //optional
    """
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'stream',
            'auth': ampache_api,
            'id': object_id,
            'type': object_type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True


def download(ampache_url: str, ampache_api: str, object_id, object_type, destination,
             transcode='raw', api_format: str = 'xml'):
    """ download
        MINIMUM_API_VERSION=400001

        download a song or podcast episode

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_id   = (string) $song_id / $podcast_episode_id
        * object_type = (string) 'song'|'podcast'
        * destination = (string) full file path
        * transcode   = (string) 'mp3', 'ogg', etc. ('raw' / original by default) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'download',
            'auth': ampache_api,
            'id': object_id,
            'type': object_type,
            'format': transcode}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True


def get_art(ampache_url: str, ampache_api: str, object_id, object_type, destination, api_format: str = 'xml'):
    """ get_art
        MINIMUM_API_VERSION=400001

        get the binary art for an item

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * object_id   = (string) $song_id / $podcast_episode_id
        * object_type = (string) 'song', 'artist', 'album', 'playlist', 'search', 'podcast'
        * destination = (string) output file path
        * api_format  = (string) 'xml'|'json' //optional
    """
    if not os.path.isdir(os.path.dirname(destination)):
        return False
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'get_art',
            'auth': ampache_api,
            'id': object_id,
            'type': object_type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    result = requests.get(full_url, allow_redirects=True)
    open(destination, 'wb').write(result.content)
    return True


def user_create(ampache_url: str, ampache_api: str, username: str, password: str, email: str,
                fullname: str = False, disable=False, api_format: str = 'xml'):
    """ user_create
        MINIMUM_API_VERSION=400001

        Create a new user. (Requires the username, password and email.) @param array $input

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    = (string) $username
        * password    = (string) hash('sha256', $password))
        * email       = (string) 'user@gmail.com'
        * fullname    = (string) //optional
        * disable     = (boolean|integer) (True,False | 0|1) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    if bool(disable):
        disable = 1
    else:
        disable = 0
    if hashlib.sha256(password.encode()).hexdigest() != password:
        password = hashlib.sha256(password.encode()).hexdigest()
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def user_update(ampache_url: str, ampache_api: str, username, password=False, fullname=False, email=False,
                website=False, state=False, city=False, disable=False, maxbitrate=False, api_format: str = 'xml'):
    """ user_update
        MINIMUM_API_VERSION=400001

        Update an existing user. @param array $input

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def user_delete(ampache_url: str, ampache_api: str, username, api_format: str = 'xml'):
    """ user_delete
        MINIMUM_API_VERSION=400001

        Delete an existing user. @param array $input

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * username    = (string) $username
        * api_format  = (string) 'xml'|'json' //optional
    """
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
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def user_preferences(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ user_preferences
        MINIMUM_API_VERSION=5.0.0

        Returns user_preferences

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'user_preferences',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user_preferences')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def user_preference(ampache_url: str, ampache_api: str, filter_str, api_format: str = 'xml'):
    """ user_preference
        MINIMUM_API_VERSION=5.0.0

        Returns preference based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a preference //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'user_preferences',
            'auth': ampache_api,
            'filter': filter_str}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'user_preferences')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def system_preferences(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ system_preferences
        MINIMUM_API_VERSION=5.0.0

        Returns system_preferences

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'system_preferences',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'system_preferences')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def system_preference(ampache_url: str, ampache_api: str, filter_str, api_format: str = 'xml'):
    """ system_preference
        MINIMUM_API_VERSION=5.0.0

        Returns preference based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a preference //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'system_preferences',
            'auth': ampache_api,
            'filter': filter_str}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'system_preferences')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def system_update(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ system_update
        MINIMUM_API_VERSION=5.0.0

        update ampache

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'system_update',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'system_update')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def preference_create(ampache_url: str, ampache_api: str, filter_str, type_str, default, category,
                      description=False, subcategory=False, level=100, api_format: str = 'xml'):
    """ preference_create
        MINIMUM_API_VERSION=5.0.0

        Returns preference based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a preference
        * type_str    = (string) 'boolean', 'integer', 'string', 'special'
        * default     = (string|integer) default value
        * category    = (string) 'interface', 'internal', 'options', 'playlist', 'plugins', 'streaming', 'system'
        * description = (string) description of preference //optional
        * subcategory = (string) $subcategory //optional
        * level       = (integer) access level required to change the value (default 100) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'preference_create',
            'auth': ampache_api,
            'filter': filter_str,
            'type': type_str,
            'default': default,
            'category': category,
            'description': description,
            'subcategory': subcategory,
            'level': level}
    if not description:
        data.pop('description')
    if not subcategory:
        data.pop('subcategory')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'preference_create')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def preference_edit(ampache_url: str, ampache_api: str, filter_str, value, apply_all=0, api_format: str = 'xml'):
    """ preference_edit
        MINIMUM_API_VERSION=5.0.0

        Returns preference based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a preference
        * value       = (string|integer) Preference value
        * apply_all   = (boolean) apply to all users //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'preference_edit',
            'auth': ampache_api,
            'filter': filter_str,
            'value': value,
            'all': apply_all}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'preference_edit')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def preference_delete(ampache_url: str, ampache_api: str, filter_str, api_format: str = 'xml'):
    """ preference_delete
        MINIMUM_API_VERSION=5.0.0

        Returns preference based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a preference
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'preference_delete',
            'auth': ampache_api,
            'filter': filter_str}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'preference_delete')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def licenses(ampache_url: str, ampache_api: str, filter_str: str = False, exact: int = False,
             add: int = False, update: int = False, offset=0, limit=0, api_format: str = 'xml'):
    """ licenses
        MINIMUM_API_VERSION=420000

        Returns licenses based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a license //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * add         = (integer) UNIXTIME() //optional
        * update      = (integer) UNIXTIME() //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'licenses',
            'auth': ampache_api,
            'exact': exact,
            'add': add,
            'update': update,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    if not add:
        data.pop('add')
    if not update:
        data.pop('update')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'licenses')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def license(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ license
        MINIMUM_API_VERSION=420000

        returns a single license

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $license_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'license',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'license')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def license_songs(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ license_songs
        MINIMUM_API_VERSION=420000

        returns a songs for a single license ID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id  = (integer) $license_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'license_songs',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'license_songs')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def labels(ampache_url: str, ampache_api: str, filter_str: str = False, exact: int = False,
           offset=0, limit=0, api_format: str = 'xml'):
    """ labels
        MINIMUM_API_VERSION=420000

        Returns labels based on the specified filter_str

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_str  = (string) search the name of a label //optional
        * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
        * offset      = (integer) //optional
        * limit       = (integer) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'labels',
            'auth': ampache_api,
            'exact': exact,
            'filter': filter_str,
            'offset': str(offset),
            'limit': str(limit)}
    if not filter_str:
        data.pop('filter')
    if not exact:
        data.pop('exact')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'labels')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def label(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ label
        MINIMUM_API_VERSION=420000

        returns a single label

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) $label_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'label',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'label')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def label_artists(ampache_url: str, ampache_api: str, filter_id: int, api_format: str = 'xml'):
    """ label_artists
        MINIMUM_API_VERSION=420000

        returns a artists for a single label ID

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id  = (integer) $label_id
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'label_artists',
            'auth': ampache_api,
            'filter': filter_id}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'label_artists')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def get_bookmark(ampache_url: str, ampache_api: str, filter_id: str, object_type: str, api_format: str = 'xml'):
    """ get_bookmark
        MINIMUM_API_VERSION=5.0.0

        Get the bookmark from it's object_id and object_type.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) object_id
        * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'get_bookmark',
            'auth': ampache_api,
            'filter': filter_id,
            'type': object_type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'get_bookmark')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def bookmarks(ampache_url: str, ampache_api: str, api_format: str = 'xml'):
    """ bookmarks
        MINIMUM_API_VERSION=5.0.0

        Get information about bookmarked media this user is allowed to manage.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'bookmarks',
            'auth': ampache_api}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'bookmarks')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


def bookmark_create(ampache_url: str, ampache_api: str, filter_id, object_type,
                    position: int = 0, client: str = 'AmpacheAPI', date=False, api_format: str = 'xml'):
    """ bookmark_create
        MINIMUM_API_VERSION=5.0.0

        Create a placeholder for the current media that you can return to later.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) object_id
        * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        * position    = (integer) current track time in seconds
        * client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
        * date        = (integer) update time (Default: UNIXTIME()) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'bookmark_create',
            'auth': ampache_api,
            'filter': filter_id,
            'type': object_type,
            'position': position,
            'client': client,
            'date': date}
    if not client:
        data.pop('client')
    if not date:
        data.pop('date')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'bookmark_create')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
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


def bookmark_edit(ampache_url: str, ampache_api: str, filter_id, object_type,
                  position: int = 0, client: str = 'AmpacheAPI', date=False, api_format: str = 'xml'):
    """ bookmark_edit
        MINIMUM_API_VERSION=5.0.0

        Edit a placeholder for the current media that you can return to later.

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) object_id
        * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        * position    = (integer) current track time in seconds
        * client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
        * date        = (integer) update time (Default: UNIXTIME()) //optional
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'bookmark_edit',
            'auth': ampache_api,
            'filter': filter_id,
            'type': object_type,
            'position': position,
            'client': client,
            'date': date}
    if not client:
        data.pop('client')
    if not date:
        data.pop('date')
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'bookmark_edit')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
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


def bookmark_delete(ampache_url: str, ampache_api: str, filter_id: int, object_type=False, api_format: str = 'xml'):
    """ bookmark_delete
        MINIMUM_API_VERSION=5.0.0

        Delete an existing bookmark. (if it exists)

        INPUTS
        * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
        * ampache_api = (string) session 'auth' key
        * filter_id   = (integer) object_id
        * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        * api_format  = (string) 'xml'|'json' //optional
    """
    ampache_url = ampache_url + '/server/' + api_format + '.server.php'
    data = {'action': 'bookmark_delete',
            'auth': ampache_api,
            'filter': filter_id,
            'type': object_type}
    data = urllib.parse.urlencode(data)
    full_url = ampache_url + '?' + data
    ampache_response = fetch_url(full_url, api_format, 'bookmark_delete')
    if not ampache_response:
        return False
    # json format
    if api_format == 'json':
        json_data = json.loads(ampache_response.decode('utf-8'))
        return json_data
    # xml format
    else:
        try:
            tree = ElementTree.fromstring(ampache_response.decode('utf-8'))
        except ElementTree.ParseError:
            return False
        return tree


"""
--------------------
BACKCOMPAT FUNCTIONS
--------------------
"""
tag = genre
tags = genres
tag_artists = genre_artists
tag_albums = genre_albums
tag_songs = genre_songs
