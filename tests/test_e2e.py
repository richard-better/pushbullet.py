import os
import json

import pytest
from pushbullet import PushBullet
from binascii import a2b_base64

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from .helpers import mock_refresh

API_KEY = os.environ["PUSHBULLET_API_KEY"]


def test_decryption():
    pb = PushBullet(API_KEY, encryption_password="hunter2")
    pb._encryption_key = a2b_base64("1sW28zp7CWv5TtGjlQpDHHG4Cbr9v36fG5o4f74LsKg=")

    test_data = "MSfJxxY5YdjttlfUkCaKA57qU9SuCN8+ZhYg/xieI+lDnQ=="
    decrypted = pb._decrypt_data(test_data)

    assert decrypted == "meow!"


@patch.object(PushBullet, "refresh", mock_refresh)
def test_encryption():
    pb = PushBullet("apikey", "hunter42")

    original = {"cat": "meow!"}
    encrypted = pb._encrypt_data(original)
    decrpyted = pb._decrypt_data(encrypted)

    assert original == json.loads(decrpyted)


@patch.object(PushBullet, "refresh", mock_refresh)
def test_encryption_invalid_version():
    pb = PushBullet("apikey", "hunter42")

    original = {"cat": "meow!"}
    encrypted = pb._encrypt_data(original)
    encrypted = "2" + encrypted[1:]

    with pytest.raises(Exception):
        pb._decrypt_data(encrypted)
