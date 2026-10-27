"""Relocate a CPU fixture package and execute via ordinary Python, no Codex."""

import json, shutil, unittest
from pathlib import Path
from tests import test_sequence_pipeline as baseline
from production import sequence_plan as plan, sequence_export as export
from production.sequence_package import build, verify, materialize, worker, ROOT


class PackageTests(unittest.TestCase):
    setUp = baseline.SequencePipelineTests.setUp
    packet = baseline.SequencePipelineTests.packet

    def package(self):
        p = self.packet()
        p["resolved_images"] = p["resolved_images"][:1]
        p["edges"] = []
        p["sequence"]["method"] = "static_frame_hold"
        p["visual_unit"] = dict(
            editorial_relationship="individual", composition="environment_only"
        )
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        frozen = self.root / "frozen"
        export.compile_packet(p, self.root, frozen, "portable", self.recipe)
        package = self.root / "package"
        manifest = build(frozen, package, ROOT)
        return package, manifest

    def test_C13_C50_relocated_noninteractive_preflight_and_one_attempt(self):
        package, manifest = self.package()
        relocated = self.root / "new mount with spaces/package"
        relocated.parent.mkdir()
        shutil.move(package, relocated)
        manifest2 = verify(relocated)
        self.assertEqual(manifest2, manifest)
        op = manifest["operations"][0]["operation_id"]
        result = json.loads(
            worker(relocated, op, expected_package_sha256=manifest["package_sha256"])
            .strip()
            .splitlines()[-1]
        )
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["recipe"]["method"], "static_frame_hold")
        auth = self.root / "auth.json"
        auth.write_text(
            json.dumps(
                dict(
                    scope="execution_authorization",
                    decision="authorized",
                    reviewer="project_owner",
                    package_sha256=manifest["package_sha256"],
                    operation_ids=[op],
                    maximum_retries=0,
                )
            )
        )
        receipt = worker(relocated, op, self.root / "journal", auth, execute=True)
        self.assertEqual(receipt["returncode"], 0)
        self.assertEqual(receipt["visual_review"], "pending")
        from production.sequence_package import collect_results, verify_results

        results = self.root / "results"
        collected = collect_results(relocated, results)
        moved = self.root / "retrieved to Mac"
        shutil.move(results, moved)
        self.assertEqual(
            verify_results(moved, manifest["package_sha256"], collected["sha256"]),
            collected,
        )
        self.assertEqual(collected["owner_selection"], "pending")
        from production.sequence_package import take_proposals
        from production.sequence_take import selected_source

        proposed = take_proposals(
            moved, manifest["package_sha256"], collected["sha256"]
        )
        piece = next(iter(proposed["takes"]))
        with self.assertRaisesRegex(ValueError, "owner take"):
            selected_source(proposed, piece)
        row = proposed["takes"][piece]
        row.update(
            owner_decision="selected",
            full_motion_review=dict(
                status="pass",
                reviewer="synthetic transport fixture only",
                output_sha256=row["sha256"],
                whole_clip_watched=True,
                joins_reviewed=True,
            ),
        )
        self.assertEqual(selected_source(proposed, piece)[0], Path(row["path"]))

        with self.assertRaises(FileExistsError):
            worker(relocated, op, self.root / "journal", auth, execute=True)
        self.assertEqual(len(list((self.root / "journal").glob("*.result.json"))), 1)

    def test_C31_C32_wrong_auth_tamper_and_path_escape_fail(self):
        package, m = self.package()
        op = m["operations"][0]["operation_id"]
        with self.assertRaisesRegex(ValueError, "authorization"):
            worker(package, op, self.root / "journal", None, True)
        asset = next((package / "assets").glob("*"))
        asset.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "changed"):
            verify(package)
        from production.sequence_package import safe_file

        with self.assertRaises(ValueError):
            safe_file(package, "../outside")

    def test_C50_materialization_never_submits_or_loads_model(self):
        package, m = self.package()
        manifest, commands = materialize(package)
        self.assertFalse(manifest["submission_authorized"])
        self.assertTrue(
            all(op["maximum_retries"] == 0 for op in manifest["operations"])
        )
        self.assertFalse((package / "outputs").exists())
        self.assertTrue(all("--runtime-sha256" in argv for argv in commands.values()))

    def test_C31_unlisted_python_payload_and_missing_trust_rejected(self):
        package, m = self.package()
        op = m["operations"][0]["operation_id"]
        with self.assertRaisesRegex(ValueError, "trusted expected"):
            worker(package, op)
        (package / "payload/production/yaml.py").write_text(
            "raise AssertionError('unverified')"
        )
        with self.assertRaisesRegex(ValueError, "unexpected"):
            verify(package)

    def test_scheduler_uses_trusted_checkout_before_package_execution(self):
        script = (ROOT / "lumi/sequence_job.sbatch").read_text()
        self.assertIn("$FELTWILLOW_REPO/production/sequence_package.py", script)
        self.assertNotIn("$1/payload/production/sequence_package.py", script)

    def test_symlinked_runtime_and_outputs_cannot_escape_package(self):
        package, m = self.package()
        outside = self.root / "outside"
        outside.mkdir()
        (package / "host_runtime").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "escapes|symlink"):
            materialize(package)
        self.assertFalse((outside / "runtime.yaml").exists())
        (package / "outputs").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "escapes|symlink"):
            worker(
                package,
                m["operations"][0]["operation_id"],
                expected_package_sha256=m["package_sha256"],
            )

    def test_empty_self_signed_result_cannot_claim_verified_completeness(self):
        from production.sequence_package import verify_results

        folder = self.root / "fabricated"
        folder.mkdir()
        fake = dict(
            schema="wrong",
            package_sha256="package",
            run_id="invented",
            runtime_sha256="invented",
            files={},
            operations=[],
        )
        fake["sha256"] = plan.fingerprint(fake)
        (folder / "results.json").write_text(json.dumps(fake))
        with self.assertRaisesRegex(ValueError, "schema"):
            verify_results(folder, "package", fake["sha256"])

    def test_collection_rejects_runtime_and_marker_rewritten_together(self):
        from production.sequence_package import collect_results
        import yaml
        package,m=self.package();materialize(package)
        runtime=package/'host_runtime/runtime.yaml';content=yaml.safe_load(runtime.read_text());content['scenes'][1]['shots'][0]['prompt']='changed after freezing'
        runtime.write_text(yaml.safe_dump(content));marker=package/'host_runtime/packet.json';data=json.loads(marker.read_text());data['runtime']['sha256']=plan.digest(runtime);marker.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'immutable'):collect_results(package,self.root/'forged_results')
        self.assertFalse((self.root/'forged_results').exists())
