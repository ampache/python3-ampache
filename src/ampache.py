#!/usr/bin/env python3


"""
Copyright (C)2024 Ampache.org
--------------------------------------------
Ampache XML and JSON Api library for python3
--------------------------------------------

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
import urllib.error
import urllib.parse
import urllib.request

from xml.etree import ElementTree

CLIENT_NAME = 'python3-ampache'


class API(object):

    def __init__(self):
        self.AMPACHE_API = 'xml'
        self.AMPACHE_VERSION = '6.9.0'
        self.AMPACHE_SERVER = ''
        self.AMPACHE_DEBUG = False
        self.DOCS_PATH = 'docs/'
        self.CONFIG_FILE = 'ampache.json'
        self.CONFIG_PATH = ''
        self.AMPACHE_URL = ''
        self.AMPACHE_SESSION = ''
        self.AMPACHE_USER = ''
        self.AMPACHE_KEY = ''
        self.AMPACHE_BEARER_TOKEN = ''
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

            Allow forcing a default API output format

            INPUTS
            * myformat = (string) 'xml'|'json'
        """
        if myformat == 'xml' or myformat == 'json':
            if self.AMPACHE_DEBUG:
                print('AMPACHE_API set to ' + myformat)
            self.AMPACHE_API = myformat

    def set_debug(self, mybool: bool):
        """ set_debug

            This function can be used to enable/disable debugging messages

            INPUTS
            * bool = (boolean) Enable/disable debug messages
        """
        if self.AMPACHE_DEBUG:
            if mybool:
                print('AMPACHE_DEBUG' + f": {self.OKGREEN}enabled{self.ENDC}")
            else:
                print('AMPACHE_DEBUG' + f": {self.WARNING}disabled{self.ENDC}")
        self.AMPACHE_DEBUG = mybool

    def set_debug_path(self, path_string: str):
        """ set_debug_path

        This function can be used to set the output folder for docs

        INPUTS
        * path_string = (string) folder path
        """
        self.DOCS_PATH = path_string

    def set_version(self, myversion: str):
        """ set_version

            Allow forcing a default API version

            api3 = '390001'
            api4 = '443000'
            api5 = '5.5.6'
            api6 = '6.6.0'

            INPUTS
            * myversion = (string) '6.6.0'|'390001'
        """
        if self.AMPACHE_DEBUG:
            print('AMPACHE_VERSION set to ' + myversion)
        self.AMPACHE_VERSION = myversion

    def set_user(self, myuser: str):
        """ set_user

            Set the user string for connection

            INPUTS
            * myuser = (string) ''
        """
        if self.AMPACHE_DEBUG:
            print('AMPACHE_USER set to ' + myuser)
        self.AMPACHE_USER = myuser

    def set_key(self, mykey: str):
        """ set_key

            set AMPACHE_KEY (api key or password)

            INPUTS
            * mykey = (string) ''
        """
        if self.AMPACHE_DEBUG:
            print('AMPACHE_KEY set to ' + mykey)
        self.AMPACHE_KEY = mykey

    def set_bearer_token(self, bearer_token: str):
        """ set_key

            set AMPACHE_BEARER_TOKEN (used for header authentication)

            INPUTS
            * bearer_token = (string) ''
        """
        if self.AMPACHE_DEBUG:
            print('AMPACHE_BEARER_TOKEN set to ' + bearer_token)
        self.AMPACHE_BEARER_TOKEN = bearer_token

    def set_url(self, myurl: str):
        """ set_url

            set the ampache url

            INPUTS
            * myurl = (string) ''
        """
        if self.AMPACHE_DEBUG:
            print('AMPACHE_URL set to ' + myurl)
        self.AMPACHE_URL = myurl

    def set_config_path(self, path: str):
        """ set_config_path

            Set the folder which contains your config to a folder instead of the working directory

            INPUTS
            * path = (string) ''
        """
        if not os.path.isdir(path):
            os.makedirs(path)
        self.CONFIG_PATH = path

    def get_config(self):
        """ get_config

            Read the config and set values from the json config file
        """
        output_file = os.path.join(self.CONFIG_PATH, self.CONFIG_FILE)
        if os.path.isfile(output_file):
            with open(output_file, 'r') as file:
                config = json.load(file)
            try:
                self.AMPACHE_URL = config["ampache_url"]
                self.AMPACHE_USER = config["ampache_user"]
                self.AMPACHE_KEY = config["ampache_apikey"]
                self.AMPACHE_BEARER_TOKEN = config["ampache_bearer_token"]
                self.AMPACHE_SESSION = config["ampache_session"]
                self.AMPACHE_API = config["api_format"]
            except TypeError:
                return False
            except IndexError:
                return False

            return True
        return False

    def save_config(self):
        """ save_config

            Save config to a json file for use later
        """
        config = {
            "ampache_url": self.AMPACHE_URL,
            "ampache_user": self.AMPACHE_USER,
            "ampache_apikey": self.AMPACHE_KEY,
            "ampache_bearer_token": self.AMPACHE_BEARER_TOKEN,
            "ampache_session": self.AMPACHE_SESSION,
            "api_format": self.AMPACHE_API
        }

        if self.CONFIG_PATH and not os.path.isdir(self.CONFIG_PATH):
            os.makedirs(self.CONFIG_PATH)
        output_file = os.path.join(self.CONFIG_PATH, self.CONFIG_FILE)
        with open(output_file, 'w') as file:
            json.dump(config, file)

    def test_result(self, result, title):
        """ test_result

            This function can be used to enable/disable debugging messages

            INPUTS
            * result = The response from the request
            * title = (string) generally the function name that was called
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
        """ return_data

            return json or xml data based on api format

            INPUTS
            * data = (string)
        """
        # json format
        if self.AMPACHE_API == 'json':
            try:
                json_data = data if isinstance(data, dict) else json.loads(data.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                return False
            return json_data
        # xml format
        else:
            try:
                tree = data if isinstance(data, ElementTree.Element) else ElementTree.fromstring(data.decode('utf-8') if isinstance(data, bytes) else data)
            except ElementTree.ParseError:
                return False
            return tree

    def get_id_list(self, data, attribute: str):
        """ get_id_list

            return a list of id's from the data you've got from the api

            INPUTS
            * data      = (mixed) XML or JSON from the API
            * attribute = (string) attribute you are searching for
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
                if data[attribute]:
                    try:
                        if data[attribute]['id']:
                            id_list.append(data[attribute]['id'])
                    except (KeyError, TypeError):
                        for data_object in data[attribute]:
                            try:
                                id_list.append(data_object[0]['id'])
                            except (KeyError, TypeError):
                                id_list.append(data_object['id'])
            except (KeyError, TypeError):
                try:
                    if data[0][attribute]:
                        try:
                            if data[0][attribute]['id']:
                                id_list.append(data[0][attribute]['id'])
                        except (KeyError, TypeError):
                            for data_object in data[0][attribute]:
                                try:
                                    id_list.append(data_object[0]['id'])
                                except (KeyError, TypeError):
                                    id_list.append(data_object['id'])
                except (KeyError, TypeError):
                    try:
                        if data[0][0][attribute]:
                            try:
                                if data[0][0][attribute]['id']:
                                    id_list.append(data[0][0][attribute]['id'])
                            except (KeyError, TypeError):
                                for data_object in data[0][0][attribute]:
                                    try:
                                        id_list.append(data_object[0]['id'])
                                    except (KeyError, TypeError):
                                        id_list.append(data_object['id'])
                                    try:
                                        id_list.append(data[0]['id'])
                                    except (KeyError, TypeError):
                                        id_list.append(data['id'])
                    except (KeyError, TypeError):
                        try:
                            if data[0]['id']:
                                for data_object in data:
                                    try:
                                        id_list.append(data_object[0]['id'])
                                    except (KeyError, TypeError):
                                        id_list.append(data_object['id'])
                                    try:
                                        id_list.append(data[0]['id'])
                                    except (KeyError, TypeError):
                                        id_list.append(data['id'])
                        except (KeyError, TypeError):
                            pass

        return id_list

    def get_object_list(self, data, field: str):
        """ get_id_list

            return a list of objects from the data matching your field stirng

            INPUTS
            * data        = (mixed) XML or JSON from the API
            * field       = (string) field you are searching for
            * data_format = (string) 'xml','json'
        """
        id_list = list()
        if self.AMPACHE_API == 'xml':
            return data.findall(field)
        else:
            if not data:
                return id_list
            try:
                for data_object in data[0][0][field]:
                    id_list.append(data_object)
            except KeyError:
                try:
                    for data_object in data[0][field]:
                        id_list.append(data_object)
                except KeyError:
                    try:
                        for data_object in data[field]:
                            id_list.append(data_object)
                    except (KeyError, TypeError):
                        id_list.append(data)

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
        """ get_message

            Return the string message text from the api response

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

    def fetch_url(self, full_url: str, api_format: str, method: str, headers: dict = None):
        """ fetch_url

            This function is used to fetch the string results using urllib

            INPUTS
            * full_url   = (string) url to fetch
            * api_format = (string) 'xml'|'json'
            * method     = (string)
            * headers    = (dict) optional HTTP headers
        """
        try:
            if not headers:
                req = urllib.request.Request(full_url)
            else:
                req = urllib.request.Request(full_url, headers=headers)
            result = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            return False
        except urllib.error.URLError:
            return False
        except ValueError:
            return False
        ampache_response = result.read()
        result.close()
        if self.AMPACHE_DEBUG:
            if self.DOCS_PATH == "docs/":
                self.DOCS_PATH = self.DOCS_PATH + api_format + "-responses/"
            url_response = ampache_response.decode('utf-8')
            print(url_response)
            print(full_url)
            try:
                if not os.path.isdir(self.DOCS_PATH):
                    os.makedirs(self.DOCS_PATH)
                text_file = open(self.DOCS_PATH + method + "." + api_format, "w", encoding="utf-8")
                text_file.write(url_response)
                text_file.close()
            except FileNotFoundError:
                pass
        return ampache_response

    def get_request(self, ampache_url, data, api_method):
        headers = {}
        if hasattr(self, 'AMPACHE_BEARER_TOKEN') and self.AMPACHE_BEARER_TOKEN:
            headers['Authorization'] = f'Bearer {self.AMPACHE_BEARER_TOKEN}'
            data.pop('auth', None)
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        request_response = self.fetch_url(full_url, self.AMPACHE_API, api_method, headers)
        if isinstance(request_response, bool):
            return False
        return self.return_data(request_response)

    """
    -------------
    API FUNCTIONS
    -------------
    """

    def handshake(self, ampache_url: str, ampache_api: str, ampache_user=False,
                  timestamp: int = 0, version: str = '6.6.0'):
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
        api_method = 'handshake'
        data = {'action': api_method,
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
        ampache_response = self.get_request(ampache_url, data, api_method)
        if isinstance(ampache_response, bool):
            return False
        # json format
        if self.AMPACHE_API == 'json':
            json_data = ampache_response if isinstance(ampache_response, dict) else json.loads(ampache_response.decode('utf-8'))
            if 'api' in json_data:
                self.AMPACHE_SERVER = json_data['api']
            if 'auth' in json_data:
                self.AMPACHE_SESSION = json_data['auth']
                return json_data['auth']
            else:
                self.AMPACHE_SESSION = False
                return False
        # xml format
        else:
            try:
                tree = ampache_response if isinstance(ampache_response, ElementTree.Element) else ElementTree.fromstring(ampache_response.decode('utf-8') if isinstance(ampache_response, bytes) else ampache_response)
            except ElementTree.ParseError:
                return False
            try:
                self.AMPACHE_SERVER = tree.find('api').text
            except AttributeError:
                pass
            try:
                token = tree.find('auth').text
            except AttributeError:
                token = False
            self.AMPACHE_SESSION = token
            return token

    def ping(self, ampache_url: str, ampache_api=False, version: str = '6.6.0'):
        """ ping
            MINIMUM_API_VERSION=380001

            This can be called without being authenticated, it is useful for determining if what the status
            of the server is, and what version it is running/compatible with

            INPUTS
            * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
            * ampache_api = (string) encrypted apikey //optional
        """
        ampache_url = ampache_url + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'ping'
        data = {'action': api_method,
                'version': version,
                'auth': ampache_api}
        if not ampache_api:
            data.pop('auth')
        ampache_response = self.get_request(ampache_url, data, api_method)
        if isinstance(ampache_response, bool):
            self.AMPACHE_SESSION = False
            return False
        # json format
        if self.AMPACHE_API == 'json':
            json_data = ampache_response if isinstance(ampache_response, dict) else json.loads(ampache_response.decode('utf-8'))
            if 'api' in json_data:
                self.AMPACHE_SERVER = json_data['api']
            if 'session_expire' in json_data:
                if not self.AMPACHE_URL:
                    self.AMPACHE_URL = ampache_url
                self.AMPACHE_SESSION = ampache_api
                return ampache_api
            else:
                self.AMPACHE_SESSION = False
                return False
        # xml format
        else:
            try:
                tree = ampache_response if isinstance(ampache_response, ElementTree.Element) else ElementTree.fromstring(ampache_response.decode('utf-8') if isinstance(ampache_response, bytes) else ampache_response)
            except ElementTree.ParseError:
                return False
            try:
                self.AMPACHE_SERVER = tree.find('api').text
            except AttributeError:
                pass
            try:
                token = tree.find('session_expire').text
                if token and not self.AMPACHE_URL:
                    self.AMPACHE_URL = ampache_url
                self.AMPACHE_SESSION = ampache_api
            except AttributeError:
                return False
            return ampache_api

    def register(self, username, fullname, password, email):
        """ register
            MINIMUM_API_VERSION=6.0.0

            Register a new user.
            Requires the username, password and email.

            INPUTS
            * username = (string) $username
            * fullname = (string) $fullname //optional
            * password = (string) hash('sha256', $password)
            * email    = (string) $email
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'register'
        data = {'action': api_method,
                'username': username,
                'fullname': fullname,
                'password': password,
                'email': email}
        return self.get_request(ampache_url, data, api_method)

    def lost_password(self, auth):
        """ lost_password
            MINIMUM_API_VERSION=6.1.0

            Allows a non-admin user to reset their password without web access to the main site.
            It requires a reset token hash using your username and email

            INPUTS
            * auth = (string) (
                $username;
                $key = hash('sha256', 'email');
                auth = hash('sha256', $username . $key);
              )
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'lost_password'
        data = {'action': api_method,
                'auth': auth}
        return self.get_request(ampache_url, data, api_method)

    def goodbye(self):
        """ goodbye
            MINIMUM_API_VERSION=400001

            Destroy session for ampache_api auth key.
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'goodbye'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

    def url_to_song(self, url):
        """ url_to_song
            MINIMUM_API_VERSION=380001

            This takes a url and returns the song object in question

            INPUTS
            * url = (string) Full Ampache URL from server, translates back into a song XML
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'url_to_song'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'url': url}
        return self.get_request(ampache_url, data, api_method)

    def get_similar(self, object_type, filter_id: int, offset=0, limit=0):
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
        api_method = 'get_similar'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    def list(self, object_type, filter_str=False, exact=False, add=False, update=False,
             offset=0, limit=0, sort=False, cond=False):
        """ list
            MINIMUM_API_VERSION=6.0.0

            This takes a named array of objects and returning `id`, `name`, `prefix` and `basename`

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'|'album_artist'|'playlist'
            * filter_str  = (string) search the name of the object_type //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'list'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_str,
                'exact': exact,
                'add': add,
                'update': update,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def browse(self, filter_str=False,
               object_type=False, catalog=False, add=False, update=False,
               offset=0, limit=0, sort=False, cond=False):
        """ browse
            MINIMUM_API_VERSION=6.0.0

            Return children of a parent object in a folder traversal/browse style
            If you don't send any parameters you'll get a catalog list (the 'root' path)

            INPUTS
            * filter_str  = (string) object_id //optional
            * object_type = (string) 'root', 'catalog', 'artist', 'album', 'podcast' // optional
            * catalog     = (integer) catalog ID you are browsing
            * add         = Api::set_filter(date) //optional
            * update      = Api::set_filter(date) //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'browse'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'type': object_type,
                'catalog': catalog,
                'add': add,
                'update': update,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not object_type:
            data.pop('type')
        if not catalog:
            data.pop('catalog')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def index(self, object_type, filter_str=False, exact=False, add=False, update=False,
              include=False, offset=0, limit=0, hide_search=False, sort=False, cond=False):
        """ index
            MINIMUM_API_VERSION=400001

            This takes a collection of inputs and return ID's for the object type
            Add 'include' to include child objects

            INPUTS
            * object_type = (string) 'catalog', 'song', 'album', 'artist', 'album_artist', 'song_artist', 'playlist', 'podcast', 'podcast_episode', 'share', 'video', 'live_stream'
            * filter_str  = (string) search the name of the object_type //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * include     = (integer) 0,1 include songs if available for that object //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * hide_search = (integer) 0,1, if true do not include searches/smartlists in the result //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include):
            include = 1
        api_method = 'index'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_str,
                'exact': exact,
                'add': add,
                'update': update,
                'include': include,
                'offset': str(offset),
                'limit': str(limit),
                'hide_search': hide_search,
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not include:
            data.pop('include')
        if not hide_search:
            data.pop('hide_search')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def get_indexes(self, object_type, filter_str=False, exact=False, add=False,
                    update=False, include=False, offset=0, limit=0, sort=False, cond=False):
        """ get_indexes
            MINIMUM_API_VERSION=400001

            This takes a collection of inputs and returns ID + name for the object type

            INPUTS
            * object_type = (string) 'catalog'|'album_artist'|'song_artist'|'song'|'album'|'artist'|'album_artist'|'playlist'
            * filter_str  = (string) search the name of the object_type //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add         = (integer) UNIXTIME() //optional
            * update      = (integer) UNIXTIME() //optional
            * include     = (integer) 0,1 include songs if available for that object //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'get_indexes'
        if bool(include):
            include = 1
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_str,
                'exact': exact,
                'add': add,
                'update': update,
                'include': include,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not include:
            data.pop('include')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def artists(self, filter_str=False, add=False, update=False,
                offset=0, limit=0, include=False, album_artist=False, sort=False, cond=False):
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
            * cond         = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort         = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        if bool(include) and not isinstance(include, str):
            include = 'albums,songs'
        api_method = 'artists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'add': add,
                'update': update,
                'offset': str(offset),
                'limit': str(limit),
                'include': include,
                'album_artist': album_artist,
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not include:
            data.pop('include')
        if not album_artist:
            data.pop('album_artist')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'artist'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def artist_albums(self, filter_id: int, offset=0, limit=0, album_artist=False,
                      sort=False, cond=False):
        """ artist_albums
            MINIMUM_API_VERSION=380001

            This returns the albums of an artist

            INPUTS
            * filter_id    = (integer) $artist_id
            * offset       = (integer) //optional
            * limit        = (integer) //optional
            * album_artist = (integer) 0,1, if true return albums where the UID is an album_artist of the object //optional
            * cond         = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort         = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'artist_albums'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'album_artist': album_artist,
                'sort': sort,
                'cond': cond}
        if not album_artist:
            data.pop('album_artist')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def artist_songs(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ artist_songs
            MINIMUM_API_VERSION=380001

            This returns the songs of the specified artist

            INPUTS
            * filter_id = (integer) $artist_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'artist_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def albums(self, filter_str=False,
               exact=False, add=False, update=False, offset=0, limit=0,
               include=False, sort=False, cond=False):
        """ albums
            MINIMUM_API_VERSION=380001

            This returns albums based on the provided search filters

            INPUTS
            * filter_str = (string) search the name of an album //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add        = (integer) UNIXTIME() //optional
            * update     = (integer) UNIXTIME() //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * include    = (string) 'songs' //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'albums'
        if bool(include) and not isinstance(include, str):
            include = 'songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'add': add,
                'update': update,
                'offset': str(offset),
                'limit': str(limit),
                'include': include,
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not include:
            data.pop('include')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def album(self, filter_id: int, include=False):
        """ album
            MINIMUM_API_VERSION=380001

            This returns a single album based on the UID provided

            INPUTS
            * filter_id   = (integer) $album_id
            * include     = (string) 'songs' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'album'
        if bool(include) and not isinstance(include, str):
            include = 'songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def album_songs(self, filter_id: int, offset=0, limit=0,
                    exact=False, sort=False, cond=False):
        """ album_songs
            MINIMUM_API_VERSION=380001

            This returns the songs of a specified album

            INPUTS
            * filter_id = (integer) $album_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * exact     = (integer) 0,1, if true don't group songs from different disks //optional (IGNORED IN API6)
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'album_songs'
        if bool(exact):
            exact = 1
        else:
            exact = 0
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def genres(self, filter_str=False,
               exact=False, offset=0, limit=0, sort=False, cond=False):
        """ genres
            MINIMUM_API_VERSION=380001

            This returns the genres (Tags) based on the specified filter

            INPUTS
            * filter_str = (string) search the name of a genre //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'genres'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def genre(self, filter_id: int):
        """ genre
            MINIMUM_API_VERSION=380001

            This returns a single genre based on UID

            INPUTS
            * filter_id = (integer) $genre_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'genre'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def genre_artists(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ genre_artists
            MINIMUM_API_VERSION=380001

            This returns the artists associated with the genre in question as defined by the UID

            INPUTS
            * filter_id = (integer) $genre_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'genre_artists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def genre_albums(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ genre_albums
            MINIMUM_API_VERSION=380001

            This returns the albums associated with the genre in question

            INPUTS
            * filter_id = (integer) $genre_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'genre_albums'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def genre_songs(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ genre_songs
            MINIMUM_API_VERSION=380001

            returns the songs for this genre

            INPUTS
            * filter_id = (integer) $genre_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'genre_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def songs(self, filter_str=False, exact=False, add=False, update=False,
              offset=0, limit=0, sort=False, cond=False):
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
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'exact': exact,
                'add': add,
                'update': update,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def song(self, filter_id: int):
        """ song
            MINIMUM_API_VERSION=380001

            returns a single song

            INPUTS
            * filter_id  = (integer) $song_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'song'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def song_delete(self, filter_id: int):
        """ song_delete
            MINIMUM_API_VERSION=5.0.0

            Delete an existing song.

            INPUTS
            * filter_id   = (string) UID of song to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'song_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def song_tags(self, filter_id: int):
        """ song_tags
            MINIMUM_API_VERSION=7.5.0

            Get the full song file tags using VaInfo
            This is used to get tags for remote catalogs to allow maximum data to be returned

            INPUTS
            * filter_id   = (string) UID of song to fetch
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'song_tags'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def user_playlists(self, filter_str=False, exact=False, offset=0, limit=0,
                       sort=False, cond=False, include=False):
        """ user_playlists
            MINIMUM_API_VERSION=6.3.0

            This returns playlists based on the specified filter (Does not include searches / smartlists)

            INPUTS
            * filter_str = (string) search the name of a playlist //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
            * include    = (integer) 0,1, if true include playlist contents
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_playlists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond,
                'include': include}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def user_smartlists(self, filter_str=False, exact=False, offset=0, limit=0,
                        sort=False, cond=False, include=False):
        """ user_smartlists
            MINIMUM_API_VERSION=6.3.0

            This returns smartlists (searches) based on the specified filter (Does not include playlists)

            INPUTS
            * filter_str = (string) search the name of a playlist //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
            * include    = (integer) 0,1, if true include playlist contents
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_smartlists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond,
                'include': include}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def playlists(self, filter_str=False, exact=False, offset=0, limit=0, hide_search=False,
                  show_dupes=False, include=False, sort=False, cond=False):
        """ playlists
            MINIMUM_API_VERSION=380001

            This returns playlists based on the specified filter

            INPUTS
            * filter_str  = (string) search the name of a playlist //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * hide_search = (integer) 0,1, if true do not include searches/smartlists in the result //optional
            * show_dupes  = (integer) 0,1, if true ignore 'api_hide_dupe_searches' setting //optional
            * include     = (integer) 0,1, if true include the objects in the playlist //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'hide_search': hide_search,
                'show_dupes': show_dupes,
                'include': include,
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not hide_search:
            data.pop('hide_search')
        if not show_dupes:
            data.pop('show_dupes')
        if not include:
            data.pop('include')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def playlist(self, filter_id: int):
        """ playlist
            MINIMUM_API_VERSION=380001

            This returns a single playlist

            INPUTS
            * filter_id  = (integer) $playlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def playlist_hash(self, filter_id: int):
        """ playlist_hash
            MINIMUM_API_VERSION=6.6.0

            his returns the md5 hash for the songs in a playlist

            INPUTS
            filter_id = (string) UID of playlist
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_hash'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def playlist_songs(self, filter_id: int, random=False, offset=0, limit=0):
        """ playlist_songs
            MINIMUM_API_VERSION=380001

            This returns the songs for a playlist

            INPUTS
            * filter_id   = (integer) $playlist_id
            * random      = (integer) 0,1, if true get random songs using limit //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'random': random,
                'offset': str(offset),
                'limit': str(limit)}
        if not random:
            data.pop('random')
        return self.get_request(ampache_url, data, api_method)

    def playlist_create(self, playlist_name, playlist_type):
        """ playlist_create
            MINIMUM_API_VERSION=380001

            This create a new playlist and return it

            INPUTS
            * playlist_name = (string)
            * playlist_type = (string) public | private
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_create'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'name': playlist_name,
                'type': playlist_type}
        return self.get_request(ampache_url, data, api_method)

    def playlist_edit(self, filter_id: int, playlist_name=False,
                      playlist_type=False, owner=False, items=False, tracks=False):
        """ playlist_edit
            MINIMUM_API_VERSION=400001

            This modifies name and type of a playlist

            INPUTS
            * filter_id     = (integer)
            * playlist_name = (string) playlist name //optional
            * playlist_type = (string) 'public'|'private' //optional
            * owner         = (string) Change playlist owner to the user id (-1 = System playlist) //optional
            * items         = (string) comma-separated song_id's (replaces existing items with a new id) //optional
            * tracks        = (string) comma-separated playlisttrack numbers matched to 'items' in order //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_edit'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'name': playlist_name,
                'type': playlist_type,
                'owner': owner,
                'items': items,
                'tracks': tracks}
        if not playlist_name:
            data.pop('name')
        if not playlist_type:
            data.pop('type')
        if not owner:
            data.pop('owner')
        if not items:
            data.pop('items')
        if not tracks:
            data.pop('tracks')
        return self.get_request(ampache_url, data, api_method)

    def playlist_delete(self, filter_id: int):
        """ playlist_delete
            MINIMUM_API_VERSION=380001

            This deletes a playlist

            INPUTS
            * filter_id   = (integer) $playlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def playlist_add(self, filter_id: int, object_id: int, object_type: str):
        """ playlist_add
            MINIMUM_API_VERSION=6.3.0

            This adds a song to a playlist, allowing different song parent types

            INPUTS
            * filter = (int) UID of playlist
            * id     = (int) $object_id
            * type   = (string) 'song', 'album', 'artist', 'playlist'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'playlist_add'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'id': object_id,
                'type': object_type}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'playlist_add_song'
        if bool(check):
            check = 1
        else:
            check = 0
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'song': song_id,
                'filter': filter_id,
                'check': check}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'playlist_remove_song'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'song': song_id,
                'track': track}
        if not song_id:
            data.pop('song')
        if not track:
            data.pop('track')
        return self.get_request(ampache_url, data, api_method)

    def playlist_generate(self, mode='random',
                          filter_str=False, album_id=False, artist_id=False, flagged=False,
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
        api_method = 'playlist_generate'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def smartlists(self, filter_str=False, exact=False, offset=0, limit=0, include=False, sort=False, cond=False):
        """ smartlists
            MINIMUM_API_VERSION=380001

            This returns smartlists based on the specified filter

            INPUTS
            * filter_str  = (string) search the name of a smartlist //optional
            * exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * include     = (integer) 0,1, if true include the objects in the smartlist //optional
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'smartlists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'include': include,
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not include:
            data.pop('include')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def smartlist(self, filter_id: int):
        """ smartlist
            MINIMUM_API_VERSION=380001

            This returns a single smartlist

            INPUTS
            * filter_id  = (integer) $smartlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'smartlist'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def smartlist_songs(self, filter_id: int, random=False, offset=0, limit=0):
        """ smartlist_songs
            MINIMUM_API_VERSION=380001

            This returns the songs for a smartlist

            INPUTS
            * filter_id   = (integer) $smartlist_id
            * random      = (integer) 0,1, if true get random songs using limit //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'smartlist_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'random': random,
                'offset': str(offset),
                'limit': str(limit)}
        if not random:
            data.pop('random')
        return self.get_request(ampache_url, data, api_method)

    def smartlist_delete(self, filter_id: int):
        """ smartlist_delete
            MINIMUM_API_VERSION=380001

            This deletes a smartlist

            INPUTS
            * filter_id   = (integer) $smartlist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'smartlist_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def shares(self, filter_str=False,
               exact=False, offset=0, limit=0, sort=False, cond=False):
        """ shares
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str = (string) search the name of a share //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'shares'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def share(self, filter_id: int):
        """ share
            MINIMUM_API_VERSION=420000

            Return shares by UID

            INPUTS
            * filter_id   = (integer) UID of Share
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'share'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'share_create'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type,
                'description': description,
                'expires': expires}
        if not description:
            data.pop('description')
        if not expires:
            data.pop('expires')
        return self.get_request(ampache_url, data, api_method)

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
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'share_edit'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def share_delete(self, filter_id: int):
        """ share_delete
            MINIMUM_API_VERSION=420000

            Delete an existing share.

            INPUT
            * filter_id   = (integer) UID of Share to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'share_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def catalogs(self, filter_str=False, offset=0, limit=0, sort=False, cond=False):
        """ catalogs
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str = (string) search the name of a catalog //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalogs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def catalog(self, filter_id: int, offset=0, limit=0):
        """ catalog
            MINIMUM_API_VERSION=420000

            Return catalogs by UID

            INPUTS
            * filter_id   = (integer) UID of catalog
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalog'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    def catalog_add(self, cat_name, cat_path, cat_type=False, media_type=False, file_pattern=False,
                    folder_pattern=False, username=False, password=False):
        """ catalog_add
            MINIMUM_API_VERSION=6.0.0

            Create a new catalog

            INPUTS
            * name           = (string) catalog_name
            * path           = (string) URL or folder path for your catalog
            * type           = (string) catalog_type default: local ('local', 'beets', 'remote', 'subsonic', 'seafile', 'beetsremote') //optional
            * media_type     = (string) Default: 'music' ('music', 'podcast', 'clip', 'tvshow', 'movie', 'personal_video') //optional
            * file_pattern   = (string) Pattern used identify tags from the file name. Default '%T - %t' //optional
            * folder_pattern = (string) Pattern used identify tags from the folder name. Default '%a/%A' //optional
            * username       = (string) login to remote catalog ('remote', 'subsonic', 'seafile') //optional
            * password       = (string) password to remote catalog ('remote', 'subsonic', 'seafile', 'beetsremote') //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalog_add'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'name': cat_name,
                'path': cat_path,
                'type': cat_type,
                'media_type': media_type,
                'file_pattern': file_pattern,
                'folder_pattern': folder_pattern,
                'username': username,
                'password': password}
        if not cat_type:
            data.pop('type')
        if not media_type:
            data.pop('media_type')
        if not file_pattern:
            data.pop('file_pattern')
        if not folder_pattern:
            data.pop('folder_pattern')
        if not username:
            data.pop('username')
        if not password:
            data.pop('password')
        return self.get_request(ampache_url, data, api_method)

    def catalog_delete(self, filter_id: int):
        """ catalog_delete
            MINIMUM_API_VERSION=6.0.0

            Delete an existing catalog. (if it exists)

            INPUTS
            * filter = (string) catalog_id to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalog_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def catalog_action(self, task, catalog_id):
        """ catalog_action
            MINIMUM_API_VERSION=400001

            Kick off a catalog update or clean for the selected catalog

            INPUTS
            * task        = (string) 'add_to_catalog'|'clean_catalog'|'verify_catalog'|'gather_art'
            * catalog_id  = (integer) $catalog_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalog_action'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'task': task,
                'catalog': catalog_id}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'catalog_file'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'file': file,
                'task': task,
                'catalog': catalog_id}
        return self.get_request(ampache_url, data, api_method)

    def catalog_folder(self, folder, task, catalog_id):
        """ catalog_folder
            MINIMUM_API_VERSION=6.0.0

            Perform actions on local catalog folders.
            Single folder versions of catalog add, clean and verify.
            Make sure you remember to urlencode those folder names!

            INPUTS
            * folder        = (string) urlencode(FULL path to local folder)
            * task        = (string) 'add'|'clean'|'verify'|'remove'
            * catalog_id  = (integer) $catalog_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'catalog_folder'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'folder': folder,
                'task': task,
                'catalog': catalog_id}
        return self.get_request(ampache_url, data, api_method)

    def podcasts(self, filter_str=False,
                 exact=False, offset=0, limit=0, sort=False, cond=False):
        """ podcasts
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_str = (string) search the name of a podcast //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcasts'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def podcast(self, filter_id: int, include=False):
        """ podcast
            MINIMUM_API_VERSION=420000

            Return podcasts by UID

            INPUTS
            * filter_id   = (integer) UID of Podcast
            * include     = (string) 'episodes' Include episodes with the response //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def podcast_create(self, url, catalog_id):
        """ podcast_create
            MINIMUM_API_VERSION=420000

            Return podcasts by UID

            INPUTS
            * url         = (string) rss url for podcast
            * catalog_id  = (string) podcast catalog
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_create'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'url': url,
                'catalog': catalog_id}
        return self.get_request(ampache_url, data, api_method)

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
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_edit'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def podcast_delete(self, filter_id: int):
        """ podcast_delete
            MINIMUM_API_VERSION=420000

            Delete an existing podcast.

            INPUTS
            * filter_id   = (integer) UID of podcast to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def podcast_episodes(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ podcast_episodes
            MINIMUM_API_VERSION=420000

            INPUTS
            * filter_id = (string) UID of podcast
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_episodes'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def podcast_episode(self, filter_id: int):
        """ podcast_episode
            MINIMUM_API_VERSION=420000

            Return podcast_episodes by UID

            INPUTS
            * filter_id   = (integer) UID of Podcast
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_episode'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def podcast_episode_delete(self, filter_id: int):
        """ podcast_episode_delete
            MINIMUM_API_VERSION=420000

            Delete an existing podcast_episode.

            INPUTS
            * filter_id   = (integer) UID of podcast_episode to delete
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'podcast_episode_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def update_podcast(self, filter_id: int):
        """ update_podcast
            MINIMUM_API_VERSION=420000

            Sync and download new podcast episodes

            INPUTS
            * filter_id   = (integer) UID of Podcast
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'update_podcast'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'search_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    def search_rules(self, filter_str):
        """ search_rules
            MINIMUM_API_VERSION=6.8.0

            Print a list of valid search rules for your search type

            INPUTS
            * filter_str = (string) 'song', 'album', 'song_artist', 'album_artist', 'artist', 'label', 'playlist', 'podcast', 'podcast_episode', 'genre', 'user', 'video'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'search_rules'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        return self.get_request(ampache_url, data, api_method)

    def search(self, rules, operator='and', object_type='song', offset=0, limit=0, random=0):
        """ search
            MINIMUM_API_VERSION=380001

            Perform an advanced search given passed rules
            the rules can occur multiple times and are joined by the operator item.

            Refer to the wiki for further information
            http://ampache.org/api/api-advanced-search

            INPUTS
            * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input],[rule_2,rule_2_operator,rule_2_input],[etc]]
            * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
            * object_type = (string)  //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * random      = (integer) 0|1' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'search'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def search_group(self, rules,
                     operator='and', object_type='all', offset=0, limit=0, random=0):
        """ search_group
            MINIMUM_API_VERSION=6.3.0

            Perform a search given passed rules and return matching objects in a group.
            If the rules to not exist for the object type or would return the entire table they will not return objects

            Refer to the wiki for further information on rule_* types and data
            https://ampache.org/api/api-xml-methods
            https://ampache.org/api/api-json-methods

            INPUTS
            * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input],[rule_2,rule_2_operator,rule_2_input],[etc]]
            * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
            * object_type = (string)  //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * random      = (integer) 0|1' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'search_group'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def videos(self, filter_str=False,
               exact=False, offset=0, limit=0, sort=False, cond=False):
        """ videos
            MINIMUM_API_VERSION=380001

            This returns video objects!

            INPUTS
            * filter_str = (string) search the name of a video //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'videos'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'exact': exact,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def video(self, filter_id: int):
        """ video
            MINIMUM_API_VERSION=380001

            This returns a single video

            INPUTS
            * filter_id   = (integer) $video_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'video'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def localplay(self, command, oid=False, otype=False, clear=False):
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
        api_method = 'localplay'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'command': command,
                'oid': oid,
                'type': otype,
                'clear': clear}
        if not oid:
            data.pop('oid')
        if not otype:
            data.pop('type')
        if not clear:
            data.pop('clear')
        return self.get_request(ampache_url, data, api_method)

    def localplay_songs(self):
        """ localplay_songs
            MINIMUM_API_VERSION=5.0.0

            Get the list of songs in your localplay playlist
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'localplay_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

    def democratic(self, method, oid):
        """ democratic
            MINIMUM_API_VERSION=380001

            This is for controlling democratic play

            INPUTS
            * oid         = (integer) object_id (song_id|playlist_id)
            * method      = (string) 'vote'|'devote'|'playlist'|'play'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'democratic'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'oid': oid,
                'method': method}
        return self.get_request(ampache_url, data, api_method)

    def stats(self, object_type, filter_str='random',
              username=False, user_id=False, offset=0, limit=0, sort=False, cond=False):
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
            * cond        = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort        = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'stats'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'filter': filter_str,
                'offset': offset,
                'limit': limit,
                'user_id': user_id,
                'username': username,
                'sort': sort,
                'cond': cond}
        if not username:
            data.pop('username')
        if not user_id:
            data.pop('user_id')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def users(self, sort=False, cond=False):
        """ users
            MINIMUM_API_VERSION=5.0.0

            Get ids and usernames for your site users

            INPUTS
            * cond = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'users'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def user(self, username: str):
        """ user
            MINIMUM_API_VERSION=380001

            This get an user public information

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username}
        return self.get_request(ampache_url, data, api_method)

    def followers(self, username: str, sort=False, cond=False):
        """ followers
            MINIMUM_API_VERSION=380001

            This get an user followers

            INPUTS
            * username =
            * cond     = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort     = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'followers'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def following(self, username: str):
        """ following
            MINIMUM_API_VERSION=380001

            This get the user list followed by an user

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'following'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username}
        return self.get_request(ampache_url, data, api_method)

    def toggle_follow(self, username: str):
        """ toggle_follow
            MINIMUM_API_VERSION=380001

            This follow/unfollow an user

            INPUTS
            * username    =
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'toggle_follow'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username}
        return self.get_request(ampache_url, data, api_method)

    def last_shouts(self, username, limit=0):
        """ last_shouts
            MINIMUM_API_VERSION=380001

            This get the latest posted shouts

            INPUTS
            * username    =
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'last_shouts'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'limit': limit}
        return self.get_request(ampache_url, data, api_method)

    def player(self, filter_str, object_type='song', state='play', play_time=0, client=CLIENT_NAME):
        """ player
            MINIMUM_API_VERSION=6.4.0

            Inform the server about the state of your client. (Song you are playing, Play/Pause state, etc.)

            filter_str  = (integer) $object_id
            object_type = (string)  $object_type ('song', 'podcast_episode', 'video'), DEFAULT 'song'//optional
            state       = (string)  'play', 'stop', DEFAULT 'play' //optional
            play_time   = (integer) current song time in whole seconds, DEFAULT 0 //optional
            client      = (string)  $agent, DEFAULT 'python3-ampache' //optional
        """
        action = self.player.__name__
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        data = {'action': action,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'type': object_type,
                'state': state,
                'time': play_time,
                'client': client}
        headers = {}
        if hasattr(self, 'AMPACHE_BEARER_TOKEN') and self.AMPACHE_BEARER_TOKEN:
            headers['Authorization'] = f'Bearer {self.AMPACHE_BEARER_TOKEN}'
            data.pop('auth', None)
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        ampache_response = self.fetch_url(full_url, self.AMPACHE_API, action)
        if isinstance(ampache_response, bool):
            return False
        return self.return_data(ampache_response)

    def now_playing(self):
        """  now_playing
             MINIMUM_API_VERSION=6.3.1

             Get what is currently being played by all users.
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'now_playing'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

    def rate(self, object_type, object_id, rating):
        """ rate
            MINIMUM_API_VERSION=380001

            This rates a library item

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'
            * object_id   = (integer) $object_id
            * rating      = (integer) 0|1|2|3|4|5
        """
        if isinstance(rating, str):
            if rating.isdigit():
                rating = int(rating)
            else:
                rating = -1
        if (rating < 0 or rating > 5) or not (
                object_type == 'song' or object_type == 'album' or object_type == 'artist'):
            return False
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'rate'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id,
                'rating': rating}
        return self.get_request(ampache_url, data, api_method)

    def flag(self, object_type, object_id, flagbool, date=False):
        """ flag
            MINIMUM_API_VERSION=400001

            This flags a library item as a favorite

            Setting flagbool to true (1) will set the flag
            Setting flagbool to false (0) will remove the flag

            INPUTS
            * object_type = (string) 'song'|'album'|'artist'
            * object_id   = (integer) $object_id
            * flagbool    = (boolean|integer) (True,False | 0|1)
            * date        = (integer) UNIXTIME() //optional
        """
        if bool(flagbool):
            flag_state = 1
        else:
            flag_state = 0
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'flag'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id,
                'flag': flag_state,
                'date': date}
        if not date:
            data.pop('date')
        return self.get_request(ampache_url, data, api_method)

    def record_play(self, object_id, user_id=False, client=CLIENT_NAME, date=False):
        """ record_play
            MINIMUM_API_VERSION=400001

            Take a song_id and update the object_count and user_activity table with a play.
            This allows other sources to record play history to ampache

            INPUTS
            * object_id   = (integer) $object_id
            * user_id     = (integer) $user_id //optional
            * client      = (string) $agent //optional
            * date        = (integer) UNIXTIME() //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'record_play'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'user': user_id,
                'client': client,
                'date': date}
        if not user_id:
            data.pop('user')
        if not date:
            data.pop('date')
        return self.get_request(ampache_url, data, api_method)

    def scrobble(self, title, artist_name, album_name,
                 mbtitle=False, mbartist=False, mbalbum=False, stime=False,
                 client=CLIENT_NAME):
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
        api_method = 'scrobble'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'client': client,
                'date': str(stime),
                'song': title,
                'artist': artist_name,
                'album': album_name,
                'songmbid': mbtitle,
                'albummbid': mbalbum,
                'artistmbid': mbartist}
        if not mbtitle:
            data.pop('songmbid')
        if not mbalbum:
            data.pop('albummbid')
        if not mbartist:
            data.pop('artistmbid')
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'timeline'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'limit': limit,
                'since': since}
        return self.get_request(ampache_url, data, api_method)

    def friends_timeline(self, limit=0, since=0):
        """ friends_timeline
            MINIMUM_API_VERSION=380001

            This get current user friends timeline

            INPUTS
            * limit       = (integer) //optional
            * since       = (integer) UNIXTIME() //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'friends_timeline'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'limit': limit,
                'since': since}
        return self.get_request(ampache_url, data, api_method)

    def update_from_tags(self, object_type, object_id):
        """ update_from_tags
            MINIMUM_API_VERSION=400001

            updates a single album,artist,song from the tag data

            INPUTS
            * object_type = (string) 'artist'|'album'|'song'
            * object_id   = (integer) $artist_id, $album_id, $song_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'update_from_tags'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id}
        return self.get_request(ampache_url, data, api_method)

    def update_art(self, object_type, object_id, overwrite=False):
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
        api_method = 'update_art'
        if bool(overwrite):
            overwrite = 1
        else:
            overwrite = 0
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'type': object_type,
                'id': object_id,
                'overwrite': overwrite}
        return self.get_request(ampache_url, data, api_method)

    def update_artist_info(self, filter_id):
        """ update_artist_info
            MINIMUM_API_VERSION=400001

            Update artist information and fetch similar artists from last.fm
            Make sure lastfm_api_key is set in your configuration file

            INPUTS
            * filter_id = (integer) $artist_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'update_artist_info'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'id': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def stream(self, object_id, object_type, destination, stats=1):
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
        api_method = 'stream'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type,
                'stats': stats}
        headers = {}
        if hasattr(self, 'AMPACHE_BEARER_TOKEN') and self.AMPACHE_BEARER_TOKEN:
            headers['Authorization'] = f'Bearer {self.AMPACHE_BEARER_TOKEN}'
            data.pop('auth', None)
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def download(self, object_id, object_type, destination,
                 transcode='raw', bitrate=False, stats=1):
        """ download
            MINIMUM_API_VERSION=400001

            download a song or podcast episode

            INPUTS
            * object_id   = (string) $song_id / $podcast_episode_id / $search_id / $playlist_id
            * object_type = (string) 'song'|'podcast'|'search'|'playlist'
            * destination = (string) full file path
            * transcode   = (string) 'mp3', 'ogg', etc. ('raw' / original by default) //optional SONG ONLY
            * bitrate     = (integer) max bitrate for transcoding, '128', '256' //optional SONG ONLY
        """
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'download'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type,
                'format': transcode,
                'bitrate': bitrate,
                'stats': stats}
        if not bitrate:
            data.pop('bitrate')
        headers = {}
        if hasattr(self, 'AMPACHE_BEARER_TOKEN') and self.AMPACHE_BEARER_TOKEN:
            headers['Authorization'] = f'Bearer {self.AMPACHE_BEARER_TOKEN}'
            data.pop('auth', None)
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def get_external_metadata(self, filter_id, object_type):
        """ get_external_metadata
            MINIMUM_API_VERSION=400001

            get data from metadata plugins

            INPUTS
            * filter_id   = (string) $song_id / $album_id / $artist_id
            * object_type = (string) 'song', 'artist', 'album'
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'get_external_metadata'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type}
        return self.get_request(ampache_url, data, api_method)

    def get_lyrics(self, filter_id, plugins=False):
        """ get_lyrics
            MINIMUM_API_VERSION=6.9.0

            Return Database lyrics or search with plugins by Song id

            INPUTS
            * filter_id = (string) $song_id / $album_id / $artist_id
            * plugins   = (int) 0,1, if false disable plugin lookup (Default: 1)
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'get_lyrics'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'plugins': plugins}
        if not plugins:
            data.pop('plugins')
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'get_art'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'id': object_id,
                'type': object_type}
        headers = {}
        if hasattr(self, 'AMPACHE_BEARER_TOKEN') and self.AMPACHE_BEARER_TOKEN:
            headers['Authorization'] = f'Bearer {self.AMPACHE_BEARER_TOKEN}'
            data.pop('auth', None)
        data = urllib.parse.urlencode(data)
        full_url = ampache_url + '?' + data
        result = requests.get(full_url, allow_redirects=True)
        open(destination, 'wb').write(result.content)
        return True

    def user_create(self, username: str, password: str, email: str,
                    fullname=False, disable=False):
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
        api_method = 'user_create'
        if bool(disable):
            disable = 1
        else:
            disable = 0
        if hashlib.sha256(password.encode()).hexdigest() != password:
            password = hashlib.sha256(password.encode()).hexdigest()
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'password': password,
                'email': email,
                'fullname': fullname,
                'disable': disable}
        if not fullname:
            data.pop('fullname')
        return self.get_request(ampache_url, data, api_method)

    def user_edit(self, username, password=False, fullname=False, email=False,
                  website=False, state=False, city=False, disable=False, maxbitrate=False,
                  fullname_public=False, reset_apikey=False, reset_streamtoken=False, clear_stats=False):
        """ user_edit
            MINIMUM_API_VERSION=6.0.0

            Update an existing user. @param array $input

            INPUTS
            * username          = (string) $username
            * password          = (string) hash('sha256', $password)) //optional
            * fullname          = (string) $fullname //optional
            * email             = (string) $email //optional
            * website           = (string) $website //optional
            * state             = (string) $state //optional
            * city              = (string) $city //optional
            * disable           = (integer) 0,1 true to disable the user (if enabled) //optional
            * group             = (integer) Catalog filter group for the new user //optional, default = 0
            * maxbitrate        = (integer) $maxbitrate //optional
            * fullname_public   = (integer) 0,1 true to enable, false to disable using fullname in public display //optional
            * reset_apikey      = (integer) 0,1 true to reset a user Api Key //optional
            * reset_streamtoken = (integer) 0,1 true to reset a user Stream Token //optional
            * clear_stats       = (integer) 0,1 true reset all stats for this user //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_edit'
        if bool(disable):
            disable = 1
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username,
                'password': password,
                'fullname': fullname,
                'email': email,
                'website': website,
                'state': state,
                'city': city,
                'disable': disable,
                'maxbitrate': maxbitrate,
                'fullname_public': fullname_public,
                'reset_apikey': reset_apikey,
                'reset_streamtoken': reset_streamtoken,
                'clear_stats': clear_stats}
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
        if not fullname_public:
            data.pop('fullname_public')
        if not reset_apikey:
            data.pop('reset_apikey')
        if not reset_streamtoken:
            data.pop('reset_streamtoken')
        if not clear_stats:
            data.pop('clear_stats')
        return self.get_request(ampache_url, data, api_method)

    def user_delete(self, username: str):
        """ user_delete
            MINIMUM_API_VERSION=400001

            Delete an existing user. @param array $input

            INPUTS
            * username    = (string) $username
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'username': username}
        return self.get_request(ampache_url, data, api_method)

    def user_preferences(self):
        """ user_preferences
            MINIMUM_API_VERSION=5.0.0

            Returns user_preferences

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_preferences'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

    def user_preference(self, filter_str):
        """ user_preference
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'user_preference'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        return self.get_request(ampache_url, data, api_method)

    def system_preferences(self):
        """ system_preferences
            MINIMUM_API_VERSION=5.0.0

            Returns system_preferences

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'system_preferences'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

    def system_preference(self, filter_str):
        """ system_preference
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'system_preference'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        return self.get_request(ampache_url, data, api_method)

    def system_update(self):
        """ system_update
            MINIMUM_API_VERSION=5.0.0

            update ampache

            INPUTS
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'system_update'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION}
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'preference_create'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

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
        api_method = 'preference_edit'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'value': value,
                'all': apply_all}
        return self.get_request(ampache_url, data, api_method)

    def preference_delete(self, filter_str):
        """ preference_delete
            MINIMUM_API_VERSION=5.0.0

            Returns preference based on the specified filter_str

            INPUTS
            * filter_str  = (string) search the name of a preference
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'preference_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str}
        return self.get_request(ampache_url, data, api_method)

    def licenses(self, filter_str=False, exact=False, add=False, update=False,
                 offset=0, limit=0, sort=False, cond=False):
        """ licenses
            MINIMUM_API_VERSION=420000

            Returns licenses based on the specified filter_str

            INPUTS
            * filter_str = (string) search the name of a license //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * add        = (integer) UNIXTIME() //optional
            * update     = (integer) UNIXTIME() //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'licenses'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'exact': exact,
                'add': add,
                'update': update,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not add:
            data.pop('add')
        if not update:
            data.pop('update')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def license(self, filter_id: int):
        """ license
            MINIMUM_API_VERSION=420000

            returns a single license

            INPUTS
            * filter_id   = (integer) $license_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'license'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def license_songs(self, filter_id: int, sort=False, cond=False):
        """ license_songs
            MINIMUM_API_VERSION=420000

            returns a songs for a single license ID

            INPUTS
            * filter_id = (integer) $license_id
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'license_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def live_streams(self, filter_str=False,
                     exact=False, offset=0, limit=0, sort=False, cond=False):
        """ live_streams
            MINIMUM_API_VERSION=5.1.0

            Returns live_streams based on the specified filter_str

            INPUTS
            * filter_str = (string) search the name of a live_stream //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'live_streams'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'exact': exact,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def live_stream(self, filter_id: int):
        """ live_stream
            MINIMUM_API_VERSION=5.1.0

            Returns a single live_stream based on UID

            INPUTS
            * filter_id   = (integer) $live_stream_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'live_stream'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def live_stream_create(self, name: str, stream_url: str, codec: str, catalog_id: int, site_url: str = ''):
        """ live_stream_create
            MINIMUM_API_VERSION=6.0.0

            Create a live_stream (radio station) object.

            INPUTS
            * name     = (string) Stream title
            * url      = (string) URL of the http/s stream
            * codec    = (string) stream codec ('mp3', 'flac', 'ogg', 'vorbis', 'opus', 'aac', 'alac')
            * catalog  = (int) Catalog ID to associate with this stream
            * site_url = (string) Homepage URL of the stream //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'live_stream_create'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'name': name,
                'url': stream_url,
                'codec': codec,
                'catalog': catalog_id,
                'site_url': site_url}
        if not site_url:
            data.pop('site_url')
        return self.get_request(ampache_url, data, api_method)

    def live_stream_edit(self, filter_id, name: str = '', stream_url: str = '', codec: str = '', catalog_id: int = 0,
                         site_url: str = ''):
        """ live_stream_edit
            MINIMUM_API_VERSION=6.0.0

            Edit a live_stream (radio station) object.

            INPUTS
            * filter   = (string) object_id
            * name     = (string) Stream title //optional
            * url      = (string) URL of the http/s stream //optional
            * codec    = (string) stream codec ('mp3', 'flac', 'ogg', 'vorbis', 'opus', 'aac', 'alac') //optional
            * catalog  = (int) Catalog ID to associate with this stream //optional
            * site_url = (string) Homepage URL of the stream //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'live_stream_edit'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'name': name,
                'url': stream_url,
                'codec': codec,
                'catalog': catalog_id,
                'site_url': site_url}
        if not name:
            data.pop('name')
        if not stream_url:
            data.pop('url')
        if not codec:
            data.pop('codec')
        if not catalog_id:
            data.pop('catalog')
        if not site_url:
            data.pop('site_url')
        return self.get_request(ampache_url, data, api_method)

    def live_stream_delete(self, filter_id: int):
        """ live_stream_delete
            MINIMUM_API_VERSION=6.0.0

            Delete an existing live_stream (radio station). (if it exists)

            INPUTS
            * filter_id = (integer) object_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'live_stream_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def labels(self, filter_str=False,
               exact=False, offset=0, limit=0, sort=False, cond=False):
        """ labels
            MINIMUM_API_VERSION=420000

            Returns labels based on the specified filter_str

            INPUTS
            * filter_str = (string) search the name of a label //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'labels'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_str,
                'exact': exact,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def label(self, filter_id: int):
        """ label
            MINIMUM_API_VERSION=420000

            returns a single label

            INPUTS
            * filter_id   = (integer) $label_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'label'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def label_artists(self, filter_id: int, sort=False, cond=False):
        """ label_artists
            MINIMUM_API_VERSION=420000

            returns a artists for a single label ID

            INPUTS
            * filter_id = (integer) $label_id
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'label_artists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def get_bookmark(self, filter_id: str, object_type: str, include=False, show_all=False):
        """ get_bookmark
            MINIMUM_API_VERSION=5.0.0

            Get the bookmark from it's object_id and object_type.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('bookmark', 'song', 'video', 'podcast_episode')
            * include     = (integer) 0,1, if true include the object in the bookmark //optional
            * all         = (integer) 0,1, if true every bookmark related to the object //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'get_bookmark'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type,
                'include': include,
                'all': show_all}
        if not include:
            data.pop('include')
        if not show_all:
            data.pop('all')
        return self.get_request(ampache_url, data, api_method)

    def bookmarks(self, client=False, include=False):
        """ bookmarks
            MINIMUM_API_VERSION=5.0.0

            Get information about bookmarked media this user is allowed to manage.

            INPUTS
            * client  = (string) filter by bookmark_id //optional
            * include = (integer) 0,1, if true include the object in the bookmark //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'bookmarks'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'client': client,
                'include': include}
        if not client:
            data.pop('client')
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def bookmark(self, filter_id: str, include=False):
        """ bookmark
            MINIMUM_API_VERSION=6.1.0

            Get information about bookmarked media this user is allowed to manage.

            INPUTS
            * filter  = (string) bookmark_id
            * include = (integer) 0,1, if true include the object in the bookmark //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'bookmark'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'include': include}
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def bookmark_create(self, filter_id, object_type,
                        position: int = 0, client: str = CLIENT_NAME, date=False, include=False):
        """ bookmark_create
            MINIMUM_API_VERSION=5.0.0

            Create a placeholder for the current media that you can return to later.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('bookmark', 'song', 'video', 'podcast_episode')
            * position    = (integer) current track time in seconds
            * client      = (string) Agent string. (Default: 'python3-ampache') //optional
            * date        = (integer) update time (Default: UNIXTIME()) //optional
            * include     = (integer) 0,1, if true include the object in the bookmark //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'bookmark_create'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type,
                'position': position,
                'client': client,
                'date': date,
                'include': include}
        if not client:
            data.pop('client')
        if not date:
            data.pop('date')
        return self.get_request(ampache_url, data, api_method)

    def bookmark_edit(self, filter_id, object_type,
                      position: int = 0, client: str = CLIENT_NAME, date=False, include=False):
        """ bookmark_edit
            MINIMUM_API_VERSION=5.0.0

            Edit a placeholder for the current media that you can return to later.

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('bookmark', 'song', 'video', 'podcast_episode')
            * position    = (integer) current track time in seconds
            * client      = (string) Agent string. (Default: 'python3-ampache') //optional
            * date        = (integer) update time (Default: UNIXTIME()) //optional
            * include     = (integer) 0,1, if true include the object in the bookmark //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'bookmark_edit'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type,
                'position': position,
                'client': client,
                'date': date,
                'include': include}
        if not client:
            data.pop('client')
        if not date:
            data.pop('date')
        if not include:
            data.pop('include')
        return self.get_request(ampache_url, data, api_method)

    def bookmark_delete(self, filter_id: int, object_type=False):
        """ bookmark_delete
            MINIMUM_API_VERSION=5.0.0

            Delete an existing bookmark. (if it exists)

            INPUTS
            * filter_id   = (integer) object_id
            * object_type = (string) object_type ('bookmark', 'song', 'video', 'podcast_episode')
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'bookmark_delete'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'type': object_type}
        return self.get_request(ampache_url, data, api_method)

    def deleted_songs(self, offset=0, limit=0):
        """ deleted_songs
            MINIMUM_API_VERSION=500000

            Returns deleted_song

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'deleted_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    def deleted_podcast_episodes(self, offset=0, limit=0):
        """ deleted_podcast_episodes
            MINIMUM_API_VERSION=500000

            Returns deleted_podcast_episode

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'deleted_podcast_episodes'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    def deleted_videos(self, offset=0, limit=0):
        """ deleted_videos
            MINIMUM_API_VERSION=500000

            Returns deleted_video

            INPUTS
            * offset      = (integer) //optional
            * limit       = (integer) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'deleted_videos'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'offset': str(offset),
                'limit': str(limit)}
        return self.get_request(ampache_url, data, api_method)

    """
    --------------------
    BACKCOMPAT FUNCTIONS
    --------------------
    """

    def advanced_search(self, rules,
                        operator='and', object_type='song', offset=0, limit=0, random=0):
        """ advanced_search
            MINIMUM_API_VERSION=380001

            Perform an advanced search given passed rules
            the rules can occur multiple times and are joined by the operator item.

            Refer to the wiki for further information
            http://ampache.org/api/api-advanced-search

            INPUTS
            * rules       = (array) = [[rule_1,rule_1_operator,rule_1_input],[rule_2,rule_2_operator,rule_2_input],[etc]]
            * operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
            * object_type = (string)  //optional
            * offset      = (integer) //optional
            * limit       = (integer) //optional
            * random      = (integer) 0|1' //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'advanced_search'
        data = {'action': api_method,
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
        return self.get_request(ampache_url, data, api_method)

    def tags(self, filter_str=False,
             exact=False, offset=0, limit=0, sort=False, cond=False):
        """ tags
            MINIMUM_API_VERSION=380001

            This returns the tags (Tags) based on the specified filter

            INPUTS
            * filter_str = (string) search the name of a tag //optional
            * exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
            * offset     = (integer) //optional
            * limit      = (integer) //optional
            * cond       = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort       = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'tags'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'exact': exact,
                'filter': filter_str,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not filter_str:
            data.pop('filter')
        if not exact:
            data.pop('exact')
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def tag(self, filter_id: int):
        """ tag
            MINIMUM_API_VERSION=380001

            This returns a single tag based on UID

            INPUTS
            * filter_id = (integer) $tag_id
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'tag'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id}
        return self.get_request(ampache_url, data, api_method)

    def tag_artists(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ tag_artists
            MINIMUM_API_VERSION=380001

            This returns the artists associated with the tag in question as defined by the UID

            INPUTS
            * filter_id = (integer) $tag_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'tag_artists'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def tag_albums(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ tag_albums
            MINIMUM_API_VERSION=380001

            This returns the albums associated with the tag in question

            INPUTS
            * filter_id = (integer) $tag_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'tag_albums'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def tag_songs(self, filter_id: int, offset=0, limit=0, sort=False, cond=False):
        """ tag_songs
            MINIMUM_API_VERSION=380001

            returns the songs for this tag

            INPUTS
            * filter_id = (integer) $tag_id
            * offset    = (integer) //optional
            * limit     = (integer) //optional
            * cond      = (string) Filter the browse using ';' separated comma string pairs (e.g. 'filter1,value1;filter2,value2') //optional
            * sort      = (string) sort name / comma separated key pair. Default 'ASC' (e.g. 'name,ASC' and 'name' are the same) //optional
        """
        ampache_url = self.AMPACHE_URL + '/server/' + self.AMPACHE_API + '.server.php'
        api_method = 'tag_songs'
        data = {'action': api_method,
                'auth': self.AMPACHE_SESSION,
                'filter': filter_id,
                'offset': str(offset),
                'limit': str(limit),
                'sort': sort,
                'cond': cond}
        if not sort:
            data.pop('sort')
        if not cond:
            data.pop('cond')
        return self.get_request(ampache_url, data, api_method)

    def user_update(self, username, password=False, fullname=False, email=False,
                    website=False, state=False, city=False, disable=False, maxbitrate=False,
                    fullname_public=False, reset_apikey=False, reset_streamtoken=False, clear_stats=False):
        """ user_update
            MINIMUM_API_VERSION=6.0.0

            Update an existing user. Backcompat function for api6 (Use user_edit)
        """
        return self.user_edit(username, password, fullname, email,
                              website, state, city, disable, maxbitrate,
                              fullname_public, reset_apikey, reset_streamtoken, clear_stats)

    def execute(self, method: str, params=None):
        if params is None:
            params = {}
        match method:
            case 'handshake':
                if not "version" in params:
                    params["version"] = self.AMPACHE_VERSION
                if not "ampache_url" in params:
                    params["ampache_url"] = self.AMPACHE_URL
                if not "ampache_api" in params:
                    params["ampache_api"] = self.AMPACHE_KEY
                if not "ampache_user" in params:
                    params["ampache_user"] = self.AMPACHE_USER
                if "timestamp" in params and not params["timestamp"] == 0:
                    return self.handshake(params["ampache_url"],
                                          self.encrypt_password(params["ampache_api"], int(params["timestamp"])),
                                          params["ampache_user"], int(params["timestamp"]), params["version"])
                return self.handshake(params["ampache_url"],
                                      self.encrypt_string(params["ampache_api"], params["ampache_user"]),
                                      False, False, params["version"])
            case 'goodbye':
                return self.goodbye()
            case 'lost_password':
                if "user" in params and "email" in params:
                    params["auth"] = self.encrypt_string(params["email"], params["user"])
                return self.lost_password(params["auth"])
            case 'ping':
                if not "ampache_url" in params:
                    params["ampache_url"] = self.AMPACHE_URL
                if not "ampache_api" in params:
                    params["ampache_api"] = self.AMPACHE_SESSION
                return self.ping(params["ampache_url"], params["ampache_api"])
            case 'search_rules':
                if not "filter_str" in params:
                    return False
                return self.search_rules(params["filter_str"])
            case 'advanced_search':
                if not "rules" in params:
                    params["rules"] = list()
                if not "operator" in params:
                    params["operator"] = 'and'
                if not "object_type" in params:
                    params["object_type"] = 'song'
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "random" in params:
                    params["random"] = 0
                return self.advanced_search(params["rules"], params["operator"], params["object_type"],
                                            params["offset"], params["limit"], params["random"])
            case 'search':
                if not "rules" in params:
                    params["rules"] = list()
                if not "operator" in params:
                    params["operator"] = 'and'
                if not "object_type" in params:
                    params["object_type"] = 'song'
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "random" in params:
                    params["random"] = 0
                return self.search(params["rules"], params["operator"], params["object_type"], params["offset"],
                                   params["limit"], params["random"])
            case 'search_group':
                if not "rules" in params:
                    params["rules"] = list()
                if not "operator" in params:
                    params["operator"] = 'and'
                if not "object_type" in params:
                    params["object_type"] = 'all'
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "random" in params:
                    params["random"] = 0
                return self.search_group(params["filter_id"], params["operator"], params["object_type"],
                                         params["offset"], params["limit"], params["random"])
            case 'album':
                if not "include" in params:
                    params["include"] = False
                return self.album(params["filter_id"], params["include"])
            case 'albums':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "include" in params:
                    params["include"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.albums(params["filter_str"], params["exact"], params["add"], params["update"],
                                   params["offset"], params["limit"], params["include"], params["sort"], params["cond"])
            case 'album_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "exact" in params:
                    params["exact"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.album_songs(params["filter_id"], params["offset"], params["limit"], params["exact"],
                                        params["sort"], params["cond"])
            case 'artist':
                if not "include" in params:
                    params["include"] = False
                return self.artist(params["filter_id"], params["include"])
            case 'artist_albums':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "album_artist" in params:
                    params["album_artist"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.artist_albums(params["filter_id"], params["offset"], params["limit"],
                                          params["album_artist"], params["sort"], params["cond"])
            case 'artists':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "include" in params:
                    params["include"] = False
                if not "album_artist" in params:
                    params["album_artist"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.artists(params["filter_str"], params["add"], params["update"], params["offset"],
                                    params["limit"], params["include"], params["album_artist"],
                                    params["sort"], params["cond"])
            case 'artist_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.artist_songs(params["filter_id"], params["offset"], params["limit"],
                                         params["sort"], params["cond"])
            case 'bookmark':
                if not "include" in params:
                    params["include"] = False
                return self.bookmark(params["filter_id"], params["include"])
            case 'bookmark_create':
                if not "position" in params:
                    params["position"] = 0
                if not "client" in params:
                    params["client"] = CLIENT_NAME
                if not "date" in params:
                    params["date"] = False
                if not "include" in params:
                    params["include"] = False
                return self.bookmark_create(params["filter_id"], params["object_type"], params["position"],
                                            params["client"], params["date"], params["include"])
            case 'bookmark_delete':
                if not "filter_id" in params or not "object_type" in params:
                    return False
                return self.bookmark_delete(params["filter_id"], params["object_type"])
            case 'bookmark_edit':
                if not "position" in params:
                    params["position"] = 0
                if not "client" in params:
                    params["client"] = CLIENT_NAME
                if not "date" in params:
                    params["date"] = False
                if not "include" in params:
                    params["include"] = False
                return self.bookmark_edit(params["filter_id"], params["object_type"], params["position"],
                                          params["client"], params["date"], params["include"])
            case 'bookmarks':
                if not "client" in params or not "include" in params:
                    return False
                return self.bookmarks(params["client"], params["include"])
            case 'browse':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "object_type" in params:
                    params["object_type"] = False
                if not "catalog" in params:
                    params["catalog"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.browse(params["filter_str"], params["object_type"], params["catalog"], params["add"],
                                   params["update"], params["offset"], params["limit"], params["sort"], params["cond"])
            case 'catalog':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.catalog(params["filter_id"], params["offset"], params["limit"])
            case 'catalog_action':
                if not "task" in params or not "catalog_id" in params:
                    return False
                return self.catalog_action(params["task"], params["catalog_id"])
            case 'catalog_add':
                if not "cat_type" in params:
                    params["cat_type"] = False
                if not "media_type" in params:
                    params["media_type"] = False
                if not "file_pattern" in params:
                    params["file_pattern"] = False
                if not "folder_pattern" in params:
                    params["folder_pattern"] = False
                if not "username" in params:
                    params["username"] = False
                if not "password" in params:
                    params["password"] = False
                return self.catalog_add(params["cat_name"], params["cat_path"], params["cat_type"],
                                        params["media_type"], params["file_pattern"], params["folder_pattern"],
                                        params["username"], params["password"])
            case 'catalog_delete':
                if not "filter_id" in params:
                    return False
                return self.catalog_delete(params["filter_id"])
            case 'catalog_file':
                if not "file" in params or not "task" in params or not "catalog_id" in params:
                    return False
                return self.catalog_file(params["file"], params["task"], params["catalog_id"])
            case 'catalog_folder':
                if not "folder" in params or not "task" in params or not "catalog_id" in params:
                    return False
                return self.catalog_folder(params["folder"], params["task"], params["catalog_id"])
            case 'catalogs':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.catalogs(params["filter_str"], params["offset"], params["limit"],
                                     params["sort"], params["cond"])
            case 'deleted_podcast_episodes':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.deleted_podcast_episodes(params["offset"], params["limit"])
            case 'deleted_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.deleted_songs(params["offset"], params["limit"])
            case 'deleted_videos':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.deleted_videos(params["offset"], params["limit"])
            case 'democratic':
                if not "method" in params or not "oid" in params:
                    return False
                return self.democratic(params["method"], params["oid"])
            case 'download':
                if not "transcode" in params:
                    params["transcode"] = 'raw'
                if not "bitrate" in params:
                    params["bitrate"] = False
                if not "stats" in params:
                    params["stats"] = 1
                return self.download(params["object_id"], params["object_type"], params["destination"], params["stats"])
            case 'flag':
                if not "date" in params:
                    params["date"] = False
                return self.flag(params["object_type"], params["object_id"], params["flagbool"], params["date"])
            case 'followers':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.followers(params["username"], params["sort"], params["cond"])
            case 'following':
                if not "username" in params:
                    return False
                return self.following(params["username"])
            case 'friends_timeline':
                if not "limit" in params:
                    params["limit"] = 0
                if not "since" in params:
                    params["since"] = 0
                return self.friends_timeline(params["limit"], params["since"])
            case 'genre':
                if not "filter_id" in params:
                    return False
                return self.genre(params["filter_id"])
            case 'genre_albums':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.genre_albums(params["filter_id"], params["sort"], params["cond"])
            case 'genre_artists':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.genre_artists(params["username"], params["sort"], params["cond"])
            case 'genres':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.genres(params["username"], params["sort"], params["cond"])
            case 'genre_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.genre_songs(params["filter_id"], params["offset"], params["limit"],
                                        params["sort"], params["cond"])
            case 'get_art':
                if not "object_id" in params or not "object_type" in params or not "destination" in params:
                    return False
                return self.get_art(params["object_id"], params["object_type"], params["destination"])
            case 'get_bookmark':
                if not "include" in params:
                    params["include"] = False
                if not "show_all" in params:
                    params["show_all"] = False
                return self.get_bookmark(params["filter_id"], params["object_type"], params["include"],
                                         params["show_all"])
            case 'get_external_metadata':
                if not "filter_id" in params or not "object_type" in params:
                    return False
                return self.get_external_metadata(params["filter_id"], params["object_type"])
            case 'get_lyrics':
                if not "filter_id" in params:
                    return False
                if not "plugins" in params:
                    params["plugins"] = False
                return self.get_lyrics(params["filter_id"], params["plugins"])
            case 'get_indexes':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "include" in params:
                    params["include"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.get_indexes(params["object_type"], params["filter_str"], params["exact"], params["add"],
                                        params["update"], params["include"], params["offset"], params["limit"],
                                        params["sort"], params["cond"])
            case 'get_similar':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.get_similar(params["object_type"], params["filter_id"], params["offset"], params["limit"])
            case 'index':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "include" in params:
                    params["include"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "hide_search" in params:
                    params["hide_search"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.index(params["object_type"], params["filter_str"], params["exact"], params["add"],
                                  params["update"], params["include"], params["offset"], params["limit"],
                                  params["hide_search"], params["sort"], params["cond"])
            case 'label':
                if not "filter_id" in params:
                    return False
                return self.label(params["filter_id"])
            case 'label_artists':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.label_artists(params["filter_id"], params["sort"], params["cond"])
            case 'labels':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.labels(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                   params["sort"], params["cond"])
            case 'last_shouts':
                if not "limit" in params:
                    params["limit"] = 0
                return self.last_shouts(params["username"], params["limit"])
            case 'license':
                if not "filter_id" in params:
                    return False
                return self.license(params["filter_id"])
            case 'licenses':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.licenses(params["filter_str"], params["exact"], params["add"], params["update"],
                                     params["offset"], params["limit"], params["sort"], params["cond"])
            case 'license_songs':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.license_songs(params["filter_id"], params["sort"], params["cond"])
            case 'list':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.list(params["object_type"], params["filter_str"], params["exact"], params["add"],
                                 params["update"], params["offset"], params["limit"], params["sort"], params["cond"])
            case 'live_stream':
                if not "filter_id" in params:
                    return False
                return self.live_stream(params["filter_id"])
            case 'live_stream_create':
                if not "site_url" in params:
                    params["site_url"] = ''
                return self.live_stream_create(params["name"], params["stream_url"], params["codec"],
                                               params["catalog_id"], params["site_url"])
            case 'live_stream_delete':
                if not "filter_id" in params:
                    return False
                return self.live_stream_delete(params["filter_id"])
            case 'live_stream_edit':
                if not "name" in params:
                    params["name"] = ''
                if not "stream_url" in params:
                    params["stream_url"] = ''
                if not "codec" in params:
                    params["codec"] = ''
                if not "catalog_id" in params:
                    params["catalog_id"] = 0
                if not "site_url" in params:
                    params["site_url"] = ''
                return self.live_stream_edit(params["filter_id"], params["name"], params["stream_url"],
                                             params["codec"], params["catalog_id"], params["site_url"])
            case 'live_streams':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.live_streams(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                         params["sort"], params["cond"])
            case 'localplay':
                if not "oid" in params:
                    params["oid"] = False
                if not "otype" in params:
                    params["otype"] = False
                if not "clear" in params:
                    params["clear"] = False
                return self.localplay(params["command"])
            case 'localplay_songs':
                return self.localplay_songs()
            case 'now_playing':
                return self.now_playing()
            case 'player':
                if not "object_type" in params:
                    params["object_type"] = 'song'
                if not "state" in params:
                    params["state"] = 'play'
                if not "play_time" in params:
                    params["play_time"] = 0
                if not "client" in params:
                    params["client"] = CLIENT_NAME
                return self.player(params["filter_str"], params["object_type"], params["state"],
                                   params["play_time"], params["client"])
            case 'playlists':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "hide_search" in params:
                    params["hide_search"] = False
                if not "show_dupes" in params:
                    params["show_dupes"] = False
                if not "include" in params:
                    params["include"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.playlists(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                      params["hide_search"], params["show_dupes"], params["include"],
                                      params["sort"], params["cond"])
            case 'playlist':
                if not "filter_id" in params:
                    return False
                return self.playlist(params["filter_id"])
            case 'playlist_songs':
                if not "random" in params:
                    params["random"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.playlist_songs(params["filter_id"], params["random"], params["offset"], params["limit"])
            case 'playlist_add':
                if not "filter_id" in params or not "object_id" in params or not "object_type" in params:
                    return False
                return self.playlist_add(params["filter_id"], params["object_id"], params["object_type"])
            case 'playlist_add_song':
                if not "check" in params:
                    params["check"] = False
                return self.playlist_add_song(params["filter_id"], params["song_id"], params["check"])
            case 'playlist_create':
                if not "playlist_name" in params or not "playlist_type" in params:
                    return False
                return self.playlist_create(params["playlist_name"], params["playlist_type"])
            case 'playlist_delete':
                if not "filter_id" in params:
                    return False
                return self.playlist_delete(params["filter_id"])
            case 'playlist_edit':
                if not "playlist_name" in params:
                    params["playlist_name"] = False
                if not "playlist_type" in params:
                    params["playlist_type"] = False
                if not "owner" in params:
                    params["owner"] = False
                if not "items" in params:
                    params["items"] = False
                if not "tracks" in params:
                    params["tracks"] = False
                return self.playlist_edit(params["filter_id"], params["playlist_name"], params["playlist_type"],
                                          params["owner"], params["items"], params["tracks"])
            case 'playlist_generate':
                if not "mode" in params:
                    params["mode"] = 'random'
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "album_id" in params:
                    params["album_id"] = False
                if not "artist_id" in params:
                    params["artist_id"] = False
                if not "flagged" in params:
                    params["flagged"] = False
                if not "list_format" in params:
                    params["list_format"] = 'song'
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.playlist_generate(params["mode"], params["filter_str"], params["album_id"],
                                              params["artist_id"], params["flagged"], params["list_format"],
                                              params["offset"], params["limit"])
            case 'playlist_hash':
                if not "filter_id" in params:
                    return False
                return self.playlist_hash(params["filter_id"])
            case 'playlist_remove_song':
                if not "song_id" in params:
                    params["song_id"] = False
                if not "track" in params:
                    params["track"] = False
                return self.playlist_remove_song(params["filter_id"])
            case 'podcast':
                if not "include" in params:
                    params["include"] = False
                return self.podcast(params["filter_id"], params["include"])
            case 'podcast_create':
                if not "url" in params or not "catalog_id" in params:
                    return False
                return self.podcast_create(params["url"], params["catalog_id"])
            case 'podcast_delete':
                if not "filter_id" in params:
                    return False
                return self.podcast_delete(params["filter_id"])
            case 'podcast_edit':
                if not "feed" in params:
                    params["feed"] = False
                if not "title" in params:
                    params["title"] = False
                if not "website" in params:
                    params["website"] = False
                if not "description" in params:
                    params["description"] = False
                if not "generator" in params:
                    params["generator"] = False
                if not "copyright_str" in params:
                    params["copyright_str"] = False
                return self.podcast_edit(params["filter_id"], params["feed"], params["title"], params["website"],
                                         params["description"], params["generator"], params["copyright_str"])
            case 'podcast_episode':
                if not "filter_id" in params:
                    return False
                return self.podcast_episode(params["filter_id"])
            case 'podcast_episode_delete':
                if not "filter_id" in params:
                    return False
                return self.podcast_episode_delete(params["filter_id"])
            case 'podcast_episodes':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.podcast_episodes(params["filter_id"], params["offset"], params["limit"],
                                             params["sort"], params["cond"])
            case 'podcasts':
                if not "exact" in params:
                    params["exact"] = 0
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.podcasts(params["filter_id"], params["exact"], params["offset"], params["limit"],
                                     params["sort"], params["cond"])
            case 'preference_create':
                if not "description" in params:
                    params["description"] = False
                if not "subcategory" in params:
                    params["subcategory"] = False
                if not "level" in params:
                    params["level"] = 100
                return self.preference_create(params["filter_str"], params["type_str"], params["category"],
                                              params["description"], params["subcategory"], params["level"])
            case 'preference_delete':
                if not "filter_str" in params:
                    return False
                return self.preference_delete(params["filter_str"])
            case 'preference_edit':
                if not "apply_all" in params:
                    params["apply_all"] = 0
                return self.preference_edit(params["filter_str"], params["value"], params["apply_all"])
            case 'rate':
                if not "object_type" in params or not "object_id" in params or not "rating" in params:
                    return False
                return self.rate(params["object_type"], params["object_id"], params["rating"])
            case 'record_play':
                if not "user_id" in params:
                    params["user_id"] = False
                if not "client" in params:
                    params["client"] = CLIENT_NAME
                if not "date" in params:
                    params["date"] = False
                return self.record_play(params["object_id"], params["user_id"], params["client"], params["date"])
            case 'register':
                if not "username" in params or not "fullname" in params or not "password" in params or not "email" in params:
                    return False
                return self.register(params["username"], params["fullname"], params["password"], params["email"])
            case 'scrobble':
                if not "mbtitle" in params:
                    params["mbtitle"] = False
                if not "mbartist" in params:
                    params["mbartist"] = False
                if not "mbalbum" in params:
                    params["mbalbum"] = False
                if not "stime" in params:
                    params["stime"] = False
                if not "client" in params:
                    params["client"] = CLIENT_NAME
                return self.scrobble(params["title"], params["artist_name"], params["album_name"],
                                     params["mbtitle"], params["mbartist"], params["mbalbum"],
                                     params["stime"], params["client"])
            case 'search_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.search_songs(params["filter_str"], params["offset"], params["limit"])
            case 'share':
                if not "filter_id" in params:
                    return False
                return self.share(params["filter_id"])
            case 'share_create':
                if not "description" in params:
                    params["description"] = False
                if not "expires" in params:
                    params["expires"] = False
                return self.share_create(params["filter_id"], params["object_type"],
                                         params["description"], params["expires"])
            case 'share_delete':
                if not "filter_id" in params:
                    return False
                return self.share_delete(params["filter_id"])
            case 'share_edit':
                if not "can_stream" in params:
                    params["can_stream"] = False
                if not "can_download" in params:
                    params["can_download"] = False
                if not "expires" in params:
                    params["expires"] = False
                if not "description" in params:
                    params["description"] = False
                return self.share_edit(params["filter_id"], params["can_stream"], params["can_download"],
                                       params["expires"], params["description"])
            case 'shares':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.shares(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                   params["sort"], params["cond"])
            case 'smartlists':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "hide_search" in params:
                    params["hide_search"] = False
                if not "show_dupes" in params:
                    params["show_dupes"] = False
                if not "include" in params:
                    params["include"] = False
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.smartlists(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                      params["include"], params["sort"], params["cond"])
            case 'smartlist':
                if not "filter_id" in params:
                    return False
                return self.smartlist(params["filter_id"])
            case 'smartlist_songs':
                if not "random" in params:
                    params["random"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                return self.smartlist_songs(params["filter_id"], params["random"], params["offset"], params["limit"])
            case 'smartlist_delete':
                if not "filter_id" in params:
                    return False
                return self.smartlist_delete(params["filter_id"])
            case 'song':
                if not "filter_id" in params:
                    return False
                return self.song(params["filter_id"])
            case 'song_delete':
                if not "filter_id" in params:
                    return False
                return self.song_delete(params["filter_id"])
            case 'song_tags':
                if not "filter_id" in params:
                    return False
                return self.song_tags(params["filter_id"])
            case 'songs':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "add" in params:
                    params["add"] = False
                if not "update" in params:
                    params["update"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.songs(params["filter_str"], params["exact"], params["add"], params["update"],
                                  params["offset"], params["limit"], params["sort"], params["cond"])
            case 'stats':
                if not "filter_str" in params:
                    params["filter_str"] = 'random'
                if not "username" in params:
                    params["username"] = False
                if not "user_id" in params:
                    params["user_id"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.stats(params["object_type"], params["filter_str"], params["username"],
                                  params["user_id"], params["offset"], params["limit"],
                                  params["sort"], params["cond"])
            case 'stream':
                if not "stats" in params:
                    params["stats"] = 1
                return self.stream(params["object_id"], params["object_type"], params["destination"], params["stats"])
            case 'system_preference':
                if not "filter_str" in params:
                    return False
                return self.system_preference(params["filter_str"])
            case 'system_preferences':
                return self.system_preferences()
            case 'system_update':
                return self.system_update()
            case 'tag':
                if not "filter_id" in params:
                    return False
                return self.tag(params["filter_id"])
            case 'tag_albums':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.tag_albums(params["filter_id"], params["offset"], params["limit"],
                                       params["sort"], params["cond"])
            case 'tag_artists':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.tag_artists(params["filter_id"], params["offset"], params["limit"],
                                        params["sort"], params["cond"])
            case 'tags':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.tags(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                 params["sort"], params["cond"])
            case 'tag_songs':
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.tag_songs(params["filter_id"], params["offset"], params["limit"],
                                      params["sort"], params["cond"])
            case 'timeline':
                if not "limit" in params:
                    params["limit"] = 0
                if not "since" in params:
                    params["since"] = 0
                return self.timeline(params["username"], params["limit"], params["since"])
            case 'toggle_follow':
                if not "username" in params:
                    return False
                return self.toggle_follow(params["username"])
            case 'update_art':
                if not "overwrite" in params:
                    params["overwrite"] = False
                return self.update_art(params["object_type"], params["object_id"], params["overwrite"])
            case 'update_artist_info':
                if not "filter_id" in params:
                    return False
                return self.update_artist_info(params["filter_id"])
            case 'update_from_tags':
                if not "object_type" in params or not "object_id" in params:
                    return False
                return self.update_from_tags(params["object_type"], params["object_id"], )
            case 'update_podcast':
                if not "filter_id" in params:
                    return False
                return self.update_podcast(params["filter_id"])
            case 'url_to_song':
                if not "url" in params:
                    return False
                return self.url_to_song(params["url"])
            case 'user':
                if not "username" in params:
                    return False
                return self.user(params["username"])
            case 'user_create':
                if not "fullname" in params:
                    params["fullname"] = False
                if not "disable" in params:
                    params["disable"] = False
                return self.user_create(params["username"], params["password"], params["email"],
                                        params["fullname"], params["disable"])
            case 'user_delete':
                if not "username" in params:
                    return False
                return self.user_delete(params["username"])
            case 'user_edit':
                if not "password" in params:
                    params["password"] = False
                if not "fullname" in params:
                    params["fullname"] = False
                if not "email" in params:
                    params["email"] = False
                if not "website" in params:
                    params["website"] = False
                if not "state" in params:
                    params["state"] = False
                if not "city" in params:
                    params["city"] = False
                if not "disable" in params:
                    params["disable"] = False
                if not "maxbitrate" in params:
                    params["maxbitrate"] = False
                if not "fullname_public" in params:
                    params["fullname_public"] = False
                if not "reset_apikey" in params:
                    params["reset_apikey"] = False
                if not "reset_streamtoken" in params:
                    params["reset_streamtoken"] = False
                if not "clear_stats" in params:
                    params["clear_stats"] = False
                return self.user_edit(params["username"], params["password"], params["fullname"], params["email"],
                                      params["website"], params["state"], params["city"], params["disable"],
                                      params["maxbitrate"], params["fullname_public"], params["reset_apikey"],
                                      params["reset_streamtoken"], params["clear_stats"])
            case 'user_playlists':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.user_playlists(params["filter_str"], params["exact"],
                                           params["offset"], params["limit"],
                                           params["sort"], params["cond"])
            case 'user_preference':
                if not "filter_str" in params:
                    return False
                return self.user_preference(params["filter_str"])
            case 'user_preferences':
                return self.user_preferences()
            case 'users':
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.users(params["sort"], params["cond"])
            case 'user_smartlists':
                if not "filter_str" in params:
                    params["filter_str"] = False
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.user_smartlists(params["filter_str"], params["exact"],
                                            params["offset"], params["limit"],
                                            params["sort"], params["cond"])
            case 'user_update':
                if not "password" in params:
                    params["password"] = False
                if not "fullname" in params:
                    params["fullname"] = False
                if not "email" in params:
                    params["email"] = False
                if not "website" in params:
                    params["website"] = False
                if not "state" in params:
                    params["state"] = False
                if not "city" in params:
                    params["city"] = False
                if not "disable" in params:
                    params["disable"] = False
                if not "maxbitrate" in params:
                    params["maxbitrate"] = False
                if not "fullname_public" in params:
                    params["fullname_public"] = False
                if not "reset_apikey" in params:
                    params["reset_apikey"] = False
                if not "reset_streamtoken" in params:
                    params["reset_streamtoken"] = False
                if not "clear_stats" in params:
                    params["clear_stats"] = False
                return self.user_update(params["username"], params["password"], params["fullname"], params["email"],
                                        params["website"], params["state"], params["city"], params["disable"],
                                        params["maxbitrate"], params["fullname_public"], params["reset_apikey"],
                                        params["reset_streamtoken"], params["clear_stats"])
            case 'video':
                if not "filter_id" in params:
                    return False
                return self.video(params["filter_id"])
            case 'videos':
                if not "exact" in params:
                    params["exact"] = False
                if not "offset" in params:
                    params["offset"] = 0
                if not "limit" in params:
                    params["limit"] = 0
                if not "sort" in params:
                    params["sort"] = False
                if not "cond" in params:
                    params["cond"] = False
                return self.videos(params["filter_str"], params["exact"], params["offset"], params["limit"],
                                   params["sort"], params["cond"])
        return None
