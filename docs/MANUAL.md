# Ampache class API (object)

## Variables

* AMPACHE_API ('xml'|'json') default: 'xml'
* AMPACHE_DEBUG (bool) default: False
* AMPACHE_URL (string)
* AMPACHE_SESSION (string)
* AMPACHE_USER (string)
* AMPACHE_KEY (string)
* DOCS_PATH = (string) default: "docs/"
* CONFIG_FILE = (string) default: "ampache.json"
* CONFIG_PATH = (string)

## HELPER FUNCTIONS

Functions that are used by the library to manipulate data, connect to Ampache or general processing

### set_format

set_format(myformat: str)

Allow forcing a default format

* myformat = (string) 'xml'|'json'

### set_debug

set_debug(mybool: bool)

This function can be used to enable/disable debugging messages

* bool = (boolean) Enable/disable debug messages

### set_debug_path

set_debug_path(path_string: str)

This function can be used to set the output folder for docs

* path_string = (string) folder path

### set_user

set_user(myuser: str)

Set the user string for connection

* myuser (string)

### set_key

set_key(mykey: str)

Set AMPACHE_KEY (api key or password)

* mykey (string)

### set_url

set_url(myurl: str)

Set the ampache url

* myurl (string)

### set_config_path

set_config_path(path: str):

Set the folder which contains your config to a folder instead of the working directory

* path = (string)

### get_config

get_config():

Read the config and set values from the json config file

### save_config

save_config():

Save config to a json file for use later

### test_result

test_result(result, title)

This function can be used to enable/disable debugging messages

* bool = (boolean) Enable/disable debug messages

### return_data

return_data(data)

Return json or xml data based on api format

* data (string)

### get_id_list

get_id_list(data, attribute: str)

Return a list of id's from the data you've got from the api

* data      = (mixed) XML or JSON from the API
* attribute = (string) attribute you are searching for

### get_object_list

get_object_list(data, field: str, data_format: str = 'xml') @staticmethod

return a list of objects from the data matching your field stirng

* data        = (mixed) XML or JSON from the API
* field       = (string) field you are searching for
* data_format = (string) 'xml','json'

### write_xml

write_xml(xmlstr, filename: str) @staticmethod

This function can be used to write your xml responses to a file.

* xmlstr   = (xml) xml to write to file
* filename = (string) path and filename (e.g. './ampache.xml')

### get_message

get_message(data) @staticmethod

Return the string message text from the api response

* data = (mixed) XML or JSON from the API

### write_json

write_json(json_data: str, filename: str) @staticmethod

This function can be used to write your json responses to a file.

* json_data = (json) json to write to file
* filename  = (string) path and filename (e.g. './ampache.json')

### encrypt_password

encrypt_password(password: str, current_time: int) @staticmethod

This function can be used to encrypt your password into the accepted format.

* password = (string) unencrypted password string
* time     = (integer) linux time

### encrypt_string

encrypt_string(api_key: str, username: str) @staticmethod

This function can be used to encrypt your apikey into the accepted format.

* api_key = (string) unencrypted apikey
* user    = (string) username

### fetch_url

fetch_url(full_url: str, api_format: str, method: str)

This function is used to fetch the string results using urllib

* full_url   = (string) url to fetch
* api_format = (string) 'xml'|'json'
* method     = (string)

## API FUNCTIONS

All the Ampache functions from the API

### handshake

handshake(ampache_url: str, ampache_api: str, ampache_user: str = False, timestamp: int = 0, version: str = '5.0.0')

This is the function that handles verifying a new handshake
Takes a timestamp, auth key, and username.

* ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
* ampache_api = (string) encrypted apikey OR password if using password auth
* user        = (string) username //optional
* timestamp   = (integer) UNIXTIME() //optional
* version     = (string) //optional

### ping

ping(ampache_url: str, ampache_api: str = False, version: str = '5.0.0')

