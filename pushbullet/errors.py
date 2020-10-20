class PushbulletError(Exception):
    pass

class InvalidKeyError(PushbulletError):
    pass

class PushError(PushbulletError):
    pass


class NoEncryptionModuleError(Exception):
    def __init__(self, msg):
        super(NoEncryptionModuleError, self).__init__(
            "cryptography is required for end-to-end encryption support and could not be imported: " + msg + "\nYou can install it by running 'pip install cryptography'")
