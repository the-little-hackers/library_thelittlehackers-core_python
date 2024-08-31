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
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from enum import Enum


class DataType(str, Enum):
    BOOLEAN = 'boolean'
    DATE = 'date'
    DECIMAL = 'decimal'
    DICTIONARY = 'dictionary'
    EMAIL_ADDRESS = 'email_address'
    ENUMERATION = 'enumeration'
    HEXADECIMAL = 'hexadecimal'
    INTEGER = 'integer'
    IPV4 = 'ipv4'
    LIST = 'list'
    LOCALE = 'locale'
    MAC_ADDRESS = 'macaddr'
    REGULAR_EXPRESSION = 'regex'
    STRING = 'string'
    TIME = 'time'
    TIMESTAMP ='timestamp'
    URI = 'uri'
    UUID = 'uuid'
    VERSION = 'version'