This can be called without being authenticated, it is useful for determining if what the status
of the server is, and what version it is running/compatible with

* ampache_url = (string) Full Ampache URL e.g. 'https://music.com.au'
* ampache_api = (string) encrypted apikey //optional

### register

register(username, fullname, password, email)

Register a new user.
Requires the username, password and email.

* username = (string)
* fullname = (string) //optional
* password = (string) hash('sha256', $password))
* email    = (string)

### lost_password

lost_password()

Allows a non-admin user to reset their password without web access to the main site.
It requires a reset token hash using your username and email

* auth = (string) (
    $username;
    $key = hash('sha256', 'email');
    auth = hash('sha256', $username . $key);
  ) 

### goodbye

goodbye()

Destroy session for ampache_api auth key.

### url_to_song

url_to_song(url)

This takes a url and returns the song object in question

* url = (string) Full Ampache URL from server, translates back into a song XML

### get_similar

get_similar(object_type, filter_id: int, offset=0, limit=0)

Return similar artist id's or similar song ids compared to the input filter

* object_type = (string) 'song'|'album'|'artist'|'playlist'
* filter_id   = (integer) $artist_id or song_id
* offset      = (integer) //optional
* limit       = (integer) //optional

### list
list(object_type, filter_str: str = False,  exact: int = False, add: int = False, update: int = False, offset=0, limit=0):

This takes a named array of objects and returning `id`, `name`, `prefix` and `basename`

* object_type = (string) 'song'|'album'|'artist'|'album_artist'|'playlist'
* filter_str  = (string) search the name of the object_type //optional
* exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* add         = (integer) UNIXTIME() //optional
* update      = (integer) UNIXTIME() //optional
* offset      = (integer) //optional
* limit       = (integer) //optional

### browse

browse(filter_str: str = False, object_type: str = False, catalog: int = False, add: int = False, update: int = False, offset=0, limit=0):

Return children of a parent object in a folder traversal/browse style
If you don't send any parameters you'll get a catalog list (the 'root' path)

* filter_str  = (string) object_id //optional
* object_type = (string) 'root', 'catalog', 'artist', 'album', 'podcast' // optional
* catalog = (integer) catalog ID you are browsing
* add     = Api::set_filter(date) //optional
* update  = Api::set_filter(date) //optional
* offset  = (integer) //optional
* limit   = (integer) //optional

### get_indexes

get_indexes(object_type, filter_str: str = False, exact: int = False, add: int = False, update: int = False, include=False, offset=0, limit=0)

This takes a collection of inputs and returns ID + name for the object type

* object_type = (string) 'song'|'album'|'artist'|'album_artist'|'playlist'
* filter_str  = (string) search the name of the object_type //optional
* exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* add         = (integer) UNIXTIME() //optional
* update      = (integer) UNIXTIME() //optional
* include     = (integer) 0,1 include songs if available for that object //optional
* offset      = (integer) //optional
* limit       = (integer) //optional

### artists

artists(filter_str: str = False, add: int = False, update: int = False, offset=0, limit=0, include=False)

This takes a collection of inputs and returns artist objects.

* filter_str   = (string) search the name of an artist //optional
* add          = (integer) UNIXTIME() //optional
* update       = (integer) UNIXTIME() //optional
* offset       = (integer) //optional
* limit        = (integer) //optional
* include      = (string) 'albums', 'songs' //optional
* album_artist = (boolean) 0,1 if true filter for album artists only //optional

### artist

artist(filter_id: int, include=False)

This returns a single artist based on the UID of said artist

* filter_id = (integer) $artist_id
* include   = (string) 'albums', 'songs' //optional

### artist_albums

artist_albums(filter_id: int, offset=0, limit=0)

This returns the albums of an artist

* filter_id = (integer) $artist_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### artist_songs

artist_songs(filter_id: int, offset=0, limit=0)

This returns the songs of the specified artist

* filter_id = (integer) $artist_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### albums

