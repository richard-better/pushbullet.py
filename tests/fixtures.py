import time

devices_list_response = {
    "devices": [
        {
            "active": True,
            "iden": "1",
            "created": time.time(),
            "modified": time.time(),
            "icon": "system",
            "generated_nickname": False,
            "nickname": "test dev",
            "manufacturer": "test c",
            "model": "test m",
            "has_sms": False,
        },
        {
            "active": False,
            "iden": "2",
            "created": time.time(),
            "modified": time.time(),
            "icon": "system",
            "generated_nickname": False,
            "nickname": "test dev",
            "manufacturer": "test c",
            "model": "test m",
            "has_sms": False,
        },
    ]
}


chats_list_response = {
    "chats": [
        {
            "active": True,
            "created": time.time(),
            "modified": time.time(),
            "with": {
                "name": "test chat",
                "status": "user",
                "email": "testcontact@example.com",
                "email_normalized": "testcontact@example.com",
            },
        },
        {
            "active": False,
            "created": time.time(),
            "modified": time.time(),
            "with": {
                "name": "test chat",
                "status": "user",
                "email": "testcontact@example.com",
                "email_normalized": "testcontact@example.com",
            },
        },
    ]
}

channels_list_response = {
    "channels": [
        {
            "iden": "test_iden",
            "name": "test channel",
            "created": time.time(),
            "modified": time.time(),
            "tag": "test_tag",
            "active": True,
        },
        {
            "iden": "test_iden2",
            "name": "test channel",
            "created": time.time(),
            "modified": time.time(),
            "tag": "test_tag",
            "active": False,
        },
    ]
}
