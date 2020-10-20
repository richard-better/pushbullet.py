import pytest
from pushbullet import PushBullet

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from .helpers import mock_refresh

from pushbullet.errors import PushbulletError
import json
from pushbullet.device import Device
from pushbullet.chat import Chat
from pushbullet.channel import Channel


@patch.object(PushBullet, "refresh", mock_refresh)
def test_new_device_ok():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"iden": "123"}

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    assert len(pb.devices) == 0

    pb.new_device("superphone", model="super")
    assert len(pb.devices) == 1
    assert session.post.called_once_with(
        pb.DEVICES_URL,
        json.dumps({"nickname": "superphone", "icon": "system", "model": "super"}),
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test_new_device_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.new_device("superphone", model="super")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_edit_device_ok():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"iden": "123", "nickname": "new name"}

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.devices = [Device(pb, {"iden": "123"})]

    pb.edit_device(pb.devices[0], nickname="new name")

    assert len(pb.devices) == 1
    assert pb.devices[0].nickname == "new name"


@patch.object(PushBullet, "refresh", mock_refresh)
def test_edit_device_error():
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"iden": "123", "nickname": "new name"}

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.devices = [Device(pb, {"iden": "123"})]

    with pytest.raises(PushbulletError):
        pb.edit_device(pb.devices[0], nickname="new name")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_remove_device_ok():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.devices = [Device(pb, {"iden": "123"})]

    pb.remove_device(pb.devices[0])

    assert len(pb.devices) == 0


@patch.object(PushBullet, "refresh", mock_refresh)
def test_remove_device_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.devices = [Device(pb, {"iden": "123"})]

    with pytest.raises(PushbulletError):
        pb.remove_device(pb.devices[0])

    assert len(pb.devices) == 1


@patch.object(PushBullet, "refresh", mock_refresh)
def test_new_chat_ok():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"iden": "123", "with": {}}

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    assert len(pb.chats) == 0

    pb.new_chat("The best chat ever", "partner@example.com")

    assert session.post.called_once_with(
        pb.CHATS_URL,
        json.dumps({"name": "The best chat ever", "email": "partner@example.com"}),
    )

    assert len(pb.chats) == 1


@patch.object(PushBullet, "refresh", mock_refresh)
def test_new_chat_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.new_chat("The best chat ever", "partner@example.com")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_edit_chat_ok():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "iden": "123",
        "with": {"name": "New chat name"},
        "muted": True,
    }

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.chats = [Chat(pb, {"iden": "123", "with": {"name": "Chat name"}})]

    pb.edit_chat(pb.chats[0], "new name", muted=True)

    assert len(pb.chats) == 1
    assert pb.chats[0].name == "New chat name"


@patch.object(PushBullet, "refresh", mock_refresh)
def test_edit_chat_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.chats = [Chat(pb, {"iden": "123", "with": {"name": "Chat name"}})]

    with pytest.raises(PushbulletError):
        pb.edit_chat(pb.chats[0], "new name")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_remove_chat_ok():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.chats = [Chat(pb, {"iden": "123", "with": {"name": "Chat name"}})]

    pb.remove_chat(pb.chats[0])

    assert len(pb.chats) == 0


@patch.object(PushBullet, "refresh", mock_refresh)
def test_remove_chat_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.chats = [Chat(pb, {"iden": "123", "with": {"name": "Chat name"}})]

    with pytest.raises(PushbulletError):
        pb.remove_chat(pb.chats[0])

    assert len(pb.chats) == 1


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_device():
    pb = PushBullet("apikey")

    pb.devices = [
        Device(pb, {"iden": "1", "nickname": "device1"}),
        Device(pb, {"iden": "2", "nickname": "device2"}),
        Device(pb, {"iden": "3", "nickname": "device3"}),
        Device(pb, {"iden": "4", "nickname": "device4"}),
        Device(pb, {"iden": "5", "nickname": "device5"}),
        Device(pb, {"iden": "6", "nickname": "device6"}),
    ]

    device = pb.get_device("device4")

    assert device.nickname == "device4"
    assert device.device_iden == "4"


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_device_not_found():
    pb = PushBullet("apikey")

    pb.devices = [
        Device(pb, {"iden": "1", "nickname": "device1"}),
        Device(pb, {"iden": "2", "nickname": "device2"}),
        Device(pb, {"iden": "3", "nickname": "device3"}),
        Device(pb, {"iden": "4", "nickname": "device4"}),
        Device(pb, {"iden": "5", "nickname": "device5"}),
        Device(pb, {"iden": "6", "nickname": "device6"}),
    ]

    with pytest.raises(PushbulletError):
        pb.get_device("device10")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_channel():
    pb = PushBullet("apikey")

    pb.channels = [
        Channel(pb, {"tag": "1", "name": "channel1"}),
        Channel(pb, {"tag": "2", "name": "channel2"}),
        Channel(pb, {"tag": "3", "name": "channel3"}),
        Channel(pb, {"tag": "4", "name": "channel4"}),
        Channel(pb, {"tag": "5", "name": "channel5"}),
        Channel(pb, {"tag": "6", "name": "channel6"}),
    ]

    channel = pb.get_channel("4")

    assert channel.channel_tag == "4"
    assert channel.name == "channel4"


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_channel_not_found():
    pb = PushBullet("apikey")

    pb.channels = [
        Channel(pb, {"tag": "1", "name": "channel1"}),
        Channel(pb, {"tag": "2", "name": "channel2"}),
        Channel(pb, {"tag": "3", "name": "channel3"}),
        Channel(pb, {"tag": "4", "name": "channel4"}),
        Channel(pb, {"tag": "5", "name": "channel5"}),
        Channel(pb, {"tag": "6", "name": "channel6"}),
    ]

    with pytest.raises(PushbulletError):
        pb.get_channel("channel10")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_delete_pushes():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.delete_pushes()

    session.delete.assert_called_once_with(pb.PUSH_URL)


@patch.object(PushBullet, "refresh", mock_refresh)
def test_delete_pushes_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.delete_pushes()

    session.delete.assert_called_once_with(pb.PUSH_URL)


@patch.object(PushBullet, "refresh", mock_refresh)
def test_delete_push():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.delete_push("123")

    session.delete.assert_called_once_with(pb.PUSH_URL + "/123")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_delete_push_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.delete.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.delete_push("123")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_dismiss_push():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb.dismiss_push("123")

    session.post.assert_called_once_with(
        pb.PUSH_URL + "/123", data=json.dumps({"dismissed": True})
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test_dismiss_push_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.dismiss_push("123")
