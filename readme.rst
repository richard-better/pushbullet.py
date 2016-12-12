pushbullet.py
=============

.. image:: https://img.shields.io/travis/randomchars/pushbullet.py.svg?style=flat-square
    :target: https://travis-ci.org/randomchars/pushbullet.py

.. image:: https://img.shields.io/coveralls/randomchars/pushbullet.py.svg?style=flat-square
    :target: https://coveralls.io/r/randomchars/pushbullet.py

.. image:: https://img.shields.io/pypi/dm/pushbullet.py.svg?style=flat-square
    :target: https://pypi.python.org/pypi?name=pushbullet.py&:action=display

.. image:: https://img.shields.io/pypi/v/pushbullet.py.svg?style=flat-square
    :target: https://pypi.python.org/pypi?name=pushbullet.py&:action=display

.. image:: https://img.shields.io/pypi/l/pushbullet.py.svg

This is a python library for the wonderful
`Pushbullet <https://www.pushbullet.com>`__ service. It allows you to
send push notifications to
`Android <https://play.google.com/store/apps/details?id=com.pushbullet.android>`__
and `iOS <https://itunes.apple.com/us/app/pushbullet/id810352052>`__
devices.

In order to use the API you need an API key that can be obtained
`here <https://www.pushbullet.com/account>`__. This is user specific and
is used instead of passwords.

Installation
------------

The easiest way is to just open your favorite terminal and type

::

    pip install pushbullet.py

Alternatively you can clone this repo and install it with

::

    python setup.py install

Requirements
------------

-  The wonderful requests library.
-  The magical python-magic library.

Usage
-----

Authentication
~~~~~~~~~~~~~~

.. code:: python

    from pushbullet import Pushbullet

    pb = Pushbullet(api_key)

If your key is invalid (that is, the Pushbullet API returns a ``401``), an ``InvalidKeyError`` is raised.

Using a proxy
^^^^^^^^^^^^^
When specified, all requests to the API will be made through the proxy. Note that the use of SOCKS proxies
requires the ``requests[socks]`` package (``pip install requests[socks]`` to install), however HTTP proxies (w/ Basic Auth) work fine without the ``requests[socks]`` package. 

.. code:: python

    from pushbullet import Pushbullet

    pb = Pushbullet(api_key, proxy={"https": "https://user:pass@10.10.1.10:3128/"})

Note that only HTTPS proxies work with Pushbullet.

Pushing things
~~~~~~~~~~~~~~

Pushing a text note
^^^^^^^^^^^^^^^^^^^

.. code:: python

    push = pb.push_note("This is the title", "This is the body")

``push`` is a dictionary containing the data returned by the Pushbullet API.

Pushing an address
^^^^^^^^^^^^^^^^^^

.. code:: python

    address = " 25 E 85th St, 10028 New York, NY"
    push = pb.push_address("home", address)

Pushing a list
^^^^^^^^^^^^^^

.. code:: python

    to_buy = ["milk", "bread", "cider"]
    push = pb.push_list("Shopping list", to_buy)

Pushing a link
^^^^^^^^^^^^^^

.. code:: python

    push = pb.push_link("Cool site", "https://github.com")

Pushing a file
^^^^^^^^^^^^^^

Pushing files is a two part process. First you need to upload the file, and after that you can push it like you would anything else.

.. code:: python

    with open("my_cool_picture.jpg", "rb") as pic:
        file_data = pb.upload_file(pic, "picture.jpg")

    push = pb.push_file(**file_data)

``upload_file`` returns a dictionary containing  ``file_type``, ``file_url`` and ``file_name`` keys. These are the same parameters that ``push_file`` take.


The advantage of this is that if you already have a file uploaded somewhere, you can use that instead of uploading again. For example:


.. code:: python

    push = pb.push_file(file_url="https://i.imgur.com/IAYZ20i.jpg", file_name="cat.jpg", file_type="image/jpeg")

Working with pushes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also view all previous pushes:

.. code:: python

    pushes = pb.get_pushes()

Pushes is a list containing dictionaries that have push data. You can use this data to dismiss notifications or delete pushes.

.. code:: python

    latest = pushes[0]

    # We already read it, so let's dismiss it
    pb.dismiss_push(latest.get("iden"))

    # Now delete it
    pb.delete_push(latest.get("iden"))

Both of these raise ``PushbulletError`` if there's an error.

You can also delete all of your pushes:

.. code:: python

    pushes = pb.delete_pushes()

Pushing to specific devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far all our pushes went to all connected devices, but there's a way to limit that.

First we need to get hold of some devices.

