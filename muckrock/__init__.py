"""
Python library for interacting with the MuckRock API.

https://www.muckrock.com/api/
"""
import os
import requests
from .exceptions import (
    ObjectNotFound,
    CredentialsMissingError,
    CredentialsWrongError
)


class BaseMuckRockClient(object):
    """
    Patterns common to all of the different API methods.
    """
    BASE_URI = 'https://www.muckrock.com/api_v1/'
    USER_AGENT = "python-muckrock (https://github.com/datadesk/python-muckrock)"

    def __init__(self, username, password, token, base_uri=None):
        self.BASE_URI = base_uri or BaseMuckRockClient.BASE_URI
        self.username = username or os.getenv("MUCKROCK_USERNAME")
        self.password = password or os.getenv("MUCKROCK_PASSWORD")
        self.token = token

    def _get_request(self, url, params={}, headers={}):
        """
        Makes a GET request to the Muckrock API.

        Returns the response as JSON.
        """
        if self.token:
            headers.update({'Authorization': 'Token {}'.format(self.token)})
        headers.update({'User-Agent': self.USER_AGENT})
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def _post_request(self, url, data={}, headers={}):
        """
        Makes a GET request to the Muckrock API.

        Returns the response as JSON.
        """
        if not self.token:
            raise CredentialsMissingError("User login credentials are required to create a request.")
        headers.update({
            'Authorization': 'Token {}'.format(self.token),
            'User-Agent': self.USER_AGENT
        })
        r = requests.post(
            url,
            json=data,
            headers=headers
        )
        print(r.status_code)
        rjson = r.json()
        if rjson == {'detail': 'Invalid token.'}:
            raise CredentialsWrongError(rjson['detail'])
        return rjson


class MuckRock(BaseMuckRockClient):
    """
    The public interface for the DocumentCloud API
    """
    def __init__(self, username=None, password=None, token=None, base_uri=None):
        # Set all the basic configuration options to this, the parent instance.
        super(MuckRock, self).__init__(username, password, token, base_uri)
        # Retrieve a token if necessary
        if not self.token and self.username and self.password:
            self.token = self._get_token()

        # Initialize the API endpoint methods that are children to this parent
        endpoint_args = (
            self.username,
            self.password,
            self.token,
            base_uri
        )
        self.foia = FoiaEndpoint(*endpoint_args)
        self.agency = AgencyEndpoint(*endpoint_args)
        self.jurisdiction = JurisdictionEndpoint(*endpoint_args)

    def _get_token(self):
        """
        Uses the provided username and password to retrieve an API token.
        """
        # Ask for the token using the username and password
        r = requests.post(
            'https://www.muckrock.com/api_v1/token-auth/',
            data={
                'username': self.username,
                'password': self.password
            }
        )
        # Get the JSON
        rjson = r.json()

        # If there's an error, raise it
        if 'non_field_errors' in rjson:
            raise CredentialsWrongError(rjson['non_field_errors'])

        # Otherwise return the token
        return rjson['token']


class BaseEndpointMixin(object):
    """
    Methods shared by endpoint classes.
    """
    def get(self, id):
        """
        Returns a request with the specified identifer.
        """
        url = self.BASE_URI + self.endpoint + "/{}/".format(id)
        r = self._get_request(url)
        if r == {'detail': 'Not found.'}:
            raise ObjectNotFound("Request {} not found".format(id))
        return r


class JurisdictionEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """
    Methods for collecting jurisdictions.
    """
    endpoint = "jurisdiction"

    def filter(
        self,
        name=None,
        abbreviation=None,
        parent_id=None,
        level=None,
        requires_proxy=None
    ):
        """
        Returns a list of requests that match the provide input filters.
        """
        params = {}
        if name:
            params['name'] = name
        if abbreviation:
            params['abbrev'] = abbreviation
        if parent_id:
            params['parent'] = parent_id
        if level:
            level_choices = {
                "federal": 'f',
                'state': 's',
                'local': 'l'
            }
            params['level'] = level_choices[level.lower()]
        requires_proxy_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params['law__requires_proxy'] = requires_proxy_choices[requires_proxy]
        return self._get_request(self.BASE_URI + self.endpoint, params)['results']


class AgencyEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """
    Methods for collecting agencies.
    """
    endpoint = "agency"

    def filter(
        self,
        name=None,
        status=None,
        jurisdiction_id=None,
        requires_proxy=None
    ):
        """
        Returns a list of requests that match the provide input filters.
        """
        params = {}
        if name:
            params['name'] = name
        if status:
            params['status'] = status
        if jurisdiction_id:
            params['jurisdiction'] = jurisdiction_id
        requires_proxy_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params['requires_proxy'] = requires_proxy_choices[requires_proxy]
        return self._get_request(self.BASE_URI + self.endpoint, params)['results']


class FoiaEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """
    Methods for collecting FOIA requests.
    """
    endpoint = "foia"

    def create(
        self,
        title="",
        document_request="",
        full_text="",
        agency_ids=[],
        embargo=False,
        permanent_embargo=False,
        attachments=[]
    ):
        """
        Creates a new request.
        """
        if not title:
            raise TypeError("title kwarg required")
        if not document_request and not full_text:
            raise TypeError("document_request or full_text kwarg required")
        if not agency_ids:
            raise TypeError("agency_id kwarg required")
        data = {
            'title': title,
            'document_request': document_request,
            'agency': agency_ids,
            'embargo': embargo,
            'permanent_embargo': permanent_embargo,
        }
        if full_text:
            data['full_text'] = full_text
        if attachments:
            data['attachments'] = attachments
        return self._post_request(self.BASE_URI + self.endpoint + "/", data)

    def filter(
        self,
        user=None,
        title=None,
        status=None,
        embargo=None,
        jurisdiction_id=None,
        agency_id=None,
        has_datetime_submitted=None,
        has_datetime_done=None,
        ordering="-datetime_submitted",
    ):
        """
        Returns a list of requests that match the provide input filters.
        """
        params = {}
        if user:
            params['user'] = user
        if title:
            params['title'] = title
        if status:
            params['status'] = status
        if embargo:
            params['embargo'] = embargo
        if jurisdiction_id:
            params['jurisdiction'] = jurisdiction_id
        if agency_id:
            params['agency'] = agency_id
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

    def latest(self):
        """
        An alias to the filter command with no input.
        """
        return self.filter()
