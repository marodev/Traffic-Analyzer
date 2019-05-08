import unittest

from main.helpers.file import file_read_helper


class TestFileReadHelperMethods(unittest.TestCase):
    def test_get_dict_reader(self):
        header1, header2 = "mac.vendor.part", "vendor"
        value1, value2 = "3c:d9:2b", "Hewlett Packard"

        csv_file = '{},{}\n{},"{}"'.format(header1, header2, value1, value2).splitlines()
        dict_reader = file_read_helper.get_csv_dict_reader(csv_file)

        field_names = [header1, header2]
        self.assertEqual(dict_reader.fieldnames, field_names)

        for row in dict_reader:
            self.assertEqual(row[header1], value1)
            self.assertEqual(row[header2], value2)

    def test_is_header(self):
        line_dict = {
            0: True,
            1: False
        }
        for key in line_dict:
            self.assertEqual(file_read_helper.is_header(key), line_dict[key])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileReadHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
