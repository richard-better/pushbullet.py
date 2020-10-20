from __future__ import unicode_literals

import warnings

from .helpers import use_appropriate_encoding


class Device(object):

    def __init__(self, account, device_info):
        self._account = account
        self.device_iden = device_info.get("iden")
        if not device_info.get("icon", None):
            device_info["icon"] = "system"
        for attr in ("push_token", "app_version", "fingerprint", "created", "modified",
                    "active", "nickname", "generated_nickname", "manufacturer", "icon",
                    "model", "has_sms", "key_fingerprint"):
            setattr(self, attr, device_info.get(attr))

    def push_note(self, title, body):
        data = {"type": "note", "title": title, "body": body}
        return self._push(data)

    def push_link(self, title, url, body=None):
        data = {"type": "link", "title": title, "url": url, "body": body}
        return self._push(data)

    def push_file(self, file_name, file_url, file_type, body=None, title=None):
        return self._account.push_file(file_name, file_url, file_type, body=body, title=title, device=self)

    def _push(self, data):
        data["device_iden"] = self.device_iden
        return self._account._push(data)

    @use_appropriate_encoding
    def __str__(self):
        return "Device('{0}')".format(self.nickname or "nameless (iden: {})".format(self.device_iden))

    def __repr__(self):
        return self.__str__()
