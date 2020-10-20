from pushbullet import PushBullet
import pytest

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from .helpers import mock_refresh
import json
from pushbullet.errors import PushError, PushbulletError


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_push")
def test_push_note_no_recipents(pb_push, pb_refresh):

    pb = PushBullet("apikey")

    pb.push_note("test_note title", "test_note body")

    pb_push.assert_called_with(
        {
            "type": "note",
            "title": "test_note title",
            "body": "test_note body",
        }
    )


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_push")
def test_push_note(pb_push, pb_refresh):
    device = Mock()
    device.device_iden = "123"

    pb = PushBullet("apikey")

    pb.push_note("test_note title", "test_note body", device=device)

    pb_push.assert_called_with(
        {
            "type": "note",
            "title": "test_note title",
            "body": "test_note body",
            "device_iden": "123",
        }
    )


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_push")
def test_push_link(pb_push, pb_refresh):
    pb = PushBullet("apikey")

    pb.push_link(
        "test_note title",
        "https://google.com",
        "test_note body",
        email="test@example.com",
    )

    pb_push.assert_called_with(
        {
            "type": "link",
            "title": "test_note title",
            "body": "test_note body",
            "url": "https://google.com",
            "email": "test@example.com",
        }
    )


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_push")
def test_push_file_no_body_with_title(pb_push, pb_refresh):
    chat = Mock()
    chat.email = "test@example.com"

    pb = PushBullet("apikey")

    pb.push_file(
        "file_name.png",
        "file_url",
        "image/png",
        title="test image",
        chat=chat,
    )

    pb_push.assert_called_with(
        {
            "file_type": "image/png",
            "file_url": "file_url",
            "file_name": "file_name.png",
            "type": "file",
            "title": "test image",
            "email": "test@example.com",
        }
    )


@patch.object(PushBullet, "refresh")
@patch.object(PushBullet, "_push")
def test_push_file_no_title_with_body(pb_push, pb_refresh):
    channel = Mock()
    channel.channel_tag = "tag1"

    pb = PushBullet("apikey")

    pb.push_file(
        "file_name.png",
        "file_url",
        "image/png",
        body="test image body",
        channel=channel,
    )

    pb_push.assert_called_with(
        {
            "file_type": "image/png",
            "file_url": "file_url",
            "file_name": "file_name.png",
            "type": "file",
            "body": "test image body",
            "channel_tag": "tag1",
        }
    )


@patch.object(PushBullet, "refresh")
@patch("pushbullet.pushbullet.requests")
def test_upload_file(requests, pb_refresh):
    first_response = Mock()
    first_response.status_code = 200
    first_response.json.return_value = {
        "data": "upload_data",
        "file_url": "imageurl",
        "upload_url": "http://uploadhere.google.com",
    }

    second_response = Mock()
    second_response.status_code = 200

    session = Mock()
    session.post.return_value = first_response

    requests.post.return_value = second_response
    requests.codes.ok = 200

    pb = PushBullet("apikey")
    pb._session = session

    with open("tests/test.png", "rb") as test_file:
        response = pb.upload_file(test_file, "test.png")

        assert response == {
            "file_type": "image/png",
            "file_url": "imageurl",
            "file_name": "test.png",
        }

        session.post.assert_called_once_with(
            pb.UPLOAD_REQUEST_URL,
            data=json.dumps({"file_name": "test.png", "file_type": "image/png"}),
        )

        requests.post.assert_called_once_with(
            "http://uploadhere.google.com",
            data="upload_data",
            files={"file": test_file},
        )


@patch.object(PushBullet, "refresh")
@patch("pushbullet.pushbullet.requests")
def test_upload_file_request_fails(requests, pb_refresh):
    first_response = Mock()
    first_response.status_code = 400
    first_response.json.return_value = {
        "data": "upload_data",
        "file_url": "imageurl",
        "upload_url": "http://uploadhere.google.com",
    }

    second_response = Mock()
    second_response.status_code = 200

    session = Mock()
    session.post.return_value = first_response

    requests.post.return_value = second_response
    requests.codes.ok = 200

    pb = PushBullet("apikey")
    pb._session = session

    with open("tests/test.png", "rb") as test_file:

        with pytest.raises(PushbulletError):
            pb.upload_file(test_file, "test.png", "image/png")

    requests.post.assert_not_called()


