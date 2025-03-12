import ampache
import sys
import time

from mutagen import File

updatefile = "genre todo.txt"
for arguments in sys.argv:
    if arguments[:3] == '/f:':
        updatefile = arguments[3:]


def update_music_metadata(ampache_connection, update_list):
    """ update_music_metadata

        Function to process search results and update the genres
        using the api function get_external_metadata
    """

    album_list = []
    for album in update_list['album']:
        album_list.append(album['id'])
        #album_list = sorted(album_list, reverse=True)
    for album in album_list:
        id = album
        genres = get_external_genres(ampache_connection, id)
        if not genres == False:
            # Found external metadata
            print("Album found " + id)

            # Replacement dictionary (keys are terms to replace, values are the preferred replacements)
            genres = filter_genres(genres)
            album_songs = ampache_connection.execute('album_songs', {'filter_id': id } )
            if not album_songs == False and  "song" in album_songs:
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
                                change = True

                    # update from tags to reflect the new changes
                    if change:
                        print(f"{id} updated {music_file}\n    {existing_genres} => {genres}\n")
                    else:
                        print("No change " + id)
                        print(genres)
        else:
            # Not found online, filter your existing genres anyway
            print("No data found " + id + " filter existing genres")
            album_songs = ampache_connection.execute('album_songs', {'filter_id': id } )
            if not album_songs == False and  "song" in album_songs:
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
                            genres = filter_genres(existing_genres)
                            if not sorted(existing_genres) == sorted(genres):
                                audio["genre"] = genres
                                audio.save()
                                change = True

                    # update from tags to reflect the new changes
                    if change:
                        print(f"{id} updated {music_file}\n    {existing_genres} => {genres}\n")
                    else:
                        print("No change " + id)
                        print(genres)
        # Always update from tags to make sure other changes are set even if we didn't find anything now
        print(ampache_connection.execute('update_from_tags', {'object_type': 'album', 'object_id': id } ))
        time.sleep(5)
        print()


def get_external_genres(ampache_connection, album_id):
    genres = False
    genres_tmp = (ampache_connection.get_external_metadata(album_id, 'album'))
    if not genres_tmp == False and "plugin" in genres_tmp:
        #print("checking " + album_id)
        genres = False
        for plugin in genres_tmp['plugin']:
            if "genre" in genres_tmp['plugin'][plugin]:
                genres = genres_tmp['plugin'][plugin]['genre']
                if isinstance(genres, dict):
                    # Check if all keys are numeric (either int or string that can be cast to int)
                    if all(isinstance(k, int) or (isinstance(k, str) and k.isdigit()) for k in genres.keys()):
                        genres = [genres[key] for key in sorted(genres, key=int)]  # Sort keys numerically
                    else:
                        genres = list(genres.values())
    return genres


