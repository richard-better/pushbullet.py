import os

import pytest
import pushbullet

API_KEY = os.environ["PUSHBULLET_API_KEY"]

def test_auth_fail():
    with pytest.raises(pushbullet.InvalidKeyError) as exinfo:
        pb = pushbullet.PushBullet("faultykey")


def test_auth_success():
    pb = pushbullet.PushBullet(API_KEY)
    assert pb.user_info["name"] == "Pushbullet Tester"
