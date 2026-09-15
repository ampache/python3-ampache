# Changelog

## python3-ampache 8.1.1

Targets Ampache API8. Branch `api8`, diverged from the `6.9.2` release
(which is API6-based) — this is a parallel major version, not an
incremental `6.x` bump.

### Added

New methods, all requiring API8+ on the server:

- Folders: `folder`, `folders`
- Album disks: `album_disk`, `album_disks`, `album_disk_songs`
- Playlist folders: `playlist_folders`, `playlist_folder`,
  `playlist_folder_items`, `playlist_folder_create`,
  `playlist_folder_edit`, `playlist_folder_delete`,
  `playlist_folder_add`, `playlist_folder_remove`
- Collections: `collections`, `collection`, `collection_items`,
  `collection_create`, `collection_edit`, `collection_delete`,
  `collection_add`, `collection_remove`
- `playlist_remove` — type-aware removal (object id + type, or track
  number), replaces `playlist_remove_song`
- `catalog_create`, `upload`, `random`, `sonic_match`,
  `set_post_secrets`, `post_request`, `debug_response`

### Changed

- **Breaking:** HTTP error responses are no longer swallowed to
  `False`. On `urllib.error.HTTPError` the request layer now returns
  the parsed error response instead of `False`. Code that checked
  `if not result:` to detect a failed call will now get a truthy
  error object instead. Call `set_return_http_errors(False)` to
  restore the old behavior.
- **Breaking:** `users()` parameter order changed from
  `(sort, cond, offset, limit)` to `(offset, limit, sort, cond)`.
  Positional callers must update their call sites.
- **Breaking:** `stream()` signature changed from
  `(object_id, object_type, destination, stats=1)` to
  `(object_id, object_type, destination, bitrate=False,
  transcode=False, offset=0, length=False, stats=1)`.
- **Breaking:** `download()` parameter order changed from
  `(object_id, object_type, destination, transcode='raw',
  bitrate=False, stats=1)` to `(object_id, object_type, destination,
  bitrate=False, transcode='raw', stats=1, zip_container=False)`
  — `bitrate`/`transcode` swapped, plus a new `zip_container` option.
- `get_indexes()` gained a `hide_search` parameter, inserted as the
  3rd positional argument (before `exact`). Positional callers
  passing `exact` as the 3rd argument will now set `hide_search`
  instead.
- `get_config()` now loads each config key (`ampache_url`,
  `ampache_user`, `ampache_apikey`, `ampache_bearer_token`,
  `ampache_session`, `api_format`) independently, so one missing key
  no longer aborts loading the rest.
- `AMPACHE_VERSION` default changed from `'6.9.0'` to `'8.1.1'`.
  Anyone relying on the default (not calling `set_version()`
  explicitly) will now advertise API8 to their server.
- `browse`, `playlist_add`, `catalog_action`, `user_edit` — internal
  behavior updated for API8 (no public signature change for
  `browse`/`catalog_action`).

### Deprecated

- `get_indexes` → use `index`
- `playlist_add_song` → use `playlist_add`
- `playlist_remove_song` → use `playlist_remove` (removed entirely in API9)
- `user_update` → use `user_edit`

### Removed

- No public methods were deleted. Stale example fixtures for
  `get_indexes` and `tag*` under `docs/json-responses` and
  `docs/xml-responses` were pruned; the underlying methods remain.

### Fixed

- `get_config()` no longer fails closed when a single config key is
  missing from the saved config file.

---

## Upgrading if you're staying on an API6 server

You do not need to switch servers to take this library update, but:

1. **Call `set_version()` explicitly**
   e.g. `set_version('6.6.0')` (or whatever your server reports)
   the library's default changed to `'8.1.1'`.
2. **Check positional-argument call sites**
   for `users()`, `stream()`, `download()`, and `get_indexes()`
   the parameter order changed (see Changed above).
   Keyword-argument callers are unaffected by the reordering.
3. **Review any code that treats a failed request as falsy**
   HTTP error responses are now returned as the parsed error object rather than `False`.
   Call `set_return_http_errors(False)` to restore the old `False`-on-error behavior
   without touching your call sites.
4. All newly added methods (folders, album disks, playlist folders, collections, etc.)
   are additive and API8-only they won't work against an API6 server.
5. No dependency or Python version floor changed
   (`requests>=2.28.1` unchanged).
