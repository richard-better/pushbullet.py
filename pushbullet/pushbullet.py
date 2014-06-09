from itertools import chain

import requests
import sys
from .device import Device

if sys.version_info >= (3, 0, 0):
    integer_type = (int,)
else:
    integer_type = (int, long)


class PushBullet(object):

    DEVICES_ENDPOINT = "https://api.pushbullet.com/v2/devices"

    def __init__(self, api_key):
        self.api_key = api_key

        self._load_devices()

    def _load_devices(self):
        self.devices = []

        resp = requests.get(self.DEVICES_ENDPOINT, auth=(self.api_key, ""))
        resp_dict = resp.json()

        device_list = resp_dict.get("devices", [])

        for device_info in device_list:
            d = Device(self.api_key, device_info)
            self.devices.append(d)

    def refresh(self):
        self._load_devices()
