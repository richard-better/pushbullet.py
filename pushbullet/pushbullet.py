import requests
import json
from .device import Device

class PushBullet(object):

    DEVICES_URL = "https://api.pushbullet.com/v2/devices"
    PUSH_URL = "https://api.pushbullet.com/v2/pushes"


    def __init__(self, api_key):
        self.api_key = api_key
        self._json_header = {'Content-Type': 'application/json'}

        self._load_devices()

    def _load_devices(self):
        self.devices = []

        resp = requests.get(self.DEVICES_URL, auth=(self.api_key, ""))
        resp_dict = resp.json()

        device_list = resp_dict.get("devices", [])

        for device_info in device_list:
            d = Device(self.api_key, device_info)
            d._account = self
            self.devices.append(d)


    def push_note(self, title, body, device=None, email=None):
        data = {"type": "note", "title": title, "body": body}
        if device:
            data["device_iden"] = device.device_iden
        elif email:
            data["email"] = email


        return self._push(data)

    def push_address(self, name, address, device=None, email=None):
        data = {"type": "address", "name": name, "address": address}
        if device:
            data["device_iden"] = device.device_iden
        elif email:
            data["email"] = email

        return self._push(data)

    def push_list(self, title, items, device=None, email=None):
        data = {"type": "list", "title": title, "items": items}
        if device:
            data["device_iden"] = device.device_iden
        elif email:
            data["email"] = email

        return self._push(data)

    def push_link(self, title, url, body=None, device=None, email=None):
        data = {"type": "link", "title": title, "url": url, "body": body}

        if device:
            data["device_iden"] = device.device_iden
        elif email:
            data["email"] = email

        return self._push(data)


    def _push(self, data):
        return requests.post(self.PUSH_URL, data=json.dumps(data),
                             headers=self._json_header,
                             auth=(self.api_key, ""))

    def refresh(self):
        self._load_devices()
