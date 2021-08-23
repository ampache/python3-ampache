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


class API(object):

    def __init__(self):
        self.AMPACHE_API = 'xml'
        self.AMPACHE_DEBUG = False
        self.AMPACHE_URL = ''
        self.AMPACHE_SESSION = ''
        self.AMPACHE_USER = ''
        self.AMPACHE_KEY = ''
        # Test colors for printing
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'

    """
    ----------------
    HELPER FUNCTIONS
    ----------------
    """

    def set_format(self, myformat: str):
        """ set_format

            Allow forcing a default format

            INPUTS
            * myformat = (string) 'xml'|'json'
        """
        if myformat == 'xml' or myformat == 'json':
            print('AMPACHE_API set to ' + myformat)
            self.AMPACHE_API = myformat

    def set_debug(self, mybool: bool):
        """ set_debug

            This function can be used to enable/disable debugging messages

            INPUTS
            * bool = (boolean) Enable/disable debug messages
        """
        if mybool:
            print('AMPACHE_DEBUG' + f": {self.OKGREEN}enabled{self.ENDC}")
        else:
            print('AMPACHE_DEBUG' + f": {self.WARNING}disabled{self.ENDC}")
        self.AMPACHE_DEBUG = mybool

    def set_user(self, myuser: str):
        """ set_user

            set user for connection

            INPUTS
            * myuser = (string) 'xml'|'json'
        """
        self.AMPACHE_USER = myuser

    def set_key(self, mykey: str):
        """ set_key

            set api key

            INPUTS
            * mykey = (string) 'xml'|'json'
        """
        self.AMPACHE_API = mykey

    def set_url(self, myurl: str):
        """ set_url

            set the ampache url

            INPUTS
            * myurl = (string) 'xml'|'json'
        """
        self.AMPACHE_URL = myurl

    def test_result(self, result, title):
        """ set_debug

            This function can be used to enable/disable debugging messages

            INPUTS
            * bool = (boolean) Enable/disable debug messages
        """
        if not result:
            print("ampache." + title + f": {self.FAIL}FAIL{self.ENDC}")
            return False
        if 'Require: ' in result:
            print(f"ampache." + title + f": {self.WARNING}WARNING{self.ENDC} " + result)
            return True
        if result:
            print("ampache." + title + f": {self.OKGREEN}PASS{self.ENDC}")
            return True
        print("ampache." + title + f": {self.FAIL}FAIL{self.ENDC}")
        return False

    def return_data(self, data):
        # json format
        if self.AMPACHE_API == 'json':
            json_data = json.loads(data.decode('utf-8'))
            return json_data
        # xml format
        else:
            try:
                tree = ElementTree.fromstring(data.decode('utf-8'))
            except ElementTree.ParseError:
                return False
            return tree

    def get_id_list(self, data, attribute: str):
        """ get_id_list

            return a list of id's from the data you've got from the api

            INPUTS
            * data        = (mixed) XML or JSON from the API
            * attribute   = (string) attribute you are searching for
        """
        id_list = list()
        if not data:
            return id_list
        if self.AMPACHE_API == 'xml':
            try:
                for child in data:
                    if child.tag == attribute:
                        id_list.append(child.attrib['id'])
            except KeyError:
                id_list.append(data['id'])
        else:
            try:
                for data_object in data[attribute]:
                    id_list.append(data_object['id'])
            except TypeError:
                for data_object in data:
                    id_list.append(data_object[0])
            except KeyError:
                id_list.append(data['id'])
        return id_list

    @staticmethod
    def get_object_list(data, field: str, data_format: str = 'xml'):
        """ get_id_list

            return a list of objects from the data matching your field stirng

            INPUTS
            * data        = (mixed) XML or JSON from the API
            * field       = (string) field you are searching for
            * data_format = (string) 'xml','json'
        """
        id_list = list()
        if data_format == 'xml':
            return data.findall(field)
        else:
            try:
                for data_object in data[field]:
                    id_list.append(data_object['id'])
            except TypeError:
                for data_object in data:
                    id_list.append(data_object[0])
        return id_list

    @staticmethod
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

    @staticmethod
    def get_message(data):
        """ get_id_list

            return a list of objects from the data matching your field stirng

            INPUTS
            * data = (mixed) XML or JSON from the API
        """
        message = data
        print(data)
        if 'error' in data:
            try:
                message = data['error']['message']
            except TypeError:
                message = data['error']
            except KeyError:
                message = data['error']['errorMessage']
        if 'success' in data:
            try:
                message = data['success']['message']
            except TypeError:
                message = data['success']
        return message

    @staticmethod
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

    @staticmethod
    def encrypt_password(password: str, current_time: int):
        """ encrypt_password

            This function can be used to encrypt your password into the accepted format.

            INPUTS
            * password = (string) unencrypted password string
            * time     = (integer) linux time
        """
        key = hashlib.sha256(password.encode()).hexdigest()
        passphrase = str(current_time) + key
        sha_signature = hashlib.sha256(passphrase.encode()).hexdigest()
        return sha_signature

    @staticmethod
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

    def fetch_url(self, full_url: str, api_format: str, method: str):
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
        except ValueError:
            return False
        ampache_response = result.read()
        result.close()
        if self.AMPACHE_DEBUG:
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

    def handshake(self, ampache_url: str, ampache_api: str, ampache_user: str = False,
                  timestamp: int = 0, version: str = '5.0.0'):
        """ handshake
            MINIMUM_API_VERSION=380001

            This is the function that handles verifying a new handshake
            Takes a timestamp, auth key, and username.

            INPUTS
            * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
            * ampache_api = (string) encrypted apikey OR password if using password auth
            * user        = (string) username //optional
            * timestamp   = (integer) UNIXTIME() //optional
            * version     = (string) //optional
        """
        self.AMPACHE_URL = ampache_url
        if timestamp == 0:
            timestamp = int(time.time())
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'handshake')
        if not ampache_response:
            return False
        # json format
        if self.AMPACHE_API == 'json':
            json_data = json.loads(ampache_response.decode('utf-8'))
            if 'auth' in json_data:
                self.AMPACHE_SESSION = json_data['auth']
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
            self.AMPACHE_SESSION = token
            return token

    def ping(self, ampache_url: str, ampache_api: str = False, version: str = '5.0.0'):
        """ ping
            MINIMUM_API_VERSION=380001

            This can be called without being authenticated, it is useful for determining if what the status
            of the server is, and what version it is running/compatible with

            INPUTS
            * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
            * ampache_api = (string) encrypted apikey //optional
        """
        ampache_url = ampache_url + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'ping',
                'version': version,
                'auth': ampache_api}
        if not ampache_api:
            data.pop('auth')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'ping')
        if not ampache_response:
            return False
        # json format
        if self.AMPACHE_API == 'json':
            json_data = json.loads(ampache_response.decode('utf-8'))
            if 'session_expire' in json_data:
                self.AMPACHE_SESSION = ampache_api
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

    def goodbye(self):
        """ goodbye
            MINIMUM_API_VERSION=400001

            Destroy session for ampache_api auth key.
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'goodbye',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'goodbye')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def url_to_song(self, url):
        """ url_to_song
            MINIMUM_API_VERSION=380001

            This takes a url and returns the song object in question

            INPUTS
            * url         = (string) Full Ampache URL from server, translates back into a song XML
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'url_to_song',
                'auth': self.AMPACHE_SESSION,
                'url': url}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'url_to_song')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def get_similar(self, object_type, filter_id: int,
                    offset=0, limit=0):
        """ get_similar
            MINIMUM_API_VERSION=420000

            Return similar artist id's or similar song ids compared to the input filter

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'|'playlist'
            * filter_id   = (integer) $artist_id or song_id
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'get_similar',
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'get_similar')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def get_indexes(self, object_type,
                    filter_str: str = False, exact: int = False, add: int = False, update: int = False,
                    include=False, offset=0, limit=0):
        """ get_indexes
            MINIMUM_API_VERSION=400001

            This takes a collection of inputs and returns ID + name for the object type

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'|'album_artist'|'playlist'
            * filter_str  = (string) search the name of the object_type //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * include     = (integer) 0,1 include songs if available for that object //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include):
            include = 1
        else:
            include = 0
        data = {'action': 'get_indexes',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'get_indexes')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def artists(self, filter_str: str = False,
                add: int = False, update: int = False, offset=0, limit=0, include=False):
        """ artists
            MINIMUM_API_VERSION=380001

            This takes a collection of inputs and returns artist objects.

            INPUTS
            * filter_str   = (string) search the name of an artist //optional
            * add          = (integer) UNIXTIME() //optional
            * update       = (integer) UNIXTIME() //optional
            * offset       = (integer) //optional
            * limit        = (integer) //optional
            * include      = (string) 'albums', 'songs' //optional
            * album_artist = (boolean) 0,1 if true filter for album artists only //optional
            * self.AMPACHE_API   = (string) 'xml'|'json' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include) and not isinstance(include, str):
            include = 'albums,songs'
        data = {'action': 'artists',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'artists')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def artist(self, filter_id: int, include=False):
        """ artist
            MINIMUM_API_VERSION=380001

            This returns a single artist based on the UID of said artist

            INPUTS
            * filter_id   = (integer) $artist_id
            * include     = (string) 'albums', 'songs' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include) and not isinstance(include, str):
            include = 'albums,songs'
        data = {'action': 'artist',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'artist')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def artist_albums(self, filter_id: int, offset=0, limit=0):
        """ artist_albums
            MINIMUM_API_VERSION=380001

            This returns the albums of an artist

            INPUTS
            * filter_id   = (integer) $artist_id
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'artist_albums',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'artist_albums')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def artist_songs(self, filter_id: int, offset=0, limit=0):
        """ artist_songs
            MINIMUM_API_VERSION=380001

            This returns the songs of the specified artist

            INPUTS
            * filter_id   = (integer) $artist_id
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'artist_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'artist_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def albums(self, filter_str: str = False,
               exact=False, add: int = False, update: int = False, offset=0, limit=0,
               include=False):
        """ albums
            MINIMUM_API_VERSION=380001

            This returns albums based on the provided search filters

            INPUTS
            * filter_str  = (string) search the name of an album //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * include     = (string) 'songs' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include) and not isinstance(include, str):
            include = 'songs'
        data = {'action': 'albums',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'albums')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def album(self, filter_id: int, include=False):
        """ album
            MINIMUM_API_VERSION=380001

            This returns a single album based on the UID provided

            INPUTS
            * filter_id   = (integer) $album_id
            * include     = (string) 'songs' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include) and not isinstance(include, str):
            include = 'songs'
        data = {'action': 'album',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'album')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def album_songs(self, filter_id: int, offset=0, limit=0):
        """ album_songs
            MINIMUM_API_VERSION=380001

            This returns the songs of a specified album

            INPUTS
            * filter_id = (integer) $album_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'album_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'album_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def genres(self, filter_str: str = False,
               exact: int = False, offset=0, limit=0):
        """ genres
            MINIMUM_API_VERSION=380001

            This returns the genres (Tags) based on the specified filter

            INPUTS
            * filter_str = (string) search the name of a genre //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'genres',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'genres')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def genre(self, filter_id: int):
        """ genre
            MINIMUM_API_VERSION=380001

            This returns a single genre based on UID

            INPUTS
            * filter_id = (integer) $genre_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'genre',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'genre')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def genre_artists(self, filter_id: int, offset=0, limit=0):
        """ genre_artists
            MINIMUM_API_VERSION=380001

            This returns the artists associated with the genre in question as defined by the UID

            INPUTS
            * filter_id   = (integer) $genre_id
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'genre_artists',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'genre_artists')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def genre_albums(self, filter_id: int, offset=0, limit=0):
        """ genre_albums
            MINIMUM_API_VERSION=380001

            This returns the albums associated with the genre in question

            INPUTS
            * filter_id = (integer) $genre_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'genre_albums',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'genre_albums')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def genre_songs(self, filter_id: int, offset=0, limit=0):
        """ genre_songs
            MINIMUM_API_VERSION=380001

            returns the songs for this genre

            INPUTS
            * filter_id = (integer) $genre_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'genre_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'genre_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def songs(self, filter_str: str = False, exact: int = False,
              add: int = False, update: int = False, offset=0, limit=0):
        """ songs
            MINIMUM_API_VERSION=380001

            Returns songs based on the specified filter_str

            INPUTS
            * filter_str = (string) search the name of a song //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add        = (integer) UNIXTIME() //optional
            * update     = (integer) UNIXTIME() //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'songs',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def song(self, filter_id: int):
        """ song
            MINIMUM_API_VERSION=380001

            returns a single song

            INPUTS
            * filter_id = (integer) $song_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'song',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'song')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def song_delete(self, filter_id: int):
        """ song_delete
            MINIMUM_API_VERSION=5.0.0

            Delete an existing song.

            INPUTS
            * filter_id   = (string) UID of song to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'song_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'song')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlists(self, filter_str: str = False,
                  exact: int = False, offset=0, limit=0):
        """ playlists
            MINIMUM_API_VERSION=380001

            This returns playlists based on the specified filter

            INPUTS
            * filter_str  = (string) search the name of a playlist //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlists',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlists')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist(self, filter_id: int):
        """ playlist
            MINIMUM_API_VERSION=380001

            This returns a single playlist

            INPUTS
            * filter_id  = (integer) $playlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_songs(self, filter_id: int, offset=0, limit=0):
        """ playlist_songs
            MINIMUM_API_VERSION=380001

            This returns the songs for a playlist

            INPUTS
            * filter_id   = (integer) $playlist_id
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_create(self, name, object_type):
        """ playlist_create
            MINIMUM_API_VERSION=380001

            This create a new playlist and return it

            INPUTS
            * name        = (string)
            * object_type = (string)
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist_create',
                'auth': self.AMPACHE_SESSION,
                'name': name,
                'type': object_type}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_edit(self, filter_id: int, name=False,
                      object_type=False):
        """ playlist_edit
            MINIMUM_API_VERSION=400001

            This modifies name and type of a playlist

            INPUTS
            * filter_id   = (integer)
            * name        = (string) playlist name //optional
            * object_type = (string) 'public'|'private'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist_edit',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'name': name,
                'type': object_type}
        if not name:
            data.pop('name')
        if not object_type:
            data.pop('type')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_edit')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_delete(self, filter_id: int):
        """ playlist_delete
            MINIMUM_API_VERSION=380001

            This deletes a playlist

            INPUTS
            * filter_id   = (integer) $playlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_add_song(self, filter_id: int, song_id, check=False):
        """ playlist_add_song
            MINIMUM_API_VERSION=380001
            CHANGED_IN_API_VERSION=400003

            This adds a song to a playlist.
            Added duplicate checks in 400003

            INPUTS
            * filter_id   = (integer) $playlist_id
            * song_id     = (integer) $song_id
            * check       = (boolean|integer) (True,False | 0|1) Check for duplicates //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(check):
            check = 1
        else:
            check = 0
        data = {'action': 'playlist_add_song',
                'auth': self.AMPACHE_SESSION,
                'song': song_id,
                'filter': filter_id,
                'check': check}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_add_song')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_remove_song(self, filter_id: int,
                             song_id=False, track=False):
        """ playlist_remove_song
            MINIMUM_API_VERSION=380001
            CHANGED_IN_API_VERSION=400001

            This removes a song from a playlist. Previous versions required 'track' instead of 'song'.

            INPUTS
            * filter_id   = (integer) $playlist_id
            * song_id     = (integer) $song_id //optional
            * track       = (integer) $playlist_track number //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'

        data = {'action': 'playlist_remove_song',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'song': song_id,
                'track': track}
        if not song_id:
            data.pop('song')
        if not track:
            data.pop('track')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_remove_song')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def playlist_generate(self, mode='random',
                          filter_str: str = False, album_id=False, artist_id=False, flagged=False,
                          list_format='song', offset=0, limit=0):
        """ playlist_generate
            MINIMUM_API_VERSION=400001
            CHANGED_IN_API_VERSION=400002

            Get a list of song XML, indexes or id's based on some simple search criteria =
            'recent' will search for tracks played after 'Popular Threshold' days
            'forgotten' will search for tracks played before 'Popular Threshold' days
            'unplayed' added in 400002 for searching unplayed tracks

            INPUTS
            * mode        = (string) 'recent', 'forgotten', 'unplayed', 'random' (default = 'random') //optional
            * filter_str  = (string) string LIKE matched to song title //optional
            * album_id    = (integer) $album_id //optional
            * artist_id   = (integer) $artist_id //optional
            * flagged     = (integer) get flagged songs only 0, 1 (default=0) //optional
            * list_format = (string) 'song', 'index','id' (default = 'song') //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'playlist_generate',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'playlist_generate')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def shares(self, filter_str: str = False,
               exact: int = False, offset=0, limit=0):
        """ shares
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str  = (string) search the name of a share //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'shares',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'shares')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def share(self, filter_id: int):
        """ share
            MINIMUM_API_VERSION=420000

            Return shares by UID

            INPUTS
            * filter_id   = (integer) UID of Share
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'share',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'share')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def share_create(self, filter_id: int, object_type,
                     description=False, expires=False):
        """ share_create
            MINIMUM_API_VERSION=420000

            Create a public url that can be used by anyone to stream media.
            Takes the file id with optional description and expires parameters.

           INPUTS
            * filter_id   = (integer) $object_id
            * object_type = (string) object_type ('song', 'album', 'artist')
            * description = (string) description (will be filled for you if empty) //optional
            * expires     = (integer) days to keep active //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'share_create',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'share_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def share_edit(self, filter_id: int, can_stream=False, can_download=False,
                   expires=False, description=False):
        """ share_edit
            MINIMUM_API_VERSION=420000

            Update the description and/or expiration date for an existing share.
            Takes the share id to update with optional description and expires parameters.

            INPUT
            * filter_id    = (integer) UID of Share
            * can_stream   = (boolean) 0,1 //optional
            * can_download = (boolean) 0,1 //optional
            * expires      = (integer) number of whole days before expiry //optional
            * description  = (string) update description //optional
            * self.AMPACHE_API   = (string) 'xml'|'json' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'share_edit',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'share_edit')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def share_delete(self, filter_id: int):
        """ share_delete
            MINIMUM_API_VERSION=420000

            Delete an existing share.

            INPUT
            * filter_id   = (integer) UID of Share to delete
         """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'share_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'share_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def catalogs(self, filter_str: str = False, offset=0, limit=0):
        """ catalogs
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str  = (string) search the name of a catalog //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'catalogs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit)}
        if not filter_str:
            data.pop('filter')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'catalogs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def catalog(self, filter_id: int, offset=0, limit=0):
        """ catalog
            MINIMUM_API_VERSION=420000

            Return catalogs by UID

            INPUTS
            * filter_id   = (integer) UID of catalog
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'catalog',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'catalog')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def catalog_action(self, task, catalog_id):
        """ catalog_action
            MINIMUM_API_VERSION=400001

            Kick off a catalog update or clean for the selected catalog

            INPUTS
            * task        = (string) 'add_to_catalog'|'clean_catalog'|'verify_catalog'|'gather_art'
            * catalog_id  = (integer) $catalog_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'catalog_action',
                'auth': self.AMPACHE_SESSION,
                'task': task,
                'catalog': catalog_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'catalog_action')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def catalog_file(self, file, task, catalog_id):
        """ catalog_file
            MINIMUM_API_VERSION=420000

            Perform actions on local catalog files.
            Single file versions of catalog add, clean and verify.
            Make sure you remember to urlencode those file names!

            INPUTS
            * file        = (string) urlencode(FULL path to local file)
            * task        = (string) 'add'|'clean'|'verify'|'remove'
            * catalog_id  = (integer) $catalog_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'catalog_file',
                'auth': self.AMPACHE_SESSION,
                'file': file,
                'task': task,
                'catalog': catalog_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'catalog_action')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcasts(self, filter_str: str = False,
                 exact: int = False, offset=0, limit=0):
        """ podcasts
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str  = (string) search the name of a podcast //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcasts',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcasts')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast(self, filter_id: int, include=False):
        """ podcast
            MINIMUM_API_VERSION=420000

            Return podcasts by UID

            INPUTS
            * filter_id   = (integer) UID of Podcast
            * include     = (string) 'episodes' Include episodes with the response //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_create(self, url, catalog_id):
        """ podcast_create
            MINIMUM_API_VERSION=420000

            Return podcasts by UID

            INPUTS
            * url         = (string) rss url for podcast
            * catalog_id  = (string) podcast catalog
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_create',
                'auth': self.AMPACHE_SESSION,
                'url': url,
                'catalog': catalog_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_edit(self, filter_id: int,
                     feed=False, title=False, website=False,
                     description=False, generator=False, copyright_str=False):
        """ podcast_edit
            MINIMUM_API_VERSION=420000

            Update the description and/or expiration date for an existing podcast.
            Takes the podcast id to update with optional description and expires parameters.

            INPUTS
            * filter_id     = (integer) $podcast_id
            * feed          = (string) feed url (xml!) //optional
            * title         = (string) title string //optional
            * website       = (string) source website url //optional
            * description   = (string) //optional
            * generator     = (string) //optional
            * copyright_str = (string) //optional
            * self.AMPACHE_API    = (string) 'xml'|'json' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_edit',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_edit')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_delete(self, filter_id: int):
        """ podcast_delete
            MINIMUM_API_VERSION=420000

            Delete an existing podcast.

            INPUTS
            * filter_id   = (integer) UID of podcast to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_episodes(self, filter_id: int, offset=0, limit=0):
        """ podcast_episodes
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_id   = (string) UID of podcast
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_episodes',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_episodes')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_episode(self, filter_id: int):
        """ podcast_episode
            MINIMUM_API_VERSION=420000

            Return podcast_episodes by UID

            INPUTS
            * filter_id   = (integer) UID of Podcast
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_episode',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_episode')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def podcast_episode_delete(self, filter_id: int):
        """ podcast_episode_delete
            MINIMUM_API_VERSION=420000

            Delete an existing podcast_episode.

            INPUTS
            * filter_id   = (integer) UID of podcast_episode to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'podcast_episode_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'podcast_episode')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def update_podcast(self, filter_id: int):
        """ update_podcast
            MINIMUM_API_VERSION=420000

            Sync and download new podcast episodes

            INPUTS
            * filter_id   = (integer) UID of Podcast
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'update_podcast',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'update_podcast')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def search_songs(self, filter_str, offset=0, limit=0):
        """ search_songs
            MINIMUM_API_VERSION=380001

            This searches the songs and returns... songs

            INPUTS
            * filter_str  = (string) search the name of a song
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'search_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'search_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def advanced_search(self, rules,
                        operator='and', object_type='song', offset=0, limit=0, random=0):
        """ advanced_search
            MINIMUM_API_VERSION=380001

            Perform an advanced search given passed rules
            the rules can occur multiple times and are joined by the operator item.

            Refer to the wiki for further information
            http://ampache.org/api/api-advanced-search

            INPUTS
            * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input], [rule_2,rule_2_operator,rule_2_input], [etc]]
            * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
            * object_type = (string)  //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * random      = (integer) 0|1' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'advanced_search',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'advanced_search')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def videos(self, filter_str: str = False,
               exact: int = False, offset=0, limit=0):
        """ videos
            MINIMUM_API_VERSION=380001

            This returns video objects!

            INPUTS
            * filter_str  = (string) search the name of a video //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'videos',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'videos')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def video(self, filter_id: int):
        """ video
            MINIMUM_API_VERSION=380001

            This returns a single video

            INPUTS
            * filter_id   = (integer) $video_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'video',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'video')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def localplay(self, command, oid=False, otype=False, clear=0):
        """ localplay
            MINIMUM_API_VERSION=380001
            CHANGED_IN_API_VERSION=5.0.0

            This is for controlling localplay

            INPUTS
            * command     = (string) 'next', 'prev', 'stop', 'play', 'pause', 'add', 'volume_up',
                                     'volume_down', 'volume_mute', 'delete_all', 'skip', 'status'
            * oid         = (integer) object_id //optional
            * otype       = (string) 'Song', 'Video', 'Podcast_Episode', 'Channel',
                                     'Broadcast', 'Democratic', 'Live_Stream' //optional
            * clear       = (integer) 0,1 Clear the current playlist before adding //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'localplay',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'localplay')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def localplay_songs(self):
        """ localplay
            MINIMUM_API_VERSION=5.0.0

            This is for controlling localplay

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'localplay_songs',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'localplay_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def democratic(self, method, oid):
        """ democratic
            MINIMUM_API_VERSION=380001

            This is for controlling democratic play

            INPUTS
            * oid         = (integer) object_id (song_id|playlist_id)
            * method      = (string) 'vote'|'devote'|'playlist'|'play'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'democratic',
                'auth': self.AMPACHE_SESSION,
                'oid': oid,
                'method': method}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'democratic')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def stats(self, object_type, filter_str='random',
              username=False, user_id=False, offset=0, limit=0):
        """ stats
            MINIMUM_API_VERSION=380001
            CHANGED_IN_API_VERSION=400001

            This gets library stats for different object types. When filter is null get some random items instead

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'
            * filter_str  = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|'random'
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * user_id     = (integer) //optional
            * username    = (string) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'stats',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'stats')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def users(self):
        """ users
            MINIMUM_API_VERSION=5.0.0

            Get ids and usernames for your site users

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'users',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def user(self, username):
        """ user
            MINIMUM_API_VERSION=380001

            This get an user public information

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'user',
                'auth': self.AMPACHE_SESSION,
                'username': username}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def followers(self, username):
        """ followers
            MINIMUM_API_VERSION=380001

            This get an user followers

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'followers',
                'auth': self.AMPACHE_SESSION,
                'username': username}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'followers')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def following(self, username):
        """ following
            MINIMUM_API_VERSION=380001

            This get the user list followed by an user

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'following',
                'auth': self.AMPACHE_SESSION,
                'username': username}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'following')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def toggle_follow(self, username):
        """ toggle_follow
            MINIMUM_API_VERSION=380001

            This follow/unfollow an user

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'toggle_follow',
                'auth': self.AMPACHE_SESSION,
                'username': username}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'toggle_follow')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def last_shouts(self, username, limit=0):
        """ last_shouts
            MINIMUM_API_VERSION=380001

            This get the latest posted shouts

            INPUTS
            * username    =
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'last_shouts',
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'limit': limit}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'last_shouts')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def rate(self, object_type, object_id, rating):
        """ rate
            MINIMUM_API_VERSION=380001

            This rates a library item

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'
            * object_id   = (integer) $object_id
            * rating      = (integer) 0|1|2|3|4|5
        """
        if (rating < 0 or rating > 5) or not (object_type == 'song' or object_type == 'album' or object_type == 'artist'):
            return False
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'rate',
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id,
                'rating': rating}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'rate')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def flag(self, object_type, object_id, flagbool):
        """ flag
            MINIMUM_API_VERSION=400001

            This flags a library item as a favorite

            Setting flagbool to true (1) will set the flag
            Setting flagbool to false (0) will remove the flag

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'
            * object_id   = (integer) $object_id
            * flagbool    = (boolean|integer) (True,False | 0|1)
        """
        if bool(flagbool):
            flag_state = 1
        else:
            flag_state = 0
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'flag',
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id,
                'flag': flag_state}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'flag')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def record_play(self, object_id, user_id, client='AmpacheAPI'):
        """ record_play
            MINIMUM_API_VERSION=400001

            Take a song_id and update the object_count and user_activity table with a play.
            This allows other sources to record play history to ampache

            INPUTS
            * object_id   = (integer) $object_id
            * user_id     = (integer) $user_id
            * client      = (string) $agent //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'record_play',
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'user': user_id,
                'client': client}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'record_play')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def scrobble(self, title, artist_name, album_name,
                 mbtitle=False, mbartist=False, mbalbum=False, stime=False,
                 client='AmpacheAPI'):
        """ scrobble
            MINIMUM_API_VERSION=400001

            Search for a song using text info and then record a play if found.
            This allows other sources to record play history to ampache

            INPUTS
            * title       = (string) song title
            * artist_name = (string) artist name
            * album_name  = (string) album name
            * mbtitle     = (string) song mbid //optional
            * mbartist    = (string) artist mbid //optional
            * mbalbum     = (string) album mbid //optional
            * stime       = (integer) UNIXTIME() //optional
            * client      = (string) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'scrobble',
                'auth': self.AMPACHE_SESSION,
                'client': client,
                'date': str(stime),
                'song': title,
                'artist': artist_name,
                'album': album_name,
                'songmbid': mbtitle,
                'albummbid': mbalbum,
                'artistmdib': mbartist}
        if not mbtitle:
            data.pop('songmbid')
        if not mbalbum:
            data.pop('albummbid')
        if not mbartist:
            data.pop('artistmdib')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'scrobble')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def timeline(self, username, limit=0, since=0):
        """ timeline
            MINIMUM_API_VERSION=380001

            This get a user timeline

            INPUTS
            * username    = (string)
            * limit       = (integer) //optional
            * since       = (integer) UNIXTIME() //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'timeline',
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'limit': limit,
                'since': since}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'timeline')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def friends_timeline(self, limit=0, since=0):
        """ friends_timeline
            MINIMUM_API_VERSION=380001

            This get current user friends timeline

            INPUTS
            * limit       = (integer) //optional
            * since       = (integer) UNIXTIME() //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'friends_timeline',
                'auth': self.AMPACHE_SESSION,
                'limit': limit,
                'since': since}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'friends_timeline')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def update_from_tags(self, ampache_type, ampache_id):
        """ update_from_tags
            MINIMUM_API_VERSION=400001

            updates a single album,artist,song from the tag data

            INPUTS
            * object_type = (string) 'artist'|'album'|'song'
            * object_id   = (integer) $artist_id, $album_id, $song_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'update_from_tags',
                'auth': self.AMPACHE_SESSION,
                'type': ampache_type,
                'id': ampache_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'update_from_tags')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def update_art(self, ampache_type, ampache_id, overwrite=False):
        """ update_art
            MINIMUM_API_VERSION=400001

            updates a single album, artist, song looking for art files
            Doesn't overwrite existing art by default.

            INPUTS
            * object_type = (string) 'artist'|'album'|'song'
            * object_id   = (integer) $artist_id, $album_id, $song_id
            * overwrite   = (boolean|integer) (True,False | 0|1) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(overwrite):
            overwrite = 1
        else:
            overwrite = 0
        data = {'action': 'update_art',
                'auth': self.AMPACHE_SESSION,
                'type': ampache_type,
                'id': ampache_id,
                'overwrite': overwrite}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'update_art')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def update_artist_info(self, object_id):
        """ update_artist_info
            MINIMUM_API_VERSION=400001

            Update artist information and fetch similar artists from last.fm
            Make sure lastfm_api_key is set in your configuration file

            INPUTS
            * object_id   = (integer) $artist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'update_artist_info',
                'auth': self.AMPACHE_SESSION,
                'id': object_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'update_artist_info')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def stream(self, object_id, object_type, destination):
        """ stream
            MINIMUM_API_VERSION=400001

            stream a song or podcast episode

            INPUTS
            * object_id   = (string) $song_id / $podcast_episode_id
            * object_type = (string) 'song'|'podcast'
            * destination = (string) full file path
        """
        if not os.path.isdir(os.path.dirname(destination)):
            return False
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'stream',
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def download(self, object_id, object_type, destination,
                 transcode='raw'):
        """ download
            MINIMUM_API_VERSION=400001

            download a song or podcast episode

            INPUTS
            * object_id   = (string) $song_id / $podcast_episode_id
            * object_type = (string) 'song'|'podcast'
            * destination = (string) full file path
            * transcode   = (string) 'mp3', 'ogg', etc. ('raw' / original by default) //optional
        """
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'download',
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type,
                'format': transcode}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def get_art(self, object_id, object_type, destination):
        """ get_art
            MINIMUM_API_VERSION=400001

            get the binary art for an item

            INPUTS
            * object_id   = (string) $song_id / $podcast_episode_id
            * object_type = (string) 'song', 'artist', 'album', 'playlist', 'search', 'podcast'
            * destination = (string) output file path
        """
        if not os.path.isdir(os.path.dirname(destination)):
            return False
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'get_art',
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def user_create(self, username: str, password: str, email: str,
                    fullname: str = False, disable=False):
        """ user_create
            MINIMUM_API_VERSION=400001

            Create a new user. (Requires the username, password and email.) @param array $input

            INPUTS
            * username    = (string) $username
            * password    = (string) hash('sha256', $password))
            * email       = (string) 'user@gmail.com'
            * fullname    = (string) //optional
            * disable     = (boolean|integer) (True,False | 0|1) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(disable):
            disable = 1
        else:
            disable = 0
        if hashlib.sha256(password.encode()).hexdigest() != password:
            password = hashlib.sha256(password.encode()).hexdigest()
        data = {'action': 'user_create',
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'password': password,
                'email': email,
                'fullname': fullname,
                'disable': disable}
        if not fullname:
            data.pop('fullname')
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def user_update(self, username, password=False, fullname=False, email=False,
                    website=False, state=False, city=False, disable=False, maxbitrate=False):
        """ user_update
            MINIMUM_API_VERSION=400001

            Update an existing user. @param array $input

            INPUTS
            * username    = (string) $username
            * password    = (string) hash('sha256', $password)) //optional
            * fullname    = (string) //optional
            * email       = (string) 'user@gmail.com' //optional
            * website     = (string) //optional
            * state       = (string) //optional
            * city        = (string) //optional
            * disable     = (boolean|integer) (True,False | 0|1) //optional
            * maxbitrate  = (string) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(disable):
            disable = 1
        else:
            disable = 0
        data = {'action': 'user_update',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user_update')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def user_delete(self, username):
        """ user_delete
            MINIMUM_API_VERSION=400001

            Delete an existing user. @param array $input

            INPUTS
            * username    = (string) $username
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'user_delete',
                'auth': self.AMPACHE_SESSION,
                'username': username}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def user_preferences(self):
        """ user_preferences
            MINIMUM_API_VERSION=5.0.0

            Returns user_preferences

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'user_preferences',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user_preferences')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def user_preference(self, filter_str):
        """ user_preference
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'user_preferences',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'user_preferences')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def system_preferences(self):
        """ system_preferences
            MINIMUM_API_VERSION=5.0.0

            Returns system_preferences

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'system_preferences',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'system_preferences')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def system_preference(self, filter_str):
        """ system_preference
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'system_preferences',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'system_preferences')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def system_update(self):
        """ system_update
            MINIMUM_API_VERSION=5.0.0

            update ampache

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'system_update',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'system_update')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def preference_create(self, filter_str, type_str, default, category,
                          description=False, subcategory=False, level=100):
        """ preference_create
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
            * type_str    = (string) 'boolean', 'integer', 'string', 'special'
            * default     = (string|integer) default value
            * category    = (string) 'interface', 'internal', 'options', 'playlist', 'plugins', 'streaming', 'system'
            * description = (string) description of preference //optional
            * subcategory = (string) $subcategory //optional
            * level       = (integer) access level required to change the value (default 100) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'preference_create',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'preference_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def preference_edit(self, filter_str, value, apply_all=0):
        """ preference_edit
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
            * value       = (string|integer) Preference value
            * apply_all   = (boolean) apply to all users //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'preference_edit',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'value': value,
                'all': apply_all}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'preference_edit')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def preference_delete(self, filter_str):
        """ preference_delete
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'preference_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'preference_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def licenses(self, filter_str: str = False, exact: int = False,
                 add: int = False, update: int = False, offset=0, limit=0):
        """ licenses
            MINIMUM_API_VERSION=420000

            Returns licenses based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a license //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'licenses',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'licenses')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def license(self, filter_id: int):
        """ license
            MINIMUM_API_VERSION=420000

            returns a single license

            INPUTS
            * filter_id   = (integer) $license_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'license',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'license')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def license_songs(self, filter_id: int):
        """ license_songs
            MINIMUM_API_VERSION=420000

            returns a songs for a single license ID

            INPUTS
            * filter_id  = (integer) $license_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'license_songs',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'license_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def labels(self, filter_str: str = False, exact: int = False,
               offset=0, limit=0):
        """ labels
            MINIMUM_API_VERSION=420000

            Returns labels based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a label //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'labels',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'labels')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def label(self, filter_id: int):
        """ label
            MINIMUM_API_VERSION=420000

            returns a single label

            INPUTS
            * filter_id   = (integer) $label_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'label',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'label')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def label_artists(self, filter_id: int):
        """ label_artists
            MINIMUM_API_VERSION=420000

            returns a artists for a single label ID

            INPUTS
            * filter_id  = (integer) $label_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'label_artists',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'label_artists')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def get_bookmark(self, filter_id: str, object_type: str):
        """ get_bookmark
            MINIMUM_API_VERSION=5.0.0

            Get the bookmark from it's object_id and object_type.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'get_bookmark',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'get_bookmark')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def bookmarks(self):
        """ bookmarks
            MINIMUM_API_VERSION=5.0.0

            Get information about bookmarked media this user is allowed to manage.

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'bookmarks',
                'auth': self.AMPACHE_SESSION}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'bookmarks')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def bookmark_create(self, filter_id, object_type,
                        position: int = 0, client: str = 'AmpacheAPI', date=False):
        """ bookmark_create
            MINIMUM_API_VERSION=5.0.0

            Create a placeholder for the current media that you can return to later.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('song', 'video', 'podcast_episode')
            * position    = (integer) current track time in seconds
            * client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
            * date        = (integer) update time (Default: UNIXTIME()) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'bookmark_create',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'bookmark_create')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def bookmark_edit(self, filter_id, object_type,
                      position: int = 0, client: str = 'AmpacheAPI', date=False):
        """ bookmark_edit
            MINIMUM_API_VERSION=5.0.0

            Edit a placeholder for the current media that you can return to later.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('song', 'video', 'podcast_episode')
            * position    = (integer) current track time in seconds
            * client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
            * date        = (integer) update time (Default: UNIXTIME()) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'bookmark_edit',
                'auth': self.AMPACHE_SESSION,
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
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'bookmark_edit')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def bookmark_delete(self, filter_id: int, object_type=False):
        """ bookmark_delete
            MINIMUM_API_VERSION=5.0.0

            Delete an existing bookmark. (if it exists)

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('song', 'video', 'podcast_episode')
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'bookmark_delete',
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'bookmark_delete')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def deleted_songs(self, offset=0, limit=0):
        """ deleted_songs
            MINIMUM_API_VERSION=500000

            Returns deleted_song

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'deleted_songs',
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'deleted_songs')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

    def deleted_podcast_episodes(self, offset=0, limit=0):
        """ deleted_podcast_episodes
            MINIMUM_API_VERSION=500000

            Returns deleted_podcast_episode

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'deleted_podcast_episodes',
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'deleted_podcast_episodes')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)


    def deleted_videos(self, offset=0, limit=0):
        """ deleted_videos
            MINIMUM_API_VERSION=500000

            Returns deleted_video

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': 'deleted_videos',
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, 'deleted_videos')
        if not ampache_response:
            return False
        return self.return_data(ampache_response)

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
