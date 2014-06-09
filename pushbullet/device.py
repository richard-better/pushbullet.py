import json

import requests

class Device(object):

	PUSH_URL = "https://api.pushbullet.com/v2/pushes"

	def __init__(self, api_key, device_info):
		self.api_key = api_key
		self.device_iden = device_info.get("iden")

		for attr in ("push_token", "app_version",
					 "android_sdk_version", "fingerprint",
					 "active", "nickname","manufacturer",
					 "kind","created", "modified",
					 "android_version", "model", "pushable"):
			setattr(self, attr, device_info.get(attr))

		self._json_header = {'Content-Type': 'application/json'}

	def push_note(self, title, body):
		data = {"type": "note", "title": title, "body": body}
		return self._push(data)

	def push_address(self, name, address):
		data = {"type": "address", "name": name, "address": address}
		return self._push(data)

	def push_list(self, title, items):
		data = {"type": "list", "title": title, "items": items}
		return self._push(data)

	def push_link(self, title, url, body=None):
		data = {"type": "link", "title": title, "url": url, "body": body}
		return self._push(data)

	def _push(self, data):
		data["device_iden"] = self.device_iden

		return requests.post(self.PUSH_URL, data=json.dumps(data),
							 headers=self._json_header,
							 auth=(self.api_key, ""))

	def __str__(self):
		return self.nickname or (self.manufacturer + " " + self.model)
