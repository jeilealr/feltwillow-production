"""Offline loader arguments are observed at mocked library call boundaries."""

import sys, types, unittest
from unittest.mock import Mock, patch
from feltwillow import wan


class OfflineLoaderTests(unittest.TestCase):
    def test_C51_frozen_loaders_propagate_cache_only_no_download(self):
        vae = Mock()
        pipeline = Mock()
        pipe = Mock()
        pipeline.from_pretrained.return_value = pipe
        diffusers = types.SimpleNamespace(
            AutoencoderKLWan=vae, WanImageToVideoPipeline=pipeline, WanPipeline=pipeline
        )
        torch = types.SimpleNamespace(float32="float32", bfloat16="bfloat16")
        with patch.dict(sys.modules, {"torch": torch, "diffusers": diffusers}):
            wan.load("i2v", 5, local_files_only=True)
        self.assertTrue(vae.from_pretrained.call_args.kwargs["local_files_only"])
        self.assertTrue(pipeline.from_pretrained.call_args.kwargs["local_files_only"])

    def test_lightning_cache_only_applies_to_both_experts(self):
        download = Mock(return_value="/cache/fixture.safetensors")
        with patch.dict(
            sys.modules,
            {"huggingface_hub": types.SimpleNamespace(hf_hub_download=download)},
        ):
            wan.lightning_lora(local_files_only=True)
        self.assertEqual(download.call_count, 2)
        self.assertTrue(
            all(call.kwargs["local_files_only"] for call in download.call_args_list)
        )

    def test_C43_installed_config_rejects_unknown_class_and_expanded_endpoints(self):
        import tempfile, json, hashlib
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "pipeline.py"
            source.write_text("synthetic inspected source")
            config = root / "model_index.json"
            for cls, expand in [
                ("UnknownPipeline", False),
                ("WanImageToVideoPipeline", True),
            ]:
                config.write_text(
                    json.dumps({"_class_name": cls, "expand_timesteps": expand})
                )
                ref = dict(
                    endpoint_supported=True,
                    expand_timesteps=False,
                    source_path=str(source),
                    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    config_path=str(config),
                    config_sha256=hashlib.sha256(config.read_bytes()).hexdigest(),
                    model_revision=wan.REVISIONS["i2v"],
                )
                with (
                    self.subTest(cls=cls, expand=expand),
                    self.assertRaises(ValueError),
                ):
                    wan.verify_endpoint_environment(ref)

    def test_C51_missing_video_executable_is_explicit(self):
        from feltwillow import local_video

        with (
            patch.object(local_video.shutil, "which", return_value=None),
            patch.object(local_video.sys, "executable", "/nonexistent/python"),
        ):
            with self.assertRaisesRegex(ValueError, "unavailable"):
                local_video.executable("ffmpeg")