.. code:: python

    # Get all devices that the current user has access to.
    print(pb.devices)
    # [Device('Motorola Moto G'), Device('N7'), Device('Chrome')]

    # Select a device from the array using indexing
    motog = pb.devices[0]

    # Or retrieve a device by its name. Note that an InvalidKeyError is raised if the name does not exist
    motog = pb.get_device('Motorola Moto G')

Now we can use the device objects like we did with `pb`:

.. code:: python

    push = motog.push_note("Hello world!", "We're using the api.")

Alternatively we can pass the device to push methods:

.. code:: python

    push = pb.push_note("Hello world!", "We're using the api.", device=motog)

Creating new devices
^^^^^^^^^^^^^^^^^^^^

Creating a new device is easy too, you only need to specify a name for it.
Though you can also specify manufacturer, model and icon too.

.. code:: python

    listener = pb.new_device("Listener")
    motog = pb.new_device("MotoG", manufacturer="Motorola", model="G", icon="android")


Now you can use it like any other device.

Editing devices
^^^^^^^^^^^^^^^

You can change the nickname, the manufacturer, model and icon of the device:

.. code:: python

    listener = pb.edit_device(listener, manufacturer="Python", model="3.4.1", icon="system")
    motog = pb.edit_device(motog, nickname="My MotoG")


Deleting devices
^^^^^^^^^^^^^^^^

Of course, you can also delete devices, even those not added by you.

.. code:: python

    pb.remove_device(listener)

A ``PushbulletError`` is raised on error.

Channels
~~~~~~~~~~~~

You can also send pushes to channels. First, create a channel on the Pushbullet
website (also make sure to subscribe to that channel). All channels which
belong to the current user can be retrieved as follows:

.. code:: python

    # Get all channels created by the current user
    print(pb.channels)
    # [Channel('My Channel' 'channel_identifier')]

    my_channel = pb.channels[0]

    # Or retrieve a channel by its channel_tag. Note that an InvalidKeyError is raised if the channel_tag does not exist
    my_channel = pb.get_channel('My Channel')

Then you can send a push to all subscribers of this channel like so:

.. code:: python

    push = my_channel.push_note("Hello Channel!", "Hello My Channel")

Alternatively we can pass the channel to push methods:

.. code:: python

    push = pb.push_note("Hello Channel!", "Hello My Channel.", channel=my_channel)

Note that you can only push to channels which have been created by the current
user.


Contacts
~~~~~~~~~~~~

Contacts, which are known as "Chats" in Pushbullet's terminilogy, work just like devices:

.. code:: python

    # Get all contacts the user has
    print(pb.chats)
    # [Chat('Peter' <peter@gmail.com>), Chat('Sophie' <sophie@gmail.com>)]

    sophie = pb.chats[1]

Now we can use the chat objects like we did with `pb` or with the devices.:

.. code:: python

    push = sophie.push_note("Hello world!", "We're using the api.")

    # Or:
    push = pb.push_note("Hello world!", "We're using the api.", chat=sophie)


Adding new chats
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    bob = pb.new_chat("Bob", "bob@gmail.com")

Editing chats
^^^^^^^^^^^^^^^^^

You can change the name of any chat:

.. code:: python

    bob = pb.edit_chat(bob, "bobby")

Deleting chats
^^^^^^^^^^^^^^^^^^^

.. code:: python

    pb.remove_chat(bob)


Sending SMS messages
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    device = pb.devices[0]
    push = pb.push_sms(device, "+3612345678", "Wowza!")

End-To-End encryption
^^^^^^^^^^^^^^^^^^^^^

You activate end-to-end encryption by specifying your encryption key during the construction of the ``Pushbullet`` instance:

.. code:: python

    from pushbullet import Pushbullet

    pb = Pushbullet(api_key, "My secret password")

When specified, all sent SMS will be encrypted. Note that the use of end-to-end encryption requires the ``cryptography`` package. Since end-to-end encryption is only supported for SMS at the moment, the ``cryptography`` library is not specified as a dependency of ``pushbullet.py`` and should be installed seperatly by running ``pip install cryptography``.

Note that Pushbullet supportes End-To-End encryption only in SMS, notification mirroring and universal copy & paste. Your pushes will not be end-to-end encrypted.


Error checking
~~~~~~~~~~~~~~

If the Pushbullet api returns an error code a ``PushError`` an __
``InvalidKeyError`` or a ``PushbulletError`` is raised. The first __
two are both subclasses of ``PushbulletError``

The `pushbullet api documetation <https://www.pushbullet.com/api>`__
contains a list of possible status codes.

TODO
----

-  More tests. Write them all.

License
-------

MIT license. See LICENSE for full text.
