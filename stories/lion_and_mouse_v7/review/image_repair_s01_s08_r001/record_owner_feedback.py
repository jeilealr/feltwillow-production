"""Freeze the owner's exact-hash feedback on the 24-card r001 review board."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REJECTED = {
    "d77e4ab28699": "S05 landing: Milo body wrong",
    "fba0e09ecdc0": "S06 front paw descending: Leo/Milo body wrong",
    "a5c471fca634": "S06 front paw ready: Leo/Milo body wrong",
    "aa65306fa37d": "S06 scramble: Leo/Milo body wrong",
    "b08932b0a78d": "S08 L016: image-top-right Leo paw still missing",
}


def main():
    prior = json.loads((HERE / "REPAIR_REVIEW.json").read_text())
    if len(prior["cards"]) != 24:
        raise ValueError("feedback applies to the prior 24-card board only")
    rows = []
    found = set()
    for card in prior["cards"]:
        h = card["candidate_sha256"]
        matches = [prefix for prefix in REJECTED if h.startswith(prefix)]
        if len(matches) > 1:
            raise ValueError(h)
        if matches:
            found.add(matches[0])
        rows.append({
            "title": card["title"],
            "candidate_path": card["candidate"],
            "candidate_sha256": h,
            "owner_feedback": "rejected_for_revision" if matches else "accepted_visual_proposal",
            "reason": REJECTED[matches[0]] if matches else "Owner said the other new candidates are okay.",
            "scope": "source_image_visual_feedback_only; no video, join, mouth_tracking_or_final_film_pass",
        })
    if found != set(REJECTED):
        raise ValueError(f"missing feedback hashes: {set(REJECTED) - found}")
    record = {
        "schema": "feltwillow.owner-image-review-feedback.v1",
        "date": "2026-10-27",
        "source": "owner message in current session naming five failed card SHA prefixes and approving the others",
        "prior_board_card_count": len(rows),
        "accepted_visual_proposals": sum(r["owner_feedback"] == "accepted_visual_proposal" for r in rows),
        "rejected_for_revision": len(REJECTED),
        "cards": rows,
    }
    (HERE / "OWNER_FEEDBACK_20261027.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