albums(filter_str: str = False, exact=False, add: int = False, update: int = False, offset=0, limit=0, include=False)

This returns albums based on the provided search filters

* filter_str = (string) search the name of an album //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* add        = (integer) UNIXTIME() //optional
* update     = (integer) UNIXTIME() //optional
* offset     = (integer) //optional
* limit      = (integer) //optional
* include    = (string) 'songs' //optional

### album

album(filter_id: int, include=False)

This returns a single album based on the UID provided

* filter_id = (integer) $album_id
* include   = (string) 'songs' //optional

### album_songs

album_songs(filter_id: int, offset=0, limit=0)

This returns the songs of a specified album

* filter_id = (integer) $album_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### genres

genres(filter_str: str = False, exact: int = False, offset=0, limit=0)

This returns the genres (Tags) based on the specified filter

* filter_str = (string) search the name of a genre //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### genre

genre(filter_id: int)

This returns a single genre based on UID

* filter_id = (integer) $genre_id

### genre_artists

genre_artists(filter_id: int, offset=0, limit=0)

This returns the artists associated with the genre in question as defined by the UID

* filter_id = (integer) $genre_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### genre_albums

genre_albums(filter_id: int, offset=0, limit=0)

This returns the albums associated with the genre in question

* filter_id = (integer) $genre_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### genre_songs

genre_songs(filter_id: int, offset=0, limit=0)

returns the songs for this genre

* filter_id = (integer) $genre_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### songs

songs(filter_str: str = False, exact: int = False, add: int = False, update: int = False, offset=0, limit=0)

Returns songs based on the specified filter_str

* filter_str = (string) search the name of a song //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* add        = (integer) UNIXTIME() //optional
* update     = (integer) UNIXTIME() //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### song

song(filter_id: int)

returns a single song

* filter_id = (integer) $song_id

### song_delete

song_delete(filter_id: int)

Delete an existing song.

* filter_id   = (string) UID of song to delete

### playlists

playlists(filter_str: str = False, exact: int = False, offset=0, limit=0)

This returns playlists based on the specified filter

* filter_str = (string) search the name of a playlist //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### playlist

playlist(filter_id: int)

This returns a single playlist

* filter_id = (integer) $playlist_id

### playlist_songs

playlist_songs(filter_id: int, offset=0, limit=0)

This returns the songs for a playlist

* filter_id = (integer) $playlist_id
* offset    = (integer) //optional
* limit     = (integer) //optional

### playlist_create

playlist_create(name, object_type)

This create a new playlist and return it

* name        = (string)
* object_type = (string)

### playlist_edit

playlist_edit(filter_id: int, name=False, object_type=False)

This modifies name and type of a playlist

* filter_id   = (integer)
* name        = (string) playlist name //optional
* object_type = (string) 'public'|'private'

### playlist_delete

playlist_delete(filter_id: int)

This deletes a playlist

* filter_id = (integer) $playlist_id

### playlist_add_song

playlist_add_song(filter_id: int, song_id, check=False)

This adds a song to a playlist.
Added duplicate checks in 400003

* filter_id = (integer) $playlist_id
* song_id   = (integer) $song_id
* check     = (boolean|integer) (True,False | 0|1) Check for duplicates //optional

### playlist_remove_song

playlist_remove_song(filter_id: int, song_id=False, track=False)


This removes a song from a playlist. Previous versions required 'track' instead of 'song'.

* filter_id = (integer) $playlist_id
* song_id   = (integer) $song_id //optional
* track     = (integer) $playlist_track number //optional

### playlist_generate

playlist_generate(mode='random', filter_str: str = False, album_id=False, artist_id=False, flagged=False, list_format='song', offset=0, limit=0)

Get a list of song XML, indexes or id's based on some simple search criteria

'recent' will search for tracks played after 'Popular Threshold' days

'forgotten' will search for tracks played before 'Popular Threshold' days

'unplayed' added in 400002 for searching unplayed tracks

