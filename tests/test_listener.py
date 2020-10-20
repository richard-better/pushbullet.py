from pushbullet import PushBullet, Listener

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from .helpers import mock_refresh


@patch.object(PushBullet, "refresh", mock_refresh)
def test_listener_init():
    pb = PushBullet("apikey")

    listener = Listener(pb)

    listener.close()
