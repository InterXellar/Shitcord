# -*- coding: utf-8 -*-

from enum import IntEnum
import os.path
from typing import BinaryIO, Optional, Union

from .base import Model
from .embed import Embed
from .emoji import PartialEmoji
from .member import Member
from .user import User
from ..http import rest_shit
from ..utils.time import parse_time

__all__ = ['Attachment', 'File', 'Message', 'MessageType']


class MessageType(IntEnum):
    DEFAULT                = 0  # noqa
    RECIPIENT_ADD          = 1  # noqa
    RECIPIENT_REMOVE       = 2  # noqa
    CALL                   = 3  # noqa
    CHANNEL_NAME_CHANGE    = 4  # noqa
    CHANNEL_ICON_CHANGE    = 5  # noqa
    CHANNEL_PINNED_MESSAGE = 6  # noqa
    GUILD_MEMBER_JOIN      = 7  # noqa


def _user_to_member(user: dict, member: dict, http):
    if 'member' in user:
        user.pop('member')

    member.pop('user', None)
    member['user'] = user
    return Member(member, http)


class File:
    """A wrapper for file objects that can be used for sending files to Discord.

    .. note::
        If you want to pass a file opened via ``open`` it is necessary to use ``rb`` mode.
        To pass any binary data, usage of ``io.BytesIO`` is recommended.

    Attributes
    ----------
    fp : str, BinaryIO
        Either a filename to open a file in the hard drive or a file's binary representation.
    filename : str, optional
        The filename to use when uploading to Discord. If not given, the default filename
        or the provided string for ``fp`` will be used.
    spoiler : bool, optional
        Whether this file should be marked as a spoiler or not. Defaults to ``False``.
    """

    __slots__ = ('fp', 'filename', '_real_fp')

    def __init__(self, fp: Union[str, BinaryIO], filename: Optional[str] = None, *, spoiler=False):
        self.fp = fp
        self._real_fp = None

        if filename is None:
            if isinstance(self.fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, 'name', None)
        else:
            self.filename = filename

        if spoiler and not self.filename.startswith('SPOILER_'):
            self.filename = 'SPOILER_{}'.format(self.filename)

    def open_file(self):
        fp = self.fp
        if isinstance(fp, str):
            self._real_fp = fp = open(fp, 'rb')
        return fp

    def close(self):
        if self._real_fp:
            self._real_fp.close()


class Attachment(Model):
    """Represents an Attachment model from the Discord API.

    .. warning:: You can retrieve this model from a Message object. However, for sending files, use :class:`File`.

    Attributes
    ----------
    snowflake : :class:`Snowflake`
        A :class:`Snowflake` object that represents the attachment's ID.
    id : int
        The attachment's ID.
    filename : str
        The name of the attached file.
    size : int
        The size of the file in bytes.
    url : str
        The source url of the file.
    proxy_url : str
        A proxied url of the file.
    height : int, optional
        The height of the file, assuming the file is an image.
    width : int, optional
        The width of the file, assuming the file is an image.
    """

    __slots__ = ('filename', 'size', 'url', 'proxy_url', 'height', 'width')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.filename = data['filename']
        self.size = data['size']
        self.url = data['url']
        self.proxy_url = data['proxy_url']
        self.height = data.get('height')
        self.width = data.get('width')

    def __repr__(self):
        return '<shitcord.Attachment filename={0.filename} size={0.size}>'.format(self)

    @property
    def is_spoiler(self):
        return self.filename.startswith('SPOILER_')


class Reaction:
    """Represents a Reaction model from the Discord API.

    Attributes
    ----------
    count : int
        The times this emoji has been used to react.
    me : bool
        Whether the current user reacted using this emoji.
    emoji : :class:`PartialEmoji`
        The emoji that was used to react with.
    """

    __slots__ = ('count', 'me', 'emoji')

    def __init__(self, data, http):
        self.count = data['count']
        self.me = data['me']
        self.emoji = PartialEmoji(data['emoji'], http)

    def __repr__(self):
        return '<shitcord.Reaction emoji={0.emoji!s}>'.format(self)


