import unittest

from io import StringIO
from unittest.mock import patch

from main.helpers.CipherSuites import CipherSuites


class TestCipherSuitesMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packets = {
            "client_hello": {
                "tls.handshake.type": "1",
                "tls.handshake.ciphersuite": "49200",
                "tcp.stream": 1
            }, "server_hello": {
                "tls.handshake.type": "2",
                "tls.handshake.ciphersuite": "49200",
                "tcp.stream": 1
            }, "first_packet": {
                "tls.handshake.type": "",
                "tls.handshake.ciphersuite": "",
                "tcp.stream": 1
            }}
        cls.cipher_suites = CipherSuites()

    def test_get_cipher_suites_client_hello(self):
        expected_value = ""
        self.test_packet(expected_value, self.packets["client_hello"])

    def test_get_cipher_suites_server_hello(self):
        expected_value = 49200
        self.test_packet(expected_value, self.packets["server_hello"])

    def test_get_cipher_suites_tls_packet(self):
        expected_value = 49200
        self.test_packet(expected_value, self.packets["first_packet"])

    def test_packet(self, expected_value, packet):
        expected_cipher_suite = '{}'.format(expected_value)
        cipher_suite_number = self.cipher_suites.get_cipher_suite(packet)
        self.assertEqual(cipher_suite_number, expected_cipher_suite)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_full_locations(self, mock_stdout):
        print_text = "Print out for all 1 stream to cipher suites entries\n1 --> 49200\n\n\n\n"
        self.cipher_suites.print()
        self.assertEqual(mock_stdout.getvalue(), print_text)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuitesMethod)
    unittest.TextTestRunner(verbosity=2).run(suite)
