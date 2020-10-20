import sys
import pytest
from requests import ConnectionError
from binascii import a2b_base64

from pushbullet import PushBullet
from pushbullet.errors import NoEncryptionModuleError

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from .helpers import mock_refresh

from .fixtures import devices_list_response, chats_list_response, channels_list_response


@patch.object(PushBullet, "refresh")
def test_proxy_is_applied(pb_refresh):
    proxy = {"https": "https://user:pass@10.10.1.10:3128/"}

    with patch("pushbullet.PushBullet.refresh"):
        pb = PushBullet("apikey", proxy=proxy)

    assert pb._session.proxies == proxy


@patch.object(PushBullet, "refresh")
def test_http_proxy_is_not_accepted(pb_refresh):
    proxy = {"http": "https://user:pass@10.10.1.10:3128/"}

    with pytest.raises(ConnectionError):
        PushBullet("apikey", proxy=proxy)

    pb_refresh.assert_not_called()


@patch.object(PushBullet, "refresh")
@patch.dict(sys.modules, {"cryptography.hazmat.primitives": None})
def test_crypto_not_found(pb_refresh):

    with pytest.raises(NoEncryptionModuleError):
        PushBullet("apikey", encryption_password="hunter2")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_crypto_found():

    pb = PushBullet("apikey", encryption_password="hunter2")

    assert pb._encryption_key == a2b_base64(
        "ZFKZG50hJs5DrGKWf8fBQ6CSLB1LtTNw+xwwT2ZBl9g="
    )


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_get_data", Mock(return_value=devices_list_response))
def test_load_devices(pb_refresh):
    pb = PushBullet("apikey")

    pb._load_devices()

    assert len(pb.devices) == 1


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_get_data", Mock(return_value=chats_list_response))
def test_load_chats(pb_refresh):
    pb = PushBullet("apikey")

    pb._load_chats()

    assert len(pb.chats) == 1


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_get_data", Mock(return_value=channels_list_response))
def test_load_channels(pb_refresh):
    pb = PushBullet("apikey")

    pb._load_channels()

    assert len(pb.channels) == 1
