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

from pathlib import Path


DEFAULT_DIRECTORY_DEPTH = 8


def generate_hierarchical_path(
        file_name: Path,
        directory_depth: int = DEFAULT_DIRECTORY_DEPTH
) -> Path:
    """
    Return a pathname built from the specified number of subdirectories,
    where each directory is named after the nth letter of the filename,
    corresponding to the directory depth.

    Examples:

    ```python
    >>> generate_hierarchical_path(Path('foo.txt'), 2)
    Path('f/o/')
    >>> generate_hierarchical_path(Path('0123456789abcdef'))
    Path('0/1/2/3/4/5/6/7/')
    ```


    :param file_name: The name of a file, with or without an extension.

    :param directory_depth: The number of subdirectories to generate.


    :return: A path representing the directory structure.
    """
    file_name_without_extension = file_name.stem
    max_depth = min(directory_depth, len(file_name_without_extension))
    path = Path(*file_name_without_extension[:max_depth])
    return path


def generate_hierarchical_file_path(
        file_name: Path,
        directory_depth: int = DEFAULT_DIRECTORY_DEPTH
) -> Path:
    """
    Generate a file path with a structured subdirectory hierarchy based on
    the characters of the filename.

    The function creates a directory structure where each level
    corresponds to a character from the filename, up to the specified
    depth.  The full filename is then appended at the end of this path.

    Examples:
    ```python
    >>> generate_hierarchical_file_path(Path('foo.txt'), 2)
    Path('f/o/foo.txt')
    >>> generate_hierarchical_file_path(Path('0123456789abcdef'))
    Path('0/1/2/3/4/5/6/7/0123456789abcdef')
    ```


    :param file_name: The name of a file, with or without an extension.

    :param directory_depth: The number of subdirectories to generate.


    :return: a file pathname.
    """
    path = generate_hierarchical_path(file_name, directory_depth)
    return Path.joinpath(path, file_name)
