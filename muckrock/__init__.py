"""
Python library for interacting with the MuckRock API.

https://www.muckrock.com/api/
"""
import requests


class BaseMuckRockClient(object):
    """
    Patterns common to all of the different API methods.
    """
    BASE_URI = 'https://www.muckrock.com/api_v1/'
    USER_AGENT = ""

    def __init__(self, username, password, base_uri=None):
        self.BASE_URI = base_uri or BaseMuckRockClient.BASE_URI
        self.username = username
        self.password = password

    def _get_request(self, url, params, headers={}):
        headers.update({'User-Agent': self.USER_AGENT})
        return requests.get(url, params=params, headers=headers).json()


class MuckRock(BaseMuckRockClient):
    """
    The public interface for the DocumentCloud API
    """
    def __init__(self, username=None, password=None, base_uri=None):
        super(MuckRock, self).__init__(username, password, base_uri)
        self.foia = FoiaClient(
            self.username,
            self.password,
            base_uri
        )


class FoiaClient(BaseMuckRockClient):
    """
    Methods for collecting FOIA requests.
    """
    endpoint = "foia"

    def get(
        self,
        user=None,
        title=None,
        status=None,
        embargo=None,
        jurisdiction=None,
        agency=None,
        page_size=100,
        ordering="-id",
    ):
        params = {}
        if user:
            params['user'] = user
        if title:
            params['title'] = title
        if status:
            params['status'] = status
        if embargo:
            params['embargo'] = embargo
        if jurisdiction:
            params['jurisdiction'] = jurisdiction
        if user:
            params['agency'] = agency
        params['page_size'] = page_size
        params['ordering'] = ordering
        return self._get_request(self.BASE_URI + self.endpoint, params)['results']
