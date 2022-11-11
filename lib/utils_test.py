# -*- coding: utf-8 -*-

import pytest
from lib.utils import string_to_int


def test_string_to_int():
    assert string_to_int('1') == 1
    assert string_to_int('1.0') == 1
    assert string_to_int('1.1') == 1
    assert string_to_int('1.9') == 1
    assert string_to_int('123,456') == 123456
    assert string_to_int('123,456.0') == 123456
    assert string_to_int('123,456k') == 123456000
    assert string_to_int('123,456.0k') == 123456000
    assert string_to_int('123,456.9k') == 123456900
    assert string_to_int('123,456.9m') == 123456900000
