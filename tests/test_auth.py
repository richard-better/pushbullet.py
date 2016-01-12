import os

import pytest
import pushbullet

API_KEY = os.environ["PUSHBULLET_API_KEY"]

def test_auth_fail():
    with pytest.raises(pushbullet.InvalidKeyError) as exinfo:
        pb = pushbullet.Pushbullet("faultykey")


def test_auth_success():
    pb = pushbullet.Pushbullet(API_KEY)
    assert pb.user_info["name"] == os.environ.get("PUSHBULLET_NAME", "Pushbullet Tester")
