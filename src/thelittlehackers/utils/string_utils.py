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

import datetime
import dateutil.parser
import re
import string
import unicodedata
from enum import Enum, StrEnum
from re import Pattern
from typing import Callable
from typing import Literal
from typing import TypeVar
from typing import cast
from typing import overload
from uuid import UUID

from anyascii import anyascii

from thelittlehackers.constants import regex
from thelittlehackers.constants.data_type import DataType
from thelittlehackers.models.locale import Locale
from thelittlehackers.models.version import Version
from thelittlehackers.utils import any_utils
from thelittlehackers.utils.any_utils import is_empty_or_none


REGEX_EMAIL_ADDRESS: Pattern[str] = re.compile(regex.REGEX_PATTERN_EMAIL_ADDRESS)
REGEX_IPV4: Pattern[str] = re.compile(regex.REGEX_PATTERN_IPV4)
REGEX_MAC_ADDRESS: Pattern[str] = re.compile(regex.REGEX_PATTERN_MAC_ADDRESS)
REGEX_NON_ALPHANUMERIC_ASCII: Pattern[str] = re.compile(r'[^a-z0-9\s]')

# Unicode general categories of the characters that separate keywords
# (control characters, separators, punctuation, and math and other
# symbols), and of the characters that are removed without separating
# keywords (format characters, surrogates, private use and unassigned
# code points, currency and modifier symbols, and other numbers).
#
# See https://www.unicode.org/reports/tr44/#General_Category_Values
KEYWORD_SEPARATOR_UNICODE_CATEGORIES: set[str] = {
    'Cc', 'Zs', 'Zl', 'Zp',
    'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po',
    'Sm', 'So',
}
KEYWORD_IGNORED_UNICODE_CATEGORIES: set[str] = {
    'Cf', 'Cs', 'Co', 'Cn',
    'Sc', 'Sk',
    'No',
}

E = TypeVar('E', bound=StrEnum)


def is_empty(value: str) -> bool:
    """
    Check whether a string is empty or contains only whitespace.


    :param value: The string to check.


    :return: ``True`` if the string is empty once stripped of its
        surrounding whitespace; ``False`` otherwise.


    :raise ValueError: If ``value`` is ``None``.
    """
    if value is None:
        raise ValueError("Input value cannot be None.")

    return len(value.strip()) == 0


def is_valid_email_address(value: str | None) -> bool:
    """
    Check whether a string is a valid email address.

    The surrounding whitespace and the case of the string are ignored.


    :param value: The string to check, or ``None``.


    :return: ``True`` if the whole string, once stripped of its surrounding
        whitespace, is a valid email address; ``False`` otherwise.
    """
    if is_empty_or_none(value):
        return False

    # The regular expression is not anchored: the whole string must match,
    # not only its beginning (e.g., "jane@example.com, john@example.com").
    return REGEX_EMAIL_ADDRESS.fullmatch(value.strip().lower()) is not None


def string_to_boolean(
        value: bool | str | None,
        strict: bool = False,
        default_value: bool = False
) -> bool:
    """
    Convert a string representation of a boolean to a boolean.

    The recognized representations, ignoring case and surrounding
    whitespace, are ``yes``, ``y``, ``true``, ``t``, and ``1`` for
    ``True``, and ``no``, ``n``, ``false``, ``f``, and ``0`` for
    ``False``.


    :param value: The string to convert, a boolean (returned unchanged), or
        ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` is
        not a recognized representation of a boolean, including ``None``
        and an empty string.  Defaults to ``False``.

    :param default_value: The boolean to return if ``value`` is not a
        recognized representation of a boolean and ``strict`` is ``False``.
        Defaults to ``False``.


    :return: The boolean represented by ``value``, or ``default_value`` if
        ``value`` is not a recognized representation of a boolean and
        ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` is not a
        recognized representation of a boolean.
    """
    if isinstance(value, bool):
        return value

    normalized_value = value.strip().lower() if isinstance(value, str) else value

    if normalized_value in ('yes', 'y', 'true', 't', '1'):
        return True

    if normalized_value in ('no', 'n', 'false', 'f', '0'):
        return False

    if strict:
        raise ValueError(f"The string \"{value}\" doesn't represent a boolean value")

    return default_value


