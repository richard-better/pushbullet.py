from __future__ import print_function
import sys

from pushbullet import filetype


class TestFiletypes(object):

    def test_mimetype(self):
        filename = 'tests/test.png'
        with open(filename, "rb") as pic:
            output = filetype._magic_get_file_type(pic, filename)
        if sys.version_info >= (3, 0):
            assert output == (b'image/png')
        else:
            assert output == ('image/png')

    def test_guess_file_type(self):
        import mimetypes
        filetype.mimetypes = mimetypes
        filename = 'tests/test.png'
        output = filetype._guess_file_type(None, filename)
        assert output == 'image/png'