def filter_genres(genres: list):
    # replace "rock" with metal if it's got a metal genre
    if any("metal" in genre.lower() for genre in genres) and "rock" in [g.lower() for g in genres]:
        genres = ["Metal" if genre.lower() == "rock" else genre for genre in genres]
    # remove "rock" if it's got Indie rock
    if any("indie rock" in genre.lower() for genre in genres) and "rock" in [g.lower() for g in genres]:
        genres = [genre for genre in genres if genre.lower() != "rock"]
    # remove "rock" if it's got Alternative rock
    if any("alternative rock" in genre.lower() for genre in genres) and "rock" in [g.lower() for g in genres]:
        genres = [genre for genre in genres if genre.lower() != "rock"]

    # Replacement dictionary (keys are terms to replace, values are the preferred replacements)
    replacements = {
        ' Female Vocal': ['Vocal'],
        ' Post Punk': ['Post Punk'],
        'Alt Country': ['Alternative Country'],
        'Alt Rock': ['Alternative Rock'],
        'Alt-Pop': ['Alternative Pop'],
        'Alt. Country': ['Alternative Country'],
        'Alt. Metal': ['Alternative Metal'],
        'Alt. Rock': ['Alternative Rock'],
        'Alt.Metal': ['Alternative Metal'],
        'Alt.Rock': ['Alternative Rock'],
        'Alter Rock': ['Alternative Rock'],
        'Alternative': ['Alternative Rock'],
        'Alternatief': ['Alternative Rock'],
        'Alternatif et Indé': ['Alternative Rock','Indie Rock'],
        'Alternativa & Indie': ['Alternative Rock','Indie Rock'],
        'Alternative  Rock': ['Alternative Rock'],
        'Alternative / Rock': ['Alternative Rock'],
        'Alternative & Indie': ['Alternative Rock','Indie Rock'],
        'Alternative & Punk': ['Punk','Alternative Rock'],
        'Alternative En Indie': ['Alternative Rock','Indie Rock'],
        'Alternative Punk': ['Alternative Rock','Punk'],
        'Alternative Rock / Progressive Rock': ['Alternative Rock','Prog Rock'],
        'Alternative-Rock': ['Alternative Rock'],
        'Alternative/Indie Rock': ['Alternative Rock','Indie Rock'],
        'Alternative/Indie': ['Alternative Rock','Indie Rock'],
        'Alternativna glazba': ['Alternative Rock'],
        'AlternRock': ['Alternative Rock'],
        'Altrnative Rock': ['Alternative Rock'],
        'Ambient Electronic': ['Electronic','Ambient'],
        'Art-Pop': ['Art Pop'],
        'Art-Rock': ['Art Rock'],
        'Atmospheric Death': ['Atmospheric Death Metal'],
        'Atmospheric Pagan': ['Atmospheric Pagan Metal'],
        'Atmospheric/Gothic Metal': ['Atmospheric Gothic Metal'],
        'Avant Garde': ['Avantgarde'],
        'Avant-garde metal': ['Avantgarde Metal'],
        'Avant-Garde': ['Avantgarde'],
        'Avante-Garde Metal': ['Avantgarde Metal'],
        'Berlin School': ['Berlin-School'],
        'Black  Metal': ['Black Metal'],
        'Black Metal Metal': ['Black Metal'],
        'Black Metal/Death Metal': ['Black Metal','Death Metal'],
        'Black/Folk Metal': ['Black Metal','Folk Metal'],
        'Black/Thrash Metal': ['Black Metal','Thrash Metal'],
        'blackmetal': ['Black Metal'],
        'Bluese': ['Blues'],
        'Books & Spoken': ['Spoken Word'],
        'Brit Pop': ['Britpop'],
        'Brit-Pop': ['Britpop'],
        'Celtic Folk Metal': ['Celtic Metal','Folk Metal'],
        'Chill Out': ['Chillout'],
        'Chill Wave': ['Chillwave'],
        'Christian & Gospel': ['Gospel'],
        'Christian Metal': ['Gospel'],
        'Christian Metalcore': ['Gospel'],
        'Christian Pop': ['Gospel'],
        'Christian Punk': ['Gospel'],
        'Christian Rap': ['Gospel'],
        'Christian Rock': ['Gospel'],
        'Christian Worship': ['Gospel'],
        'Coldwave. Post-Punk': ['Coldwave','Post-Punk'],
        'Contemporary Christian': ['Gospel'],
        'Country-Rock': ['Country Rock'],
        'Crossover Prog': ['Rock','Prog Rock'],
        'Crustcore': ['Crust','Post-Metal'],
        'Dance Pop': ['Dance-Pop'],
        'Dance Punk': ['Dance-Punk'],
        'Dark Pop Synthpop': ['Synthpop'],
        'Dark Wave': ['Darkwave'],
        'Darkfolk': ['Dark Folk'],
        'darksynth': ['Dark Synth'],
        'Darkwave/EBM': ['Darkwave','EBM'],
        'Death Rock': ['Deathrock'],
        'Dreampop': ['Dream Pop'],
        'Drum & Bass': ['Drum n Bass'],
        'Drum and Bass': ['Drum n Bass'],
        'Electro Industrial': ['Electronic','Rock','Industrial'],
        'Electro Pop': ['Electropop'],
        'Electronica & Dance': ['Dance','Electronica'],
        'Électronique': ['Electronic'],
        'Elektronička glazba': ['Electronica'],
        'Eletronic': ['Electronic'],
        'Emo-Pop': ['Emo Pop'],
        'Epic Atmospheric Black Metal': ['Atmospheric Black Metal'],
        'Epic Black Metal': ['Black Metal'],
        'Epic Doom Metal': ['Doom Metal'],
        'Epic Folk Metal': ['Folk Metal'],
        'Epic Heavy Metal': ['Heavy Metal'],
        'Epic Pagan Meta': ['Epic Pagan Metal'],
        'Epic Viking Metal': ['Viking Metal'],
        'Epic': ['Epic Metal'],
        'Euro-House': ['Euro House'],
        'Eurohouse': ['Euro House'],
        'Experemental Black Metal': ['Experimental Black Metal'],
        'Experemental Folk': ['Experimental Folk'],
        'Experemental Metal': ['Experimental Metal'],
        'Experemental': ['Experimental'],
        'Expiremental': ['Experimental'],
        'Female Vocalist': ['Vocal'],
        'Female Vocals': ['Vocal'],
        'Films/Games': ['Video Game Music'],
        'Folk-Pop': ['Folk Pop'],
        'Folk-Rock': ['Folk Rock'],
        'Funeral Doom': ['Funeral Doom Metal'],
        'Funk / Soul': ['Funk/Soul'],
        'Futurepop': ['Future Pop'],
        'Gabba': ['Gabber'],
        'Game': ['Video Game Music'],
        'German Hip-Hop': ['German Hip Hop'],
        'Germany': ['German'],
        'Glitch-Hop': ['Glitch Hop'],
        'goth-rock': ['Goth Rock'],
        'Gothic Rock': ['Goth Rock'],
        'Hardcore Hip-Hop': ['Hardcore Hip Hop'],
        'Hardcore Punk': ['Hardcore'],
        'Heavy / Power Metal': ['Heavy Metal','Power Metal'],
        'Heavy-Metal': ['Heavy Metal'],
        'Hip-hop': ['Hip Hop'],
        'Idie-Pop': ['Indie Pop'],
        'Imdustrial': ['Industrial'],
        'Indie / Folk Rock / Singer-Songwriter': ['Folk Rock','Indie Rock'],
        'Indie / Pop-Rock': ['Indie Rock','Pop Rock'],
        'Indie Pop / Electronic': ['Electronic','Indie Pop'],
        'Indie Pop / Hip Hop': ['Hip Hop','Indie Pop'],
        'Indie Pop / Indie Rock': ['Indie Pop','Indie Rock'],
        'Indie Rock - Shoegaze': ['Indie Rock','Shoegaze'],
        'Indie Rock / Electronic': ['Electronic','Indie Rock'],
        'Indie Rock / Psychedelic / Experimental / Electronic': ['Electronic','Experimental','Indie Rock','Psychedelic'],
        'Indie rock/ Electronic': ['Electronic','Indie Rock'],
        'Indie Rock/Rock Pop': ['Indie Rock','Rock Pop'],
        'Indie-Folk': ['Indie Folk'],
        'Indie-Pop': ['Indie Pop'],
        'Indie-Rock': ['Indie Rock'],
        'Indiel Rock': ['Indie Rock'],
        'Indierock': ['Indie Rock'],
        'Industrial Metal / NDH': ['Industrial Metal','Neue Deutsche Harte'],
        'Jam Bands': ['Jam Band'],
        'Jazz Rock': ['Jazz-Rock'],
        'JPop': ['J-Pop'],
        'JRock': ['J-Rock'],
        'Kids': ['Children\'s'],
        'Melodic Black Metal': ['Black Metal'],
        'Melodic Black': ['Melodic Black Metal'],
        'Melodic BlackDeath Metal': ['Death Metal','Melodic Black Metal'],
        'Melodic Death': ['Melodic Death Metal'],
        'Melodic Death/Groove Metal': ['Groove Metal','Melodic Death Metal'],
        'NDH': ['Neue Deutsche Harte'],
        'Neo - Classical': ['Neo-Classical'],
        'Neo Folk': ['Neofolk'],
        'Neo Psychedelia': ['Neo-psychedelia'],
        'Neo Psychedelic': ['Neo-psychedelia'],
        'Neo-Soul': ['Neo Soul'],
        'Neoclassical': ['Neo-Classical'],
        'New Wave Pop': ['New Wave','Pop'],
        'newage': ['New Age'],
        'Noise-rock': ['Noise Rock'],
        'Nu Disco': ['Nu-Disco'],
        'Nu Metal)': ['Nu Metal'],
        'Nu-Metal': ['Nu Metal'],
        'Occult Black Metal': ['Black Metal'],
        'Pagan/Folk Metal': ['Folk Metal','Pagan Metal'],
        'pop emo': ['Emo Pop'],
        'Pop Indé': ['Indie Pop'],
        'Pop Rock/ Christian': ['Gospel','Pop Rock'],
        'Pop-Punk': ['Pop Punk'],
        'Pop-Rock': ['Pop Rock'],
        'Pop/Rock': ['Pop','Rock'],
        'Post-bop': ['Post Bop'],
        'Post Grunge': ['Post-grunge'],
        'Post Hardcore': ['Post-Hardcore'],
        'Post Metal': ['Post-Metal'],
        'Post Modern': ['Post-Modern'],
        'Post Punk Revival': ['Post-Punk Revival'],
        'Post Punk': ['Post-Punk'],
        'Post-Black Metal': ['Black Metal','Post-Metal'],
        'PostRock': ['Post Rock'],
        'Post-Rock': ['Post Rock'],
        'Powerpop': ['Power Pop'],
        'Prog-Rock': ['Prog Rock'],
        'Progressive Black': ['Progressive Black Metal'],
        'Progressive Death Metal  Grindcore': ['Grindcore','Progressive Death Metal'],
        'Progressive Rock': ['Prog Rock'],
        'Progressive Rocl': ['Prog Rock'],
        'Psych Rock': ['Psychedelic Rock'],
        'Psychedelic Folk Rock': ['Folk Rock','Psychedelic Rock'],
        'Psychedelic-Rock': ['Psychedelic Rock'],
        'Psytrance': ['Psy-Trance'],
        'Raggae': ['Reggae'],
        'Retro Wave': ['Retrowave'],
        'rimental Black Metal': ['Experimental Black Metal'],
        'Rock \'N\' Roll': ['Rock & Roll'],
        'Rock indé': ['Indie Rock'],
        'Rock progressif': ['Prog Rock'],
        'Rock Progressivo Italiano': ['Prog Rock'],
        'Rock`n`Roll': ['Rock & Roll'],
        'Rosk': ['Rock'],
        'Shoegazer': ['Shoegaze'],
        'Shoegazing': ['Shoegaze'],
        'Singer & Songwriter': ['Singer-songwriter'],
        'Singer/Songwriter': ['Singer-songwriter'],
        'Ska Punk': ['Ska'],
        'Ska-Punk': ['Ska'],
        'Soft-Rock': ['Soft Rock'],
        'Soundtracks': ['Soundtrack'],
        'Speech': ['Spoken Word'],
        'Stand-Up Comedy': ['Standup Comedy'],
        'Sunthpop': ['Synthpop'],
        'Sympho Power Metal': ['Symphonic Metal','Power Metal'],
        'Symphonic Power Metal': ['Symphonic Metal','Power Metal'],
        'Symphonic Power': ['Symphonic Metal','Power Metal'],
        'Synth Gothic': ['Synth Goth'],
        'Synth Pop': ['Synthpop'],
        'Synth-Goth': ['Synth Goth'],
        'Synth-pop': ['Synthpop'],
        'Synth-Punk': ['Synth Punk'],
        'Synth-Rock': ['Synth Rock'],
        'Syntwave': ['Synthwave'],
        'TBM': ['Technical Black Metal'],
        'Technical Black': ['Technical Black Metal'],
        'Thrash': ['Thrash Metal'],
        'Trip-Hop': ['Trip Hop'],
        'Unblack': ['Unblack Metal'],
        'Video Game Soundtrack': ['Video Game Music'],
        'Video Game': ['Video Game Music'],
        'Viking': ['Viking Metal'],
        'Vocaloud': ['Vocaloid'],
        'Альтернативная музыка': ['Alternative Rock'],
        'Детская музыка': ['Children\'s'],
        'Поп': ['Pop'],
        'Рок': ['Rock'],
    }

    # Loop to replace keys with values in the genre list
    output_genres = []
    for genre in genres:
        if genre in replacements:
            output_genres.extend(replacements[genre])  # Add multiple mapped values
        else:
            output_genres.append(genre)
    return list(dict.fromkeys(output_genres))


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