@patch.object(PushBullet, "refresh", mock_refresh)
@patch.object(PushBullet, "_encrypt_data")
def test_push_sms_encrypted_ok(pb_encrypt):
    device = Mock()
    device.device_iden = "123"

    mock_response = Mock()
    mock_response.status_code = 200

    session = Mock()
    session.post.return_value = mock_response

    pb_encrypt.return_value = "encrypted text"

    pb = PushBullet("apikey")
    pb._session = session
    pb._encryption_key = "123"

    # When
    pb.push_sms(device, "+123456789", "This is an example text")

    session.post.assert_called_once_with(
        pb.EPHEMERALS_URL,
        data=json.dumps(
            {
                "type": "push",
                "push": {"ciphertext": "encrypted text", "encrypted": True},
            }
        ),
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test_push_sms_plaintext_failure():
    device = Mock()
    device.device_iden = "123"

    mock_response = Mock()
    mock_response.status_code = 500

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushError):
        pb.push_sms(device, "+123456789", "This is an example text")

    session.post.assert_called_once_with(
        pb.EPHEMERALS_URL,
        data=json.dumps(
            {
                "type": "push",
                "push": {
                    "type": "messaging_extension_reply",
                    "package_name": "com.pushbullet.android",
                    "source_user_iden": "123",
                    "target_device_iden": "123",
                    "conversation_iden": "+123456789",
                    "message": "This is an example text",
                },
            }
        ),
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test__push_ok():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"X-Ratelimit-Remaining": "1000"}
    mock_response.json.return_value = {}

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    server_response = pb._push({"key": "value"})

    session.post.assert_called_once_with(
        pb.PUSH_URL,
        data=json.dumps({"key": "value"}),
    )

    assert server_response == {
        "rate_limit": {
            "remaining": "1000",
            "limit": None,
            "reset": None,
        }
    }


@patch.object(PushBullet, "refresh", mock_refresh)
def test__push_fail():
    mock_response = Mock()
    mock_response.status_code = 400

    session = Mock()
    session.post.return_value = mock_response

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushError):
        pb._push({"key": "value"})

    session.post.assert_called_once_with(
        pb.PUSH_URL,
        data=json.dumps({"key": "value"}),
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_pushes_error():
    response1 = Mock()
    response1.status_code = 400
    response1.json.return_value = {"pushes": []}

    session = Mock()
    session.get.side_effect = [response1]

    pb = PushBullet("apikey")
    pb._session = session

    with pytest.raises(PushbulletError):
        pb.get_pushes()


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_pushes_no_cursor():
    response1 = Mock()
    response1.status_code = 200
    response1.json.return_value = {"pushes": []}

    session = Mock()
    session.get.side_effect = [response1]

    pb = PushBullet("apikey")
    pb._session = session

    pushes = pb.get_pushes(filter_inactive=False)

    assert len(pushes) == 0
    session.get.assert_called_once_with(
        pb.PUSH_URL, params={"modified_after": None, "limit": None, "active": False}
    )


@patch.object(PushBullet, "refresh", mock_refresh)
def test_get_pushes_no_cursor():
    response1 = Mock()
    response1.status_code = 200
    response1.json.return_value = {"pushes": ["push1", "push2"], "cursor": "cursor1"}

    response2 = Mock()
    response2.status_code = 200
    response2.json.return_value = {"pushes": ["push3"]}

    session = Mock()
    session.get.side_effect = [response1, response2]

    pb = PushBullet("apikey")
    pb._session = session

    pushes = pb.get_pushes(filter_inactive=False)

    assert len(pushes) == 3

    assert session.get.call_count == 2
