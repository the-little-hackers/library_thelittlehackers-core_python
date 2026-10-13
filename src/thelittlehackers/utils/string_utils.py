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
from typing import Callable, cast, Any, Literal, LiteralString
from typing import overload
from typing import TypeVar
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
    Checks if the specified value is empty.

    A value is considered empty if it is an empty string after stripping
    whitespace.


    :param value: The value to check for being empty.

    :return: ``True`` if the value is empty , ``False`` otherwise.


    :raise ValueError: if the input value is ``None``.
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
    Convert a string representation of a date value to its corresponding
    date.


    :param value: The input to be converted into a date.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        date strings.  If ``False``, the function returns ``None`` for
        invalid date strings.


    :return: The date corresponding to the string.


    :raise OverflowError: Raised if the parsed date exceeds the largest
        valid C integer on your system.

    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid date or the string format is unknown.
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
    Convert a string representation of a floating number value to its
    corresponding floating number.


    :param value: The input to be converted into an floating number.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        floating number strings.  If ``False``, the function returns
        ``None`` for invalid floating number strings.


    :return: The floating number value corresponding to the string.


    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid floating number.
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


    :raises ValueError: If ``strict`` is ``True`` and the string is not a
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
    Convert a string representation of an enumeration member to its
    corresponding enumeration member.


    :param value: The name of an enumeration member, or its value, or
        ``None``.

    :param enumeration: The enumeration class to which the value should
        belong.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        enumeration strings.  If ``False``, the function returns ``None``
        for invalid enumeration strings.

    :param default_value: The default enumeration member to return if
        ``value`` is ``None`` or an empty string.  Defaults to ``None``.


    :return: The corresponding enumeration member if conversion succeeds,
        or ``None`` if ``strict`` is ``False`` and conversion fails.


    :raise ValueError: If ``enumeration`` is not a subclass of ``Enum``.

    :raise ValueError: If ``value`` is a string that does not match any
        member of ``enumeration`` and ``strict`` is ``True``.
    """
    if not isinstance(enumeration, type):
        raise TypeError(f"'enumeration' must be an StrEnum class, got {enumeration!r}")

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
    Convert a string representation of an integer value to its
    corresponding integer.


    :param value: The input to be converted into an integer.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        integer strings.  If ``False``, the function returns ``None`` for
        invalid integer strings.


    :return: The integer value corresponding to the string.


    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid integer.
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
    Convert a string representation of an IPv4 address into a tuple of
    four integers.

    Examples:
    >>> string_to_ipv4('192.168.1.1')
    (192, 168, 1, 1)

    >>> string_to_ipv4('256.168.1.1')
    ValueError: The IPv4 "256.168.1.1" has invalid byte(s)

    >>> string_to_ipv4(None)
    ValueError: The specified string "None" does not represent an IPv4

    >>> string_to_ipv4(None, strict=False)
    None


    :param value: The input to be converted into an IPv4 address.  It
        should be in the format `'X.X.X.X'`, where X is an integer between
        ``0`` and ``255``.   If ``value`` is ``None`` or an empty string,
         the function will return ``None`` unless ``strict`` is set to
         ``True``.

    :param strict: If ``True``, the function will raise a ``ValueError``
        if the string is ``None``, empty, or does not represent a valid
        IPv4 address.  If ``False``, the function will return ``None`` fpr
        such cases.


    :return: A tuple of four integers representing the IPv4 address, where
        each integer corresponds to one byte of the address (e.g.,
        ``(192, 168, 1, 1)``).  If ``value`` is ``None``, empty, or
        invalid (and ``strict`` is ``False``), the function returns ``None``.


    :raise ValueError: If the input string does not represent a valid IPv4
        address and ``strict`` is ``True``.  This includes cases where the
        string is ``None``, empty, or has invalid bytes (e.g., values not
        in the range ``0-255``).
    """
    match = None if any_utils.is_empty_or_none(value) else REGEX_IPV4.match(value)
    ipv4_address = match and match.group(0).split('.')

    if ipv4_address is None:
        if strict:
            raise ValueError(
                f"The string \"{value}\" does not represent a IPV4 address"
            )
    else:
        ipv4_address = tuple(
            int(component)
            for component in ipv4_address
        )

    return ipv4_address


