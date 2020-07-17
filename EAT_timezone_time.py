from datetime import datetime

from pytz import timezone


def current_datetime():
    """
    Get the current datetime in EAT timezone
    :return: datetime
    """
    eat_zone = timezone("Africa/Nairobi")
    return datetime.now().replace(tzinfo=eat_zone)