""" Get a session key using the handshake

    * ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
    * ampache_api = (string) encrypted apikey OR password if using password auth
    * user        = (string) username //optional
    * timestamp   = (integer) UNIXTIME() //optional
    * version     = (string) API Version //optional
"""
ampache_session = ampache_connection.execute('handshake')

# Fail if you didn't connect
if not ampache_session:
    sys.exit(ampache_connection.AMPACHE_VERSION + ' ERROR Failed to connect to ' + ampache_connection.AMPACHE_URL)

# Update using the API

""" SEARCH RULES

    Define your own search rules here using the examples below
    Check https://ampache.org/api/api-advanced-search/ for more rules and examples
"""

### Get ALL albums
update_music_metadata(ampache_connection.execute('albums'))

### Albums with a genre that only has 1 album
#update_music_metadata(ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
#                      'rules': [
#                           ['genre_count_album', 2, 1]
#                      ] } ))

### Genre = Rock but another genre is Indie Rock
#update_music_metadata(ampache_connection, ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
#                      'rules': [
#                          ['genre', 4, 'Rock'],
#                          ['genre', 4, 'Indie Rock']
#                      ] } ))

### Genre = Rock but another genre contains metal
update_music_metadata(ampache_connection, ampache_connection.execute('search', {
                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
                      'rules': [
                          ['genre', 4, 'Rock'],
                          ['genre', 0, 'metal']
                      ] } ))

