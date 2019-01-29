

class CredentialsMissingError(Exception):
    """
    Raised if an API call is attempted without the required login credentials
    """
    pass


class RequestNotFound(Exception):
    """
    Raised if an API for a request does not return a result.
    """
    pass
