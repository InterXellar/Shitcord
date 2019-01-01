from .base import Model
from .channel import PartialChannel


class Invite(Model):

    def __init__(self, data, http):
        super().__init__(0, http=http)

        self.code = data['code']
        self.guild = data.get('guild')
        self.channel = PartialChannel(data['channel'], http=http)
        self.online_members = data.get('approximate_presence_count')
        self.total_members = data.get('approximate_member_count')
