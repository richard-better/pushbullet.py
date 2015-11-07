from __future__ import print_function

from pushbullet import filetype

class TestFiletypes(object):

    def test_mimetype(self):
        filename = 'tests/test.png'
        with open(filename, "rb") as pic:
            output = filetype._magic_get_file_type(pic, filename)
        assert output == 'image/png'  # With 3.4 will fail if output is b'image/png'
