"""A simple python wrapper for the [MuckRock API."""
import os

import requests

from .exceptions import CredentialsMissingError, CredentialsWrongError, ObjectNotFound


class BaseMuckRockClient:
    """Create patterns common to all of the different API methods."""

    BASE_URI = "https://www.muckrock.com/api_v1/"
    USER_AGENT = "python-muckrock (https://github.com/palewire/python-muckrock)"

    def __init__(self, token=None, base_uri=None):
        """Create a new client object."""
        self.BASE_URI = base_uri or BaseMuckRockClient.BASE_URI
        if token:
            self.token = token
        else:
            if os.getenv("MUCKROCK_API_TOKEN"):
                self.token = os.getenv("MUCKROCK_API_TOKEN")
            else:
                self.token = None

    def _get_request(self, url, params=None, headers=None):
        """Make a GET request to the Muckrock API.

        Returns the response as JSON.
        """
        if not headers:
            headers = {}
        if self.token:
            headers.update({"Authorization": f"Token {self.token}"})
        if not params:
            params = {}
        headers.update({"User-Agent": self.USER_AGENT})
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def _post_request(self, url, data=None, headers=None):
        """Make a GET request to the Muckrock API.

        Returns the response as JSON.
        """
        if not self.token:
            raise CredentialsMissingError(
                "User login credentials are required to create a request."
            )
        if not data:
            data = {}
        if not headers:
            headers = {}
        headers.update(
            {
                "Authorization": f"Token {self.token}",
                "User-Agent": self.USER_AGENT,
            }
        )
        r = requests.post(url, json=data, headers=headers)
        rjson = r.json()
        if rjson == {"detail": "Invalid token."}:
            raise CredentialsWrongError(rjson["detail"])
        return rjson


class MuckRock(BaseMuckRockClient):
    """The public interface for the DocumentCloud API."""

    def __init__(self, username=None, password=None, token=None, base_uri=None):
        """Create an object."""
        # Set all the basic configuration options to this, the parent instance.
        super().__init__(token, base_uri)

        # Initialize the API endpoint methods that are children to this parent
        endpoint_args = (self.token, base_uri)
        self.foia = FoiaEndpoint(*endpoint_args)
        self.agency = AgencyEndpoint(*endpoint_args)
        self.jurisdiction = JurisdictionEndpoint(*endpoint_args)


class BaseEndpointMixin:
    """Methods shared by endpoint classes."""

    def get(self, id):
        """Return a request with the specified identifer."""
        url = self.BASE_URI + self.endpoint + f"/{id}/"
        r = self._get_request(url)
        if r == {"detail": "Not found."}:
            raise ObjectNotFound(f"Request {id} not found")
        return r


class JurisdictionEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """Methods for collecting jurisdictions."""

    endpoint = "jurisdiction"

    def filter(
        self,
        name=None,
        abbreviation=None,
        parent_id=None,
        level=None,
        requires_proxy=None,
    ):
        """Return a list of requests that match the provide input filters."""
        params = {}
        if name:
            params["name"] = name
        if abbreviation:
            params["abbrev"] = abbreviation
        if parent_id:
            params["parent"] = parent_id
        if level:
            level_choices = {"federal": "f", "state": "s", "local": "l"}
            params["level"] = level_choices[level.lower()]
        requires_proxy_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params["law__requires_proxy"] = requires_proxy_choices[requires_proxy]
        return self._get_request(self.BASE_URI + self.endpoint, params)["results"]


class AgencyEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """Methods for collecting agencies."""

    endpoint = "agency"

    def filter(self, name=None, status=None, jurisdiction_id=None, requires_proxy=None):
        """Return a list of requests that match the provide input filters."""
        params = {}
        if name:
            params["name"] = name
        if status:
            params["status"] = status
        if jurisdiction_id:
            params["jurisdiction"] = jurisdiction_id
        requires_proxy_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params["requires_proxy"] = requires_proxy_choices[requires_proxy]
        return self._get_request(self.BASE_URI + self.endpoint, params)["results"]


class FoiaEndpoint(BaseMuckRockClient, BaseEndpointMixin):
    """Methods for collecting FOIA requests."""

    endpoint = "foia"

    def create(
        self,
        title="",
        document_request="",
        full_text="",
        agency_ids=None,
        embargo=False,
        permanent_embargo=False,
        attachments=None,
    ):
        """Create a new request."""
        if not title:
            raise TypeError("title kwarg required")
        if not document_request and not full_text:
            raise TypeError("document_request or full_text kwarg required")
        if not agency_ids:
            raise TypeError("agency_id kwarg required")
        if not attachments:
            attachments = []
        data = {
            "title": title,
            "document_request": document_request,
            "agency": agency_ids,
            "embargo": embargo,
            "permanent_embargo": permanent_embargo,
        }
        if full_text:
            data["full_text"] = full_text
        if attachments:
            data["attachments"] = attachments
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
        """Return a list of requests that match the provide input filters."""
        params = {}
        if user:
            params["user"] = user
        if title:
            params["title"] = title
        if status:
            params["status"] = status
        if embargo:
            params["embargo"] = embargo
        if jurisdiction_id:
            params["jurisdiction"] = jurisdiction_id
        if agency_id:
            params["agency"] = agency_id
        datetime_submitted_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params["has_datetime_submitted"] = datetime_submitted_choices[
            has_datetime_submitted
        ]
        datetime_done_choices = {
            None: 1,
            True: 2,
            False: 3,
        }
        params["has_datetime_done"] = datetime_done_choices[has_datetime_done]
        params["ordering"] = ordering
        return self._get_request(self.BASE_URI + self.endpoint, params)["results"]

    def latest(self):
        """Serve as an alias to the filter command with no input."""
        return self.filter()
