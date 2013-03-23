# PushBullet.py

This is a python library for the wonderful [PushBullet](https://www.pushbullet.com) service.
It allows you to send push notifications to Android devices.  

In order to use the API you need an API key that can be obtained [here](https://www.pushbullet.com/settings). This is user specific and is used instead of passwords.

## Installation

The easiest way is to just open your favorite terminal and type
```
pip install pushbullet.py
```

Alternatively you can clone this repo and install it with

```
python setup.py install
```

## Requirements

 - Python. Tested on 2.7 and 3.2
 - The wonderful requests library.

## Usage


### Authentication

```python
from pushbullet import PushBullet


pb = PushBullet("API_KEY")

```

### Getting the devices

```python
# Get all devices that the current user has access to.
print(pb.devices())
# [{'dev_id: '12435', 'name': "Test Phone"}]

# Get a device by it's ID
phone = pb.get(12345)

# Reload the list of devices, in case a new one was added.
pb.reload_devices()
```

### Pushing things

#### Pushing a text note

```python
push = phone.push_note("This is the title", "This is the body".)
```

#### Pushing an address

```python
address = " 25 E 85th St, 10028 New York, NY"
push = phone.push_address("home", address)
```

#### Pushing a list

```python
to_buy = ["milk", "bread", "cider"]
push = phone.push_list("Shopping list", to_buy)
```

#### Pushing a link

```python
push = phone.push_link("Cool site", "https://github.com")
```

#### Pushing a file

```python
with open("my_cool_app.apk", "b") as apk:
	push = phone.push_(apk)
```

#### Error checking

All pushes return the underlying requests object that can be used to check the status of the operation

``` Python
print(push.status_code)
# 200
```

The [pushbullet api documetation](https://www.pushbullet.com/api) cobtains a list of possible status codes.

## TODO

 - Add better error handling

## License

MIT license. See LICENSE for full text.
