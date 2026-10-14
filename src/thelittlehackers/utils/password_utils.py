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

from __future__ import annotations

from os import PathLike
from pathlib import Path


def read_password_file(file_path: str | PathLike[str]) -> str:
    """
    Return the password (or any other secret, such as an API secret key)
    stored in a file.

    Container platforms, such as Docker and Kubernetes, pass a secret to
    an application as a file (e.g., `/run/secrets/db_password`) rather
    than as an environment variable, which any process able to inspect
    the container could read.  The application usually gets the path of
    this file from an environment variable suffixed with `_FILE` (e.g.,
    `DB_PASSWORD_FILE`).


    :param file_path: The path of the file containing the password.


    :return: The content of the file, stripped of its leading and
        trailing whitespace (e.g., the newline that most editors add at
        the end of a file).


    :raise FileNotFoundError: If the file does not exist.

    :raise IsADirectoryError: If the path is a directory.

    :raise PermissionError: If the file cannot be read.

    :raise ValueError: If the file is empty or only contains whitespace.
    """
    password = Path(file_path).read_text(encoding='utf-8').strip()
    if not password:
        raise ValueError(f"The password file \"{file_path}\" is empty")

    return password