class Message(Model):
    """Represents a Message model from Discord API.

    Attributes
    ----------
    snowflake : :class:`Snowflake`
        A :class:`Snowflake` object that represents the message's ID.
    id : int
        The message ID.
    channel_id : int
        The ID of the channel the message was sent to.
    guild_id : int, optional
        The ID of the guild this message belongs to. None when the message was sent to a DM channel.
    author : :class:`User`, :class:`Member`, dict optional
        The author of the message. If the message was sent by a Webhook, the author is None.
    content : str
        The content of the message.
    timestamp : :class:`datetime.datetime`
        The timestamp when this message was sent.
    edited_timestamp : :class:`datetime.datetime`, optional
        The timestamp when this message was edited.
    tts : bool
        Whether this message was sent using tts or not.
    mention_everyone : bool
        Whether this message mentioned everyone or not.
    mentions : List[:class:`User`, :class:`Member`], optional
        The users that were mentioned by this message.
    mention_roles : List[int]
        The IDs of the roles that were mentioned by this message.
    attachments : List[:class:`Attachment`]
        A list of attachment objects that were sent with this message.
    embeds : List[:class:`Embed`]
        A list of embed objects that were sent with this message.
    reactions : List[:class:`Reaction`], optional
        A list of reaction objects to the message.
    nonce : int, optional
        Used for validating a message was sent.
    pinned : bool
        Whether the message is pinned or not.
    webhook_id : int, optional
        When this message was generated by a webhook, this is its ID.
    type : :class:`MessageType`
        The type of the message.
    activity : dict, optional
        A dictionary containing information about the activity from Rich Presence related chat embeds.
    application : dict, optional
        A dictionary containing information about the application from Rich Presence related chat embeds.
    """

    __slots__ = ('channel_id', 'guild_id', 'author', 'content', 'content', 'timestamp', 'edited_timestamp', 'tts',
                 'mention_everyone', 'mentions', 'mention_roles', 'attachments', 'embeds', 'reactions', 'nonce',
                 'pinned', 'webhook_id', 'type', 'activity', 'application')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.channel_id = int(data['channel_id'])
        self.guild_id = data.get('guild_id')

        if self.guild_id is not None:
            self.guild_id = int(self.guild_id)

        author = data.get('author')
        if data.get('member') is not None:
            member = data['member']
            member.pop('user', None)  # for convenience
            self.author = _user_to_member(author, member, http)
        else:
            self.author = User(author, http)

        self.content = data['content']
        self.timestamp = parse_time(data['timestamp'])
        self.edited_timestamp = parse_time(data.get('edited_timestamp'))
        self.tts = data['tts']
        self.mention_everyone = data['mention_everyone']
        self.mentions = [
            User(user, http) if user.get('member') is None
            else _user_to_member(user, user.pop('member'), http)
            for user in data['mentions']
        ]
        self.mention_roles = [int(role_id) for role_id in data['mention_roles']]
        self.attachments = [Attachment(attachment, http) for attachment in data['attachments']]
        self.embeds = [Embed.from_json(embed) for embed in data['embeds']]
        self.reactions = [Reaction(reaction, http) for reaction in data.get('reactions', [])]
        self.nonce = int(data['nonce']) if data.get('nonce') else None
        self.pinned = data['pinned']
        self.webhook_id = int(data['webhook_id']) if data.get('webhook_id') else None
        self.type = MessageType(data['type'])
        self.activity = data.get('activity')
        self.application = data.get('application')

    def __repr__(self):
        return '<shitcord.Message id={0.id} author={0.author!s} nonce={0.nonce}>'.format(self)

    def __str__(self):
        return self.content

    @rest_shit()
    async def respond(self, content: str):
        """|coro|
        |rs|

        Responds to a message.

        This sends a message to the same channel this
        message object was created in.

        Parameters
        ----------
        content : str
            The content of the "response".

        Returns
        -------
        :class:`Message`
            The newly created message.
        """

        return await self._http.create_message(self.channel_id, content)
