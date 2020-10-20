from __future__ import print_function

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import time

from pushbullet import device


class TestDevices(object):
    def setup_class(self):
        self.device_iden = "test_iden"
        self.device_info = {
            "active": True,
            "iden": self.device_iden,
            "created": time.time(),
            "modified": time.time(),
            "icon": "system",
            "generated_nickname": False,
            "nickname": "test dev",
            "manufacturer": "test c",
            "model": "test m",
            "has_sms": False,
        }
        self.account = Mock(return_value=True)
        self.device = device.Device(self.account, self.device_info)

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
        pushed_data = {
            "type": "note",
            "title": title,
            "body": body,
            "device_iden": self.device_iden,
        }
        self.account._push.assert_called_with(pushed_data)

    def test_push_link(self):
        title = "test title"
        url = "http://test.url"
        body = "test body"
        self.device.push_link(title, url, body)
        pushed_data = {
            "type": "link",
            "title": title,
            "url": url,
            "body": body,
            "device_iden": self.device_iden,
        }
        self.account._push.assert_called_with(pushed_data)

    def test_push_file(self):
        file_name = "test_file.name"
        file_url = "http://file.url"
        file_type = "test/type"
        body = "test body"
        title = "test title"
        self.device.push_file(file_name, file_url, file_type, body=body, title=title)
        self.account.push_file.assert_called_with(
            file_name, file_url, file_type, title=title, body=body, device=self.device
        )

    def test_push(self):
        data = {"title": "test title"}
        self.device._push(data)
        pushed_data = {"title": "test title", "device_iden": self.device_iden}
        self.account._push.assert_called_with(pushed_data)

    def test_no_icon(self):
        del self.device_info["icon"]

        new_device = device.Device(self.account, self.device_info)

        assert new_device.icon == "system"
