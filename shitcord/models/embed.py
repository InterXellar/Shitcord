# -*- coding: utf-8 -*-

import datetime

from .colour import Colour
from .errors import TooLarge
from ..utils import time

__all__ = ['EmbedThumbnail', 'EmbedVideo', 'EmbedImage', 'EmbedProvider',
           'EmbedAuthor', 'EmbedFooter', 'EmbedField', 'Embed']


class _EmbedEmpty:
    def __bool__(self):
        return False

    def __repr__(self):
        return 'shitcord.Embed.Empty'

    def __str__(self):
        return None


EmbedEmpty = _EmbedEmpty()


class EmbedThumbnail:
    """Represents an EmbedThumbnail model from the Discord API.

    This wraps around a thumbnail in an embed for the case it is included.

    Attributes
    ----------
    url : str, optional
        The source url of the thumbnail image.
    proxy_url : str, optional
        A proxied url of the thumbnail image.
    height : int, optional
        The height of the thumbnail image. Set by Discord.
    width : int, optional
        The width of the thumbnail image. Set by Discord.
    """

    __slots__ = ('url', 'proxy_url', 'height', 'width')

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', EmbedEmpty)
        self.proxy_url = kwargs.get('proxy_url', EmbedEmpty)
        self.height = kwargs.get('height', EmbedEmpty)
        self.width = kwargs.get('width', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedThumbnail url={}>'.format(self.url)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width,
        }


class EmbedVideo:
    """Represents an EmbedVideo model from the Discord API.

    This wraps around an embedded video, if given.

    .. warning:: Embedding videos is restricted to Discord only.

    Attributes
    ----------
    url : str, optional
        The source url of the video.
    height : int, optional
        The height of the video. Set by Discord.
    width : int, optional
        The width of the video. Set by Discord.
    """

    __slots__ = ('url', 'height', 'width')

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', EmbedEmpty)
        self.height = kwargs.get('height', EmbedEmpty)
        self.width = kwargs.get('width', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedVideo url={}>'.format(self.url)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'url': self.url,
            'height': self.height,
            'width': self.width,
        }


class EmbedImage:
    """Represents an EmbedImage model from the Discord API.

    This wraps around an embedded image if given.

    Attributes
    ----------
    url : str, optional
        The source url of the image.
    proxy_url : str, optional
        A proxied url of the image.
    height : int, optional
        The height of the image. Set by Discord.
    width : int, optional
        The width of the image. Set by Discord.
    """

    __slots__ = ('url', 'proxy_url', 'height', 'width')

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', EmbedEmpty)
        self.proxy_url = kwargs.get('proxy_url', EmbedEmpty)
        self.height = kwargs.get('height', EmbedEmpty)
        self.width = kwargs.get('width', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedImage url={}>'.format(self.url)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width,
        }


class EmbedProvider:
    """Represents an EmbedProvider model from the Discord API.

    .. warning:: Setting a provider in an embed is restricted to Discord only.

    Attributes
    ----------
    name : str. optional
        The name of the provider.
    url : str, optional
        The url of the provider.
    """

    __slots__ = ('name', 'url')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', EmbedEmpty)
        self.url = kwargs.get('url', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedProvider name={0.name} url={0.url}>'.format(self)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'name': self.name,
            'url': self.url,
        }


class EmbedAuthor:
    """Represents an EmbedAuthor model from the Discord API.

    Attributes
    ----------
    name : str, optional
        The name of the author.
    url : str, optional
        The url of the author.
    icon_url : str, optional
        The source url of the author's icon.
    proxy_icon_url : str, optional
        A proxied url of the author's icon.
    """

    __slots__ = ('name', 'url', 'icon_url', 'proxy_icon_url')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', EmbedEmpty)
        if len(self.name) > 256:
            raise TooLarge('The author\'s name mustn\'t be longer than 256 characters.')

        self.url = kwargs.get('url', EmbedEmpty)
        self.icon_url = kwargs.get('icon_url', EmbedEmpty)
        self.proxy_icon_url = kwargs.get('proxy_icon_url', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedAuthor name={}>'.format(self.name)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'name': self.name,
            'url': self.url,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.proxy_icon_url,
        }


class EmbedFooter:
    """Represents an EmbedFooter model from the Discord API.

    Attributes
    ----------
    text : str
        The text of the footer.
    icon_url : str, optional
        The source url of the footer icon.
    proxy_icon_url : str, optional
        A proxied url of the footer icon.
    """

    __slots__ = ('text', 'icon_url', 'proxy_icon_url')

    def __init__(self, **kwargs):
        self.text = kwargs['text']
        if len(self.text) > 2048:
            raise TooLarge('The text of a footer mustn\'t have more than 2048 characters.')

        self.icon_url = kwargs.get('icon_url', EmbedEmpty)
        self.proxy_icon_url = kwargs.get('proxy_icon_url', EmbedEmpty)

    def __repr__(self):
        return '<shitcord.EmbedFooter text={}>'.format(self.text)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'text': self.text,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.icon_url,
        }