* mode        = (string) 'recent', 'forgotten', 'unplayed', 'random' (default = 'random') //optional
* filter_str  = (string) string LIKE matched to song title //optional
* album_id    = (integer) $album_id //optional
* artist_id   = (integer) $artist_id //optional
* flagged     = (integer) get flagged songs only 0, 1 (default=0) //optional
* list_format = (string) 'song', 'index','id' (default = 'song') //optional
* offset      = (integer) //optional
* limit       = (integer) //optional

### shares

shares(filter_str: str = False,  exact: int = False, offset=0, limit=0)

* filter_str = (string) search the name of a share //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### share

share(filter_id: int)

Return shares by UID

* filter_id = (integer) UID of Share

### share_create

share_create(filter_id: int, object_type, description=False, expires=False)

Create a public url that can be used by anyone to stream media.
Takes the file id with optional description and expires parameters.

* filter_id   = (integer) $object_id
* object_type = (string) object_type ('song', 'album', 'artist')
* description = (string) description (will be filled for you if empty) //optional
* expires     = (integer) days to keep active //optional

### share_edit

share_edit(filter_id: int, can_stream=False, can_download=False, expires=False, description=False)

Update the description and/or expiration date for an existing share.
Takes the share id to update with optional description and expires parameters.

INPUT
* filter_id    = (integer) UID of Share
* can_stream   = (boolean) 0,1 //optional
* can_download = (boolean) 0,1 //optional
* expires      = (integer) number of whole days before expiry //optional
* description  = (string) update description //optional

### share_delete

share_delete(filter_id: int)

Delete an existing share.

INPUT
* filter_id = (integer) UID of Share to delete

### catalogs

catalogs(filter_str: str = False, offset=0, limit=0)

* filter_str = (string) search the name of a catalog //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### catalog

catalog(filter_id: int, offset=0, limit=0)

Return catalogs by UID

* filter_id = (integer) UID of catalog

### catalog_add

catalog_add(cat_name, cat_path, cat_type=False, media_type=False, file_pattern=False, folder_pattern=False, username=False, password=False)

Create a new catalog

* name           = (string) catalog_name
* path           = (string) URL or folder path for your catalog
* type           = (string) catalog_type default: local ('local', 'beets', 'remote', 'subsonic', 'seafile', 'beetsremote') //optional
* media_type     = (string) Default: 'music' ('music', 'podcast', 'clip', 'tvshow', 'movie', 'personal_video') //optional
* file_pattern   = (string) Pattern used identify tags from the file name. Default '%T - %t' //optional
* folder_pattern = (string) Pattern used identify tags from the folder name. Default '%a/%A' //optional
* username       = (string) login to remote catalog ('remote', 'subsonic', 'seafile') //optional
* password       = (string) password to remote catalog ('remote', 'subsonic', 'seafile', 'beetsremote') //optional

### catalog_delete

catalog_delete(filter_id: int)

Delete an existing catalog. (if it exists)

* filter = (string) catalog_id to delete

### catalog_action

catalog_action(task, catalog_id)

Kick off a catalog update or clean for the selected catalog

* task       = (string) 'add_to_catalog'|'clean_catalog'|'verify_catalog'|'gather_art'
* catalog_id = (integer) $catalog_id

### catalog_file

catalog_file(file, task, catalog_id)

Perform actions on local catalog files.
Single file versions of catalog add, clean and verify.
Make sure you remember to urlencode those file names!

* file       = (string) urlencode(FULL path to local file)
* task       = (string) 'add'|'clean'|'verify'|'remove'
* catalog_id = (integer) $catalog_id

### catalog_folder

catalog_folder(folder, task, catalog_id)

Perform actions on local catalog folders.
Single folder versions of catalog add, clean and verify.
Make sure you remember to urlencode those folder names!

* folder      = (string) urlencode(FULL path to local folder)
* task        = (string) 'add'|'clean'|'verify'|'remove'
* catalog_id  = (integer) $catalog_id

