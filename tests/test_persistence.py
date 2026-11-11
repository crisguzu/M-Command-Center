"""Injected syscall failures are not physical power-loss tests."""
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
from mcc.fs import root_fd, write_at

class SnapshotPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.fd = root_fd(self.root)
        write_at(self.fd, "snapshot.json", "old")
    def tearDown(self):
        os.close(self.fd)
        self.tmp.cleanup()
    def test_success_mode_and_replacement(self):
        write_at(self.fd, "snapshot.json", "new")
        self.assertEqual((self.root / "snapshot.json").read_text(), "new")
        self.assertEqual(stat.S_IMODE((self.root / "snapshot.json").stat().st_mode), 0o600)
        self.assertFalse((self.root / "snapshot.json.next").exists())
    def test_file_fsync_failure_preserves_original(self):
        with patch("mcc.fs.os.fsync", side_effect=OSError("synthetic sync failure")):
            with self.assertRaises(OSError): write_at(self.fd, "snapshot.json", "new")
        self.assertEqual((self.root / "snapshot.json").read_text(), "old")
        self.assertFalse((self.root / "snapshot.json.next").exists())
    def test_replace_failure_preserves_original(self):
        with patch("mcc.fs.os.replace", side_effect=OSError("synthetic replace failure")):
            with self.assertRaises(OSError): write_at(self.fd, "snapshot.json", "new")
        self.assertEqual((self.root / "snapshot.json").read_text(), "old")
        self.assertFalse((self.root / "snapshot.json.next").exists())
    def test_existing_temporary_not_clobbered(self):
        (self.root / "snapshot.json.next").write_text("held")
        with self.assertRaises(FileExistsError): write_at(self.fd, "snapshot.json", "new")
        self.assertEqual((self.root / "snapshot.json").read_text(), "old")
        self.assertEqual((self.root / "snapshot.json.next").read_text(), "held")
    def test_v1_durability_boundary_file_only(self):
        real = os.fsync
        kinds = []
        def observe(fd):
            kinds.append(stat.S_ISDIR(os.fstat(fd).st_mode))
            return real(fd)
        with patch("mcc.fs.os.fsync", side_effect=observe):
            write_at(self.fd, "snapshot.json", "new")
        self.assertEqual(kinds, [False])
