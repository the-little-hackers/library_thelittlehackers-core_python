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

import pytest

from thelittlehackers.utils.mapping_utils import normalize_key
from thelittlehackers.utils.mapping_utils import normalize_mapping_keys


@pytest.mark.parametrize(
    ('value', 'expected_key'),
    [
        ("English", 'english'),
        ("Français", 'francais'),
        ("Español", 'espanol'),
        ("Tiếng Việt", 'tieng viet'),
        ("Đặng", 'dang'),
        ("Straße", 'strasse'),
        ("Русский", 'russkiy'),
        ("中文", 'zhongwen'),
        ("한국어", 'hangugeo'),
    ]
)
def test_normalize_key(value, expected_key):
    assert normalize_key(value) == expected_key


def test_normalize_mapping_keys():
    assert normalize_mapping_keys({"Français": 'fr', "English": 'en', "Español": 'es'}) == {
        'francais': 'fr',
        'english': 'en',
        'espanol': 'es',
    }
