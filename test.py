import os
import unittest
from muckrock import MuckRock
from muckrock.exceptions import ObjectNotFound


class GetTest(unittest.TestCase):

    def setUp(self):
        """
        Initialize a bunch of variables we'll use across tests.
        """
        self.public_client = MuckRock()
        self.private_client = MuckRock(
            username=os.getenv("MUCKROCK_TEST_USERNAME"),
            password=os.getenv("MUCKROCK_TEST_PASSWORD")
        )
        self.private_request_id = 67271

    def test_agency_get(self):
        public_obj = self.public_client.agency.get(1)
        self.assertEqual(public_obj['name'], "Suffolk County Sheriff's Department")

        with self.assertRaises(ObjectNotFound):
            self.public_client.agency.get(999999999999999)

    def test_foia_filter(self):
        default_list = self.public_client.foia.latest()
        self.assertEqual(len(default_list), 50)

        done_list = self.public_client.foia.filter(status="done")
        [self.assertEqual(done['status'], 'done') for done in done_list]

        sorted_list = self.public_client.foia.filter(
            status="done",
            has_datetime_done=True,
            ordering="-datetime_done"
        )

        latest_list = self.public_client.foia.filter(
            has_datetime_submitted=True,
            ordering="-datetime_submitted"
        )

    def test_foia_get(self):
        public_obj = self.public_client.foia.get(100)
        self.assertEqual(public_obj['title'], "Cyber Security Analyst's Regular Reports")

        private_obj = self.private_client.foia.get(self.private_request_id)
        self.assertEqual(private_obj['title'], "@MayorOfLA Direct Messages")

        with self.assertRaises(ObjectNotFound):
            self.public_client.foia.get(999999999999999)
            self.public_client.foia.get(self.private_request_id)


if __name__ == '__main__':
    unittest.main()
