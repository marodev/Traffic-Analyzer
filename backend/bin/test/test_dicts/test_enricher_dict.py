import unittest
from collections import OrderedDict

from main.dicts.enrichers_dict import get_enricher_dict
from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.tls_enricher import TlsEnricher
from test.test_dicts.keys import id_keys


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enricher_keys = [
            "location_enricher",
            "fqdn_resolve_enricher",
            "cipher_suite_enricher",
            "tls_ssl_version_enricher",
            "ip_type_enricher",
            "stream_enricher",
            "dns_lookup_enricher",
            "ad_enricher"
        ]

    def setUp(self):
        self.enricher_dict = get_enricher_dict()

    def test_create_enrichers_classes(self):
        for key in self.enricher_dict.keys():
            if key == "location_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], LocationEnricher))

            elif key == "fqdn_resolve_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], TlsEnricher))

            elif key == "ip_type_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], IpTypeEnricher))

            elif key == "stream_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], StreamEnricher))

            elif key == "dns_lookup_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], DnsLookupEnricher))

            elif key == "ad_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], AdEnricher))

            else:
                self.assertTrue(False)

    def test_create_enrichers_is_dict(self):
        self.assertTrue(isinstance(self.enricher_dict, OrderedDict))

    def test_create_enrichers_keys(self):
        self.assertEqual(list(self.enricher_dict.keys()), self.enricher_keys)

    def test_enricher_dict_keys(self):
        id_index = 0
        enricher_classes_key_ids = [key.split("_")[id_index] for key in self.enricher_dict.keys()]
        self.assertEqual(enricher_classes_key_ids, id_keys)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
