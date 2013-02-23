import json

class Device:

	PUSH_URL = "https://www.pushbullet.com/api/pushes"

	def __init__(self, session, device_info):
		self._session = session
		self.dev_id = device_info.get("id")
		self.owner = device_info.get("owner_name", None)

		extras = device_info["extras"]
		self.model = extras.get("model")
		self.manufacturer = extras.get("manufacturer")
		self.android_version = extras.get("android_version")
		self.sdk_version = extras.get("sdk_version")
		self.app_version = extras.get("app_version")

		self._fullname = "{} {} {}".format(self.manufacturer,
										   self.model, self.android_version)
		
		nickname = extras.get("nickname")
		self.name = nickname or self._fullname

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

	def push_file(self, file):
		data = {"type": "file"}
		files = {"file": file}
		return self._push(data, files=files)

	def push_link(self, title, url):
		data = {"type": "link", "title": title, "url": url}
		return self._push(data, headers=self._json_header)

	def _push(self, data, headers={}, files = {}):
		data["device_id"] = self.dev_id
		if not files:
			data = json.dumps(data)
		return self._session.post(self.PUSH_URL, data=data, headers=headers, files=files)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		owner_info = ", 'owner': '%s '}" % (self.owner) if self.owner else "}"
		return "{'dev_id': %s, 'name': '%s'" % (self.dev_id, self.name) + owner_info
