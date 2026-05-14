# MIT License
#
# Copyright (C) 2019 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from datetime import timedelta


def format_duration(delay: timedelta) -> str:
    """
    Format a duration using a human-readable approximate time unit.

    The selected unit depends on the total duration:

    - less than 1 minute  -> seconds
    - less than 1 hour    -> minutes
    - less than 1 day     -> hours
    - 1 day or more       -> days

    Examples:
        >>> format_duration(timedelta(seconds=42))
        'about 42 seconds'

        >>> format_duration(timedelta(minutes=12))
        'about 12 minutes'

        >>> format_duration(timedelta(hours=3, minutes=15))
        'about 3 hours'

        >>> format_duration(timedelta(days=2, hours=5))
        'about 2 days'


    :param delay: The duration to format.


    :return: A human-readable string representing the approximate
        duration.
    """
    total_seconds = abs(delay.total_seconds())

    if total_seconds < 60:
        value = round(total_seconds)
        unit = "second"

    elif total_seconds < 3600:
        value = round(total_seconds / 60)
        unit = "minute"

    elif total_seconds < 86400:
        value = round(total_seconds / 3600)
        unit = "hour"

    else:
        value = round(total_seconds / 86400)
        unit = "day"

    if value != 1:
        unit += "s"

    return f"about {value} {unit}"
