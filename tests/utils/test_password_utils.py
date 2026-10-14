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

from thelittlehackers.utils import password_utils


@pytest.mark.parametrize('content', ['s3cr3t', 's3cr3t\n', '  s3cr3t \r\n'])
def test_read_password_file(tmp_path, content):
    file_path = tmp_path / 'secret'
    file_path.write_text(content, encoding='utf-8')
    assert password_utils.read_password_file(file_path) == 's3cr3t'


def test_read_password_file_with_string_path(tmp_path):
    file_path = tmp_path / 'secret'
    file_path.write_text('s3cr3t', encoding='utf-8')
    assert password_utils.read_password_file(str(file_path)) == 's3cr3t'


@pytest.mark.parametrize('content', ['', '  \n'])
def test_read_password_file_with_empty_file(tmp_path, content):
    file_path = tmp_path / 'secret'
    file_path.write_text(content, encoding='utf-8')
    with pytest.raises(ValueError):
        password_utils.read_password_file(file_path)


def test_read_password_file_with_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        password_utils.read_password_file(tmp_path / 'missing')
