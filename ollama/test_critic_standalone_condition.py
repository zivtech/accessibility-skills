"""Offline repaired-condition and custody regressions; no model calls."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ollama.local_eval_202610 import freeze as fr, runner as rr


class RepairedConditionTests(unittest.TestCase):
    def test_fresh_freeze_is_explicit_and_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            self.assertEqual(manifest['condition'], 'critic-standalone-v2-202610')
            self.assertEqual(set(manifest['clean']), {
                'button-skip-link-clean', 'interactive-dropdown-clean',
                'modal-complete-clean', 'search-results-dynamic-clean'})
            prompt = json.loads((Path(directory) / 'freeze/prompts/critic/button-skip-link-clean.json').read_text())
            self.assertNotIn('Invoke the a11y-critic subagent', prompt['system'])
            self.assertIn('No tools', prompt['system'])
            self.assertNotIn('Accessibility Features Implemented', prompt['prompt'])
            self.assertNotIn('CLEAN fixture', prompt['prompt'])
            self.assertEqual(rr.summary(directory)['condition'], manifest['condition'])
            self.assertEqual(fr.verify(directory), manifest)

    def test_legacy_capture_cannot_be_silently_recreated(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'sealed'):
                fr.freeze(directory, condition='neutral-H1-blind-no-features-202610')
            self.assertFalse((Path(directory) / 'freeze').exists())

    def test_unknown_condition_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'condition'):
                fr.freeze(directory, condition='typo')
            self.assertFalse((Path(directory) / 'freeze').exists())

    def test_freeze_records_actual_commit_and_resume_rejects_drift(self):
        head = 'a' * 40
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(fr.subprocess, 'check_output', return_value=head):
                manifest = fr.freeze(directory)
                self.assertEqual(manifest['source'], head)
                fr.verify(directory)
            with patch.object(fr.subprocess, 'check_output', return_value='b' * 40):
                with self.assertRaisesRegex(ValueError, 'wrong source'):
                    fr.verify(directory)

    def test_live_condition_edit_blocks_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            original = Path.read_bytes
            def edited(path):
                raw = original(path)
                return raw + b'changed' if path == fr.CONDITION_DIR / 'system.md' else raw
            with patch.object(Path, 'read_bytes', edited):
                with self.assertRaisesRegex(ValueError, 'condition'):
                    fr.verify(directory)
            self.assertIn('sources/condition/system.md', manifest['files'])

    def test_companion_rubric_and_each_fixture_input_are_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            original = Path.read_bytes
            fixture = 'interactive-dropdown-clean'
            for suffix in ('.md', '.metadata.yaml', '.rubric.yaml'):
                base = Path(fr.rb.FIXTURES_DIR)
                if suffix == '.rubric.yaml':
                    base = base.parent / 'rubrics'
                live = base / (fixture + suffix)
                key = 'sources/critic/' + fixture + suffix
                self.assertEqual((Path(directory) / 'freeze' / key).read_bytes(), live.read_bytes())
                def edited(path, live=live):
                    raw = original(path)
                    return raw + b'changed' if path == live else raw
                with patch.object(Path, 'read_bytes', edited):
                    with self.assertRaisesRegex(ValueError, 'live fixture source changed'):
                        fr.verify(directory)
                self.assertIn(key, manifest['files'])

    def test_historical_inspection_rejects_corrupt_frozen_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            fr.freeze(directory)
            path = Path(directory) / 'freeze/sources/condition/system.md'
            path.write_text('altered')
            with self.assertRaisesRegex(ValueError, 'frozen file hash mismatch'):
                fr.verify_files(directory)

    def test_historical_file_integrity_does_not_authorize_resume(self):
        # A frozen cohort can pass byte-integrity inspection while live source
        # has drifted. The resume verifier must retain its separate live gate.
        with tempfile.TemporaryDirectory() as directory:
            fr.freeze(directory)
            report = fr.verify_files(directory)
            self.assertGreater(report['verified_files'], 0)
            self.assertFalse(report['resume_authorized'])
            original = Path.read_bytes
            def edited(path):
                raw = original(path)
                return raw + b'changed' if path == fr.ROOT / 'ollama/local_eval_202610/runner.py' else raw
            with patch.object(Path, 'read_bytes', edited):
                self.assertFalse(fr.verify_files(directory)['resume_authorized'])
                with self.assertRaisesRegex(ValueError, 'live supplemental module changed'):
                    fr.verify(directory)


if __name__ == '__main__':
    unittest.main()
