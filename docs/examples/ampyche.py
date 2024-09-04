#!/usr/bin/env python3

import ampache
import os
import playsound
import sys


VERSION = "0.0.2"

# Get OS type
OS = os.name
if OS == 'nt':
    SLASH = '\\'
    CONFIG = 'ampyche.json'
elif OS == 'posix':
    SLASH = '/'
    CONFIG = 'ampyche.json'

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
        print("\n##################\n"
              "# amPYche v" + VERSION + " #\n"
              "##################\n"
              "\nHOW DOES ALL THIS WORK?\n"
              "\n  Possible Actions:\n"
              "\n    /u:%CUSTOM_USER%\t(Custom username for the current action)"
              "\n    /k:%CUSTOM_APIKEY%\t(Custom apikey for the current action)"
              "\n    /a:%ACTION% \t(ping, playlists, localplay, stream, download list, configure, logout, showconfig)"
              "\n    /l:%LIMIT%  \t(integer)"
              "\n    /o:%OBJECT_ID%  \t(string)"
              "\n    /t:%OBJECT_TYPE%  \t(song, playlist)"
              "\n    /p:%PATH%\t\t(folder for downloads)"
              "\n    /f:%FORMAT%  \t(raw, mp3, ogg, flac)"
              "\n    /usb\t\t(split files into numeric 0-9 folders for car USBs)"
              "\n    /c:%COMMAND%\t(localplay command)"
              "\n       (next, prev, stop, play, pause, add, volume_up,"
              "\n        volume_down, volume_mute, delete_all, skip, status)\n")
        ampache_connection = ampache.API()
        ampache_connection.CONFIG_FILE = CONFIG
        if ampache_connection.get_config():
            print("URL:     " + ampache_connection.AMPACHE_URL)
            print("USER:    " + ampache_connection.AMPACHE_USER)
            print("API_KEY: " + ampache_connection.AMPACHE_KEY)
            print("SESSION: " + ampache_connection.AMPACHE_SESSION)
            print("FORMAT:  " + ampache_connection.AMPACHE_API)
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
        self.check_config()
        self.ampache_connection = ampache.API()
        self.ampache_connection.CONFIG_FILE = CONFIG
        self.ampache_connection.get_config()
        self.ampache_connection.set_format(self.ampache_connection.AMPACHE_API)

        # ping the last session to see if active
        self.handshake()
        if not self.ampache_connection.AMPACHE_SESSION:
            print('CONNECTION ERROR ' + self.ampache_connection.AMPACHE_URL)
            return

        # workaround for bugs
        if not self.ampache_connection.AMPACHE_URL:
            self.ampache_connection.AMPACHE_URL = self.ampache_connection.AMPACHE_URL
        if not self.ampache_connection.AMPACHE_SESSION:
            self.ampache_connection.AMPACHE_SESSION = self.ampache_connection.AMPACHE_SESSION

        # get your lists
        self.list_songs = list()
        if int(OID) > 0:
            if TYPE == 'playlist':
                self.playlist_songs(OID)
            if TYPE == 'song':
                song = self.ampache_connection.song(OID)
                if self.ampache_connection.AMPACHE_API == 'xml':
                    for child in song:
                        if child.tag == 'song':
                            self.list_songs.append(child.attrib['id'])
                else:
                    for child in song:
                        self.list_songs.append(child['id'])
        # run your action
        if ACTION == 'ping':
            print("\nSESSION: " + self.ampache_connection.ping(self.ampache_connection.AMPACHE_URL, self.ampache_connection.AMPACHE_SESSION))
        elif ACTION == 'configure':
            self.saveconf()
        elif ACTION == 'logout':
            self.quit()
        elif ACTION == 'showconfig':
            print("URL:     " + self.ampache_connection.AMPACHE_URL)
            print("USER:    " + self.ampache_connection.AMPACHE_USER)
            print("API_KEY: " + self.ampache_connection.AMPACHE_KEY)
            print("SESSION: " + self.ampache_connection.AMPACHE_SESSION)
            print("FORMAT:  " + self.ampache_connection.AMPACHE_API + "\n")
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
                        if self.ampache_connection.AMPACHE_API == 'xml':
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
        elif ACTION == 'list' and OID and type:
            print('playlist has the following song')
            for song_id in self.list_songs:
                print(song_id)
        return

    def check_config(self):
        """ create a default config if not available """
        if not os.path.dirname(CONFIG) == '' and not os.path.isdir(os.path.dirname(CONFIG)):
            os.makedirs(os.path.dirname(CONFIG))
        if not os.path.isfile(CONFIG):
            print("This is the first time you're running amPYche.\nEnter your user and site details.\n")
            ampache_url = input("Enter Ampache URL:")
            username = input("Enter Username:")
            apikey = input("Enter apikey:")
            self.ampache_connection.AMPACHE_URL = ampache_url
            self.ampache_connection.AMPACHE_USER = username
            self.ampache_connection.AMPACHE_KEY = apikey
            self.ampache_connection.AMPACHE_SESSION = ''
            self.ampache_connection.AMPACHE_API = 'xml'
            self.ampache_connection.save_config()
        return

    def saveconf(self):
        """ save any config changes or press enter to keep the current value """
        ampache_url = input("\nAmpache URL [" + self.ampache_connection.AMPACHE_URL + "]\nEnter: ")
        ampache_user = input("\nUsername [" + self.ampache_connection.AMPACHE_USER + "]\nEnter: ")
        ampache_apikey = input("\nAPIKey [" + self.ampache_connection.AMPACHE_KEY + "]\nEnter: ")
        api_format = input("\nAPI Format (json/xml) [" + self.ampache_connection.AMPACHE_API + "]\nEnter: ")
        if ampache_url:
            self.ampache_connection.AMPACHE_URL = ampache_url
        if ampache_user:
            self.ampache_connection.AMPACHE_USER = ampache_user
        if ampache_apikey:
            self.ampache_connection.AMPACHE_KEY = ampache_apikey
        if api_format:
            self.ampache_connection.AMPACHE_API = api_format.lower()

        # write to conf file
        self.ampache_connection.save_config()
        return

    def handshake(self):
        """ Log into Ampache """
        if not self.ampache_connection.execute('ping'):
            self.ampache_connection.execute('handshake')

        # if you didn't get a session there's nothing you can do
        if not self.ampache_connection.AMPACHE_SESSION:
            print()
            sys.exit('ERROR: Failed to connect to ' + self.ampache_connection.AMPACHE_URL)

        # did all this work?
        if not self.ampache_connection.execute('ping'):
            print()
            sys.exit('ERROR: Failed to ping ' + self.ampache_connection.AMPACHE_URL)

        # write to conf file
        self.ampache_connection.save_config()

    def quit(self):
        """ delete your session and close the program"""
        return self.ampache_connection.goodbye()

    def playlists(self):
        """ print a list of playlists """
        print("\nChecking for playlists\n")
        playlists = self.ampache_connection.execute('playlists')
        if playlists:
            if self.ampache_connection.AMPACHE_API == 'xml':
                for child in playlists:
                    if child.tag == 'playlist':
                        print("\t" + child.attrib['id'] + ":\t" + child.find('name').text)
            else:
                for child in playlists:
                    print("\t" + child['id'] + ":\t" + child['name'])

    def playlist_songs(self, playlist_id):
        """ collect all the songs in chosen playlist into self.list_songs """
        playlist = self.ampache_connection.playlist_songs(playlist_id, 0, LIMIT)
        print("\nChecking for songs in playlist " + str(playlist_id) + " with a limit of " + str(LIMIT) + "\n")
        self.list_songs = self.ampache_connection.get_id_list(playlist, 'song')

    def localplay(self, action, object_id='', object_type='', clear=0):
        """ Perform a localplay command/action """
        command = self.ampache_connection.localplay(action, int(object_id), object_type, clear)

        result = False
        statuslist = list()
        # if your command processed you will have a response
        if command:
            if self.ampache_connection.AMPACHE_API == 'xml':
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
                self.ampache_connection.localplay('play', False, False, False)
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
        search_song = self.ampache_connection.song(object_id)
        list_songs = list()
        # get your song details into a list
        for child in search_song:
            if self.ampache_connection.AMPACHE_API == 'xml':
                if child.tag == 'song':
                    if transcode != 'raw':
                        # transcoded files have a different extension to the original
                        list_songs.append([object_id,
                                           process((child.find('albumartist')).find('name').text),
                                           process((child.find('album')).find('name').text),
                                           process(os.path.basename(os.path.splitext(child.find('filename').text)[0] + '.' + transcode))])
                    else:
                        list_songs.append([object_id,
                                           process((child.find('albumartist')).find('name').text),
                                           process((child.find('album')).find('name').text),
                                           process(os.path.basename(child.find('filename').text))])
            else:
                if transcode != 'raw':
                    # transcoded files have a different extension to the original
                    list_songs.append([object_id,
                                       process(child['albumartist']['name']),
                                       process(child['album']['name']),
                                       process(os.path.basename(os.path.splitext(child['filename'])[0] + '.' + transcode))])
                else:
                    list_songs.append([object_id,
                                       process(child['albumartist']['name']),
                                       process(child['album']['name']),
                                       process(os.path.basename(child['filename']))])
        # now you have the details you can construct a file destination
        for song in list_songs:
            if NUMERIC:
                # e.g. E:\7\Elliott Smith - 108 - Last Call.mp3
                output = os.path.join(destination, (song[0][-1]), song[1] + " - " + song[3])
            else:
                # e.g. E:\Elliott Smith\An Introduction to Elliott Smith\108 - Last Call.mp3
                output = os.path.join(destination, song[1], song[2], song[3])
            if not os.path.isfile(output):
                # download this file if it's not already there
                print('OUTPUT: ', output)
                self.ampache_connection.download(song[0],
                                 'song', output, transcode)
            else:
                # skip existing files
                print('**EXISTS**: ', output)

    def stream(self, song_id, transcode='raw'):
        """ Download the requested track This could be extended or changed to support lists"""
        # look for various Artists
        object_id = song_id
        search_song = self.ampache_connection.song(object_id)
        list_songs = list()
        # get your song details into a list
        for child in search_song:
            if self.ampache_connection.AMPACHE_API == 'xml':
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
    AMPYCHE()
