import json

import requests
import magic

from .device import Device
from .contact import Contact

class PushBullet(object):

    DEVICES_URL = "https://api.pushbullet.com/v2/devices"
    CONTACTS_URL = "https://api.pushbullet.com/v2/contacts"
    PUSH_URL = "https://api.pushbullet.com/v2/pushes"
    UPLOAD_REQUEST_URL = "https://api.pushbullet.com/v2/upload-request"


    def __init__(self, api_key):
        self.api_key = api_key
        self._json_header = {'Content-Type': 'application/json'}

        self._session = requests.Session()
        self._session.auth = (self.api_key, "")
        self._session.headers.update(self._json_header)

        self.refresh()

    def _load_devices(self):
        self.devices = []

        resp = self._session.get(self.DEVICES_URL)
        resp_dict = resp.json()
        device_list = resp_dict.get("devices", [])

        for device_info in device_list:
            d = Device(self, device_info)
            self.devices.append(d)

    def _load_contacts(self):
        self.contacts = []

        resp = self._session.get(self.CONTACTS_URL)
        resp_dict = resp.json()
        contacts_list = resp_dict.get("contacts", [])

        for contact_info in contacts_list:
            c = Contact(self, contact_info)
            self.contacts.append(c)

    def new_device(self, nickname):
        data = {"nickname": nickname, "type": "stream"}
        r = self._session.post(self.DEVICES_URL, data=json.dumps(data))
        if r.status_code == requests.codes.ok:
            new_device = Device(self, r.json())
            self.devices.append(new_device)
            return True, new_device
        else:
            return False, None

    def edit_device(self, device, nickname=None, model=None, manufacturer=None):
        data = {"nickname": nickname}
        iden = device.device_iden
        r = self._session.post("{}/{}".format(self.DEVICES_URL, iden), data=json.dumps(data))
        if r.status_code == requests.codes.ok:
            new_device = Device(self, r.json())
            self.devices[self.devices.index(device)] = new_device
            return True, new_device
        else:
            return False, device

    def remove_device(self, device):
        iden = device.device_iden
        r = self._session.delete("{}/{}".format(self.DEVICES_URL, iden))
        if r.status_code == requests.codes.ok:
            self.devices.remove(device)
            return True, r.json()
        else:
            return False, r.json()

    def get_pushes(self, modified_after=None):
        data = {"modified_after": modified_after}
        r = self._session.get(self.PUSH_URL, params=data) 

        if r.status_code == requests.codes.ok:
            return True, r.json().get("pushes")
        else:
            return False, r.json()

    def dismiss_push(self, iden):
        data = {"dismissed": True}
        r = self._session.post("{}/{}".format(self.PUSH_URL, iden), data=json.dumps(data))
 
        if r.status_code == requests.codes.ok:
            return True, r.json()
        else:
            return False, r.json()  

    def delete_push(self, iden):
        r = self._session.delete("{}/{}".format(self.PUSH_URL, iden))
 
        if r.status_code == requests.codes.ok:
            return True, r.json()
        else:
            return False, r.json()

    def upload_file(self, f, file_name, file_type=None):
        if not file_type:
            file_type = magic.from_buffer(f.read(1024), mime=True)
            f.seek(0)
        
        data = {"file_name": file_name, "file_type": file_type}

        # Request url for file upload
        r = self._session.post(self.UPLOAD_REQUEST_URL, data=json.dumps(data))

        if r.status_code != requests.codes.ok:
            return False, r.json()
        
        upload_data = r.json().get("data")
        file_url = r.json().get("file_url")
        upload_url = r.json().get("upload_url")

        upload = requests.post(upload_url, data=upload_data, files={"file": f})

        return True, {"file_type": file_type, "file_url": file_url, "file_name": file_name}

    def push_file(self, file_name, file_url, file_type, body=None, device=None, email=None):
        data = {"type": "file", "file_type": file_type, "file_url": file_url, "file_name": file_name}
        if body:
            data["body"] = body

        if device:
            data["device_iden"] = device.device_iden
        elif email:
            data["email"] = email
    
        return self._push(data)
    
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
        r = self._session.post(self.PUSH_URL, data=json.dumps(data))

        if r.status_code == requests.codes.ok:
            return True, r.json()
        else:
            return False, r.json()

    def refresh(self):
        self._load_devices()
        self._load_contacts()
