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

from thelittlehackers.utils import string_utils

from thelittlehackers.utils.string_utils import is_valid_email_address
from thelittlehackers.utils.string_utils import string_to_email_address
from thelittlehackers.utils.string_utils import string_to_keywords


@pytest.mark.parametrize(
    'value',
    ['jane.doe@example.com', 'Jane.Doe@Example.COM', '  jane+news@example.co.uk\n'],
)
def test_is_valid_email_address(value):
    assert is_valid_email_address(value)


@pytest.mark.parametrize(
    'value',
    [None, '', '   ', 'jane.doe', 'jane.doe@', '@example.com', 'jane.doe@example.com, john@example.com'],
)
def test_is_valid_email_address_with_invalid_value(value):
    assert not is_valid_email_address(value)


@pytest.mark.parametrize(
    ('value', 'expected_email_address'),
    [
        ('jane.doe@example.com', 'jane.doe@example.com'),
        ('Jane.Doe@Example.COM', 'jane.doe@example.com'),
        ('  jane.doe@example.com\n', 'jane.doe@example.com'),
    ],
)
def test_string_to_email_address(value, expected_email_address):
    assert string_to_email_address(value) == expected_email_address


@pytest.mark.parametrize('value', [None, '', 'jane.doe'])
def test_string_to_email_address_with_invalid_value(value):
    with pytest.raises(ValueError):
        string_to_email_address(value)

    assert string_to_email_address(value, strict=False) is None


@pytest.mark.parametrize(
    ('value', 'expected_keywords'),
    [
        # Latin-script names whose letters decompose to a base letter and
        # diacritics.
        ("François Dupont", ['dupont', 'francois']),
        ("Hélène de La Tour-d'Auvergne", ['auvergne', 'de', 'helene', 'la', 'tour']),
        ("José María Núñez", ['jose', 'maria', 'nunez']),
        ("Müller", ['muller']),
        ("İsmail", ['ismail']),
        ("Nguyễn Thị Minh Khai", ['khai', 'minh', 'nguyen', 'thi']),

        # Latin-script letters that don't decompose.
        ("Đặng Văn Đức", ['dang', 'duc', 'van']),
        ("Straße", ['strasse']),
        ("Søren Kierkegaard", ['kierkegaard', 'soren']),
        ("Ægir", ['aegir']),
        ("Cœur de Lion", ['coeur', 'de', 'lion']),
        ("Łukasz Żółć", ['lukasz', 'zolc']),
        ("Þórður Guðmundsson", ['gudmundsson', 'thordur']),
        ("Kılıç Işık", ['isik', 'kilic']),
        ("Ədalət Əliyev", ['edalet', 'eliyev']),

        # Other scripts.
        ("Владимир Путин", ['putin', 'vladimir']),
        ("Ελένη Παπαδοπούλου", ['eleni', 'papadopoyloy']),
        ("毛泽东", ['maozedong']),
        ("김정은", ['gimjeongeun']),
        ("मोहनदास करमचंद गांधी", ['gamdhi', 'krmcmd', 'mohndas']),

        # Punctuation, symbols, and whitespace.
        ("Jean-Paul O'Brien", ['brien', 'jean', 'paul']),
        ("Jean–Paul O’Brien", ['brien', 'jean', 'paul']),
        ("Anne Marie", ['anne', 'marie']),
        ("tab\tand\nnewline", ['and', 'newline', 'tab']),
        ("zero​width", ['zerowidth']),
        ("Email template: Welcome (v2)!", ['email', 'template', 'v2', 'welcome']),
        ("Rappel — réunion parents/professeurs", ['parents', 'professeurs', 'rappel', 'reunion']),
        ("Prix: 10€ / $5", ['10', 'prix']),
        ("N° 5, 2ème étage", ['2eme', 'etage']),
        ("user@example.com", ['com', 'example', 'user']),
        ("2024-09-01", ['01', '09', '2024']),
        ("Anna 🌸 Smith", ['anna', 'smith']),
        ("C++ & C#", []),

        # Compatibility characters.
        ("ﬁnal ﬂight", ['final', 'flight']),
        ("ＡＢＣ　ｄｅｆ", ['abc', 'def']),
        ("x² + y² ½", ['x2', 'y2']),
        ("abc™", ['abctm']),
    ]
)
def test_string_to_keywords(value, expected_keywords):
    assert sorted(string_to_keywords(value)) == expected_keywords


@pytest.mark.parametrize('value', [None, '', '   ', '!!!'])
def test_string_to_keywords_with_no_keywords(value):
    assert string_to_keywords(value) == []


def test_string_to_keywords_with_minimal_length():
    assert sorted(string_to_keywords("Le petit chat de Đà Lạt", keyword_minimal_length=2)) == [
        'chat', 'lat', 'petit'
    ]


@pytest.mark.parametrize(
    'converter',
    [
        string_utils.string_to_date,
        string_utils.string_to_decimal,
        string_utils.string_to_integer,
        string_utils.string_to_locale,
        string_utils.string_to_time,
        string_utils.string_to_timestamp,
        string_utils.string_to_uuid,
        string_utils.string_to_version,
    ],
)
@pytest.mark.parametrize('value', [None, '', '   '])
def test_converter_with_no_value(converter, value):
    assert converter(value, strict=True) is None


@pytest.mark.parametrize(
    'value',
    ['01-23-45-67-89-AB', '01:23:45:67:89:AB', '0123456789AB', '0123.4567.89AB'],
)
def test_string_to_mac_address(value):
    assert string_utils.string_to_mac_address(value) == ('01', '23', '45', '67', '89', 'AB')


@pytest.mark.parametrize('value', [None, '', '01-23-45-67-89', '01-23-45-67-89-GH'])
def test_string_to_mac_address_with_invalid_value(value):
    with pytest.raises(ValueError):
        string_utils.string_to_mac_address(value)

    assert string_utils.string_to_mac_address(value, strict=False) is None
