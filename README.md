# AMPACHE LIBRARY FOR PYTHON3

## INFO

Right now this is just a library for scrobbling to an ampache server but this would be easy to expand.

## EXAMPLES

```python3
    import hashlib
    import time
    import threading

    import ampache

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
                ping = ampache.ping(ampache_url, key)
                if not ping == False:
                    return ping
                auth = ampache.handshake(self.ampache_url, self.encrypt_string(self.conf.get(C, 'ampache_api')))
                if not auth == False:
                    return auth
        return False

hash_string = encrypt_string('123749hfd208u' 'user')
auth = ampache_auth('https://ampache/server', hash_string)
if auth:
    Process(target=ampache.scrobble,
            args=(int('https://ampache/server', hash_string, 'Hear.Life.Spoken', 'Sub Atari Knives', 'Unearthed',
            '', '', ''time.time()))).start()
```

## HOMEPAGE

[https://github.com/lachlan-00/python3-ampache]
