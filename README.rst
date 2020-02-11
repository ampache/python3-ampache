AMPACHE LIBRARY FOR PYTHON3
===========================

INFO
====

A python3 library for interaction with your Ampache server using the XML API
https://github.com/ampache/ampache/wiki/API

If you run a develop server you now have access to JSON as well!

Code examples and scripts are available from github

INSTALL
=======

You can now install from pip directly::

    pip3 install -U ampache

EXAMPLES
========

Practical example::

    import time
    import ampache

    # user variables
    ampache_url = 'https://music.server'
    my_api_key  = 'mysuperapikey'
    user        = 'myusername'

    # processed details
    encrypted_key = ampache.encrypt_string(my_api_key, user)
    ampache_api   = ampache.handshake(ampache_url, encrypted_key)

    if ampache_api:
        # Scrobble a music track to your ampache server
        Process(target=ampache.scrobble,
                args=(ampache_url, ampache_api, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
                '', '', int(time.time()))).start()

LINKS
=====

`<https://github.com/ampache/python3-ampache/>`_

`<https://pypi.org/project/ampache/>`_
