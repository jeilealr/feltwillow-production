"""Review-bound 2D continuity checks; no physical lens or anatomy inference."""

from __future__ import annotations
import math


def validate_geometry(unit, uses, reviews):
    if unit.get("continuity_strength") != "camera_locked":
        return
    anchor = None
    for use in uses:
        evidence = reviews.get(use["id"], {}).get("geometry", {})
        if evidence.get("status") != "reviewed" or not evidence.get("reviewer"):
            raise ValueError(use["id"] + ": reviewed 2D camera/root geometry required")
        if (
            evidence.get("source_sha256") != (use.get("source") or {}).get("sha256")
            or evidence.get("fit_sha256") != (use.get("fit") or {}).get("pixel_sha256")
            or not evidence.get("source_sha256")
        ):
            raise ValueError(use["id"] + ": geometry image/fit changed")
        if evidence.get("camera_and_crop_lock") != unit.get("camera_and_crop_lock"):
            raise ValueError(use["id"] + ": camera/crop mismatch")
        observed = evidence.get("observed", {})
        for field in ("root_xy", "body_extent_wh"):
            values = observed.get(field)
            if (
                not isinstance(values, list)
                or len(values) != 2
                or any(
                    isinstance(v, bool)
                    or not isinstance(v, (int, float))
                    or not math.isfinite(v)
                    for v in values
                )
            ):
                raise ValueError("finite native 2D landmarks required")
        if (
            min(observed["body_extent_wh"]) <= 0
            or not observed.get("protected_background_pixel_sha256")
            or not observed.get("canvas_wh")
            or not observed.get("crop_xywh")
        ):
            raise ValueError("background/canvas/crop/body observations required")
        if anchor is None:
            anchor = observed
        elif any(
            observed.get(k) != anchor.get(k)
            for k in (
                "root_xy",
                "body_extent_wh",
                "protected_background_pixel_sha256",
                "canvas_wh",
                "crop_xywh",
            )
        ):
            raise ValueError(
                use["id"]
                + ": locked root/body/background/canvas/crop differs; repair source or author an explicit new setup"
            )