def string_to_date(
        value: str | datetime.date | None = None,
        strict: bool = True
) -> datetime.date | None:
    """
    Convert a string representation of a date to a date.

    The string can be in any format that ``dateutil.parser.parse`` supports
    (e.g., ``2026-10-13``, ``13 Oct 2026``).  The time part of the string,
    if any, is ignored.


    :param value: The string to convert, a date (returned unchanged), a
        date/time (whose date part is returned), or ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a date.  Defaults to ``True``.


    :return: The date represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if ``value``
        does not represent a date and ``strict`` is ``False``.


    :raise OverflowError: If the parsed date exceeds the largest valid C
        integer on the system.

    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a date.
    """
    try:
        date = (
            None if any_utils.is_empty_or_none(value)
            # A `datetime` is also a `date`: keep its date part only.
            else value.date() if isinstance(value, datetime.datetime)
            else value if isinstance(value, datetime.date)
            else dateutil.parser.parse(value).date()
        )
    except ValueError:
        if strict:
            raise
        date = None

    return date


def string_to_decimal(
        value: str | float | None,
        strict: bool = True
) -> float | None:
    """
    Convert a string representation of a decimal number to a floating
    point number.


    :param value: The string to convert, a floating point number (returned
        unchanged), or ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a decimal number.  Defaults to ``True``.


    :return: The floating point number represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``,
        or if ``value`` does not represent a decimal number and ``strict``
        is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a decimal number.
    """
    try:
        decimal = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, float) \
            else float(value)
    except ValueError:
        if strict:
            raise
        decimal = None

    return decimal


@overload
def string_to_email_address(
        value: str | None,
        strict: Literal[True] = True
) -> str:
    ...


@overload
def string_to_email_address(
        value: str | None,
        strict: bool
) -> str | None:
    ...


def string_to_email_address(
        value: str | None,
        strict: bool = True
) -> str | None:
    """
    Convert a string to a normalized email address.

    Email addresses are case-insensitive in practice.  Normalizing them
    (stripped of their surrounding whitespace and converted to lowercase)
    allows an application to store and compare them consistently,
    whatever the case in which the user typed them.


    :param value: The string to convert, or ``None``.

    :param strict: Indicate whether to raise an exception if the string is
        ``None``, empty, or not a valid email address.  Defaults to
        ``True``.


    :return: The normalized email address, or ``None`` if the string is
        ``None``, empty, or not a valid email address, and ``strict`` is
        ``False``.


    :raise ValueError: If ``strict`` is ``True`` and the string is not a
        valid email address.
    """
    if value is not None and is_valid_email_address(value):
        return value.strip().lower()

    if strict:
        raise ValueError(f"The string \"{value}\" does not represent an email address")

    return None


def string_to_enumeration_member(
        value: str | E | None,
        enumeration: type[E],
        *,
        strict: bool = True,
        default_value: str | E | None = None,
) -> E | None:
    """
    Convert the name or the value of an enumeration member to this member.

    The name of a member is looked up first, then its value.


    :param value: The name or the value of a member of ``enumeration``, a
        member of ``enumeration`` (returned unchanged), or ``None``.

    :param enumeration: The enumeration class the member belongs to.

    :param strict: Indicate whether to raise an exception if ``value`` is
        neither the name nor the value of a member of ``enumeration``.
        Defaults to ``True``.

    :param default_value: The name, the value, or the member to convert if
        ``value`` is ``None`` or an empty string.  Defaults to ``None``.


    :return: The member of ``enumeration``, or ``None`` if ``value`` and
        ``default_value`` are both ``None`` or empty, or if ``value`` is
        neither the name nor the value of a member and ``strict`` is
        ``False``.


    :raise TypeError: If ``enumeration`` is not an enumeration class.

    :raise ValueError: If ``strict`` is ``True`` and ``value`` is neither
        the name nor the value of a member of ``enumeration``.
    """
    if not isinstance(enumeration, type):
        raise TypeError(f"'enumeration' must be an enumeration class, got {enumeration!r}")

    if not issubclass(enumeration, Enum):
        raise TypeError(f"'enumeration' must be a subclass of Enum, got {enumeration!r}")

    def convert(e: str | E) -> E:
        """Convert an enumeration member, name, or value to a member."""
        if isinstance(e, enumeration):
            return e

        try:
            return enumeration[e]  # type: ignore  # by member name
        except KeyError:
            return enumeration(e)  # by member value

    candidate = (
        default_value
        if any_utils.is_empty_or_none(value)
        else value
    )

    if candidate is None:
        return None

    try:
        return convert(candidate)
    except (KeyError, ValueError):
        if strict:
            raise ValueError(f'"{candidate}" is not a member of {enumeration.__name__}.') from None
        return None