### podcasts

podcasts(filter_str: str = False, exact: int = False, offset=0, limit=0)

* filter_str = (string) search the name of a podcast //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### podcast

podcast(filter_id: int, include=False)

Return podcasts by UID

* filter_id = (integer) UID of Podcast
* include   = (string) 'episodes' Include episodes with the response //optional

### podcast_create

podcast_create(url, catalog_id)

Return podcasts by UID

* url        = (string) rss url for podcast
* catalog_id = (string) podcast catalog

### podcast_edit

podcast_edit(filter_id: int, feed=False, title=False, website=False, description=False, generator=False, copyright_str=False)

Update the description and/or expiration date for an existing podcast.
Takes the podcast id to update with optional description and expires parameters.

* filter_id     = (integer) $podcast_id
* feed          = (string) feed url (xml!) //optional
* title         = (string) title string //optional
* website       = (string) source website url //optional
* description   = (string) //optional
* generator     = (string) //optional
* copyright_str = (string) //optional

### podcast_delete

podcast_delete(filter_id: int)

Delete an existing podcast.

* filter_id = (integer) UID of podcast to delete

### podcast_episodes

podcast_episodes(filter_id: int, offset=0, limit=0)

* filter_id = (string) UID of podcast
* offset    = (integer) //optional
* limit     = (integer) //optional

### podcast_episode

podcast_episode(filter_id: int)

Return podcast_episodes by UID

* filter_id = (integer) UID of Podcast

### podcast_episode_delete

podcast_episode_delete(filter_id: int)

Delete an existing podcast_episode.

* filter_id = (integer) UID of podcast_episode to delete

### update_podcast

update_podcast(filter_id: int)

Sync and download new podcast episodes

* filter_id = (integer) UID of Podcast

### search_songs

search_songs(filter_str, offset=0, limit=0)

This searches the songs and returns... songs

* filter_str = (string) search the name of a song
* offset     = (integer) //optional
* limit      = (integer) //optional

### advanced_search

advanced_search(rules, operator='and', object_type='song', offset=0, limit=0, random=0)

Perform an advanced search given passed rules
the rules can occur multiple times and are joined by the operator item.

Refer to the wiki for further information
http://ampache.org/api/api-advanced-search

* rules       = (array) = [[rule_1,rule_1_operator,rule_1_input], [rule_2,rule_2_operator,rule_2_input], [etc]]
* operator    = (string) 'and'|'or' (whether to match one rule or all) //optional
* object_type = (string)  //optional
* offset      = (integer) //optional
* limit       = (integer) //optional
* random      = (integer) 0|1' //optional

### videos

videos(filter_str: str = False, exact: int = False, offset=0, limit=0)

This returns video objects!

* filter_str = (string) search the name of a video //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### video

video(filter_id: int)

This returns a single video

* filter_id = (integer) $video_id

### localplay

localplay(command, oid=False, otype=False, clear=0)

This is for controlling localplay

* command = (string) 'next', 'prev', 'stop', 'play', 'pause', 'add', 'volume_up', 'volume_down', 'volume_mute', 'delete_all', 'skip', 'status'
* oid     = (integer) object_id //optional
* otype   = (string) 'Song', 'Video', 'Podcast_Episode', 'Channel', 'Broadcast', 'Democratic', 'Live_Stream' //optional
* clear   = (integer) 0,1 Clear the current playlist before adding //optional

### localplay_songs

localplay()

Get the list of songs in your localplay playlist

### democratic

democratic(method, oid)

This is for controlling democratic play

* oid    = (integer) object_id (song_id|playlist_id)
* method = (string) 'vote'|'devote'|'playlist'|'play'

### stats

stats(object_type, filter_str='random', username=False, user_id=False, offset=0, limit=0)

This gets library stats for different object types. When filter is null get some random items instead

