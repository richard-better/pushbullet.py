from __future__ import print_function

import mock
import time

from pushbullet import contact


class TestContacts(object):

    def setup_class(cls):
        cls.contact_email = "test.contact@example.com"
        contact_info = {"active": True, "created": time.time(), "modified": time.time(), "name": "test contact", 
                        "status": "user", "email": cls.contact_email, "email_normalized": "testcontact@example.com"}
        cls.account = mock.Mock(return_value=True)
        cls.contact = contact.Contact(cls.account, contact_info)

    def test_encoding_support(self):
        # We're not actually intersted in the output, just that it doesn't
        # cause any errors.
        print(self.contact)

    def test_push(self):
        data = {"title": "test title"}
        self.contact._push(data)
        pushed_data = {"title": "test title", "email": self.contact_email}
        self.account._push.assert_called_with(pushed_data)
