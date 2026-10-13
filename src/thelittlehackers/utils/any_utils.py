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

from collections.abc import Sized
from numbers import Number
from typing import Any
from typing import SupportsFloat
from typing import SupportsInt
from uuid import UUID


def is_empty_or_none(value: Any) -> bool:
    """
    Check whether a value is ``None`` or empty.

    A value is empty if it is:

    - A string that is empty or contains only whitespace.
    - A collection with no items (e.g., ``list``, ``tuple``, ``set``,
      ``dict``).
    - Any other object that is falsy, except a number.

    A number (including a boolean) is never empty, even if it is zero.


    :param value: The value to check, of any type.


    :return: ``True`` if the value is ``None`` or empty; ``False``
        otherwise.
    """
    if value is None:
        return True
    elif isinstance(value, Number):
        # A number is never empty, including zero (e.g., `Decimal(0)`,
        # which is falsy).
        return False
    elif isinstance(value, str):
        return len(value.strip()) == 0
    elif isinstance(value, Sized):
        return len(value) == 0
    else:
        return not value


def is_integer(value: int | str | SupportsInt | None) -> bool:
    """
    Check whether a value is an integer or can be converted to an integer.

    A value can be converted to an integer if it implements ``__int__``
    (e.g., a ``float``, which is truncated, or a ``bool``), or if it is a
    string representing an integer in base 10 (e.g., ``"42"``,
    ``" -42 "``).


    :param value: The value to check, or ``None``.


    :return: ``True`` if the value is an integer or can be converted to an
        integer; ``False`` otherwise.
    """
    if value is None:
        return False

    if isinstance(value, SupportsInt):
        return True

    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def is_numeric(value: float | str | SupportsFloat | None) -> bool:
    """
    Check whether a value is a number or can be converted to a floating
    point number.

    A value can be converted to a floating point number if it implements
    ``__float__`` (e.g., an ``int``, a ``Decimal``), or if it is a string
    representing a decimal number (e.g., ``"3.14"``, ``"1e-3"``,
    ``"nan"``, ``"inf"``).


    :param value: The value to check, or ``None``.


    :return: ``True`` if the value is a floating point number or can be
        converted to one; ``False`` otherwise.
    """
    if value is None:
        return False

    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def is_uuid(value: str | UUID | None) -> bool:
    """
    Check whether a value is a Universally Unique Identifier (UUID) or a
    string representation of a UUID.

    The string representation can be in any format that the ``UUID``
    constructor accepts (e.g., with or without hyphens and braces, in
    any case).


    :param value: The value to check, or ``None``.


    :return: ``True`` if the value is a ``UUID`` or a string representation
        of a UUID; ``False`` otherwise.
    """
    if isinstance(value, UUID):
        return True

    if not isinstance(value, str):
        return False

    try:
        UUID(value)
        return True
    except ValueError:
        return False
