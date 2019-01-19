import unittest
from muckrock import MuckRock


class GetTest(unittest.TestCase):

    def setUp(self):
        """
        Initialize a bunch of variables we'll use across tests.
        """
        self.public_client = MuckRock()

    def test_foia(self):
        self.public_client.foia.get()
        self.public_client.foia.get(status="done")


if __name__ == '__main__':
    unittest.main()