* object_type = (string) 'song'|'album'|'artist'
* filter_str  = (string) 'newest'|'highest'|'frequent'|'recent'|'flagged'|'random'
* offset      = (integer) //optional
* limit       = (integer) //optional
* user_id     = (integer) //optional
* username    = (string) //optional

### users

users()

Get ids and usernames for your site users

INPUTS

### user

user(username)

This gets a user's public information

* username = (string)

### followers

followers(username)

This gets a user's followers

* username = (string)

### following

following(username)

This get the user list followed by an user

* username = (string)

### toggle_follow

toggle_follow(username)

This follow/unfollow an user

* username = (string)

### last_shouts

last_shouts(username, limit=0)

This get the latest posted shouts

* username = (string)
* limit    = (integer) //optional

### rate

rate(object_type, object_id, rating)

This rates a library item

* object_type = (string) 'song'|'album'|'artist'
* object_id   = (integer) $object_id
* rating      = (integer) 0|1|2|3|4|5

### flag

flag(object_type, object_id, flagbool)

This flags a library item as a favorite

Setting flagbool to true (1) will set the flag
Setting flagbool to false (0) will remove the flag

* object_type = (string) 'song'|'album'|'artist'
* object_id   = (integer) $object_id
* flagbool    = (boolean|integer) (True,False | 0|1)

### record_play

record_play(object_id, user_id, client='AmpacheAPI')

Take a song_id and update the object_count and user_activity table with a play.
This allows other sources to record play history to ampache

* object_id = (integer) $object_id
* user_id   = (integer) $user_id
* client    = (string) $agent //optional

### scrobble

scrobble(title, artist_name, album_name, mbtitle=False, mbartist=False, mbalbum=False, stime=False, client='AmpacheAPI')

Search for a song using text info and then record a play if found.
This allows other sources to record play history to ampache

* title       = (string) song title
* artist_name = (string) artist name
* album_name  = (string) album name
* mbtitle     = (string) song mbid //optional
* mbartist    = (string) artist mbid //optional
* mbalbum     = (string) album mbid //optional
* stime       = (integer) UNIXTIME() //optional
* client      = (string) //optional

### timeline

timeline(username, limit=0, since=0)

This get a user timeline

* username = (string)
* limit    = (integer) //optional
* since    = (integer) UNIXTIME() //optional

### friends_timeline

friends_timeline(limit=0, since=0)

This get current user friends timeline

* limit = (integer) //optional
* since = (integer) UNIXTIME() //optional

### update_from_tags

update_from_tags(ampache_type, ampache_id)

updates a single album,artist,song from the tag data

* object_type = (string) 'artist'|'album'|'song'
* object_id   = (integer) $artist_id, $album_id, $song_id

### update_art

update_art(ampache_type, ampache_id, overwrite=False)

updates a single album, artist, song looking for art files
Doesn't overwrite existing art by default.

* object_type = (string) 'artist'|'album'|'song'
* object_id   = (integer) $artist_id, $album_id, $song_id
* overwrite   = (boolean|integer) (True,False | 0|1) //optional

### update_artist_info

update_artist_info(object_id)

Update artist information and fetch similar artists from last.fm
Make sure lastfm_api_key is set in your configuration file

* object_id = (integer) $artist_id

### stream

stream(object_id, object_type, destination)

stream a song or podcast episode

* object_id   = (string) $song_id / $podcast_episode_id
* object_type = (string) 'song'|'podcast'
* destination = (string) full file path

### download

download(object_id, object_type, destination, transcode='raw')

download a song or podcast episode

* object_id   = (string) $song_id / $podcast_episode_id
* object_type = (string) 'song'|'podcast'
* destination = (string) full file path
* transcode   = (string) 'mp3', 'ogg', etc. ('raw' / original by default) //optional

### get_art

get_art(object_id, object_type, destination)

get the binary art for an item

* object_id   = (string) $song_id / $podcast_episode_id
* object_type = (string) 'song', 'artist', 'album', 'playlist', 'search', 'podcast'
* destination = (string) output file path

