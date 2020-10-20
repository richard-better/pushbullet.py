from __future__ import print_function

import mimetypes

from pushbullet import filetype


class TestFiletypes(object):
    def test_magic(self):

        filename = "tests/test.png"
        with open(filename, "rb") as pic:
            output = filetype.get_file_type(pic, filename)
            assert output == ("image/png")

    def test_mimetypes(self):
        del filetype.magic_from_buffer
        filetype.mimetypes = mimetypes

        filename = "tests/test.png"
        with open(filename, "rb") as pic:
            output = filetype.get_file_type(pic, filename)
            assert output == "image/png"
