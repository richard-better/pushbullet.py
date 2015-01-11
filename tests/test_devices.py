from __future__ import print_function

import os

import pushbullet

API_KEY = os.environ["PUSHBULLET_API_KEY"]

class TestDevices(object):

    @classmethod
    def setup_class(cls):
        cls.pb = pushbullet.PushBullet(API_KEY)

    def test_encoding_support(self):
        for device in self.pb.devices:
            # We're not actually intersted in the output, just that it doesn't
            # cause any errors.
            print(device)