### user_create

user_create(username: str, password: str, email: str, fullname: str = False, disable=False)

Create a new user. (Requires the username, password and email.) @param array $input

* username    = (string) $username
* password    = (string) hash('sha256', $password))
* email       = (string) 'user@gmail.com'
* fullname    = (string) //optional
* disable     = (boolean|integer) (True,False | 0|1) //optional

### user_edit

user_edit(username, password=False, fullname=False, email=False, website=False, state=False, city=False, disable=False, maxbitrate=False)

Update an existing user. @param array $input

(Alias for old function user_update redirects to this method)

* username   = (string) $username
* password   = (string) hash('sha256', $password)) //optional
* fullname   = (string) //optional
* email      = (string) 'user@gmail.com' //optional
* website    = (string) //optional
* state      = (string) //optional
* city       = (string) //optional
* disable    = (boolean|integer) (True,False | 0|1) //optional
* maxbitrate = (string) //optional

### user_delete

user_delete(username)

Delete an existing user. @param array $input

* username = (string) $username

### user_preferences

user_preferences()

Returns user_preferences

INPUTS

### user_preference

user_preference(filter_str)

Returns preference based on the specified filter_str

* filter_str = (string) search the name of a preference //optional

### system_preferences

system_preferences()

Returns system_preferences

INPUTS

### system_preference

system_preference(filter_str)

Returns preference based on the specified filter_str

* filter_str = (string) search the name of a preference //optional

### system_update

system_update()

update ampache

INPUTS

### preference_create

preference_create(filter_str, type_str, default, category, description=False, subcategory=False, level=100)

Returns preference based on the specified filter_str

* filter_str  = (string) search the name of a preference
* type_str    = (string) 'boolean', 'integer', 'string', 'special'
* default     = (string|integer) default value
* category    = (string) 'interface', 'internal', 'options', 'playlist', 'plugins', 'streaming', 'system'
* description = (string) description of preference //optional
* subcategory = (string) $subcategory //optional
* level       = (integer) access level required to change the value (default 100) //optional

### preference_edit

preference_edit(filter_str, value, apply_all=0)

Returns preference based on the specified filter_str

* filter_str = (string) search the name of a preference
* value      = (string|integer) Preference value
* apply_all  = (boolean) apply to all users //optional

### preference_delete

preference_delete(filter_str)

Returns preference based on the specified filter_str

* filter_str = (string) search the name of a preference

### licenses

licenses(filter_str: str = False, exact: int = False, add: int = False, update: int = False, offset=0, limit=0)

Returns licenses based on the specified filter_str

* filter_str = (string) search the name of a license //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* add        = (integer) UNIXTIME() //optional
* update     = (integer) UNIXTIME() //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### license

license(filter_id: int)

returns a single license

* filter_id = (integer) $license_id

### license_songs

license_songs(filter_id: int)

returns a songs for a single license ID

* filter_id = (integer) $license_id

### live_streams

live_streams(filter_str: str = False, exact: int = False, offset=0, limit=0):

Returns live_streams based on the specified filter_str

* filter_str  = (string) search the name of a live_stream //optional
* exact       = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset      = (integer) //optional
* limit       = (integer) //optional

### live_stream

live_stream(filter_id: int)

Returns a single live_stream based on UID

* filter_id   = (integer) $live_stream_id

### live_stream_create

live_stream_create(name: str, stream_url: str, codec: str, catalog_id: int, site_url: str = ''):

Create a live_stream (radio station) object.

* name     = (string) Stream title
* url      = (string) URL of the http/s stream
* codec    = (string) stream codec ('mp3', 'flac', 'ogg', 'vorbis', 'opus', 'aac', 'alac')
* catalog  = (int) Catalog ID to associate with this stream
* site_url = (string) Homepage URL of the stream //optional

### live_stream_edit

