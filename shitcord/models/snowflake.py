# -*- coding: utf-8 -*-

from datetime import datetime

DISCORD_EPOCH = 1420070400000


class Snowflake:
    """Represents a generic Snowflake class.

    As of the Discord API using Twitter's Snowflakes, there are many
    data stored inside them. This class represents an interface that lets
    you access and modify these Snowflake data.

    Parameters
    ----------
    snowflake : int
        The Snowflake ID to initialize this class with.

    Attributes
    ----------
    binary : str
        A string representing the Snowflake's binary representation.
    timestamp : datetime
        An offset-naive datetime object representing the Snowflake's creation time.
    worker_id : int
        The Worker ID that belongs to the Snowflake.
    process_id : int
        The Process ID that belongs to the Snowflake.
    increment : int
        The increment that belongs to the Snowflake.
    """

    __slots__ = ('snowflake', 'binary', 'timestamp', 'worker_id', 'process_id', 'increment')

    def __init__(self, snowflake: int):
        self.snowflake = snowflake

        self.binary = bin(self.snowflake)[2:].zfill(8)
        self.timestamp = datetime.utcfromtimestamp(((self.snowflake >> 22) + DISCORD_EPOCH) / 1000)
        self.worker_id = (self.snowflake & 0x3E0000) >> 17
        self.process_id = (self.snowflake & 0x1F000) >> 12
        self.increment = self.snowflake & 0xFFF

    @classmethod
    def create_snowflake(cls, date, high=False):
        """Creates a Snowflake ID pretending to be created at the given time.

        Parameters
        ----------
        date : datetime
            The datetime to create the snowflake with.
        high : bool
            Whether or not set the lower 22 bit to high.
        """

        unix_seconds = cls._to_unix_seconds(date)
        milliseconds = int(unix_seconds) * 1000 - DISCORD_EPOCH

        return (milliseconds << 22) + (2 ** 22 - 1 if high else 0)

    @staticmethod
    def _to_unix_seconds(date):
        return (date - datetime(1970, 1, 1)).total_seconds()

    def get_shard_id(self, shard_count):
        """Computes the shard ID from a given shard count.

        This only works if this class was initialized with a valid Guild ID!
        Useful for determining what events will be sent to which shard.

        Parameters
        ----------
        shard_count : int
            The total amount of shards.
        """

        return (self.snowflake >> 22) % shard_count
