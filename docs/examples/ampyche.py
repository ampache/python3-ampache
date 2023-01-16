#!/usr/bin/env python3

import ampache
import configparser
import os
import playsound
import sys


VERSION = "0.0.2"

# Get OS type
OS = os.name
if OS == 'nt':
    SLASH = '\\'
    CONFIG = './ampyche.conf'
elif OS == 'posix':
    from xdg.BaseDirectory import xdg_config_dirs
    SLASH = '/'
    CONFIG = xdg_config_dirs[0] + '/ampyche.conf'

# troublesome unicode characters
REPLACE = ('%', "#", ';', '"', '<', '>', '?', '[', '\\', "]", '^', '`', '{',
           '|', '}', '€', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹',
           'Œ', 'Ž', '‘', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›',
           'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¥', '"', '§', '¨', '©', 'ª', '«',
           '¬', '¯', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸',
           '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å',
           'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò',
           'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à',
           'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í',
           'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú',
           'û', 'ü', 'ý', 'þ', 'ÿ', '¦', ':', '*', '<<', '...')


def check_config():
    """ create a default config if not available """
    if not os.path.isdir(os.path.dirname(CONFIG)):
        os.makedirs(os.path.dirname(CONFIG))
    if not os.path.isfile(CONFIG):
        print("This is the first time you're running amPYche.\nEnter your user and site details.\n")
        ampache_url = input("Enter Ampache URL:")
        username = input("Enter Username:")
        apikey = input("Enter apikey:")
        conffile = open(CONFIG, "w")
        conffile.write("[conf]\nampache_url = " + ampache_url +
                       "\nampache_user = " + username +
                       "\nampache_apikey = " + apikey +
                       "\nampache_session = None" +
                       "\napi_format = xml")
        conffile.close()
    return


# Process names and replace any undesired characters
def process(string):
    """ Prevent / character to avoid creating folders """
    string = string.replace('/', '_')  # if present
    for items in REPLACE:
        string = string.replace(items, '')
    string = ''.join(c for c in string if c not in '<>:"\\|?*')
    while string.endswith('.'):
        string = string[:-1]
    return string


def show_help():
    """ show the help and current config """
    if os.path.isfile(CONFIG):
        conf = configparser.RawConfigParser()
        conf.read(CONFIG)
        print("\n##################\n"
              "# amPYche v" + VERSION + " #\n"
              "##################\n"
              "\nHOW DOES ALL THIS WORK?\n"
              "\n  Possible Actions:\n"
              "\n    /u:%CUSTOM_USER%\t(Custom username for the current action)"
              "\n    /k:%CUSTOM_APIKEY%\t(Custom apikey for the current action)"
              "\n    /a:%ACTION% \t(ping, playlists, localplay, stream, download, configure, logout, showconfig)"
              "\n    /l:%LIMIT%  \t(integer)"
              "\n    /o:%OBJECT_ID%  \t(string)"
              "\n    /t:%OBJECT_TYPE%  \t(song, playlist)"
              "\n    /p:%PATH%\t\t(folder for downloads)"
              "\n    /f:%FORMAT%  \t(raw, mp3, ogg, flac)"
              "\n    /usb\t\t(split files into numeric 0-9 folders for car USBs)"
              "\n    /c:%COMMAND%\t(localplay command)"
              "\n       (next, prev, stop, play, pause, add, volume_up,"
              "\n        volume_down, volume_mute, delete_all, skip, status)\n")
        print("URL:     " + conf.get('conf', 'ampache_url'))
        print("USER:    " + conf.get('conf', 'ampache_user'))
        print("API_KEY: " + conf.get('conf', 'ampache_apikey'))
        print("SESSION: " + conf.get('conf', 'ampache_session'))
        print("FORMAT:  " + conf.get('conf', 'api_format'))
        print()
    return


# default action is to just send a ping
ACTION = 'ping'
LIMIT = 0
OID = 0
TRANSCODE = 'raw'
TYPE = 'song'
NUMERIC = False
COMMAND = 'status'