class EmbedField:
    """Represents an EmbedField model from the Discord API.

    Attributes
    ----------
    name : str
        The name of the field.
    value : str
        The value of the field.
    inline : bool
        Whether or not this field should display inline.
    """

    __slots__ = ('name', 'value', 'inline')

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        if len(self.name) > 256:
            raise TooLarge('A field name isn\'t supposed to have more than 256 characters.')

        self.value = kwargs['value']
        if len(self.value) > 1024:
            raise TooLarge('A field value isn\'t supposed to have more than 1024 characters.')

        self.inline = kwargs['inline']

    def __repr__(self):
        return '<shitcord.EmbedField name={0.name} value={0.value}>'.format(self)

    def to_json(self):
        """Returns the JSON representation of this object."""

        return {
            'name': self.name,
            'value': self.value,
            'inline': self.inline,
        }


def _colour_field(colour):
    if isinstance(colour, (_EmbedEmpty, Colour)):
        return colour
    elif isinstance(colour, int):
        return Colour(colour)
    else:
        raise TypeError('Expected _EmbedEmpty, Colour or int. Got {} instead.'.format(type(colour)))


class Embed:
    """Represents an Embed model from the Discord API.

    Embeds can be attached to messages. They allow for extended markdown
    usage, e.g. ``[Vale's GitHub](https://github.com/itsVale)``, can contain
    way larger amounts of text and can embed various things like images or videos.

    There are however limitations how much characters can be sent in an embed.

    +-------------------+-------+
    | Field Type        | Limit |
    +-------------------+-------+
    | Embed.title       | 256   |
    +-------------------+-------+
    | Embed.description | 2048  |
    +-------------------+-------+
    | Embed.fields      | 25    |
    +-------------------+-------+
    | EmbedField.name   | 256   |
    +-------------------+-------+
    | EmbedField.value  | 2048  |
    +-------------------+-------+
    | EmbedAuthor.name  | 256   |
    +-------------------+-------+

    In our documentation, optional attributes usually mean that they may be ``None``.
    Not in this case. Optional attributes for embed may have `Embed.Empty` as their value.

    Attributes
    ----------
    Empty
        A special sentinel value used to denote that the attribute's value is empty.
    title : str, optional
        The title of the embed.
    type : str, optional
        The type of the embed. Usually ``rich``.
    description : str, optional
        The description of the embed.
    url : str, optional
        The url of the embed.
    timestamp: :class:`datetime.datetime`, optional
        The timestamp of the embed. Either an offset or an aware datetime.
    colour : :class:`Colour`, int, optional
        The colour code of the embed. There's an alias for this under ``color``.
    """

    __slots__ = ('title', 'type', 'description', 'url', 'timestamp', 'colour', 'footer',
                 'image', 'thumbnail', 'video', 'provider', 'author', 'fields')

    Empty = EmbedEmpty

    def __init__(self, **kwargs):
        # Swap the colour/color fields
        try:
            colour = kwargs['colour']
        except KeyError:
            colour = kwargs.get('color', EmbedEmpty)

        self.title = kwargs.get('title', EmbedEmpty)
        if isinstance(self.title, str) and len(self.title) > 256:
            raise TooLarge('title mustn\'t be longer than 256 characters.')

        self.type = kwargs.get('type', 'rich')
        self.description = kwargs.get('description', EmbedEmpty)
        if isinstance(self.description, str) and len(self.description) > 2048:
            raise TooLarge('description mustn\'t be longer than 2048 characters.')

        self.url = kwargs.get('url', EmbedEmpty)

        if 'timestamp' in kwargs and isinstance(kwargs['timestamp'], (datetime.datetime, _EmbedEmpty)):
            self.timestamp = kwargs['timestamp']

        self.colour = _colour_field(colour)

    @classmethod
    def from_json(cls, data):
        """Constructs an embed given its JSON representation."""

        # __init__ doesn't apply here so we bypass it
        self = cls.__new__(cls)

        self.title = data.get('title', EmbedEmpty)
        self.type = data.get('type', EmbedEmpty)
        self.description = data.get('description', EmbedEmpty)
        self.url = data.get('url', EmbedEmpty)

        if 'timestamp' in data:
            self.timestamp = time.parse_time(data['timestamp'])

        if 'colour' in data:
            self.colour = Colour(data['colour'])

        if 'footer' in data:
            self.footer = EmbedFooter(**data['footer'])

        if 'image' in data:
            self.image = EmbedImage(**data['image'])

        if 'thumbnail' in data:
            self.thumbnail = EmbedThumbnail(**data['thumbnail'])

        if 'video' in data:
            self.video = EmbedVideo(**data['video'])

        if 'provider' in data:
            self.provider = EmbedProvider(**data['provider'])

        if 'author' in data:
            self.author = EmbedAuthor(**data['author'])

        if 'fields' in data:
            self.fields = [EmbedField(**field) for field in data['fields']]

    def set_footer(self, text, *, icon_url=EmbedEmpty):
        """Sets a footer at this embed object.

        Parameters
        ----------
        text : str
            The text of the footer.
        icon_url : str, optional
            The source url for the footer icon.

        Returns
        -------
        The current embed object.
        """

        self.footer = EmbedFooter(text=text, icon_url=icon_url)
        return self

    def set_image(self, url):
        """Adds an image to this embed object.

        Parameters
        ----------
        url : str
            The source url of the image.

        Returns
        -------
        The current embed object.
        """

        self.image = EmbedImage(url=url)
        return self

    def set_thumbnail(self, url):
        """Sets a thumbnail for this embed object.

        Parameters
        ----------
        url : str
            The source url of the thumbnail image.

        Returns
        -------
        The current embed object.
        """

        self.thumbnail = EmbedThumbnail(url=url)
        return self

    def set_author(self, *, name, url=EmbedEmpty, icon_url=EmbedEmpty):
        """Sets the author of the current embed object.

        Parameters
        ----------
        name : str
            The author's name.
        url : str, optional
            The author's url.
        icon_url : str, optional
            The source url of the author's icon.

        Returns
        -------
        The current embed object.
        """

        self.author = EmbedAuthor(name=name, url=url, icon_url=icon_url)
        return self

    def add_field(self, name, value, *, inline=True):
        """Adds a field to the embed object.

        Fields are used to extend the embed's content.

        .. warning:: Having more than 25 fields per embed isn't allowed!

        Parameters
        ----------
        name : str
            The name of the field.
        value : str
            The value of the field.
        inline : bool, optional
            Whether or not the field should display inline. Defaults to `True`.

        Returns
        -------
        The current embed object.

        Raises
        ------
        TooLarge
            Will be raised when the amount of fields already is 25.
        """

        if hasattr(self, 'fields') and len(self.fields) > 25:
            raise TooLarge('An embed isn\'t supposed to have more than 25 fields.')

        field = EmbedField(name=name, value=value, inline=inline)

        try:
            self.fields.append(field)
        except AttributeError:
            self.fields = [field]

        return self

    def clear_fields(self):
        """Clears all fields of this embed object.

        Returns
        -------
        The current embed object.
        """

        try:
            self.fields.clear()
        except AttributeError:
            self.fields = []

        return self

    def remove_field(self, index):
        """Removes a field of this embed object given its index.

        .. note:

            The embed fields are stored inside a list.
            This means that the indexes of the other fields shift to fill the gap.

        Parameters
        ----------
        index : int
            The index to remove the field at.

        Raises
        ------
        IndexError
            Will be raised when an invalid field was specified.
        """

        try:
            del self.fields[index]
        except AttributeError:  # Don't catch IndexErrors. We want to let people know when they fucked up.
            self.fields = []

        return self

    def set_field_at(self, index, name, value, *, inline=True):
        """Sets a field at a given index.

        The documentation for this method is the same as for :meth:`add_field`
        except that the first parameter is the index where the field should be set.
        """

        try:
            field = self.fields[index]
        except (AttributeError, IndexError):
            raise AttributeError('Couldn\'t find a field to replace.')
        except TypeError:
            raise IndexError('Provide an index and nothing else, you faggot.')

        self.fields[field] = EmbedField(name=name, value=value, inline=inline)
        return self

    def to_json(self):
        """Converts the embed object into a dictionary."""

        embed = {}
        for item in self.__slots__:
            # From this point, we want to fill the dict. There are several things to pay attention to.
            # First of all, instances of _EmbedEmpty shouldn't be added to the embed dict.
            # The colour and the timestamp attribute require extra wrappers.
            # We don't need to add empty values that aren't _EmbedEmpty objects.
            attr = getattr(self, item)

            # First of all, get rid of the _EmbedEmpty objects
            if isinstance(attr, _EmbedEmpty):
                continue

            if item == 'colour':
                # Though our attribute is called colour, the Discord API wants a color key.
                embed['color'] = attr.value
            elif item == 'timestamp':
                embed['timestamp'] = attr.isoformat()
            else:
                if attr:
                    # This way, we won't have problems with empty strings and stuff like that.
                    try:
                        field = attr.to_json()
                        # There are still cases where our wrappers for special embed fields
                        # contain _EmbedEmpty objects as values. Let's filter that crap out.
                        embed[item] = {key: value for key, value in field if not isinstance(value, _EmbedEmpty)}
                    except AttributeError:  # The attribute was a str or such crap.
                        embed[item] = attr

        return embed
