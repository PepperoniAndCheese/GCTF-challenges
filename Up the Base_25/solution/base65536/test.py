# -*- coding: utf-8 -*-
import os
import unicodedata

import pytest
from six import int2byte

import base65536


SAMPLES_DIRNAME = os.path.join(os.path.dirname(__file__), 'sample-files')
UNICODE_NORMAL_FORMS = ['NFC', 'NFD', 'NFKC', 'NFKD']


def assert_encoding(data):
    encoded = base65536.encode(data)
    for form in UNICODE_NORMAL_FORMS:
        assert unicodedata.normalize(form, encoded) == encoded
    assert base65536.decode(encoded) == data


@pytest.mark.parametrize('filename', os.listdir(SAMPLES_DIRNAME))
def test_sample_file(filename):
    # https://github.com/ferno/base65536/blob/
    # 25d6ea5104a16c24787fa1d8b4af836ba8bb6214/test.js#L72
    with open(os.path.join(SAMPLES_DIRNAME, filename), 'rb') as f:
        data = f.read()
    assert_encoding(data)


def test_1_byte():
    # https://github.com/ferno/base65536/blob/
    # 25d6ea5104a16c24787fa1d8b4af836ba8bb6214/test.js#L10
    for x in range(256):
        assert_encoding(int2byte(x))


def test_2_bytes():
    # https://github.com/ferno/base65536/blob/
    # 25d6ea5104a16c24787fa1d8b4af836ba8bb6214/test.js#L47
    for x in range(256):
        for y in range(256):
            assert_encoding(int2byte(x) + int2byte(y))


def test_bad():
    # https://github.com/ferno/base65536/blob/
    # 25d6ea5104a16c24787fa1d8b4af836ba8bb6214/test.js#L24
    bad = base65536.encode(b'\x25') + base65536.encode(b'\x13')
    with pytest.raises(ValueError):
        base65536.decode(bad)


def test_hello_world():
    # https://github.com/ferno/base65536/blob/
    # 25d6ea5104a16c24787fa1d8b4af836ba8bb6214/test.js#L86
    encoded = base65536.encode(b'hello world')
    assert encoded == u'驨ꍬ啯𒁷ꍲᕤ'
    assert base65536.decode(encoded) == b'hello world'


def test_ascii():
    encoded = base65536.encode(b'hello')
    assert encoded == u'\u9a68\ua36c\u156f'
    assert base65536.decode(encoded) == b'hello'


def test_non_ascii():
    # Python base65536-1.0 had a bug with UTF-8 encoded non-ASCII string.
    encoded = base65536.encode(u'안녕'.encode('utf-8'))
    assert base65536.decode(encoded).decode('utf-8') == u'안녕'
