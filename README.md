<div align="center">
    <img src="https://user-images.githubusercontent.com/38182450/46910084-abad8d80-cf3e-11e8-9be3-09c9078b2c3a.png" width="400px" />
    <h1>~~ Shitcord ~~</h1>
    <strong>A shitty, probably not even that shitty Discord API wrapper.</strong>
    <br><br>
    <a class="badge-align" href="https://www.codacy.com/app/itsVale/Shitcord?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=itsVale/Shitcord&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/b3ed9f02a50142bf9fd337978be88b24"/></a>
    &nbsp;
    <a href="https://travis-ci.com/itsVale/Shitcord"><img src="https://travis-ci.com/itsVale/Shitcord.svg?branch=async" /></a>
    &nbsp;
    <a href="https://GitHub.com/itsVale/Shitcord/issues/"><img src="https://img.shields.io/github/issues/itsVale/Shitcord.svg" /></a>
    &nbsp;
    <a href="https://GitHub.com/itsVale/Shitcord/pulls/"><img src="https://img.shields.io/github/issues-pr/itsVale/Shitcord.svg" /></a>
    &nbsp;
    <a href="http://perso.crans.org/besson/LICENSE.html"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" /></a>
    <hr>
</div>

_Though this library is incomplete yet, contributions are very appreciated!_

## Installation
For now, you can only install the dev branch which is constantly updated.
```
pip install -U https://github.com/itsVale/Shitcord/archive/async.zip
```

Shitcord already features the REST API and also the Discord Gateway. Though the lib is very
incomplete at this moment what you can see from the code below.  
  
__Note that this branch features an asynchronous version of Shitcord that hasn't got a Gateway implementation yet.__

## Usage
```python
import logging

import trio
from shitcord.http import Endpoints, HTTP

# Set up logging for receiving Shitcord's debug logs.
logger = logging.getLogger('shitcord')
logger.level = logging.DEBUG

# Create an instance of the HTTP class that interfaces with the REST API.
http = HTTP('Bot token goes here.')
# Define the channel ID where the messages should be sent.
channel_id = 12345
# Define the payload that should be sent. For sending messages, we only need a content key.
json = {'content': 'Hello, I\'m using Shitcord and I\'m cool.'}


# Please don't do this lol. Insider from the Shitcord Discord server.
async def spam_the_api(channel_id: int):
    while True:
        await http.make_request(Endpoints.CREATE_MESSAGE, dict(channel=channel_id), json=json)


# And finally launch your program.
trio.run(spam_the_api, channel_id)
```

## Support
Need help with something or just want to hang out with more or less cool guys? [Join our cool Discord server!](https://discord.gg/HbKGrVT)
