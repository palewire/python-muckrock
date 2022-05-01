"""Test the muckrock module."""
import unittest

from muckrock import MuckRock
from muckrock.exceptions import ObjectNotFound


class GetTest(unittest.TestCase):
    """Test requests for data."""

    def setUp(self):
        """Initialize a bunch of variables we'll use across tests."""
        self.client = MuckRock()
        self.private_request_id = 67271

    def test_jurisdiction_get(self):
        """Test the request for a jurisdiction."""
        obj = self.client.jurisdiction.get(1)
        self.assertEqual(obj["name"], "Massachusetts")
        with self.assertRaises(ObjectNotFound):
            self.client.jurisdiction.get(999999999999999)

    def test_jurisdiction_filter(self):
        """Test a filter for a jurisdiction list."""
        jurisdiction = self.client.jurisdiction.filter(name="Massachusetts")
        self.assertEqual(jurisdiction[0]["id"], 1)

        fed_list = self.client.jurisdiction.filter(level="Federal")
        self.assertEqual(len(fed_list), 1)
        self.assertEqual(fed_list[0]["name"], "United States of America")

    def test_agency_get(self):
        """Test the request for an agency."""
        obj = self.client.agency.get(1)
        self.assertEqual(obj["name"], "Suffolk County Sheriff's Department")
        with self.assertRaises(ObjectNotFound):
            self.client.agency.get(999999999999999)

    def test_agency_filter(self):
        """Test a filter for an agency list."""
        agency = self.client.agency.filter(name="Suffolk County Sheriff's Department")
        self.assertEqual(agency[0]["id"], 1)

        requires_proxy_list = self.client.agency.filter(requires_proxy=True)
        [self.assertEqual(a["requires_proxy"], True) for a in requires_proxy_list]

    #     def test_foia_create(self):
    #         kwargs = dict(
    #             agency_ids=248,
    #             title='API Test File Request',
    #             document_request="I would like the government's secret receipe for the world's best burrito"
    #         )
    #         self.private_client.foia.create(**kwargs)
    #         with self.assertRaises(CredentialsMissingError):
    #             self.public_client.foia.create(**kwargs)

    def test_foia_get(self):
        """Test the request for a request."""
        obj = self.client.foia.get(100)
        self.assertEqual(obj["title"], "Cyber Security Analyst's Regular Reports")

        obj = self.client.foia.get(self.private_request_id)
        self.assertEqual(obj["title"], "@MayorOfLA Direct Messages")

        with self.assertRaises(ObjectNotFound):
            self.client.foia.get(999999999999999)

    def test_foia_filter(self):
        """Test a filter for a request."""
        default_list = self.client.foia.latest()
        self.assertEqual(len(default_list), 50)

        done_list = self.client.foia.filter(status="done")
        [self.assertEqual(done["status"], "done") for done in done_list]

        self.client.foia.filter(
            status="done", has_datetime_done=True, ordering="-datetime_done"
        )

        self.client.foia.filter(
            has_datetime_submitted=True, ordering="-datetime_submitted"
        )


if __name__ == "__main__":
    unittest.main()
