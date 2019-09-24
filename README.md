# AMPACHE LIBRARIES FOR PYTHON3

## INFO

Right now this is just a library for scrobbling to an ampache server but this would be easy to expand.

## EXAMPLES

```python3
    import hashlib
    import time
    import threading

    import Scrobble

    def encrypt_string(hash_string, user):
        key = hashlib.sha256(hash_string.encode()).hexdigest()
        # don't encrypt strings in the old way
        if not user:
            return hash_string
        passphrase = user + key
        sha_signature = hashlib.sha256(passphrase.encode()).hexdigest()
        return sha_signature

    def ampache_auth(ampache_url, key):
        """ ping ampache for auth key """
        if ampache_url[:8] == 'https://' or ampache_url[:7] == 'http://':
                ping = Scrobble.ping(ampache_url, key)
                if not ping == False:
                    return ping
                auth = Scrobble.auth(self.ampache_url, self.encrypt_string(self.conf.get(C, 'ampache_api')))
                if not auth == False:
                    return auth
        return False

hash_string = encrypt_string('123749hfd208u' 'user')
auth = ampache_auth('https://ampache/server', hash_string)
if auth:
    Process(target=Scrobble.run,
            args=(int(time.time()), 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
            '', '', '', 'https://ampache/server', hash_string)).start()
```

## HOMEPAGE

[https://github.com/lachlan-00/python3-ampache]
