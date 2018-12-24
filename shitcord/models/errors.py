class ModelError(Exception):
    """Base exception for everything related to the model implementations."""


class InvalidPermission(ModelError):
    """Exception that will be raised when resolving a permission failed."""


class MissingProfile(ModelError):
    """Exception that will be raised when attributes of User should be accessed that
    are only accessible via OAuth grant."""
