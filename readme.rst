PushBullet.py
=============

.. image:: https://img.shields.io/travis/randomchars/pushbullet.py.svg?style=flat-square
    :target: https://travis-ci.org/randomchars/pushbullet.py

.. image:: https://img.shields.io/coveralls/randomchars/pushbullet.py.svg?style=flat-square
    :target: https://coveralls.io/r/randomchars/pushbullet.py

.. image:: https://img.shields.io/pypi/dm/pushbullet.py.svg?style=flat-square
    :target https://pypi.python.org/pypi?name=pushbullet.py&:action=display

.. image:: https://img.shields.io/pypi/v/pushbullet.py.svg?style=flat-square
    :target https://pypi.python.org/pypi?name=pushbullet.py&:action=display

.. image:: https://img.shields.io/pypi/l/pushbullet.py.svg

This is a python library for the wonderful
`PushBullet <https://www.pushbullet.com>`__ service. It allows you to
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

    from pushbullet import PushBullet

    pb = PushBullet(api_key)

Pushing things
~~~~~~~~~~~~~~

Pushing a text note
^^^^^^^^^^^^^^^^^^^

.. code:: python

    success, push = pb.push_note("This is the title", "This is the body".)

Pushing an address
^^^^^^^^^^^^^^^^^^

.. code:: python

    address = " 25 E 85th St, 10028 New York, NY"
    success, push = pb.push_address("home", address)

Pushing a list
^^^^^^^^^^^^^^

.. code:: python

    to_buy = ["milk", "bread", "cider"]
    success, push = phone.push_list("Shopping list", to_buy)

Pushing a link
^^^^^^^^^^^^^^

.. code:: python

    success, push = phone.push_link("Cool site", "https://github.com")

Pushing a file
^^^^^^^^^^^^^^

Pushing files is a two part process. First you need to upload the file, and after that you can push it like you would anything else.

.. code:: python

    with open("my_cool_picture.jpg", "rb") as pic:
        success, file_data = pb.upload_file(pic, "picture.jpg")

    success, push = pb.push_file(**file_data)


The advantage of this is that if you already have a file uploaded somewhere, you can use that instead of uploading again. For example:


.. code:: python

    success, push = pb.push_file(file_url="https://i.imgur.com/IAYZ20i.jpg", file_name="cat.jpg", file_type="image/jpeg")

Working with pushes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also view all previous pushes:

.. code:: python

    success, pushes = pb.get_pushes()

Pushes is a list containg dictionaries that have push data. You can use this data to dismiss notifications or delete pushes.

.. code:: python

    latest = pushes[0]

    # We already read it, so let's dismiss it
    success, error_message = pb.dismiss_push(lates.get("iden"))

    # Now delete it
    success, error_message = pb.delete_push(lates.get("iden"))


Pushing to specific devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far all our pushes went to all connected devices, but there's a way to limit that.

First we need to get hold of some devices.

.. code:: python

    # Get all devices that the current user has access to.
    print(pb.devices)
    # [Device('Motorola Moto G'), Device('N7'), Device('Chrome')]

    motog = pb.devices[0]

Now we can use the device objects like we did with `pb`:

.. code:: python

    success, push = motog.push_note("Hello world!", "We're using the api.")

Alternatively we can pass the device to push methods:

.. code:: python

    success, push = pb.push_note("Hello world!", "We're using the api.", device=motog)

Creating new devices
^^^^^^^^^^^^^^^^^^^^

Creating a new device is easy too, you only need to specify a name for it.

.. code:: python

    success, listener = pb.new_device("Listener")

Now you can use it like any other device.

Editing devices
^^^^^^^^^^^^^^^

You can change the nickname, the manufacturer and the model of the device:

.. code:: python

    success, listener = pb.edit_device(listener, make="Python", model="3.4.1")
    success, motog = pb.edit_device(motog, nickname="My MotoG")


Deleting devices
^^^^^^^^^^^^^^^^

Of course, you can also delete devices, even those not added by you.

.. code:: python

    success, error_message = pb.remove_device(listener)


Channels
~~~~~~~~~~~~

You can also send pushes to channels. First, create a channel on the PushBullet
website (also make sure to subscribe to that channel). All channels which
belong to the current user can be retrieved as follows:

.. code:: python

    # Get all channels created by the current user
    print(pb.channels)
    # [Channel('My Channel' 'channel_identifier')]

    my_channel = pb.channels[0]

Then you can send a push to all subscribers of this channel like so:

.. code:: python

    success, push = my_channel.push_note("Hello Channel!", "Hello My Channel")

Note that you can only push to channels which have been created by the current
user.


Contacts
~~~~~~~~~~~~

Contacts work just like devices:

.. code:: python

    # Get all contacts the user has
    print(pb.contacts)
    # [Contact('Peter' <peter@gmail.com>), Contact('Sophie' <sophie@gmail.com>]

    sophie = pb.contacs[1]

Now we can use the contact objects like we did with `pb` or with the devices.:

.. code:: python

    success, push = sophie.push_note("Hello world!", "We're using the api.")

    # Or:
    success, push = pb.push_note("Hello world!", "We're using the api.", contact=sophie)


Adding new contacts
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    success, bob = pb.new_contact("Bob", "bob@gmail.com")

Editing contacts
^^^^^^^^^^^^^^^^^

You can change the name of any contact:

.. code:: python

    success, bob = pb.edit_contact(bob, "bobby")

Deleting contacts
^^^^^^^^^^^^^^^^^^^

.. code:: python

    success, error_message = pb.remove_contact(bob)


Error checking
~~~~~~~~~~~~~~

Most methods return a tuple containing a bool value indicating success or failure, and the response from the server.

.. code:: Python

    success, push = pb.push_note("Hello world!", "We're using the api.")


The `pushbullet api documetation <https://www.pushbullet.com/api>`__
contains a list of possible status codes.

TODO
----

-  Websocket support
-  Tests, tests, tests. Write them.

License
-------

MIT license. See LICENSE for full text.
