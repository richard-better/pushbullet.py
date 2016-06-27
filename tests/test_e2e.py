import os

import pytest
import pushbullet
from binascii import a2b_base64

API_KEY = os.environ["PUSHBULLET_API_KEY"]

def test_decryption():
    pb = pushbullet.Pushbullet(API_KEY, encryption_password="hunter2")
    pb._encryption_key = a2b_base64("1sW28zp7CWv5TtGjlQpDHHG4Cbr9v36fG5o4f74LsKg=")

    test_data = "MSfJxxY5YdjttlfUkCaKA57qU9SuCN8+ZhYg/xieI+lDnQ=="
    decrypted = pb._decrypt_data(test_data)

    assert decrypted == "meow!"
