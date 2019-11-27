# AMPACHE LIBRARY FOR PYTHON3

## INFO

This library is starting to take shape and is able to connect to Ampache and return the
xml or binary data received from the queries.

## INSTALL

You can now install from pip directly!

```python3
    pip3 install -U ampache
```

## EXAMPLES

```python3
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
                args=(int(ampache_url, ampache_api, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
                '', '', ''time.time()))).start()
```

## LINKS

<https://github.com/lachlan-00/python3-ampache>

<https://pypi.org/project/ampache/>