def string_to_integer(
        value: str | int | None,
        strict: bool = True
) -> int | None:
    """
    Convert a string representation of an integer to an integer.


    :param value: The string to convert, an integer (returned unchanged), or
        ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent an integer.  Defaults to ``True``.


    :return: The integer represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if
        ``value`` does not represent an integer and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent an integer.
    """
    try:
        integer = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, int) \
            else int(value)
    except ValueError:
        if strict:
            raise
        integer = None

    return integer


def string_to_ipv4(
        value: str | None,
        strict: bool = True
) -> tuple[int, int, int, int] | None:
    """
    Convert a string representation of an IPv4 address to a tuple of its
    four bytes.

    >>> string_to_ipv4('192.168.1.1')
    (192, 168, 1, 1)

    >>> string_to_ipv4('256.168.1.1', strict=False) is None
    True


    :param value: The string to convert, in the dot-decimal notation
        ``X.X.X.X`` where each ``X`` is an integer between ``0`` and
        ``255``, or ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` is
        ``None``, empty, or not an IPv4 address.  Defaults to ``True``.


    :return: The four bytes of the IPv4 address (e.g., ``(192, 168, 1, 1)``),
        or ``None`` if ``value`` is ``None``, empty, or not an IPv4 address
        and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` is ``None``,
        empty, or not an IPv4 address.
    """
    match = None if any_utils.is_empty_or_none(value) else REGEX_IPV4.match(value)
    if match is None:
        if strict:
            raise ValueError(f"The string \"{value}\" does not represent an IPv4 address")
        return None

    return cast(
        tuple[int, int, int, int],
        tuple(int(byte) for byte in match.group(0).split('.'))
    )


def string_to_keywords(
        value: str,
        keyword_minimal_length: int = 1
) -> list[str]:
    """
    Convert a string to a list of distinct keywords.

    The function:

    - Separates the words on punctuation, symbols, and whitespace.
    - Transliterates the Unicode characters, whatever their script, to their
      closest lowercase ASCII equivalents (e.g., "Đặng" to "dang", "Straße"
      to "strasse", "Владимир" to "vladimir").
    - Keeps the distinct words longer than ``keyword_minimal_length``.


    :param value: The string to convert, or ``None``.

    :param keyword_minimal_length: The length that a keyword must exceed to
        be returned.  Defaults to ``1``, which excludes single-character
        keywords.


    :return: The distinct keywords of the string, in no particular order,
        or an empty list if ``value`` is ``None`` or empty.
    """
    if is_empty_or_none(value):
        return []

    # Replace any punctuation, symbol, separator, or control character with
    # a space, before transliterating the string, so that keywords are
    # separated the same way whatever the script of the string.
    #
    # The string is first normalized to its compatibility composed form
    # (NFKC) to replace compatibility characters (e.g., ligatures,
    # superscripts, full-width forms) with their canonical equivalents.
    characters = []
    for c in unicodedata.normalize('NFKC', value):
        unicode_category = unicodedata.category(c)
        if unicode_category in KEYWORD_SEPARATOR_UNICODE_CATEGORIES:
            characters.append(' ')
        elif unicode_category not in KEYWORD_IGNORED_UNICODE_CATEGORIES:
            characters.append(c)

    # Transliterate the string to lowercase ASCII characters, and remove
    # any non-alphanumeric character resulting from the transliteration
    # (e.g., "`" for the Arabic letter ain), without separating keywords.
    ascii_string = anyascii(''.join(characters)).lower()
    cleansed_string = REGEX_NON_ALPHANUMERIC_ASCII.sub('', ascii_string)

    # Decompose the string into distinct keywords.
    distinct_keywords = set(cleansed_string.split())

    # Keep the keywords longer than the minimal length.
    return [
        keyword
        for keyword in distinct_keywords
        if len(keyword) > keyword_minimal_length
    ]


