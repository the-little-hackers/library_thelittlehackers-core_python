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

from __future__ import annotations

import dateutil.parser
from datetime import date
from datetime import datetime
from uuid import UUID

from thelittlehackers.model.locale import Locale
from thelittlehackers.utils import any_utils
from thelittlehackers.utils.any_utils import is_empty_or_none


def string_to_boolean(
        value: bool | str | None,
        strict: bool = False,
        default_value: bool = False
):
    """
    Convert a string representation of a boolean value to its
    corresponding boolean.

    This function interprets common string representations of boolean
    values (e.g., 'yes', 'true', '1') and returns the corresponding
    boolean.  If the ``strict`` parameter is set to ``True``, the function
    will raise a ``ValueError`` or if the string is not a recognized
    boolean representation.  Otherwise, it will return the ``default_value``
    or ``False`` if no valid representation is found.


    :param value: The input to be converted into a boolean.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        boolean strings.  If ``False``, the function returns ``None`` for
        invalid boolean strings.

    :param default_value: The boolean value to return if ``value`` is ``None``
        or an empty string.  Defaults to ``False``.


    :return: The boolean value corresponding to the string, or
        ``default_value`` if the string is not valid and ``strict`` is
        ``False``.


    :raise ValueError: If ``strict`` is ```True``` and `value` does not
        represent a valid boolean.
    """
    if is_empty_or_none(value) and default_value is not None:
        return default_value

    if isinstance(value, bool):
        return value

    if isinstance(value, str) and value is not None:
        value = value.lower()

    if value in ('yes', 'y', 'true', 't', '1'):
        return True

    if value in ('no', 'n', 'false', 'f', '0'):
        return False

    if strict:
        raise ValueError(f"The string \"{value}\" doesn't represent a boolean value")

    return default_value


def string_to_date(
        value: str | date | None = None,
        strict: bool = True
) -> date | None:
    """
    Convert a string representation of a date value to its corresponding
    date.


    :param value: The input to be converted into a date.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        date strings.  If ``False``, the function returns ``None`` for
        invalid date strings.


    :return: The date value corresponding to the string.


    :raise OverflowError: Raised if the parsed date exceeds the largest
        valid C integer on your system.

    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid date or the string format is unknown.
    """
    try:
        if not any_utils.is_empty_or_none(value):
            return value if isinstance(value, date) \
                else dateutil.parser.parse(value).date()
    except ValueError as error:
        if strict:
            raise error

    return None


def string_to_locale(
        value: str | Locale | None,
        strict: bool = True
) -> Locale | None:
    """
    Convert a string representation of a locale to its corresponding
    ``Locale`` instance.


    :param value: The input to be converted into a locale.  The input
        needs to be a ISO 639-3 alpha-3 code (or alpha-2 code), optionally
         followed by a dash character `-` and a ISO 3166-1 alpha-2 code.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, the input value must strictly comply
        with RFC 4646, otherwise a ``ValueError`` is raised.  If ``False``,
        the input value can be a Java-style locale (character `_` instead
        of `-`).


    :return: The ``Locale`` instance corresponding to the string.


    :raise MalformedLocaleException: If ``locale`` does not represent a
        valid locale.
    """
    try:
        return None if is_empty_or_none(value) else Locale.from_string(value, strict=strict)
    except Locale.MalformedLocaleException as exception:
        if strict:
            raise exception


def string_to_timestamp(
        value: str | datetime | None,
        strict: bool = True
) -> datetime | None:
    """
    Convert a string representation of a date/time value to its
    corresponding date/time.


    :param value: The input to be converted into a date/time.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        date/time strings.  If ``False``, the function returns ``None``
        for invalid date/time strings.


    :return: The date/time value corresponding to the string.


    :raise OverflowError: Raised if the parsed date exceeds the largest
        valid C integer on your system.

    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid date/time or the string format is unknown.
    """
    try:
        if not any_utils.is_empty_or_none(value):
            return value if isinstance(value, datetime) \
                else dateutil.parser.isoparse(value)
    except ValueError as error:
        if strict:
            raise error

    return None

def string_to_uuid(
        value: str | UUID | None,
        strict: bool = True
) -> UUID | None:
    """
    Convert a string representation of a UUID into a UUID object.

    This function attempts to parse the given string into a UUID object.
    If the string is not a valid UUID and strict mode is enabled, a
    ``ValueError`` is raised.  If strict mode is disabled, the function
    returns ``None`` when the string is not a valid UUID.


    :param value: The string to be converted into a UUID.  It should
        represent a valid UUID.  If the string is empty or ``None``, the
        function returns ``None``.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        UUID strings.  If ``False``, the function returns ``None`` for
        invalid UUID strings.


    :return: A UUID object corresponding to the given string, or ``None``
        if the string is invalid and strict mode is disabled.


    :raises ValueError: If ``strict`` is ``True`` and the string is not a
        valid UUID.
    """
    try:
        if not any_utils.is_empty_or_none(value):
            return value if isinstance(value, UUID) \
                else UUID(value)
    except ValueError as error:
        if strict:
            raise error

    return None