live_stream_edit(filter_id, name: str = '', stream_url: str = '', codec: str = '', catalog_id: int = 0, site_url: str = ''):

Edit a live_stream (radio station) object.

* filter   = (string) object_id
* name     = (string) Stream title //optional
* url      = (string) URL of the http/s stream //optional
* codec    = (string) stream codec ('mp3', 'flac', 'ogg', 'vorbis', 'opus', 'aac', 'alac') //optional
* catalog  = (int) Catalog ID to associate with this stream //optional
* site_url = (string) Homepage URL of the stream //optional

### live_stream_delete

live_stream_delete(self, filter_id: int):

Delete an existing live_stream (radio station). (if it exists)

* filter_id = (integer) object_id



### labels

labels(filter_str: str = False, exact: int = False, offset=0, limit=0)

Returns labels based on the specified filter_str

* filter_str = (string) search the name of a label //optional
* exact      = (integer) 0,1, if true filter is exact rather then fuzzy //optional
* offset     = (integer) //optional
* limit      = (integer) //optional

### label

label(filter_id: int)

returns a single label

* filter_id = (integer) $label_id

### label_artists

label_artists(filter_id: int)

returns a artists for a single label ID

* filter_id = (integer) $label_id

### get_bookmark

get_bookmark(filter_id: str, object_type: str, include=False)

Get the bookmark from it's object_id and object_type.

* filter_id   = (integer) object_id
* object_type = (string) object_type ('song', 'video', 'podcast_episode')
* include     = (integer) 0,1, if true include the object in the bookmark //optional
* all         = (integer) 0,1, if true every bookmark related to the object //optional

### bookmarks

bookmarks(client=False, include=False)

Get information about bookmarked media this user is allowed to manage.

* client  = (string) filter by bookmark_id //optional
* include = (integer) 0,1, if true include the object in the bookmark //optional

### bookmark

bookmark(filter_id: str, include=False):

Get information about bookmarked media this user is allowed to manage.

* filter  = (string) bookmark_id
* include = (integer) 0,1, if true include the object in the bookmark //optional

### bookmark_create

bookmark_create(filter_id, object_type, position: int = 0, client: str = 'AmpacheAPI', date=False)

Create a placeholder for the current media that you can return to later.

* filter_id   = (integer) object_id
* object_type = (string) object_type ('song', 'video', 'podcast_episode')
* position    = (integer) current track time in seconds
* client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
* date        = (integer) update time (Default: UNIXTIME()) //optional

### bookmark_edit

bookmark_edit(filter_id, object_type, position: int = 0, client: str = 'AmpacheAPI', date=False)

Edit a placeholder for the current media that you can return to later.

* filter_id   = (integer) object_id
* object_type = (string) object_type ('song', 'video', 'podcast_episode')
* position    = (integer) current track time in seconds
* client      = (string) Agent string. (Default: 'AmpacheAPI') //optional
* date        = (integer) update time (Default: UNIXTIME()) //optional

### bookmark_delete

bookmark_delete(filter_id: int, object_type=False)

Delete an existing bookmark. (if it exists)

* filter_id   = (integer) object_id
* object_type = (string) object_type ('song', 'video', 'podcast_episode')

### deleted_songs

deleted_songs(offset=0, limit=0)

Returns deleted_song

* offset = (integer) //optional
* limit  = (integer) //optional

### deleted_podcast_episodes

deleted_podcast_episodes(offset=0, limit=0)

Returns deleted_podcast_episode

* offset = (integer) //optional
* limit  = (integer) //optional

### deleted_videos

deleted_videos(offset=0, limit=0)

Returns deleted_video

* offset = (integer) //optional
* limit  = (integer) //optional

## BACKWARD COMPATIBLE FUNCTION NAMES

Renamed Ampache 4 functions that are not part of Ampache 5+

* tags        = genres
* tag         = genre
* tag_artists = genre_artists
* tag_albums  = genre_albums
* tag_songs   = genre_songs
* user_update = user_edit

