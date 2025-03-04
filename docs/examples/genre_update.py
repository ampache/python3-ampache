import ampache
import sys
import time

from mutagen import File

# Function to process each line and update the genre tag
def update_music_metadata(file_path):
    # Open Ampache library
    ampache_connection = ampache.API()

    # load up previous config
    if not ampache_connection.get_config():
        # Set your details manually if we can't get anything
        ampache_connection.set_version('6.6.1')
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

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")  # Split by tab
            if len(parts) != 4:
                continue
            id, album, artist, genre = parts
            genres = genre.split(";")
            album_songs = ampache_connection.execute('album_songs', {'filter_id': id } )
            if "song" in album_songs:
                #print(album_songs)
                for song in album_songs['song']:
                    if "filename" in song:
                        #print(song['filename'])
                        music_file = f"{song['filename']}"

                        # Open the audio file and set the genre
                        audio = File(music_file, easy=True)
                        if audio:
                            print(genres)
                            audio["genre"] = genres
                            audio.save()
                            print(f"Updated {music_file} -> Genre: {genres}")

# Example DOC
#202277	Solar Drifter	Waveshaper	Electronic;Electro;Nu-Disco;Synthwave
#202276	Station Nova	Waveshaper	Electronic;Synthwave
#202275	Endemic	We The North	Electronic;Electro;Synthpop
#201772	Naga: Daemonum Praeteritum	Weapon	Rock;Death Metal;Black Metal
update_music_metadata("genre todo.txt")

