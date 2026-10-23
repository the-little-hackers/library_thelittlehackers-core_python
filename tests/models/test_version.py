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

import pytest

from thelittlehackers.models.version import Version


def _project(tmp_path, content: str, encoding: str = 'utf-8'):
    (tmp_path / 'pyproject.toml').write_bytes(content.encode(encoding))
    return tmp_path


def test_reads_the_version_of_the_project_table(tmp_path):
    project = _project(tmp_path, '[project]\nname = "x"\nversion = "1.2.3"\n')

    assert str(Version.from_pyproject(project)) == '1.2.3'


def test_reads_the_version_of_the_poetry_table(tmp_path):
    project = _project(tmp_path, '[tool.poetry]\nname = "x"\nversion = "2.3.4"\n')

    assert str(Version.from_pyproject(project)) == '2.3.4'


def test_prefers_the_project_table(tmp_path):
    project = _project(tmp_path, '[project]\nversion = "1.2.3"\n[tool.poetry]\nversion = "9.9.9"\n')

    assert str(Version.from_pyproject(project)) == '1.2.3'


def test_reads_a_file_with_non_ascii_characters(tmp_path):
    project = _project(tmp_path, '[project]\nname = "x"\nversion = "1.0.0"\ndescription = "é à ü 日本語"\n')

    assert str(Version.from_pyproject(project)) == '1.0.0'


@pytest.mark.parametrize(
    'content, exception',
    [
        ('[project]\nversion = "1.0.0"\n[unclosed\n', 'TOMLDecodeError'),  # Not valid TOML.
        ('[project]\nversion = "not-a-version"\n', 'ValueError'),  # Not a valid version.
        ('[project]\nname = "x"\ndynamic = ["version"]\n', 'KeyError'),  # No version declared.
        ('[project]\nname = "x"\nversion = ""\n', 'KeyError'),  # No version declared.
    ]
)
def test_strict_raises_when_the_version_cannot_be_read(tmp_path, content, exception):
    project = _project(tmp_path, content)

    with pytest.raises(Exception) as error:
        Version.from_pyproject(project)

    assert type(error.value).__name__ == exception


@pytest.mark.parametrize(
    'content',
    [
        '[project]\nversion = "1.0.0"\n[unclosed\n',
        '[project]\nversion = "not-a-version"\n',
        '[project]\nname = "x"\ndynamic = ["version"]\n',
        '[project]\nname = "x"\nversion = ""\n',
    ]
)
def test_not_strict_returns_none_when_the_version_cannot_be_read(tmp_path, content):
    project = _project(tmp_path, content)

    assert Version.from_pyproject(project, strict=False) is None


def test_a_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        Version.from_pyproject(tmp_path)

    assert Version.from_pyproject(tmp_path, strict=False) is None
