from __future__ import print_function

import mock
import time

from pushbullet import device


class TestDevices(object):

    def setup_class(cls):
        cls.device_iden = "test_iden"
        device_info = {"active": True, "iden": cls.device_iden, "created": time.time(), "modified": time.time(),
                       "icon": "system", "generated_nickname": False, "nickname": "test dev", "manufacturer": "test c",
                       "model": "test m", "has_sms": False}
        cls.account = mock.Mock(return_value=True)
        cls.device = device.Device(cls.account, device_info)

    def test_encoding_support(self):
        # We're not actually intersted in the output, just that it doesn't
        # cause any errors.
        print(self.device)

    def test_repr(self):
        assert repr(self.device) == "Device('test dev')"

    def test_push_note(self):
        title = "test title"
        body = "test body"
        self.device.push_note(title, body)
        pushed_data = {"type": "note", "title": title, "body": body, "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)

    def test_push_address(self):
        name = "test name"
        address = "test address"
        self.device.push_address(name, address)
        pushed_data = {"type": "note", "title": name, "body": address, "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)

    def test_push_list(self):
        title = "test title"
        items = ["test item 1", "test item 2"]
        self.device.push_list(title, items)
        pushed_data = {"type": "note", "title": title, "body": ",".join(items), "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)

    def test_push_link(self):
        title = "test title"
        url = "http://test.url"
        body = "test body"
        self.device.push_link(title, url, body)
        pushed_data = {"type": "link", "title": title, "url": url, "body": body, "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)

    def test_push_file(self):
        file_name = "test_file.name"
        file_url = "http://file.url"
        file_type = "test/type"
        body = "test body"
        title = "test title"
        self.device.push_file(file_name, file_url, file_type, body=body, title=title)
        self.account.push_file.assert_called_with(file_name, file_url, file_type, title=title, body=body, device=self.device)

    def test_push(self):
        data = {"title": "test title"}
        self.device._push(data)
        pushed_data = {"title": "test title", "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)
