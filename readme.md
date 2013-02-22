# PushBullet.py

This is a python library for the wonderful [PushBullet](https://www.pushbullet.com) service.
It allows you to send push notifications to Android devices.  

In order to use the API you need an API key that can be obtained [here](https://www.pushbullet.com/settings). This is user specific and is used instead of passwords.

## Requirements

 - Python. Tested on 2.7 and 3.2
 - The wonderful requests library.

## Usage

The library is work in progress. More features will be added soon.

```Python
from pushbullet import PushBullet
pb = PushBullet("API_KEY")

# See what devices we controll
print(pb.devices())
[{'dev_id: '12435', 'name': ""}]
# Get a device by it's numeric id
nexus = pb.get(12345)
# Push a text note. The underlying request object is returned for all pushes.
note = nexus.push_note("Hello!", "Hello Nexus! Sent from python.")
print(note.status_code)
200
# Push a list
l = nexus.push_list("Shopping list", ["Milk", Eggs", "Bacon"])
```

# License

MIT license. See LICENSE for full text.