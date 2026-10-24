"""Bounded, reference-to-frame muzzle tracking for closed-mouth source takes.

This supports small in-plane motion, not turns or newly visible face surfaces.
Uncertain frames are rejected; no fixed-position fallback is permitted.
"""
from __future__ import annotations

import cv2
import numpy as np

VERSION = "tracked-mouth-delta-v1"


class TrackingError(ValueError):
    pass


class MouthTracker:
    def __init__(self, closed, opened, mask, roi):
        self.closed = np.asarray(closed, dtype=np.float32)
        self.delta = np.asarray(opened, dtype=np.float32) - self.closed
        self.mask = np.asarray(mask, dtype=np.float32).reshape(closed.shape[:2])
        self.gray = cv2.cvtColor(self.closed.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        h, w = self.gray.shape
        if not (len(roi) == 4 and 0 <= roi[0] < roi[2] <= 1 and 0 <= roi[1] < roi[3] <= 1):
            raise ValueError("Invalid normalized mouth ROI")
        x0, y0, x1, y1 = np.array(roi) * [w, h, w, h]
        # Surrounding muzzle texture, including nose/cheek features but excluding
        # the edited mouth. Keep the window local to avoid following background.
        px, py = max(12, (x1-x0)*0.7), max(12, (y1-y0)*0.9)
        support = np.zeros((h, w), np.uint8)
        support[max(0, int(y0-py)):min(h, int(y1+py)),
                max(0, int(x0-px)):min(w, int(x1+px))] = 255
        excluded = cv2.dilate((self.mask > 0.01).astype(np.uint8), np.ones((7, 7), np.uint8))
        support[excluded != 0] = 0
        self.support = support
        self.points = cv2.goodFeaturesToTrack(self.gray, 160, 0.01, 4, mask=support, blockSize=5)
        if self.points is None or len(self.points) < 8:
            raise TrackingError("Too few muzzle features; review calibration/crop")
        self.size = (w, h)

    def locate(self, frame):
        current = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        if current.shape != self.gray.shape:
            raise ValueError("Source/calibration geometry differs")
        lk = dict(winSize=(21, 21), maxLevel=3,
                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
        dest, forward, _ = cv2.calcOpticalFlowPyrLK(self.gray, current, self.points, None, **lk)
        if dest is None:
            raise TrackingError("Muzzle optical flow unavailable")
        back, reverse, _ = cv2.calcOpticalFlowPyrLK(current, self.gray, dest, None, **lk)
        if back is None:
            raise TrackingError("Reverse muzzle optical flow unavailable")
        fb = np.linalg.norm(back-self.points, axis=2).ravel()
        valid = (forward.ravel() != 0) & (reverse.ravel() != 0) & (fb < 1.5)
        if valid.sum() < max(8, len(self.points)*0.5):
            raise TrackingError("Insufficient consistent muzzle tracks (occlusion or motion)")
        source = self.points[valid, 0]
        target = dest[valid, 0]
        matrix, inliers = cv2.estimateAffine2D(source, target, method=cv2.RANSAC,
                                                    ransacReprojThreshold=3.0, maxIters=2000)
        if matrix is None or inliers is None:
            raise TrackingError("Muzzle transform unavailable")
        keep = inliers.ravel().astype(bool)
        ratio = float(keep.mean())
        if keep.sum() < 8 or ratio < 0.65:
            raise TrackingError(f"Muzzle features do not share one reliable transform ({keep.sum()}/{len(keep)}, ratio={ratio:.2f})")
        # An inlier cluster on one edge cannot constrain the whole mouth.
        if np.any(np.ptp(source[keep], axis=0) < np.ptp(self.points[:, 0], axis=0)*0.45):
            raise TrackingError("Muzzle track has insufficient spatial coverage")
        singular = np.linalg.svd(matrix[:, :2], compute_uv=False)
        if np.linalg.det(matrix[:, :2]) <= 0 or singular.min() < 0.8 or singular.max() > 1.25:
            raise TrackingError("Face deformation exceeds bounded muzzle tracker")
        scale = float(np.sqrt(np.linalg.det(matrix[:, :2])))
        angle = float(np.degrees(np.arctan2(matrix[1, 0], matrix[0, 0])))
        if not 0.8 <= scale <= 1.25 or abs(angle) > 25:
            raise TrackingError("Face turn/scale exceeds bounded muzzle tracker")
        warped_mask = cv2.warpAffine(self.mask, matrix, self.size)
        if warped_mask.sum() < self.mask.sum()*scale**2*0.98:
            raise TrackingError("Mouth leaves the frame")
        aligned = cv2.warpAffine(current, cv2.invertAffineTransform(matrix), self.size)
        compare = self.support != 0
        a, b = self.gray[compare].astype(float), aligned[compare].astype(float)
        corr = float(np.corrcoef(a, b)[0, 1]) if b.std() > 1 else 0.0
        if not np.isfinite(corr) or corr < 0.70:
            raise TrackingError("Muzzle appearance changed or is occluded")
        # Catch an occluder covering just the mouth while the cheeks still track.
        residual = aligned.astype(float)-self.gray.astype(float)
        residual -= np.median(residual[compare])
        mouth = self.mask > 0.2
        occluded = float(np.mean(np.abs(residual[mouth]) > 55))
        if occluded > 0.25:
            raise TrackingError("Mouth appearance changed or is occluded")
        error = float(np.median(np.linalg.norm((source @ matrix[:, :2].T + matrix[:, 2])-target, axis=1)[keep]))
        if error > 1.5:
            raise TrackingError("Muzzle reprojection error exceeds 1.5 pixels")
        return matrix, warped_mask, dict(inlier_ratio=ratio, inliers=int(keep.sum()),
                                         residual_px=error, appearance_correlation=corr,
                                         occluded_fraction=occluded, transform=matrix.tolist())

    def composite(self, frame, amount):
        if not np.isfinite(amount) or not 0 <= amount <= 1:
            raise ValueError("Mouth activation must be within [0, 1]")
        if amount == 0:
            return frame.copy(), {"status": "unchanged", "amount": 0.0}
        matrix, mask, details = self.locate(frame)
        # Premultiply before warping so interpolation never leaks unrelated
        # calibration differences outside the original mouth mask.
        delta = cv2.warpAffine(self.delta*self.mask[:, :, None], matrix, self.size)
        result = np.clip(np.rint(frame.astype(np.float32)+amount*delta), 0, 255).astype(np.uint8)
        result[mask == 0] = frame[mask == 0]
        return result, dict(status="tracked", amount=float(amount), **details)


def composite_frames(frames, closed, opened, mask, roi, amounts, *, diagnostic=False):
    """Preserve boundaries/silence; reject active uncertainty before encoding.

    Diagnostic mode preserves rejected frames and reports them for comparison.
    Production mode raises, so a partial repair cannot enter an edit.
    """
    if len(frames) != len(amounts):
        raise ValueError("One activation is required per source frame")
    tracker = None
    results, records = [], []
    for index, (frame, amount) in enumerate(zip(frames, amounts)):
        if index in (0, len(frames)-1) or amount == 0:
            result, record = frame.copy(), {"status": "unchanged", "amount": 0.0}
        else:
            try:
                if tracker is None:
                    tracker = MouthTracker(closed, opened, mask, roi)
                result, record = tracker.composite(frame, amount)
            except TrackingError as exc:
                if not diagnostic:
                    raise TrackingError(f"Frame {index}: {exc}") from exc
                result, record = frame.copy(), {"status": "rejected", "amount": float(amount), "reason": str(exc)}
        results.append(result)
        records.append(dict(frame=index, **record))
    return np.asarray(results), {"version": VERSION, "frames": records,
                                 "rejected_active_frames": sum(r["status"] == "rejected" for r in records)}
