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
def update_music_metadata(file_path):
    # Open Ampache library
    ampache_connection = ampache.API()

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
    
    update_list = [200404,200403,200402,200401,200400,200399,200397,200396,200395,200394,200393,200391,200390,200386,200385,200383,200382,200381,200380,200374,200363,200362,200361,200360,200359,200358,200357,200356,200355,200354,200353,200352,200351,200350,200349,200348,200347,200346,200345,200344,200343,200342,200341,200340,200339,200338,200337,200336,200335,200334,200332,200331,200330,200329,200328,200327,200326,200325,200324,200323,200322,200321,200320,200319,200318,200317,200315,200314,200312,200310,200308,200307,200306,200305,200304,200303,200301,200300,200299,200298,200297,200296,200295,200294,200291,200289,200288,200286,200285,200284,200282,200281]
    for item_id in update_list:
        print(ampache_connection.execute('update_from_tags', {'object_type': 'album', 'object_id': item_id } ))
    print("checking " + file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")  # Split by tab
            if len(parts) != 4:
                continue
            id, album, artist, genre = parts
            genre_tmp = genre.split(";")
            genres = [item for item in genre_tmp if item != '']
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


# Example DOC
#album	AlbumName	Artist	GenreList
#202277	Solar Drifter	Waveshaper	Electronic;Electro;Nu-Disco;Synthwave
#202276	Station Nova	Waveshaper	Electronic;Synthwave
#202275	Endemic	We The North	Electronic;Electro;Synthpop
#201772	Naga: Daemonum Praeteritum	Weapon	Rock;Death Metal;Black Metal

if os.path.isfile(updatefile):
    update_music_metadata(updatefile)

