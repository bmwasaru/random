from datetime import datetime

from pytz import timezone


def timesince(when):
    """Returns string representing "time since" or "time until".

        Examples:
            5 days ago, 3 hours ago, 1 minutes from now, 8 hours from now, now.
        """

    if not when:
        return ''

    now = datetime.now(tz=timezone('Africa/Nairobi'))

    if now > when:
        diff = now - when
        suffix = "ago"
    else:
        diff = when - now
        suffix = "from now"

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:
        if period:
            return '%d %s %s' % (
                period,
                singular if period == 1 else plural,
                suffix
            )

    return "now"


timesince("2020, 6, 22, 11, 54, 11, 363590")

