import json

import requests

class Device(object):

	PUSH_URL = "https://api.pushbullet.com/api/pushes"

	def __init__(self, api_key, device_id, device_info = None):
		self.api_key = api_key
		self.device_id = device_id

		device_info = device_info or {}

		self.owner = device_info.get("owner_name")

		extras = device_info.get("extras", {})
		self.model = extras.get("model")
		self.manufacturer = extras.get("manufacturer")
		self.android_version = extras.get("android_version")
		self.sdk_version = extras.get("sdk_version")
		self.app_version = extras.get("app_version")
		self.pushable = extras.get("pushable")
		self.active = extras.get("active")

		self._fullname = "{} {} {}".format(self.manufacturer,
										   self.model, self.android_version)

		self.nickname = extras.get("nickname")
		#self.name = self.nickname

		self._json_header = {'Content-Type': 'application/json'}

	def push_note(self, title, body):
		data = {"type": "note", "title": title, "body": body}
		return self._push(data, headers=self._json_header)

	def push_address(self, name, address):
		data = {"type": "address", "name": name, "address": address}
		return self._push(data, headers=self._json_header)

	def push_list(self, title, items):
		data = {"type": "list", "title": title, "items": items}
		return self._push(data, headers=self._json_header)

	def push_file(self, file, body):
		data = {"type": "file", "body": body}
		files = {"file": file}
		return self._push(data, files=files)

	def push_link(self, title, url, body):
		data = {"type": "link", "title": title, "url": url, "body": body}
		return self._push(data, headers=self._json_header)

	def _push(self, data, headers={}, files = {}):
		data["device_id"] = self.device_id
		if not files:
			data = json.dumps(data)
		headers.update({"User-Agent": "ifttt2pushbullet.herokuapp.com"})
		return requests.post(self.PUSH_URL, data=data, headers=headers,
							 files=files, auth=(self.api_key, ""))

	def __repr__(self):
		return "Device('{}', {})".format(self.api_key, self.device_id)
