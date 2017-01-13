from __future__ import print_function

import mock
import time

from pushbullet import chat


class TestChats(object):

    def setup_class(self):
        self.contact_email = "test.chat@example.com"
        chat_info = {
            "active": True, "created": time.time(), "modified": time.time(),
            "with": {
                "name": "test chat",
                "status": "user", "email": self.contact_email,
                "email_normalized": "testcontact@example.com"}}

        self.account = mock.Mock(return_value=True)
        self.chat = chat.Chat(self.account, chat_info)

    def test_encoding_support(self):
        # We're not actually intersted in the output, just that it doesn't
        # cause any errors.
        print(self.chat)

    def test_push(self):
        data = {"title": "test title", "muted": True}
        self.chat._push(data)
        pushed_data = {"title": "test title", "email": self.contact_email, "muted": True}
        self.account._push.assert_called_with(pushed_data)