### Album genre count > 1 and < 5 
update_music_metadata(ampache_connection, ampache_connection.execute('search', {
                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
                      'rules': [
                          ['genre_count_album', 4, 1],
                          ['genre_count_album', 5, 5]
                      ] } ))

### Search by album; ID < 160304
#update_music_metadata(ampache_connection, ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
#                      'rules': [
#                          ['id', 5, 160304]
#                      ] } ))

### Search by album with no genre tags
#update_music_metadata(ampache_connection, ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0,
#                      'rules': [
#                          ['no_genre', 0, '']
#                      ] } ))

### Search by Album Artist = 'Green day'
#update_music_metadata(ampache_connection, ampache_connection.execute 'search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0,
#                      'rules': [
#                          ['album_artist', 4, 'Green day']
#                      ] } ))

### Search by Song Artist = 'newt'
#update_music_metadata(ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0,
#                      'rules': [
#                         ['song_artist', 4, 'newt']
#                      ] } ))

### Album updated BEFORE 2024-01-11T00:00
#update_music_metadata(ampache_connection, ampache_connection.execute('search', {
#                      'object_type': 'album', 'operator': 'and', 'limit': 0, 'random': 1,
#                      'rules': [
#                          ['updated', 0, '2024-01-11T00:00']
#                      ] } ))