import unittest

import main.convert_pcap as convert_pcap
from test.filenames import get_filenames


class TestConvertPcapMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filenames = get_filenames()
        cls.csv_filenames = filenames["csv_filenames"]
        cls.pcap_filenames_without_prefix = filenames["pcap_filenames_without_prefix"]
        cls.pcapng_filenames_without_prefix = filenames["pcapng_filenames_without_prefix"]
        cls.pcap_filenames_with_prefix = filenames["pcap_filenames_with_prefix"]
        cls.pcapng_filenames_with_prefix = filenames["pcapng_filenames_with_prefix"]

    def test_get_new_filename_without_prefix(self):
        new_pcap_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcap_filenames_without_prefix
        ]
        new_pcapng_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcapng_filenames_without_prefix
        ]
        csv_filenames_lower = [filename.lower() for filename in self.csv_filenames]

        self.assertEqual(new_pcap_filenames, csv_filenames_lower)
        self.assertEqual(new_pcapng_filenames, csv_filenames_lower)

    def test_get_new_filename_with_prefix(self):
        new_pcap_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcap_filenames_with_prefix
        ]
        new_pcapng_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcapng_filenames_with_prefix
        ]
        csv_filenames_lower = [filename.lower() for filename in self.csv_filenames]

        self.assertEqual(new_pcap_filenames, csv_filenames_lower)
        self.assertEqual(new_pcapng_filenames, csv_filenames_lower)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertPcapMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
