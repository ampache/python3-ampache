#!/usr/bin/env python3

"""    Copyright (C)2019
       Lachlan de Waard <lachlan.00@gmail.com>
       --------------------------------------
       Scrobble to Ampache
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

import urllib.parse
import urllib.request

from xml.etree import ElementTree as ET

def run(time, title, artist, album, MBtitle, MBartist, MBalbum, ampache_url, ampache_api):
    """ Request Ampache record your play """
    if not ampache_url and not ampache_api:
        return False
    print('Scrobbling to ' + ampache_url + '\nusing auth key: ' + ampache_api)
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'scrobble',
                                   'auth': ampache_api,
                                   'client': 'AmpacheFM Rhythmbox',
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
        print(token)
        return token
    try:
        token = tree.find('error').text
    except AttributeError:
        token = False
    if token:
        print(token)
    # return false when you can't confirm scrobble
    return token

def auth(ampache_url, ampache_api):
    """ Request Ampache handshake auth """
    if not ampache_url and not ampache_api:
        return False
    if ping(ampache_url, ampache_api):
        return ampache_api
    print('Connecting to ' + ampache_url)
    ampache_url = ampache_url + '/server/xml.server.php'
    data = urllib.parse.urlencode({'action': 'handshake',
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
    if token:
        print("AUTH TOKEN FOUND %s" % (token))
    return token

def ping(ampache_url, ampache_api):
    """ Request Ampache ping auth """
    if not ampache_url and not ampache_api:
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
    if token:
        print("AUTH TOKEN FOUND %s" % (token))
    return token

