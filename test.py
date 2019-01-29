import os
import unittest
from muckrock import MuckRock


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

    def test_foia(self):
        default_list = self.public_client.foia.get()
        self.assertEqual(len(default_list), 50)

        done_list = self.public_client.foia.get(status="done")
        [self.assertEqual(done['status'], 'done') for done in done_list]

        sorted_list = self.public_client.foia.get(
            status="done",
            has_datetime_done=True,
            ordering="-datetime_done"
        )

        latest_list = self.public_client.foia.get(
            has_datetime_submitted=True,
            ordering="-datetime_submitted"
        )

        private_obj = self.private_client.foia.get()


if __name__ == '__main__':
    unittest.main()
