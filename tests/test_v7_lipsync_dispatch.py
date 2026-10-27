import io, json, types, unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from tests import test_v7_dialogue as base
from production import lip_sync


class V7DispatchTests(unittest.TestCase):
    setUp = base.DialogueFixture.setUp
    add_line = base.DialogueFixture.add_line
    alignment = base.DialogueFixture.alignment
    refresh_mapping_review = base.DialogueFixture.refresh_mapping_review
    compile = base.DialogueFixture.compile

    def args(self, packet=True):
        folder = self.root / "stories/lion_and_mouse_v7"
        folder.mkdir(parents=True)
        (folder / "audio_visual_plan.json").write_text(json.dumps(self.plan))
        takes = self.root / "takes.json"
        takes.write_text(json.dumps(self.takes))
        path = self.root / "packet.json"
        if packet:
            path.write_text(json.dumps(self.compile()))
        return types.SimpleNamespace(
            story="lion_and_mouse_v7",
            sequence_selection=takes,
            v7_packet=path if packet else None,
            out=self.root / "oral_output",
        )

    def test_C42_real_v7_dispatch_without_legacy_manifests(self):
        args = self.args()
        with (
            patch.object(lip_sync.paths, "STORIES", self.root / "stories"),
            patch.object(lip_sync.paths, "REPO", self.root),
            redirect_stdout(io.StringIO()),
        ):
            lip_sync.apply(args)
        self.assertTrue((args.out / "dialogue_receipt.json").is_file())
        self.assertFalse(
            (self.root / "stories/lion_and_mouse_v7/prompt_manifest.json").exists()
        )

    def test_C42_missing_packet_and_changed_selection_fail_explicitly(self):
        args = self.args(False)
        with (
            patch.object(lip_sync.paths, "STORIES", self.root / "stories"),
            self.assertRaisesRegex(SystemExit, "V7 requires"),
        ):
            lip_sync.apply(args)
        args.v7_packet = self.root / "packet.json"
        args.v7_packet.write_text(json.dumps(self.compile()))
        self.takes["takes"]["piece"]["owner_decision"] = "pending"
        args.sequence_selection.write_text(json.dumps(self.takes))
        with (
            patch.object(lip_sync.paths, "STORIES", self.root / "stories"),
            self.assertRaisesRegex(SystemExit, "selection differs"),
        ):
            lip_sync.apply(args)
        self.assertFalse(args.out.exists())
