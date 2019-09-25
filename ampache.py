#!/usr/bin/env python3

"""    Copyright (C)2019
Lachlan de Waard <lachlan.00@gmail.com>
--------------------------------------
Ampache XML-Api for python
--------------------------------------

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
    * timestamp   = (int) UNIXTIME() //optional
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
                                   'timestamp': timestamp,
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

""" goodbye
    MINIMUM_API_VERSION=400001

    Destroy session for ampache_api auth key.

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
"""
def goodbye(ampache_url, ampache_api):
    """ Request Ampache destroy an api session """
    if not ampache_url and not ampache_api:
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
    This allows other sources to record play history to ampache parameters

    INPUTS
    * ampache_url = (string)
    * ampache_api = (string)
    * title       = (string)
    * artist      = (string)
    * album       = (string)
    * MBtitle     = (string) //optional
    * MBartist    = (string) //optional
    * MBalbum     = (string) //optional
    * time        = (int) UNIXTIME() //optional
    * client      = (string) //optional)
"""
def scrobble(ampache_url, ampache_api, title, artist, album, MBtitle='', MBartist='', MBalbum='', time='', client = 'AmpacheAPI'):
    if not ampache_url and not ampache_api:
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