def string_to_locale(
        value: str | Locale | None,
        strict: bool = True
) -> Locale | None:
    """
    Convert a string representation of a locale to a ``Locale``.


    :param value: The string to convert, a ``Locale`` (returned unchanged),
        or ``None``.  The string is an ISO 639-3 alpha-3 code (or an ISO
        639-1 alpha-2 code), optionally followed by a dash character ``-``
        and an ISO 3166-1 alpha-2 code (e.g., ``fra``, ``fr-CA``).

    :param strict: Indicate whether the string must strictly comply with
        RFC 4646, and whether to raise an exception if it does not represent
        a locale.  If ``False``, a Java-style locale (with an underscore
        character ``_`` instead of a dash) is also accepted.  Defaults to
        ``True``.


    :return: The ``Locale`` represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if
        ``value`` does not represent a locale and ``strict`` is ``False``.


    :raise MalformedLocaleException: If ``strict`` is ``True`` and ``value``
        does not represent a locale.
    """
    # Imported here to avoid a circular import.
    from thelittlehackers.models.locale import MalformedLocaleException

    try:
        locale = (
            None if any_utils.is_empty_or_none(value)
            else value if isinstance(value, Locale)
            else Locale.from_string(value, strict=strict)
        )
    except MalformedLocaleException as exception:
        if strict:
            raise exception
        locale = None

    return locale


def string_to_mac_address(
        value: str | None,
        strict: bool = True
) -> tuple[str, str, str, str, str, str] | None:
    """
    Convert a string representation of a Media Access Control (MAC) address
    to a tuple of its six bytes.

    The standard IEEE 802 format of an EUI-48 address is six groups of two
    hexadecimal digits separated by hyphens (e.g., ``01-23-45-67-89-AB``).
    The following formats are also accepted:

    - Six groups of two hexadecimal digits separated by colons (e.g.,
      ``01:23:45:67:89:AB``), or not separated (e.g., ``0123456789AB``).
    - Three groups of four hexadecimal digits separated by dots (e.g.,
      ``0123.4567.89AB``).


    :param value: The string to convert, or ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` is
        ``None``, empty, or not a MAC address.  Defaults to ``True``.


    :return: The six bytes of the MAC address, as strings of two hexadecimal
        digits in the case of ``value`` (e.g., ``('01', '23', '45', '67',
        '89', 'AB')``), or ``None`` if ``value`` is ``None``, empty, or not
        a MAC address and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` is ``None``,
        empty, or not a MAC address.
    """
    match = None if any_utils.is_empty_or_none(value) else REGEX_MAC_ADDRESS.match(value)
    if match is None:
        if strict:
            raise ValueError(f"The string \"{value}\" does not represent a MAC address")
        return None

    # Remove the separator characters, and split the twelve hexadecimal
    # digits into six pairs.
    hexdigits = ''.join(c for c in match.group(0) if c in string.hexdigits)
    return cast(
        tuple[str, str, str, str, str, str],
        tuple(hexdigits[i:i + 2] for i in range(0, len(hexdigits), 2))
    )


def string_to_string(
        value: str | None
) -> str | None:
    """
    Return a string, or ``None`` if it is empty.


    :param value: A string, or ``None``.


    :return: The string unchanged, or ``None`` if it is ``None``, empty, or
        contains only whitespace.
    """
    return None if any_utils.is_empty_or_none(value) else value


