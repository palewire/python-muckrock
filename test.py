import unittest
from muckrock import MuckRock


class GetTest(unittest.TestCase):

    def setUp(self):
        """
        Initialize a bunch of variables we'll use across tests.
        """
        self.public_client = MuckRock()

    def test_foia(self):
        default_list = self.public_client.foia.get()
        self.assertTrue(len(default_list) == 100)

        done_list = self.public_client.foia.get(status="done")
        [self.assertTrue(done['status'] == 'done') for done in done_list]

        short_list = self.public_client.foia.get(page_size=1)
        self.assertTrue(len(short_list) == 1)

        sorted_list = self.public_client.foia.get(ordering="-datetime_submitted")



if __name__ == '__main__':
    unittest.main()
