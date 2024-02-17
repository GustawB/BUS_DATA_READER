class WarsawBusPyException(Exception):
    """Base class for all warsawbuspy exceptions."""


class InvalidFileExtensionException(WarsawBusPyException):
    def __init__(self, wanted_exception):
        super().__init__('Invalid file exception. Expected: ' + wanted_exception)
