from itertools import chain

import requests

from .device import Device

class PushBullet:

    DEV_LIST_URL = "https://www.pushbullet.com/api/devices"

    def __init__(self, apikey):
        self._session = requests.Session()
        self._session.auth = (apikey, "")

        self._devices = []
        self._load_devices()

    def _load_devices(self):
        resp = self._session.get(self.DEV_LIST_URL)
        resp_dict = resp.json()

        own_devices = resp_dict.get("devices", [])
        shared_devices = resp_dict.get("shared_devices", [])

        devices = []
        for device_info in chain(own_devices, shared_devices):
            d = Device(self._session, device_info)
            devices.append(d)

        self._devices = devices

    def reload_devices(self):
        self._load_devices()

    def devices(self):
        return self._devices

    def get(self, query):
        if type(query) is int:
            device = list(filter(lambda x: x.dev_id == query, self._devices))
            if not device:
                return None
            else:
                return device[0]
