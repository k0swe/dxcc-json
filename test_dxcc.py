import csv
import re
import unittest


class DxccRegexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('dxcc-2026-01.csv', encoding='utf8', newline='') as infile:
            cls.rows = {row['entityCode']: row for row in csv.DictReader(infile)}

    def assert_matches(self, entity_code, *callsigns):
        row = self.rows[str(entity_code)]
        pattern = re.compile(row['prefixRegex'])
        for callsign in callsigns:
            self.assertIsNotNone(
                pattern.fullmatch(callsign),
                f'{callsign} must match {entity_code} {row["name"]}: {pattern.pattern}',
            )

    def test_every_listed_prefix_matches_its_regex(self):
        for row in self.rows.values():
            if not row['prefix']:
                continue
            pattern = re.compile(row['prefixRegex'])
            for prefix in row['prefix'].split(','):
                with self.subTest(entity=row['entityCode'], prefix=prefix):
                    self.assertIsNotNone(pattern.fullmatch(prefix + '0A'))

    def test_arrl_2026_prefix_coverage_additions(self):
        # ARRL's January 2026 list includes these allocations. CU remains
        # excluded from Portugal because it identifies the Azores DXCC entity.
        cases = {
            315: ('4P0A', '4Q0A', '4R0A', '4S0A'),
            400: ('7R0A', '7T0A', '7Y0A'),
            414: ('9O0A', '9P0A', '9T0A'),
            402: ('A20A', '8O0A'),
            372: ('AP0A', 'AQ0A', 'AR0A', 'AS0A'),
            70: ('CL0A', 'CM0A', 'CO0A'),
            446: ('CN0A', '5C0A', '5G0A'),
            272: ('CQ0A', 'CR0A', 'CS0A', 'CT0A'),
            153: ('VK0A', 'VK7A'),
            170: ('ZK0A', 'ZL0A', 'ZM0A'),
            235: ('VP0A', 'VP8A', 'LU0A'),
            238: ('VP0A', 'VP8A', 'LU0A'),
            240: ('VP0A', 'VP8A', 'LU0A'),
            241: ('VP0A', 'VP8A', 'LU0A', 'CE9A', 'HF0A', '4K1A'),
        }
        for entity_code, callsigns in cases.items():
            with self.subTest(entity=entity_code):
                self.assert_matches(entity_code, *callsigns)

    def test_juan_de_nova_and_europa_prefixes_do_not_match_bare_e_callsigns(self):
        self.assert_matches(124, 'FT/J0A', 'FT/E0A', 'TO0A')
        pattern = self.rows['124']['prefixRegex']
        self.assertIsNone(re.fullmatch(pattern, 'E50A'))

    def test_portugal_does_not_claim_azores_cu_prefix(self):
        self.assertIsNone(re.fullmatch(self.rows['272']['prefixRegex'], 'CU0A'))


if __name__ == '__main__':
    unittest.main()