# get custom options from launch arguments
for arguments in sys.argv:
    if arguments[:2] == '/h':
        # SHOW HELP HERE
        show_help()
        sys.exit()
    if arguments[:3] == '/a:':
        ACTION = arguments[3:]
    if arguments[:3] == '/u:':
        CUSTOM_USER = arguments[3:]
    if arguments[:3] == '/k:':
        CUSTOM_APIKEY = arguments[3:]
    if arguments[:3] == '/l:':
        LIMIT = arguments[3:]
    if arguments[:3] == '/o:':
        OID = arguments[3:]
    if arguments[:3] == '/t:':
        TYPE = arguments[3:]
    if arguments[:3] == '/c:':
        COMMAND = arguments[3:]
    if arguments[:3] == '/f:':
        TRANSCODE = arguments[3:]
    if arguments[:3] == '/p:':
        DESTIN = arguments[3:]
    if arguments[:4] == '/usb':
        NUMERIC = True


class AMPYCHE(object):
    """ do commands from the cli! """
    def __init__(self):
        """ start amPYche """
        print("\n##################\n"
              "# amPYche v" + VERSION + " #\n"
              "##################\n")
        check_config()
        self.conf = configparser.RawConfigParser()
        self.conf.read(CONFIG)
        self.ampache_url = self.conf.get('conf', 'ampache_url')
        self.ampache_user = self.conf.get('conf', 'ampache_user')
        self.ampache_apikey = self.conf.get('conf', 'ampache_apikey')
        self.ampache_session = self.conf.get('conf', 'ampache_session')
        self.api_format = self.conf.get('conf', 'api_format')
        self.ampacheConnection = ampache.API()
        self.ampacheConnection.set_format(self.api_format)

        # ping the last session to see if active
        my_ping = self.ampacheConnection.ping(self.ampache_url, self.ampache_session)
        if not my_ping:
            self.handshake()
        if not my_ping:
            print('CONNECTION ERROR')
            return

        # workaround for bugs
        if not self.ampacheConnection.AMPACHE_URL:
            self.ampacheConnection.AMPACHE_URL = self.ampache_url
        if not self.ampacheConnection.AMPACHE_SESSION:
            self.ampacheConnection.AMPACHE_SESSION = self.ampache_session

        # get your lists
        self.list_songs = list()
        if int(OID) > 0:
            if TYPE == 'playlist':
                self.playlist_songs(OID)
            if TYPE == 'song':
                song = self.ampacheConnection.song(OID)
                if self.api_format == 'xml':
                    for child in song:
                        if child.tag == 'song':
                            self.list_songs.append(child.attrib['id'])
                else:
                    for child in song:
                        self.list_songs.append(child['id'])
        # run your action
        if ACTION == 'ping':
            print("\nSESSION: " + self.ampacheConnection.ping(self.ampache_url, self.ampache_session))
        elif ACTION == 'configure':
            self.saveconf()
        elif ACTION == 'logout':
            self.quit()
        elif ACTION == 'showconfig':
            print("\nURL:     " + self.conf.get('conf', 'ampache_url'))
            print("USER:    " + self.conf.get('conf', 'ampache_user'))
            print("API_KEY: " + self.conf.get('conf', 'ampache_apikey'))
            print("SESSION: " + self.conf.get('conf', 'ampache_session'))
            print("FORMAT:  " + self.conf.get('conf', 'api_format') + "\n")
        elif ACTION == 'playlists':
            self.playlists()
        elif ACTION == 'localplay':
            for song_id in self.list_songs:
                if song_id:
                    self.localplay('add', song_id, 'song', 0)
            if COMMAND != 'add':
                result = self.localplay(COMMAND)
                if result:
                    for lines in result:
                        if self.api_format == 'xml':
                            print(lines[0] + ": " + lines[1])
                        else:
                            print(str(lines) + ": " + str(result[lines]))
        elif ACTION == 'download':
            if not os.path.isdir(DESTIN):
                os.makedirs(DESTIN)
            for song_id in self.list_songs:
                if song_id and os.path.isdir(os.path.dirname(DESTIN)):
                    self.download(song_id, DESTIN, TRANSCODE)
        elif ACTION == 'stream':
            for song_id in self.list_songs:
                if song_id:
                    self.stream(song_id, TRANSCODE)
        return

    def saveconf(self):
        """ save any config changes or press enter to keep the current value """
        self.conf.read(CONFIG)
        ampache_url = input("\nAmpache URL [" + self.ampache_url + "]\nEnter: ")
        ampache_user = input("\nUsername [" + self.ampache_user + "]\nEnter: ")
        ampache_apikey = input("\nAPIKey [" + self.ampache_apikey + "]\nEnter: ")
        api_format = input("\nAPI Format (json/xml) [" + self.api_format + "]\nEnter: ")
        if ampache_url:
            self.conf.set('conf', 'ampache_url', ampache_url)
        if ampache_user:
            self.conf.set('conf', 'ampache_user', ampache_user)
        if ampache_apikey:
            self.conf.set('conf', 'ampache_apikey', ampache_apikey)
        if api_format:
            self.conf.set('conf', 'api_format', api_format.lower())

        # write to conf file
        conffile = open(CONFIG, "w")
        self.conf.write(conffile)
        conffile.close()
        return

    def handshake(self):
        """ Log into Ampache """
        encrypted_key = self.ampacheConnection.encrypt_string(self.ampache_apikey, self.ampache_user)

        # handshake
        self.ampache_session = self.ampacheConnection.handshake(self.ampache_url, encrypted_key, '', 0, '5.5.6')
        # if you didn't get a sessoin there's nothing you can do
        if not self.ampache_session:
            print()
            sys.exit('ERROR: Failed to connect to ' + self.ampache_url)

        # did all this work?
        my_ping = self.ampacheConnection.ping(self.ampache_url, self.ampache_session)
        if not my_ping:
            print()
            sys.exit('ERROR: Failed to ping ' + self.ampache_url)

        # save the last session key so you don't have to keep shaking each run
        self.conf.read(CONFIG)
        self.conf.set('conf', 'ampache_session', self.ampache_session)

        # write to conf file
        conffile = open(CONFIG, "w")
        self.conf.write(conffile)
        conffile.close()

    def quit(self):
        """ delete your session and close the program"""
        return self.ampacheConnection.goodbye(self.ampache_url, self.ampache_session)

    def playlists(self):
        """ print a list of playlists """
        print("\nChecking for playlists\n")
        playlists = self.ampacheConnection.playlists(False, False, 0, LIMIT)
        if playlists:
            if self.api_format == 'xml':
                for child in playlists:
                    if child.tag == 'playlist':
                        print("\t" + child.attrib['id'] + ":\t" + child.find('name').text)
            else:
                for child in playlists:
                    print("\t" + child['id'] + ":\t" + child['name'])

    def playlist_songs(self, playlist_id):
        """ collect all the songs in chosen playlist into self.list_songs """
        playlist = self.ampacheConnection.playlist_songs(playlist_id, 0, LIMIT)
        print("\nChecking for songs in playlist " + str(playlist_id) + " with a limit of " + str(LIMIT) + "\n")
        if self.api_format == 'xml':
            for child in playlist:
                if child.tag == 'song':
                    self.list_songs.append(child.attrib['id'])
        else:
            for child in playlist:
                self.list_songs.append(child['id'])

    def localplay(self, action, object_id='', object_type='', clear=0):
        """ Perform a localplay command/action """
        command = self.ampacheConnection.localplay(action, object_id, object_type, clear)

        result = False
        statuslist = list()
        # if your command processed you will have a response
        if command:
            if self.api_format == 'xml':
                for child in command:
                    if action == 'status':
                        for status in child[0][0]:
                            statuslist.append([status.tag, status.text])
                    elif child.tag == 'localplay':
                        try:
                            result = child[0][0].text
                        except TypeError:
                            result = False
            else:
                if action == 'status':
                    statuslist = command['localplay']['command'][action]
                else:
                    result = command['localplay']['command'][action]
        if result:
            # All commands except status have a single response which isn't that exciting
            if object_id:
                print(action + " to localplay: " + str(object_id))
                self.ampacheConnection.localplay('play', False, False, False,
                                  self.api_format)
            else:
                print("\n" + action + " sent to localplay\n")
        else:
            # If you've requested the status, lets return all the details you asked for
            if action == 'status':
                return statuslist
            # otherwise it's a failed action
            elif object_id:
                print("Failed localplay action " + action + " on " + str(object_id))
            else:
                print("Failed localplay action " + action)

    def download(self, song_id, destination, transcode='raw'):
        """ Download the requested track This could be extended or changed to support lists"""
        # look for various Artists
        object_id = song_id
        search_song = self.ampacheConnection.song(object_id)
        list_songs = list()
        # get your song details into a list
        for child in search_song:
            if self.api_format == 'xml':
                if child.tag == 'song':
                    if transcode != 'raw':
                        # transcoded files have a different extension to the original
                        list_songs.append([child.attrib['id'],
                                           process(child.find('albumartist').text),
                                           process(child.find('album').text),
                                           process(os.path.basename(os.path.splitext(child.find('filename').text)[0] + '.' + transcode))])
                    else:
                        list_songs.append([child.attrib['id'],
                                           process(child.find('albumartist').text),
                                           process(child.find('album').text),
                                           process(os.path.basename(child.find('filename').text))])
            else:
                if transcode != 'raw':
                    # transcoded files have a different extension to the original
                    list_songs.append([child['id'],
                                       process(child['albumartist']['name']),
                                       process(child['album']['name']),
                                       process(os.path.basename(os.path.splitext(child['filename'])[0] + '.' + transcode))])
                else:
                    list_songs.append([child['id'],
                                       process(child['albumartist']['name']),
                                       process(child['album']['name']),
                                       process(os.path.basename(child['filename']))])
        # now you have the details you can construct a file destination
        for object_id in list_songs:
            if NUMERIC:
                # e.g. E:\7\Elliott Smith - 108 - Last Call.mp3
                output = os.path.join(destination, (object_id[0][-1]), object_id[1] + " - " + object_id[3])
            else:
                # e.g. E:\Elliott Smith\An Introduction to Elliott Smith\108 - Last Call.mp3
                output = os.path.join(destination, object_id[1], object_id[2], object_id[3])
            if not os.path.isfile(output):
                # download this file if it's not already there
                print('OUTPUT: ' + output)
                self.ampacheConnection.download(object_id[0],
                                 'song', output, transcode)
            else:
                # skip existing files
                print('**EXISTS**: ' + output)

    def stream(self, song_id, transcode='raw'):
        """ Download the requested track This could be extended or changed to support lists"""
        # look for various Artists
        object_id = song_id
        search_song = self.ampacheConnection.song(object_id)
        list_songs = list()
        # get your song details into a list
        for child in search_song:
            if self.api_format == 'xml':
                if child.tag == 'song':
                    if transcode != 'raw':
                        # transcoded files have a different extension to the original
                        list_songs.append([child.attrib['id'], child.find('url').text])
                    else:
                        list_songs.append([child.attrib['id'], child.find('url').text])
            else:
                if transcode != 'raw':
                    # transcoded files have a different extension to the original
                    list_songs.append([child['id'], child['url']['name']])
                else:
                    list_songs.append([child['id'], child['url']['name']])
        # now you have the details you can construct a file destination
        for song_object in list_songs:
            print("Playing " + song_object[0])
            print("URL     " + song_object[1])

            playsound.playsound(song_object[1])


if __name__ == "__main__":
    check_config()
    AMPYCHE()