def string_to_keywords(
        value: str,
        keyword_minimal_length: int = 1
) -> list[str]:
    """
    Convert a string to a list of distinct keywords by removing
    punctuation, reducing whitespace, and transliterating Unicode
    characters to lowercase ASCII.

    This function cleanses a given string by:
    - Separating words on punctuation, symbols, and whitespace.
    - Transliterating Unicode characters, whatever their script, to their
      closest lowercase ASCII equivalents (e.g., "Đặng" to "dang",
      "Straße" to "strasse", "Владимир" to "vladimir").
    - Splitting the string into unique keywords and filtering by length.


    :param value: The input string to be processed into keywords.

    :param keyword_minimal_length: The minimum length a keyword must have
        to be included in the final list.


    :return: A list of unique keywords, stripped of punctuation,
        accentuated characters, and extra spaces, meeting the specified
        minimal length.
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

    # Filter out keywords of less than 2 characters.
    valid_keywords = [
        keywords
        for keywords in distinct_keywords
        if len(keywords) > keyword_minimal_length
    ]

    return valid_keywords


def string_to_locale(
        value: str | Locale | None,
        strict: bool = True
) -> Locale | None:
    """
    Convert a string representation of a locale to its corresponding
    ``Locale`` object.


    :param value: The input to be converted into a locale.  The input
        needs to be a ISO 639-3 alpha-3 code (or alpha-2 code), optionally
         followed by a dash character `-` and a ISO 3166-1 alpha-2 code.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, the input value must strictly comply
        with RFC 4646, otherwise a ``ValueError`` is raised.  If ``False``,
        the input value can be a Java-style locale (character `_` instead
        of `-`).


    :return: The ``Locale`` object corresponding to the string.


    :raise MalformedLocaleException: If ``locale`` does not represent a
        valid locale.
    """
    from thelittlehackers.models.locale import MalformedLocaleException  # Declare here To avoid circular dependency.

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
    Convert a string representation of a Media Access Control (MAC)
    address into a tuple of hexadecimal strings.

    A MAC address is a unique identifier assigned to a network interface
    controller (NIC) for communications at the data link layer of a
    network segment. The standard IEEE 802 format for representing EUI-48
    addresses is six groups of two hexadecimal digits, separated by
    hyphens (e.g., ``01-23-45-67-89-AB``). Other common formats include:

    - Six groups separated by colons (e.g., ``01:23:45:67:89:AB``)
    - Three groups of four hexadecimal digits separated by dots (e.g.,
      ``0123.4567.89AB``)

    The function validates the input string against these formats and
    returns the corresponding hexadecimal components.


    :param value: A string representation of a MAC address.  If `None`,
        the function will behave according to the ``strict`` parameter.

    :param strict: If `True`, the function raises a ValueError when the
        input string does not match a valid MAC address format.  If
        ``False``, the function returns ``None`` for invalid inputs.


    :return: A tuple of six hexadecimal strings ``(hex1, hex2, hex3, hex4,
        hex5, hex6)`` representing the MAC address, each ranging from
        ``0x00`` to ``0xFF``.  Return ``None`` if the input is invalid and
        ``strict`` is set to ``False``.
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
    Return the input string if it is not empty or ``None``.


    :param value: A string.


    :return: The input string if it is non-empty and not ``None``;
        otherwise, ``None``.
    """
    return None if any_utils.is_empty_or_none(value) else value


def string_to_time(
        value: str | datetime.time | None,
        strict: bool = True
) -> datetime.time | None:
    """
    Convert a string representation of a time value into a `datetime.time`
    object.


    :param value: The input to be converted into a `datetime.time` object.
        This can be a string, a ``datetime.time`` object, or ``None``.
        A string must be given in the format `HH:MM` or `HH:MM:SS`, where:

        - ``HH``: Two-digit hour in 24-hour format (00-23).
        - ``MM``: Two-digit minute (00-59).
        - ``SS``: Two-digit second (00-59).

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        time strings.  If ``False``, the function returns ``None`` for
        invalid time strings.


    :return: A ``datetime.time`` object representing the time specified by
        the input string, or ``None`` if the input is ``None`` or an
        invalid string in non-strict mode.


    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid time in the expected format.
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
    Convert a string representation of a date/time value into a
    ``datetime.datetime`` object.


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
    Convert a string representation of a version value to its
    corresponding version.


    :param value: The input to be converted into a version.

    :param strict: A boolean flag indicating whether to enforce strict
        validation.  If ``True``, a ``ValueError`` is raised for invalid
        version strings complying with Semantic Version 2.  If ``False``,
        the function returns ``None`` for invalid version strings.


    :return: The ``Version`` instance corresponding to the string.


    :raise ValueError: If ``strict`` is ```True``` and ``value`` does not
        represent a valid version or the string doesn't comply to Semantic
        Version 2.
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
