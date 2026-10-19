"""Offline synthetic intake records only; no claim of legal or provider validation."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from asset_intake import validate, sha256_file, load_record, SCHEMA


class AssetIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ('original.bin', 'evidence.txt', 'adapted.blend'):
            (self.root/name).write_text('SYNTHETIC FIXTURE NOT AN ASSET: ' + name)
        self.bind = lambda n: {'path': n, 'sha256': sha256_file(self.root/n)}
        self.doc = {'schema': SCHEMA, 'asset_id': 'synthetic_moss',
          'origin': {'provider': 'Synthetic fixture', 'creator': 'Not a real author',
            'asset_url': 'https://example.org/asset', 'license_url': 'https://example.org/license',
            'version_or_tier': 'test only', 'checked_at': '2026-10-19', 'license_id': 'SYNTHETIC',
            'evidence': [self.bind('evidence.txt')]},
          'rights': {'commercial_render': 'allowed', 'modification': 'allowed',
            'raw_redistribution': 'unknown', 'external_processing_upload': 'unknown',
            'attribution_required': False, 'attribution_text': '', 'conditions_met': True,
            'unresolved_questions': [], 'reviewer': 'SYNTHETIC NOT USER APPROVAL', 'reviewed_at': '2026-10-19'},
          'files': {'originals': [self.bind('original.bin')], 'derivatives': []},
          'storage': {'publish_originals': False, 'publish_derivatives': False, 'source_dependency_audit_complete': False},
          'use': {'purpose': 'Synthetic material test', 'credit_destination': None},
          'inspection': {'auto_execution_disabled': True}, 'owner_approval': 'pending'}
    def run_check(self, intent='local_test'):
        return validate(self.doc, self.root, intent)
    def contains(self, result, substring):
        self.assertTrue(any(substring in v for v in result['errors']), result)
    def test_valid_metadata_not_approval(self):
        r=self.run_check(); self.assertTrue(r['metadata_ok']); self.assertFalse(r['production_approved'])
    def test_pure_no_input_mutation(self):
        d=copy.deepcopy(self.doc); self.run_check(); self.assertEqual(self.doc,d)
    def test_research_allows_unknown_rights(self):
        self.doc['rights']['commercial_render']='unknown'; self.assertTrue(self.run_check('research')['metadata_ok'])
    def test_local_unknown_render_refused(self):
        self.doc['rights']['commercial_render']='unknown'; self.contains(self.run_check(),'commercial_render')
    def test_noncommercial_refused(self):
        self.doc['rights']['commercial_render']='denied'; self.contains(self.run_check(),'commercial_render')
    def test_no_modifications_refused(self):
        self.doc['rights']['modification']='denied'; self.contains(self.run_check(),'modification')
    def test_unknown_license_refused(self):
        self.doc['origin']['license_id']='unknown'; self.contains(self.run_check(),'license still unknown')
    def test_missing_evidence_refused(self):
        self.doc['origin']['evidence']=[]; self.contains(self.run_check(),'origin.evidence')
    def test_missing_original_refused(self):
        self.doc['files']['originals']=[]; self.contains(self.run_check(),'files.originals')
    def test_hash_mismatch(self):
        (self.root/'original.bin').write_text('changed'); self.contains(self.run_check(),'SHA-256 mismatch')
    def test_invalid_hash(self):
        self.doc['files']['originals'][0]['sha256']=4; self.contains(self.run_check(),'invalid SHA')
    def test_missing_file(self):
        (self.root/'original.bin').unlink(); self.contains(self.run_check(),'missing or external')
    def test_traversal(self):
        self.doc['files']['originals'][0]['path']='../other'; self.contains(self.run_check(),'unsafe')
    def test_external_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'outside'; p.write_text('x'); (self.root/'link').symlink_to(p)
            self.doc['files']['originals'][0]['path']='link'; self.contains(self.run_check(),'external')
    def test_absolute_path(self):
        self.doc['files']['originals'][0]['path']=str(self.root/'original.bin'); self.contains(self.run_check(),'unsafe')
    def test_duplicate_binding(self):
        self.doc['files']['originals']*=2; self.contains(self.run_check(),'duplicate binding')
    def test_secret_url_refused(self):
        self.doc['origin']['asset_url']='https://example.org/asset?token=secret'; self.contains(self.run_check(),'stable HTTPS')
    def test_url_userinfo_refused(self):
        self.doc['origin']['asset_url']='https://secret@example.org/a'; self.contains(self.run_check(),'stable HTTPS')
    def test_malformed_sections(self):
        for key in ('origin','rights','files','storage','use','inspection'):
            d=copy.deepcopy(self.doc); d[key]=[]; self.assertFalse(validate(d,self.root)['metadata_ok'])
    def test_malformed_bindings(self):
        for value in (None, {}, ['wrong'], [{'path': []}]):
            d=copy.deepcopy(self.doc); d['files']['originals']=value
            self.assertFalse(validate(d,self.root,'local_test')['metadata_ok'])
    def test_required_credit(self):
        self.doc['rights']['attribution_required']=True; self.contains(self.run_check(),'credit text')
    def test_credit_complete(self):
        self.doc['rights'].update(attribution_required=True,attribution_text='SYNTHETIC attribution')
        self.doc['use']['credit_destination']='test credits'; self.assertTrue(self.run_check()['metadata_ok'])
    def test_unresolved_conflict(self):
        self.doc['rights']['unresolved_questions']=['Two different licenses']; self.contains(self.run_check(),'unresolved')
    def test_no_terms_reviewer(self):
        self.doc['rights']['reviewer']=None; self.contains(self.run_check(),'who checked')
    def test_autoexec_refused(self):
        self.doc['inspection']['auto_execution_disabled']=False; self.contains(self.run_check(),'script execution')
    def test_no_upload_permission_granted(self):
        r=self.run_check(); self.assertTrue(any('do not upload' in s for s in r['notes']))
    def test_raw_rights_not_implied(self):
        self.doc['storage'].update(publish_originals=True,source_dependency_audit_complete=True)
        self.contains(self.run_check('public_bundle'),'source redistribution')
    def test_public_metadata(self):
        self.doc['storage'].update(publish_originals=True,source_dependency_audit_complete=True)
        self.doc['rights']['raw_redistribution']='allowed'
        r=self.run_check('public_bundle'); self.assertTrue(r['metadata_ok']); self.assertFalse(r['production_approved'])
    def test_embedded_dependency_review(self):
        self.doc['storage']['publish_originals']=True; self.doc['rights']['raw_redistribution']='allowed'
        self.contains(self.run_check('public_bundle'),'dependency review')
    def test_derivative_missing(self):
        self.doc['storage'].update(publish_derivatives=True,source_dependency_audit_complete=True)
        self.doc['rights']['raw_redistribution']='allowed'; self.contains(self.run_check('public_bundle'),'no bound derivative')
    def test_valid_derivative(self):
        self.doc['storage'].update(publish_derivatives=True,source_dependency_audit_complete=True)
        self.doc['rights']['raw_redistribution']='allowed'; self.doc['files']['derivatives']=[self.bind('adapted.blend')]
        self.assertTrue(self.run_check('public_bundle')['metadata_ok'])
    def test_invalid_intent(self):
        self.contains(self.run_check('approve_for_real'),'Unsupported intent')
    def test_top_level_type(self):
        self.assertFalse(validate([],self.root)['metadata_ok'])
    def test_duplicate_json_keys(self):
        p=self.root/'r.json'; p.write_text('{"schema": 1, "schema": 2}')
        with self.assertRaisesRegex(ValueError,'Duplicate'): load_record(p)
    def test_nan_json_refused(self):
        p=self.root/'r.json'; p.write_text('{"x": NaN}')
        with self.assertRaises(ValueError): load_record(p)
    def test_large_record_refused(self):
        p=self.root/'r.json'; p.write_bytes(b' '*(2*1024*1024+1))
        with self.assertRaisesRegex(ValueError,'exceeds'): load_record(p)
    def test_bad_boolean(self):
        self.doc['storage']['publish_originals']='false'; self.contains(self.run_check(),'expected boolean')
    def test_bad_date(self):
        self.doc['origin']['checked_at']='2026-19-40'; self.contains(self.run_check(),'ISO date')


if __name__=='__main__': unittest.main()
