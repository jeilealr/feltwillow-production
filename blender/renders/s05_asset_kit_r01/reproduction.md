# Local reproduction

Run from the workspace parent (`/Users/lealroja/Documents/feltwillow`). Blender execution required an approved sandbox escalation on this host. No new add-ons were installed.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python feltwillow-production/blender/scripts/audit_s05_asset_kit_r01.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python feltwillow-production/blender/scripts/build_s05_asset_kit_r01.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python feltwillow-production/blender/scripts/check_s05_asset_kit_r01.py
python3 feltwillow-production/blender/scripts/boards_s05_asset_kit_r01.py
```

The build refuses to overwrite the existing sample; it already used the twelve-render local budget. Do not rerun it as part of this handoff. Audit/check are read-only with respect to Blender inputs; their reports can be regenerated. Bulk downloads are preserved in ignored work storage. Intake checks are offline metadata/hash checks, not legal clearance or visual approval; exact results and pending records are included.
