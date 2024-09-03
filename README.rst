AMPACHE LIBRARY FOR PYTHON3
===========================

Upload to PyPI
    .. image:: https://github.com/ampache/python3-ampache/workflows/Upload%20Python%20Package/badge.svg
       :target: https://pypi.org/project/ampache/

INFO
====

A python3 library for interaction with your Ampache server using the XML & JSON API

`<https://ampache.org/api/>`_

Code examples and scripts are available from github

The class documentation has been extracted out into a markdown file for easier reading.

`<https://raw.githubusercontent.com/ampache/python3-ampache/master/docs/MANUAL.md>`_

There has been a pretty significant change in the library between Ampache 4 and Ampache 5.

For anyone wanting to stay on v4 the branch has been separated from the master branch.

`<https://github.com/ampache/python3-ampache/tree/api4>`_

Once you connect with your passphrase or api key, the url and auth token are stored allowing you to call methods without them.

.. code-block:: python3

    import ampache
    import time

    # connect to the server
    ampache_connection = ampache.API()

    # if using password auth use encrypt_password
    mytime = int(time.time())
    passphrase = ampache_connection.encrypt_password('mypassword', mytime)
    auth = ampache_connection.handshake('https://music.com.au', passphrase, 'my username', mytime)

    # if using an API key auth keep using encrypt_string
    passphrase = ampache_connection.encrypt_string('my apikey', 'my username')
    auth = ampache_connection.handshake('https://music.com.au', passphrase)

    # now you can call methods without having to keep putting in the url and userkey
    ampache_connection.label(1677)
    
    # ping has always allowed empty calls so you have to ping with a url and session still
    ampache_connection.ping('https://music.com.au', auth)

NEWS
====

- Password handshake auth is available now.
- This library now supports every Ampache API release (3, 4, 5 and 6)
- You can save and restore from a json config file using new methods

  - set_config_path: Set a folder to your config path
  - get_config: Load the config and set Ampache globals
  - save_config: Save the config file with the current globals

    - AMPACHE_URL = The URL of your Ampache server
    - AMPACHE_USER = config["ampache_user"]
    - AMPACHE_KEY = Your encrypted apikey OR password if using password auth
    - AMPACHE_SESSION = Current session auth from the handshake. Use to reconnect to an existing session
    - AMPACHE_API = API output format "json" || "xml"

INSTALL
=======

You can now install from pip directly::

    pip3 install -U ampache

EXAMPLES
========

There is a fairly simple cli example for windows/linux to perform a few functions.
It's a good example for testing and might make things a bit easier to follow.

`<https://raw.githubusercontent.com/ampache/python3-ampache/master/docs/examples/ampyche.py>`_

ampyche.py help:

.. code-block:: bash

    Possible Actions:

        /u:%CUSTOM_USER%    (Custom username for the current action)
        /k:%CUSTOM_APIKEY%  (Custom apikey for the current action)
        /a:%ACTION%         (ping, playlists, localplay, download, configure, logout, showconfig)
        /l:%LIMIT%          (integer)
        /o:%OBJECT_ID%      (string)
        /t:%OBJECT_TYPE%    (song, playlist)
        /p:%PATH%           (folder for downloads)
        /f:%FORMAT%         (raw, mp3, ogg, flac)
        /usb                (split files into numeric 0-9 folders for car USBs)
        /c:%COMMAND%        (localplay command)
        (next, prev, stop, play, pause, add, volume_up,
            volume_down, volume_mute, delete_all, skip, status)

Here is a short code sample for python using version 5.x.x+ to scrobble a track to your server

.. code-block:: python3

    import ampache
    import sys
    import time

    # Open Ampache library
    ampache_connection = ampache.API()

    # load up previous config
    if not ampache_connection.get_config():
        # user variables
        api_version = '6.6.1'
        ampache_url = 'https://music.server'
        ampache_api_key = 'mysuperapikey'
        ampache_user = 'myusername'

        # Set your details
        ampache_connection.set_version(api_version)
        ampache_connection.set_url(ampache_url)
        ampache_connection.set_key(ampache_api_key)
        ampache_connection.set_user(ampache_user)

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

    # save your successful connection in your local config
    ampache_connection.save_config()

    # Scrobble a music track to your ampache server
    #
    # * title       = (string) song title
    # * artist_name = (string) artist name
    # * album_name  = (string) album name
    # * mbtitle     = (string) song mbid //optional
    # * mbartist    = (string) artist mbid //optional
    # * mbalbum     = (string) album mbid //optional
    # * stime       = (integer) UNIXTIME() //optional
    # * client      = (string) //optional
    ampache_connection.execute('scrobble', {'title': 'Beneath The Cold Clay', 'artist_name': 'Crust', 'album_name': '...and a Dirge Becomes an Anthem', 'stime': int(time.time())})

LINKS
=====

`<https://github.com/ampache/python3-ampache/>`_

`<https://pypi.org/project/ampache/>`_

