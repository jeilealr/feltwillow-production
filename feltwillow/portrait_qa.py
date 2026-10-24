"""Measured portrait warnings; no automatic limb, teeth or artistic certification."""
from __future__ import annotations

import cv2
import numpy as np

VERSION = "portrait-warning-metrics-v1"


def region_mask(shape, roi):
    if len(roi) != 4 or not all(np.isfinite(roi)) or not (0 <= roi[0] < roi[2] <= 1 and 0 <= roi[1] < roi[3] <= 1):
        raise ValueError("invalid normalized portrait region")
    h, w = shape[:2]
    x0, y0, x1, y1 = np.asarray(roi) * [w, h, w, h]
    mask = np.zeros((h, w), dtype=bool)
    mask[int(np.floor(y0)):int(np.ceil(y1)), int(np.floor(x0)):int(np.ceil(x1))] = True
    return mask


def assess_frames(reference, frames, contract):
    """Flag changes against shot-reviewed limits, never infer correct anatomy.

    Limits are supplied with an exact-source reviewer contract. They are not
    universal anatomical tolerances. A low-feature image reports unavailable
    motion evidence instead of a fabricated camera pass.
    """
    reference = np.asarray(reference)
    frames = np.asarray(frames)
    if reference.dtype != np.uint8 or frames.dtype != np.uint8 or frames.ndim != 4 or frames.shape[1:] != reference.shape or reference.ndim != 3 or reference.shape[2] != 3:
        raise ValueError("portrait frames/reference geometry or RGB8 representation differs")
    if not contract.get("reviewer") or contract.get("status") != "reviewed":
        raise ValueError("portrait geometry limits require a reviewed source contract")
    limits = contract["limits"]
    names = {"pixel_delta", "protected_change_fraction", "body_change_fraction", "max_translation_px", "max_scale_delta"}
    if set(limits) != names or any(isinstance(v, bool) or not np.isfinite(v) or v < 0 for v in limits.values()):
        raise ValueError("invalid or incomplete shot-specific portrait limits")
    if limits["pixel_delta"] > 255 or any(limits[n] > 1 for n in ("protected_change_fraction", "body_change_fraction", "max_scale_delta")):
        raise ValueError("portrait limits outside their defined range")
    allowed = region_mask(reference.shape, contract["allowed_change_roi"])
    body = region_mask(reference.shape, contract["body_exclusion_roi"])
    if np.any(allowed & body):
        raise ValueError("portrait face-change and body-exclusion regions overlap")
    protected = ~allowed
    gray = cv2.cvtColor(reference, cv2.COLOR_RGB2GRAY)
    points = cv2.goodFeaturesToTrack(gray, 160, 0.01, 4, mask=protected.astype(np.uint8) * 255)
    records, warnings = [], []
    for index, frame in enumerate(frames):
        changed = np.max(np.abs(frame.astype(np.int16) - reference.astype(np.int16)), axis=2) > limits["pixel_delta"]
        fraction = float(changed[protected].mean()) if protected.any() else 0
        body_fraction = float(changed[body].mean())
        record = dict(frame=index, protected_change_fraction=fraction, body_change_fraction=body_fraction)
        if fraction > limits["protected_change_fraction"]:
            warnings.append(dict(frame=index, kind="portrait_crop_or_protected_change", metric=fraction))
        if body_fraction > limits["body_change_fraction"]:
            warnings.append(dict(frame=index, kind="portrait_intrusion", metric=body_fraction, meaning="new/changed contour in excluded body region; manual identification required"))
        current = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        transform = None
        if points is not None and len(points) >= 8:
            dest, valid, _ = cv2.calcOpticalFlowPyrLK(gray, current, points, None)
            if dest is not None and valid is not None and int(valid.sum()) >= 8:
                keep = valid.ravel() != 0
                transform, inliers = cv2.estimateAffinePartial2D(points[keep, 0], dest[keep, 0], method=cv2.RANSAC)
                if transform is not None and inliers is not None:
                    translation = float(np.linalg.norm(transform[:, 2]))
                    scale = float(np.sqrt(abs(np.linalg.det(transform[:, :2]))))
                    record.update(translation_px=translation, scale=scale, tracked_points=int(inliers.sum()))
                    if translation > limits["max_translation_px"] or abs(scale - 1) > limits["max_scale_delta"]:
                        warnings.append(dict(frame=index, kind="portrait_camera_or_scale_drift", translation_px=translation, scale=scale))
        if transform is None:
            record["motion_measurement"] = "unavailable"
            warnings.append(dict(frame=index, kind="portrait_motion_measurement_unavailable"))
        records.append(record)
    return dict(version=VERSION, status="needs_visual_review" if warnings else "structural_checks_passed", frames=records, warnings=warnings, visual_review="pending; metrics cannot certify limbs, teeth, identity or whole-motion quality")
