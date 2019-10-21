# AMPACHE LIBRARY FOR PYTHON3

## INFO

This library is starting to take shape and is apble to connect oto ampache and return the xml data received from the queries.
Further testing is required but it works pretty well so far.

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

## HOMEPAGE

[https://github.com/lachlan-00/python3-ampache]
