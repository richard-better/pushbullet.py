from __future__ import print_function

import os

import pushbullet

API_KEY = os.environ["PUSHBULLET_API_KEY"]

class TestContacts(object):

    @classmethod
    def setup_class(cls):
        cls.pb = pushbullet.Pushbullet(API_KEY)

    def test_encoding_support(self):
        for contact in self.pb.contacts:
            # We're not actually intersted in the output, just that it doesn't
            # cause any errors.
            print(contact)
