from pushbullet import PushBullet
import pytest

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from .helpers import mock_refresh

from pushbullet.errors import InvalidKeyError, PushbulletError


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_data_ok():
    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.get.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    pb._get_data("url")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_data_rate_limited():
    mock_response = Mock()
    mock_response.status_code = 429

    session = Mock()
    session.get.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb._get_data("url")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_data_invalid_key():
    mock_response = Mock()
    mock_response.status_code = 401

    session = Mock()
    session.get.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(InvalidKeyError):
        pb._get_data("url")


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_data_other_error():
    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.get.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb._get_data("url")
