AMPACHE LIBRARY FOR PYTHON3
===========================

Upload to PyPI
    .. image:: https://github.com/ampache/python3-ampache/workflows/Upload%20Python%20Package/badge.svg
       :target: https://pypi.org/project/ampache/

INFO
====

A python3 library for interaction with your Ampache server using the XML & JSON API

`<https://ampache.org/API/>`_

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
    ampacheConnection = ampache.API()

    # if using password auth use encrypt_password
    mytime = int(time.time())
    passphrase = ampacheConnection.encrypt_password('mypassword', mytime)
    auth = ampacheConnection.handshake('https://music.com.au', passphrase, 'my username', mytime)

    # if using an API key auth keep using encrypt_string
    passphrase = ampacheConnection.encrypt_string('my apikey', 'my username')
    auth = ampacheConnection.handshake('https://music.com.au', passphrase)

    # now you can call methods without having to keep putting in the url and userkey
    ampacheConnection.label(1677)
    
    # ping has always allowed empty calls so you have to ping with a url and session still
    ampacheConnection.ping('https://music.com.au', auth)

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

    import time
    import ampache

    # user variables
    ampache_url = 'https://music.server'
    my_api_key = 'mysuperapikey'
    user = 'myusername'

    # processed details
    ampacheConnection = ampache.API()
    encrypted_key = ampacheConnection.encrypt_string(my_api_key, user)
    ampache_session = ampacheConnection.handshake(ampache_url, encrypted_key)

    if ampache_session:
        # Scrobble a music track to your ampache server
        Process(target=ampacheConnection.scrobble,
                args=('Beneath The Cold Clay', 'Crust', '...and a Dirge Becomes an Anthem',
                      '', '', '', int(time.time()))).start()

LINKS
=====

`<https://github.com/ampache/python3-ampache/>`_

`<https://pypi.org/project/ampache/>`_

