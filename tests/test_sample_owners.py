#!/usr/bin/env python3
"""Synthetic sample-parser tests, without a game or private stack capture."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "sample_owners", Path(__file__).resolve().parents[1] / "scripts/sample_owners.py")
owners = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owners)


class SampleOwnersTest(unittest.TestCase):
    def parse(self, label):
        capture = f"""Call graph:
    100 Thread_123{label}
    + 100 start  (in dyld) + 4
    +   50 main  (in BlueWake) + 8
    500 Thread_456: graphics worker
    + 500 worker  (in BlueWake) + 16
Total number in stack (recursive counted multiple, when >=5):
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.txt"
            path.write_text(capture)
            return owners.parse(path)

    def test_dispatch_queue_label(self):
        rows = self.parse("   DispatchQueue_1: com.apple.main-thread  (serial)")
        self.assertEqual([row[1] for row in rows], [100, 50])
        self.assertEqual([row[2] for row in rows], ["start", "main"])

    def test_main_thread_label(self):
        rows = self.parse(": Main Thread   DispatchQueue_<multiple>")
        self.assertEqual([row[1] for row in rows], [100, 50])
        self.assertEqual([row[2] for row in rows], ["start", "main"])

    def test_unidentified_thread_is_not_assumed_main(self):
        with self.assertRaises(SystemExit):
            self.parse(": other thread")


if __name__ == "__main__":
    unittest.main()
