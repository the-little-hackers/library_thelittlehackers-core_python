# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
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

import json

import pytest
from pydantic import BaseModel

from thelittlehackers.models.locale import DEFAULT_LOCALE
from thelittlehackers.models.locale import Locale
from thelittlehackers.models.locale import LocaleJSONEncoder
from thelittlehackers.models.locale import LocaleMatch
from thelittlehackers.models.locale import MalformedLocaleException


# Existing locales, without script, must keep parsing and serializing
# exactly as before.
@pytest.mark.parametrize('value, expected', [
    ('eng', 'eng'),
    ('en', 'eng'),
    ('eng-US', 'eng-US'),
    ('fr-CA', 'fra-CA'),
    ('vie', 'vie'),
])
def test_locale_without_script_is_unchanged(value, expected):
    locale = Locale.from_string(value)

    assert locale.script_code is None
    assert str(locale) == expected


@pytest.mark.parametrize('value, language_code, script_code, country_code', [
    ('zh-Hans', 'zho', 'Hans', None),
    ('zho-Hant', 'zho', 'Hant', None),
    ('zh-Hans-SG', 'zho', 'Hans', 'SG'),
    ('zho-Hant-TW', 'zho', 'Hant', 'TW'),
    ('sr-Latn', 'srp', 'Latn', None),
])
def test_parse_locale_with_script(value, language_code, script_code, country_code):
    locale = Locale.from_string(value)

    assert locale.language_code == language_code
    assert locale.script_code == script_code
    assert locale.country_code == country_code


@pytest.mark.parametrize('value, expected', [
    ('zh_hant_hk', 'zho-Hant-HK'),
    ('ZH-HANS', 'zho-Hans'),
    ('eng_us', 'eng-US'),
])
def test_parse_permissive_locale(value, expected):
    assert str(Locale.from_string(value, strict=False)) == expected


@pytest.mark.parametrize('value', ['zh_hant_hk', 'zh-hans', 'zh-Hans-cn', 'eng-us', 'zh-Hans-'])
def test_strict_parsing_rejects_non_canonical_locale(value):
    with pytest.raises(MalformedLocaleException):
        Locale.from_string(value)


@pytest.mark.parametrize('value', ['zh-Hanx', 'zho-Abcd-TW'])
def test_reject_unknown_script(value):
    with pytest.raises(ValueError):
        Locale.from_string(value)


def test_from_string_returns_none_for_undefined_locale():
    assert Locale.from_string(None) is None
    assert Locale.from_string('') is None


def test_decompose_locale_tag():
    assert Locale.decompose_locale_tag('zho-Hant-HK') == ('zho', 'Hant', 'HK')
    assert Locale.decompose_locale_tag('zh-Hans') == ('zh', 'Hans', None)
    assert Locale.decompose_locale_tag('eng-US') == ('eng', None, 'US')
    assert Locale.decompose_locale_tag('zh_hant_hk', strict=False) == ('zh', 'Hant', 'HK')


def test_decompose_locale_keeps_its_contract():
    assert Locale.decompose_locale('eng-US') == ('eng', 'US')
    assert Locale.decompose_locale('fra') == ('fra', None)

    with pytest.raises(MalformedLocaleException):
        Locale.decompose_locale('zho-Hant-HK')


def test_compose_locale():
    assert Locale.compose_locale('eng') == 'eng'
    assert Locale.compose_locale('eng', 'US') == 'eng-US'
    assert Locale.compose_locale('zho', script_code='Hans') == 'zho-Hans'
    assert Locale.compose_locale('zho', 'HK', 'Hant') == 'zho-Hant-HK'


def test_script_code_is_normalized_to_title_case():
    assert Locale(language_code='zh', script_code='hant').script_code == 'Hant'


def test_to_http_string():
    assert Locale.from_string('zho-Hant-HK').to_http_string() == 'zh-Hant-HK'
    assert Locale.from_string('zho-Hans').to_http_string() == 'zh-Hans'
    assert Locale.from_string('eng-US').to_http_string() == 'en-US'
    assert Locale.from_string('fra').to_http_string() == 'fr'


def test_equality_and_hash_include_script():
    assert Locale.from_string('zh-Hans') == Locale.from_string('zho-Hans')
    assert Locale.from_string('zho-Hans') != Locale.from_string('zho-Hant')
    assert Locale.from_string('zho-Hant') != Locale.from_string('zho')

    locales = {Locale.from_string('zho-Hans'), Locale.from_string('zh-Hans'), Locale.from_string('zho-Hant')}
    assert len(locales) == 2


def test_is_similar_ignores_script_and_country():
    assert Locale.from_string('zho-Hans').is_similar(Locale.from_string('zho-Hant-HK'))
    assert not Locale.from_string('zho-Hans').is_similar(Locale.from_string('jpn'))


@pytest.mark.parametrize('this, that, expected', [
    ('zho-Hant-HK', 'zho-Hant-HK', LocaleMatch.IDENTICAL),
    ('eng', 'eng', LocaleMatch.IDENTICAL),
    ('zho-Hant-HK', 'zho-Hant', LocaleMatch.SCRIPT),
    ('zho-Hant-HK', 'zho-Hant-TW', LocaleMatch.SCRIPT),
    ('eng-US', 'eng-GB', LocaleMatch.SCRIPT),
    ('eng-US', 'eng', LocaleMatch.SCRIPT),
    ('zho-Hant-HK', 'zho-Hans', LocaleMatch.LANGUAGE),
    ('zho-Hant', 'zho', LocaleMatch.LANGUAGE),
    ('zho-Hant', 'jpn', LocaleMatch.DIFFERENT),
])
def test_match(this, that, expected):
    assert Locale.from_string(this).match(Locale.from_string(that)) == expected
    assert Locale.from_string(that).match(Locale.from_string(this)) == expected


def test_best_match_prefers_the_same_script():
    requested = Locale.from_string('zho-Hant-HK')
    available = [Locale.from_string(value) for value in ('eng', 'zho-Hans', 'zho-Hant-TW')]

    assert str(max(available, key=requested.match)) == 'zho-Hant-TW'


def test_serialization_includes_script():
    class Model(BaseModel):
        locale: Locale

    locale = Locale.from_string('zh-Hant-HK')

    assert Model(locale=locale).model_dump_json() == '{"locale":"zho-Hant-HK"}'
    assert json.dumps({'locale': locale}, cls=LocaleJSONEncoder) == '{"locale": "zho-Hant-HK"}'


def test_default_locale_is_english():
    assert str(DEFAULT_LOCALE) == 'eng'
