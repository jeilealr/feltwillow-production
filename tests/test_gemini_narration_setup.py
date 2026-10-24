"""Local credential handling and bounded narration behavior without network/TTS."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'voice'))
import gemini_local
import narrate_scenes as narration


class GeminiNarrationSetupTests(unittest.TestCase):
    def test_key_saved_outside_repo_with_private_permissions_and_roundtrips(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'config/env'
            gemini_local.save_key('unit-test-only-value',path)
            self.assertEqual(gemini_local.read_saved_key(path),'unit-test-only-value')
            self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode),0o700)
            with self.assertRaises(ValueError):gemini_local.save_key('invalid\nkey',path)

    def test_credential_file_is_parsed_without_executing_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'env';marker=Path(tmp)/'executed'
            path.write_text("GEMINI_API_KEY='unit-test-only'\ntouch "+str(marker)+'\n')
            self.assertEqual(gemini_local.read_saved_key(path),'unit-test-only')
            self.assertFalse(marker.exists())

    def test_reusing_existing_key_does_not_print_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'config/env';gemini_local.save_key('unit-test-only',path);path.chmod(0o644)
            stdout=io.StringIO()
            with patch.object(gemini_local,'KEY_FILE',path),patch.object(gemini_local,'read_saved_key',return_value='unit-test-only'),patch.object(sys,'argv',['gemini_local.py','setup']),contextlib.redirect_stdout(stdout):
                self.assertEqual(gemini_local.main(),0)
            self.assertNotIn('unit-test-only',stdout.getvalue())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)

    def test_v7_dryrun_needs_no_credentials_sdk_or_output_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'r001'
            args=[sys.executable,str(ROOT/'voice/narrate_scenes.py'),'--story','lion_and_mouse_v7','--lines','stories/lion_and_mouse_v7/dialogue_coverage.json','--scenes','1','--out-root',str(out),'--dry-run']
            env={k:v for k,v in os.environ.items() if k not in ['GEMINI_API_KEY','GOOGLE_API_KEY']}
            result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            plan=json.loads(result.stdout)
            self.assertEqual(plan['requests_without_retries'],4)
            self.assertEqual(plan['maximum_attempts'],4)
            self.assertEqual({r['voice'] for r in plan['requests']},{'voice_v5bpq98uj7qh'})
            self.assertFalse(out.exists())

    def test_v7_rejects_unversioned_output_and_redo(self):
        base=[sys.executable,str(ROOT/'voice/narrate_scenes.py'),'--story','lion_and_mouse_v7','--lines','stories/lion_and_mouse_v7/dialogue_coverage.json','--dry-run']
        for extra,expected in [([], 'explicit versioned --out-root'),(['--redo'],'immutable revisions')]:
            result=subprocess.run(base+extra,cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn(expected,result.stderr)

    def test_default_tts_failure_is_one_attempt_without_implicit_paid_retry(self):
        with patch.object(narration,'synthesize',side_effect=RuntimeError('provider failure')) as synth,patch.object(narration.time,'sleep'),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):narration.speak(None,'voice','text','style')
            self.assertEqual(synth.call_count,1)

    def test_request_budget_stops_before_an_unapproved_retry(self):
        count=0
        def budget():
            nonlocal count
            if count==1:raise SystemExit('request budget reached')
            count+=1
        with patch.object(narration,'synthesize',side_effect=RuntimeError('provider failure')) as synth,patch.object(narration.time,'sleep'),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(SystemExit,'budget reached'):
                narration.speak(None,'voice','text','style',attempts=2,before_call=budget)
            self.assertEqual(synth.call_count,1)

    def test_v7_owner_identity_rename_preserves_exact_source_bytes(self):
        library=json.loads((ROOT/'stories/lion_and_mouse_v7/character_library.json').read_text())
        for name,actor in library['characters'].items():
            record=actor['canonical']
            self.assertEqual(Path(record['path']).name,f'full-body_{name.lower()}_neutral_pose_r01.png')
            if name == 'Milo':
                self.assertEqual((ROOT/record['path']).read_bytes(),(ROOT/record['source_path']).read_bytes())
            else:
                # The owner explicitly reconciled the displayed transparent bytes;
                # preserve the inherited RGB approval as history, never relabel it.
                import copy
                import hashlib
                from production.audio_visual_plan import load, readiness
                reconciliation=json.loads((ROOT/'stories/lion_and_mouse_v7/owner_leo_canonical_reconciliation_r001.json').read_text())
                self.assertEqual(hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest(),reconciliation['canonical']['sha256'])
                self.assertEqual(hashlib.sha256((ROOT/record['source_path']).read_bytes()).hexdigest(),reconciliation['previous_recorded_approval']['sha256'])
                self.assertFalse(reconciliation['image_bytes_changed'])
                _, plan, chars, locs = load(ROOT, 'lion_and_mouse_v7')
                with patch('production.audio_visual_plan.validate', side_effect=lambda *args, **kwargs: []):
                    self.assertFalse(any('Leo: canonical bytes differ' in e for e in readiness(plan, chars, locs, ROOT, 'image')))
                    wrong=copy.deepcopy(chars)
                    wrong['characters']['Leo']['canonical']['sha256']=reconciliation['previous_recorded_approval']['sha256']
                    self.assertTrue(any('Leo: canonical bytes differ' in e for e in readiness(plan, wrong, locs, ROOT, 'image')))
        self.assertIn('r03_candidate',library['characters']['Milo']['canonical']['source_revision_filename'])

if __name__=='__main__':unittest.main()
