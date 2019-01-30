

class CredentialsMissingError(Exception):
    """
    Raised if an API call is attempted without the required login credentials
    """
    pass


class ObjectNotFound(Exception):
    """
    Raised if an API get request does not return a result.
    """
    pass
