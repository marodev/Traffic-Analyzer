import unittest
from os import path
from unittest.mock import patch

from main.helpers.environment_helper import EnvironmentHelper


class Process:
    def __init__(self, name):
        self.info = {"name": name}


class TestEnrivonmentHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.environment_helper = EnvironmentHelper()
        cls.docker_init_files_base_path = path.join("..", "..", "..", "docker", "init_files")
        cls.lookup_base_path = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer", "lookups")
        cls.tmp_base_path = path.join("/tmp")
        cls.file_path = path.join("..", "files")

        cls.development_variables = {
            "pcap_path": path.join(cls.docker_init_files_base_path, "pcaps"),
            "pcap_processed_path": path.join(cls.docker_init_files_base_path, "pcaps"),
            "csv_tmp_path": cls.file_path,
            "csv_list_path": cls.file_path,
            "csv_capture_path": cls.file_path,
            "dns_request_files": cls.file_path,
            "pickle_dict_file_path": path.join(cls.file_path, "stream.pickle")
        }
        cls.production_variables = {
            "pcap_path": path.join(cls.tmp_base_path, "pcaps"),
            "pcap_processed_path": path.join(cls.tmp_base_path, "pcaps_processed"),
            "csv_tmp_path": path.join(cls.tmp_base_path, "csvs"),
            "csv_list_path": path.join(cls.lookup_base_path, "lists"),
            "csv_capture_path": path.join(cls.lookup_base_path, "captures"),
            "dns_request_files": path.join(cls.lookup_base_path, "dns_request_files"),
            "pickle_dict_file_path": path.join(cls.tmp_base_path, "csvs", "stream.pickle")
        }

    @patch("psutil.process_iter")
    def test_development_variables(self, process_iter):
        process = Process("dev_test")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.development_variables)

    @patch("psutil.process_iter")
    def test_production_variables(self, process_iter):
        process = Process("splunkd")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrivonmentHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
