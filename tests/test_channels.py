from __future__ import print_function

import mock
import time

from pushbullet import channel


class TestChannels(object):

    @classmethod
    def setup_class(cls):
        cls.channel_tag = "test_tag"
        channel_info = {'iden': "test_iden", 'name': 'test channel', 'created': time.time(), 'modified': time.time(), 'tag': cls.channel_tag, 'active': True}
        cls.account = mock.Mock(return_value=True)
        cls.channel = channel.Channel(cls.account, channel_info)

    def test_encoding_support(self):
        # We're not actually intersted in the output, just that it doesn't
        # cause any errors.
        print(self.channel)

    def test_repr(self):
        assert repr(self.channel) == "Channel(name: 'test channel' tag: '%s')" % self.channel_tag

    def test_push_note(self):
        title = "test title"
        body = "test body"
        self.channel.push_note(title, body)
        pushed_data = {"type": "note", "title": title, "body": body, "channel_tag": self.channel_tag}
        self.account._push.assert_called_with(pushed_data)

    def test_push_address(self):
        name = "test name"
        address = "test address"
        self.channel.push_address(name, address)
        pushed_data = {"type": "note", "title": name, "body": address, "channel_tag": self.channel_tag}
        self.account._push.assert_called_with(pushed_data)

    def test_push_list(self):
        title = "test title"
        items = ["test item 1", "test item 2"]
        self.channel.push_list(title, items)
        pushed_data = {"type": "note", "title": title, "body": ",".join(items), "channel_tag": self.channel_tag}
        self.account._push.assert_called_with(pushed_data)

    def test_push_link(self):
        title = "test title"
        url = "http://test.url"
        body = "test body"
        self.channel.push_link(title, url, body)
        pushed_data = {"type": "link", "title": title, "url": url, "body": body, "channel_tag": self.channel_tag}
        self.account._push.assert_called_with(pushed_data)

    def test_push_file(self):
        file_name = "test_file.name"
        file_url = "http://file.url"
        file_type = "test/type"
        body = "test body"
        title = "test title"
        self.channel.push_file(file_name, file_url, file_type, body=body, title=title)
        self.account.push_file.assert_called_with(file_name, file_url, file_type, body=body, title=title, channel=self.channel)

    def test_push(self):
        data = {"title": "test title"}
        self.channel._push(data)
        pushed_data = {"title": "test title", "channel_tag": self.channel_tag}
        self.account._push.assert_called_with(pushed_data)
