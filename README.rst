AMPACHE LIBRARY FOR PYTHON3
===========================

Upload to PyPI
    .. image:: https://github.com/ampache/python3-ampache/workflows/Upload%20Python%20Package/badge.svg
       :target: https://pypi.org/project/ampache/

INFO
====

A python3 library for interaction with your Ampache server using the XML & JSON API

`<http://ampache.org/API/>`_

Code examples and scripts are available from github

INSTALL
=======

You can now install from pip directly::

    pip3 install -U ampache

EXAMPLES
========

There is a fairly simple cli example for windows/linux to perform a few functions.
It's a good example for testing and might make things a bit easier to follow.

`<https://raw.githubusercontent.com/ampache/python3-ampache/master/docs/examples/ampyche.py>`_

ampyche example help:
.. example-code::

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

    .. code-block:: python3
        import time
        import ampache

        # user variables
        ampache_url = 'https://music.server'
        my_api_key = 'mysuperapikey'
        user = 'myusername'

        # processed details
        encrypted_key = ampache.encrypt_string(my_api_key, user)
        ampache_session = ampache.handshake(ampache_url, encrypted_key)

        if ampache_session:
            # Scrobble a music track to your ampache server
            Process(target=ampache.scrobble,
                    args=(ampache_url, ampache_session, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
                    '', '', int(time.time()))).start()

LINKS
=====

`<https://github.com/ampache/python3-ampache/>`_

`<https://pypi.org/project/ampache/>`_