def string_to_time(
        value: str | datetime.time | None,
        strict: bool = True
) -> datetime.time | None:
    """
    Convert a string representation of a time to a time.


    :param value: The string to convert, a time (returned unchanged), or
        ``None``.  The string is in the format ``HH:MM:SS`` or ``HH:MM``,
        where ``HH`` is the hour in the 24-hour format (``00`` to ``23``),
        ``MM`` the minute, and ``SS`` the second (``00`` to ``59``).

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a time.  Defaults to ``True``.


    :return: The time represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if ``value``
        does not represent a time and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a time.
    """
    try:
        time = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, datetime.time) \
            else datetime.datetime.strptime(value, '%H:%M:%S').time()
    except ValueError:
        try:
            return datetime.datetime.strptime(value, '%H:%M').time()
        except ValueError:
            if strict:
                raise
            time = None

    return time


def string_to_timestamp(
        value: str | datetime.datetime | None,
        strict: bool = True
) -> datetime.datetime | None:
    """
    Convert an ISO 8601 representation of a date/time to a date/time.


    :param value: The string to convert (e.g., ``2026-10-13T08:30:00Z``),
        a date/time (returned unchanged), or ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a date/time.  Defaults to ``True``.


    :return: The date/time represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if
        ``value`` does not represent a date/time and ``strict`` is
        ``False``.


    :raise OverflowError: If the parsed date exceeds the largest valid C
        integer on the system.

    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a date/time.
    """
    try:
        timestamp = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, datetime.datetime) \
            else dateutil.parser.isoparse(value)
    except ValueError:
        if strict:
            raise
        timestamp = None

    return timestamp


def string_to_version(
        value: str | Version | None,
        strict: bool = True
) -> Version | None:
    """
    Convert a string representation of a version to a ``Version``.


    :param value: The string to convert, complying with Semantic Versioning
        2.0.0 (e.g., ``1.4.1``), a ``Version`` (returned unchanged), or
        ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a version.  Defaults to ``True``.


    :return: The ``Version`` represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if
        ``value`` does not represent a version and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a version.
    """
    try:
        version = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, Version) \
            else Version.from_string(value)
    except ValueError:
        if strict:
            raise
        version = None

    return version


def string_to_uuid(
        value: str | UUID | None,
        strict: bool = True
) -> UUID | None:
    """
    Convert a string representation of a UUID to a ``UUID``.


    :param value: The string to convert, a ``UUID`` (returned unchanged), or
        ``None``.

    :param strict: Indicate whether to raise an exception if ``value`` does
        not represent a UUID.  Defaults to ``True``.


    :return: The ``UUID`` represented by ``value``, ``None`` if ``value`` is ``None`` or an empty
            string, whatever ``strict``, or if
        ``value`` does not represent a UUID and ``strict`` is ``False``.


    :raise ValueError: If ``strict`` is ``True`` and ``value`` does not
        represent a UUID.
    """
    try:
        uuid = None if any_utils.is_empty_or_none(value) \
            else value if isinstance(value, UUID) \
            else UUID(value)
    except ValueError:
        if strict:
            raise
        uuid = None

    return uuid


DATA_TYPE_CONVERTERS: dict[DataType, Callable] = {
    DataType.BOOLEAN: string_to_boolean,
    DataType.DATE: string_to_date,
    DataType.DECIMAL: string_to_decimal,
    DataType.EMAIL_ADDRESS: string_to_email_address,
    DataType.ENUMERATION: lambda value, **kwargs: string_to_enumeration_member(value, **kwargs),
    DataType.INTEGER: string_to_integer,
    DataType.IPV4: string_to_ipv4,
    # DataType.LIST: __convert_to_list,
    DataType.LOCALE: string_to_locale,
    DataType.MAC_ADDRESS: string_to_mac_address,
    DataType.STRING: string_to_string,
    DataType.TIME: string_to_time,
    DataType.TIMESTAMP: string_to_timestamp,
    DataType.UUID: string_to_uuid,
    DataType.VERSION: string_to_version,
}
