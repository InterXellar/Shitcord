from .channel import PartialChannel


class Invite:
    """Represents a Guild Invite model from the Discord API.

    Invites are always created by guild members to invite other users to the guild.

    Attributes
    ----------
    code : str
        A unique invite code.
    guild : :class:`Guild`, optional
        The guild that corresponds to the invite code.
    channel : :class:`PartialChannel`
        The channel this invite is for.
    online_members : int, optional
        Approximate count of online members.
    total_members : int, optional
        Approximate count of total members.
    """

    __slots__ = ('code', 'guild', 'channel', 'online_members', 'total_members')

    def __init__(self, data, http):
        self.code = data['code']
        self.guild = data.get('guild')
        self.channel = PartialChannel(data['channel'], http=http)
        self.online_members = data.get('approximate_presence_count')
        self.total_members = data.get('approximate_member_count')
