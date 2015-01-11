class PushBulletError(Exception):
    pass

class InvalidKeyError(PushBulletError):
    pass

class PushError(PushBulletError):
    pass
