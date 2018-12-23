class ModelError(Exception):
    """Base exception for everything related to the model implementations."""


class NoFlags(ModelError):
    """Exception that will be raised when a flag value should be compared, but the User object
    has no flags attached."""


class InvalidPermission(ModelError):
    """Exception that will be raised when resolving a permission failed."""
