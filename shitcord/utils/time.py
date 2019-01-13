import datetime
import re


def parse_time(time):
    if time:
        return datetime.datetime(*map(int, re.split(r'[^\d]', time.replace('+00:00', ''))))
    return None
