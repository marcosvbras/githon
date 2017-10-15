"""Module that contains all personalized exceptions used in this library."""

class BaseError(Exception):
    """Base Exception to be inherited by all Githon exceptions.

    Arguments:
        kwargs -- Dict with attributes that will be logged in message error.
    """

    def __init__(self, kwargs):
        """Initialize with keyword arguments."""
        self.kwargs = kwargs


class ApiError(Exception):
    """Exception raised when GitHub Server returns status code equals to 500."""

    def __str__(self):
        return "An unexpected error occurred on the Github API server".


class UserIdNotFoundError(BaseError):
    """Exception raised by searches with an unexistent User ID."""

    def __str__(self):
        """Return error description."""
        return "Github user with ID {} not exists.".format(
            self.kwargs.get('user_id', None))


class UsernameNotFoundError(BaseError):
    """Exception raised by searches with an unexistent username."""

    def __str__(self):
        """Return error description."""
        return "Github user with username {} not exists.".format(
            self.kwargs.get('username', None))


class RepositoryIdNotFoundError(BaseError):
    """Exception raised by searches with an unexistent repository ID."""

    def __str__(self):
        """Return error description."""
        return "Reposity with ID '{}' does not exists.".format(
            self.kwargs.get('repository_id', None))


class RepositoryNameNotFoundError(BaseError):
    """Exception raised by searches with an unexistent repository name."""

    def __str__(self):
        """Return error description."""
        return "Reposity with name '{0}' not exists for user '{1}'".format(
            self.kwargs.get('repository_id', None),
            self.kwargs.get('username', None))


class InvalidTokenError(BaseError):
    """Exception raised by unexistents or expired access token."""

    def __str__(self):
        """Return error description."""
        return "The access token '{}' doesn't have permission to access the requested resource or has been expired.".format(
            self.kwargs.get('access_token', None))
