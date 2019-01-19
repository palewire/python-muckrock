from functools import wraps
from .exceptions import CredentialsMissingError


def credentials_required(method_func):
    """
    Decorator for methods that checks that the client has credentials.
    Throws a CredentialsMissingError when they are absent.
    """
    def _checkcredentials(self, *args, **kwargs):
        if self.username and self.password:
            return method_func(self, *args, **kwargs)
        else:
            raise CredentialsMissingError(
                "This is a private method. You must provide a username and password."
            )
    return wraps(method_func)(_checkcredentials)
