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

    def __init__(self, username, password, token, base_uri=None):
        self.BASE_URI = base_uri or BaseMuckRockClient.BASE_URI
        self.username = username
        self.password = password
        self.token = token
        if self.username and self.password:
            response = requests.post(
                'https://www.muckrock.com/api_v1/token-auth/',
                data={
                    'username': self.username,
                    'password': self.password
                })
            if not response.raise_for_status():
                data = response.json()
                self.token = data['token']

    def _get_request(self, url, params, headers={}):
        if self.token:
            headers.update({'Authorization': 'Token %s' % self.token})
        headers.update({'User-Agent': self.USER_AGENT})
        response = requests.get(url, params=params, headers=headers)
        return response.json()


class MuckRock(BaseMuckRockClient):
    """
    The public interface for the DocumentCloud API
    """
    def __init__(self, username=None, password=None, token=None, base_uri=None):
        super(MuckRock, self).__init__(username, password, token, base_uri)
        self.foia = FoiaClient(
            self.username,
            self.password,
            self.token,
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
        has_datetime_submitted=None,
        has_datetime_done=None,
        ordering="-datetime_submitted",
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
        datetime_submitted_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params['has_datetime_submitted'] = datetime_submitted_choices[has_datetime_submitted]
        datetime_done_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params['has_datetime_done'] = datetime_done_choices[has_datetime_done]
        params['ordering'] = ordering
        return self._get_request(self.BASE_URI + self.endpoint, params)['results']
