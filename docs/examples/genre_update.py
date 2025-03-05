import ampache
import os
import sys
import time

from mutagen import File

updatefile = "genre todo.txt"
for arguments in sys.argv:
    if arguments[:3] == '/f:':
        updatefile = arguments[3:]

# Function to process each line and update the genre tag
def update_music_metadata():
    # Open Ampache library
    ampache_connection = ampache.API()

    #ampache_connection.set_debug(True)

    # load up previous config
    if not ampache_connection.get_config():
        # Set your details manually if we can't get anything
        ampache_connection.set_version('6.6.6')
        ampache_connection.set_url('https://music.server')
        ampache_connection.set_key('mysuperapikey')
        ampache_connection.set_user('myusername')

    # Get a session key using the handshake
    #
    # * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
    # * ampache_api = (string) encrypted apikey OR password if using password auth
    # * user        = (string) username //optional
    # * timestamp   = (integer) UNIXTIME() //optional
    # * version     = (string) API Version //optional
    ampache_session = ampache_connection.execute('handshake')


    # Fail if you didn't connect
    if not ampache_session:
        sys.exit(ampache_connection.AMPACHE_VERSION + ' ERROR Failed to connect to ' + ampache_connection.AMPACHE_URL)
    
    update_list = (ampache_connection.execute('search', {'object_type': 'album', 'operator': 'and', 'rules': [['id', 5, 196833]], 'limit': 0 } ))

    for album in update_list['album']:
        genres_tmp = (ampache_connection.get_external_metadata(album['id'], 'album'))
        if "plugin" in genres_tmp:
            genres = False
            for plugin in genres_tmp['plugin']:
                if "genre" in genres_tmp['plugin'][plugin]:
                    genres = genres_tmp['plugin'][plugin]['genre']
            if not genres == False:
                id = album['id']
                album_songs = ampache_connection.execute('album_songs', {'filter_id': id } )
                if "song" in album_songs:
                    #print(album_songs)
                    change = False
                    for song in album_songs['song']:
                        if "filename" in song:
                            #print(song['filename'])
                            music_file = f"{song['filename']}"

                            # Open the audio file and set the genre
                            audio = File(music_file, easy=True)
                            if audio:
                                existing_genres = audio.get("genre", [])
                                if not sorted(existing_genres) == sorted(genres):
                                    audio["genre"] = genres
                                    audio.save()
                                    print(f"{id} updated {music_file}\n    {existing_genres} => {genres}\n")
                                    change = True

                    # update from tags to reflect the new changes
                    if change:
                        print("update_from_tags " + id)
                        print(ampache_connection.execute('update_from_tags', {'object_type': 'album', 'object_id': id } ))
                    else:
                        print("No change " + id)


# Update using the API
update_music_metadata()

