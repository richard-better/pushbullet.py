from itertools import chain

import requests
import sys
from .device import Device

if sys.version_info >= (3, 0, 0):
    integer_type = (int,)
else:
    integer_type = (int, long)


class PushBullet(object):

    DEV_LIST_URL = "https://api.pushbullet.com/api/devices"

    def __init__(self, api_key):
        self.api_key = api_key

        self._devices = []
        self._load_devices()

    def _load_devices(self):
        resp = requests.get(self.DEV_LIST_URL, auth=(self.api_key, ""))
        resp_dict = resp.json()

        own_devices = resp_dict.get("devices", [])
        shared_devices = resp_dict.get("shared_devices", [])

        devices = []
        for device_info in chain(own_devices, shared_devices):
            d = Device(self.api_key, device_info["id"], device_info)
            devices.append(d)

        self._devices = devices

    def reload_devices(self):
        self._load_devices()

    @property
    def devices(self):
        return self._devices

    def get(self, query):
        if isinstance(query, integer_type):
            device = list(filter(lambda x: x.device_id == query, self._devices))
            if not device:
                return None
            else:
                return device[0]

    def __getitem__(self, device_id):
        if not isinstance(device_id, integer_type):
            raise TypeError("device_id must be an integer")
        else:
            return self.get(device_id)
