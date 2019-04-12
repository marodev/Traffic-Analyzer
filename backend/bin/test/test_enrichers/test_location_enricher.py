import unittest

from io import StringIO
from unittest.mock import patch

from main.enrichers.location_enricher import LocationEnricher


class TestLocationEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public_ip_address = "152.96.36.100"
        cls.private_ip_address = "10.0.0.1"
        cls.dst_src = {"dst": cls.public_ip_address, "src": cls.private_ip_address}
        cls.location = [47.1449, 8.1551]
        cls.empty_location = ["", ""]

    def setUp(self):
        self.locator = LocationEnricher()

    def assert_location(self, ip_address, location):
        self.locator.get_location(ip_address)
        self.assertEqual(self.locator.locations[ip_address], location)

    def test_get_location(self):
        lat_long = self.locator.locate_ip(self.public_ip_address)
        self.assertEqual(lat_long, self.location)

    def test_locate_public_ip_first_time(self):
        ip_address = self.public_ip_address
        self.assert_location(ip_address, self.location)

        size_before = len(self.locator.locations)
        self.assert_location(ip_address, self.location)
        size_after = len(self.locator.locations)
        self.assertEqual(size_after, size_before)

    def test_locate_private_ip(self):
        ip_address = self.private_ip_address
        self.assert_location(ip_address, self.empty_location)

    def test_locate_no_ip(self):
        ip_address = ""
        self.assert_location(ip_address, self.empty_location)

    def test_locate(self):
        line = self.locator.locate(self.dst_src)
        expected_line = '"47.1449","8.1551","",""'
        self.assertEqual(line, expected_line)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_empty_locations(self, mock_stdout):
        print_text = "Print out for all {} location entries\n\n\n\n".format(len(self.locator.locations))
        self.locator.print()
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_full_locations(self, mock_stdout):
        self.locator.set_entry(self.private_ip_address, self.empty_location)
        print_text = "Print out for all {} location entries\n{} --> {}\n\n\n\n" \
            .format(len(self.locator.locations), self.private_ip_address, self.empty_location)

        self.locator.print()
        self.assertEqual(mock_stdout.getvalue(), print_text)

    def tearDown(self):
        self.locator = None


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
