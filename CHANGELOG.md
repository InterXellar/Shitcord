# Changelog

## 0.0.3b
### Added
  - Even more model implementations.
  - RESTShit as a high-level interface for HTTP requests to the Discord REST API.

### Changed
  - Rate Limit cooldown is now blocking.
  - If you're under Python 3.5.2, Shitcord does no longer raise a RuntimeError when you try to import it. Instead, Shitcord now raises a SystemExit during installation.
  - Many documentation improvements.
  - Made the method `shitcord.gateway.DiscordWebSocketClient.decompress` private.

### Fixed
  - Some documentation mistakes.

## 0.0.2b
### Added
  - The `shitcord.sync` module which allows the execution of all coroutines synchronously.
  - More model implementations.
  - A full implementation of the Discord Gateway.

### Changed
  - Models without an ID do no longer inherit from `shitcord.Model`.
  - pylava will be stricter from now on.

### Removed
  - Anything that has to do with JSON serialization because currently there's no need for it.
  - `shitcord.SessionStartLimit` which represented a wrapper for Session Start Limit objects from the Discord Gateway. This is no longer required and the object will now be parsed manually.

### Fixed
  - Some bug with the `shitcord.EventEmitter` where callbacks were only executed once.

## 0.0.1b
### Added
  -  Useful utility classes and functions.
  -  Some model implementations from the Discord API.
  -  Better documentation straight away from the beginning.
  
### Changed
  -  The library will no be use trio instead of gevent and with that, it requires an async/await syntax.
  -  The structure of how docstrings are written.
  
### Removed
  -  Literally everything from other branches