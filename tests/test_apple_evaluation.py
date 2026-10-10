"""Unit tests for Apple Evaluation Script."""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from apple_evaluation import generate_report, run_zsh_diagnostics
from import_github_sources import calculate_sha256, quarantine_source_file

class TestAppleEvaluation(unittest.TestCase):
    def test_generate_report(self):
        data = {
            "computer_name": "MacBook-Pro-Allan",
            "hardware_model": "Mac15,3",
            "os_version": "15.0",
            "os_build": "24A335",
            "architecture": "arm64",
            "kernel": "Darwin Kernel Version 24.0.0",
            "boot_storage": "/dev/disk3s1s1 465Gi 120Gi 320Gi 28%"
        }
        report = generate_report(data)
        self.assertIn("MacBook-Pro-Allan", report)
        self.assertIn("arm64", report)
        self.assertIn("Read-Only Verification", report)

    def test_run_diagnostics(self):
        data = run_zsh_diagnostics()
        self.assertIn("computer_name", data)
        self.assertIn("architecture", data)

    def test_quarantine_import(self):
        staging_dir = "/tmp/test_staging"
        content = "print('Untrusted code for inspection')"
        manifest = quarantine_source_file("sample.py", content, target_dir=staging_dir)
        self.assertTrue(manifest["quarantined"])
        self.assertFalse(manifest["executable"])
        self.assertTrue(os.path.exists(manifest["path"]))

if __name__ == "__main__":
    unittest.main()
