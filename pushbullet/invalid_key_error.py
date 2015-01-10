class InvalidKeyError(Exception):
    def __init__(self):
        self.value = "Invalid API Key"

    def __str__(self):
        return repr(self.value)
