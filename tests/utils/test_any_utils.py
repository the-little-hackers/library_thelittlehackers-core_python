# MIT License
#
# Copyright (C) 2026 The Little Hackers.  All rights reserved.
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

from decimal import Decimal
from fractions import Fraction
from uuid import UUID

import pytest

from thelittlehackers.utils import any_utils


@pytest.mark.parametrize('value', [None, '', '   \n', [], (), set(), {}])
def test_is_empty_or_none(value):
    assert any_utils.is_empty_or_none(value)


@pytest.mark.parametrize('value', [0, 0.0, False, Decimal(0), Fraction(0), 0j, 'a', [0], {'a': 1}])
def test_is_empty_or_none_with_value(value):
    assert not any_utils.is_empty_or_none(value)


@pytest.mark.parametrize(
    'value',
    ['7f4df2d0-4f6c-4a1a-9b8e-2d6c3f1a5e90', '7F4DF2D04F6C4A1A9B8E2D6C3F1A5E90', UUID(int=0)],
)
def test_is_uuid(value):
    assert any_utils.is_uuid(value)


@pytest.mark.parametrize('value', [None, '', 'not-a-uuid', 123, b'7f4df2d04f6c4a1a9b8e2d6c3f1a5e90'])
def test_is_uuid_with_invalid_value(value):
    assert not any_utils.is_uuid(value)
