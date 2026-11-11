"""Fixture contract only; no performance loop executes in CI."""
import importlib.util
import json
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/'benchmarks/snapshot_probe.py'
spec=importlib.util.spec_from_file_location('snapshot_probe_contract',p)
probe=importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
class ProbeContractTests(unittest.TestCase):
    def test_deterministic_bounded_fixture(self):
        payload=probe.fixture()
        self.assertEqual(payload,probe.fixture())
        self.assertLessEqual(len(payload),2_000_000)
    def test_cap_and_unique_ids(self):
        rows=probe.decode_snapshot(probe.fixture())['projects']
        self.assertEqual(len(rows),200)
        self.assertEqual(len({x['id'] for x in rows}),200)
    def test_private_identity_absent(self):
        rows=json.loads(probe.fixture())['projects']
        self.assertTrue(all(x['id'].startswith('synthetic-') and x['name'].startswith('Fictional project') for x in rows))
