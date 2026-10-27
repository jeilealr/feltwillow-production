"""Build a source-art comparison board without implying owner selection."""

from __future__ import annotations

import hashlib
import html
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
EXPRESSIONS = ROOT / "character/characters/lion_and_mouse_v7"


def scene(name: str) -> Path:
    return SCENES / name


def expression(name: str) -> Path:
    return EXPRESSIONS / name


CARDS = [
    ("S01", "Tiny toothless contact", scene("S01-L004-B03-I03_key_acorn_glade_r005_candidate.png"), scene("S01-L004-B03_key_tiny_toothless_contact_r002_candidate.png"), "Bounded mouth/acorn/hand edit. Check one acorn, support, muzzle and actual tiny no-teeth opening."),
    ("S01", "Tasted, mouth settled", scene("S01-L004-B03-I03_key_acorn_glade_r005_candidate.png"), scene("S01-L004-B03-I04_end_tasted_acorn_r002_candidate.png"), "Bounded edit. Check small notch, closed mouth, hand contact and same actor root."),
    ("S02", "Acorn contact beside stone", scene("S02-L004-B02-I02_key_stone_acorn_contact_r004_candidate.png"), scene("S02-L004-B02-I02_key_ground_beside_stone_contact_r006_candidate.png"), "Bounded correction on the selected contact camera plate. Check actor/stone seams and acorn ground support; no active selection changed."),
    ("S02", "Release beside stone", scene("S02-L004-B02-I03_end_stone_beside_stream_r004_candidate.png"), scene("S02-L004-B02-I03_end_ground_beside_stone_release_r007_candidate.png"), "Bounded release from the same contact camera plate. Check acorn position/custody and contact-to-release join."),
    ("S03", "Fork L002 upward view", scene("S03-L002-B01-I02_end_two_routes_r003_candidate.png"), scene("S03-L002-B01-I02_locked_local_head_r004_candidate.png"), "Fixed accepted L001 r004 body/root and exterior background; head-envelope seam needs native review."),
    ("S03", "Fork L003 screen-left route", scene("S03-L003-B01-I02_end_safe_left_meadow_r003_candidate.png"), scene("S03-L003-B01-I02_locked_local_head_r004_candidate.png"), "Screen-left head turn; exact exterior background; check projection and neck seam."),
    ("S03", "Fork L004 screen-right route", scene("S03-L004-B01-I02_end_short_right_route_r003_candidate.png"), scene("S03-L004-B01-I02_locked_local_head_r004_candidate.png"), "Screen-right head turn; exact exterior background; check projection and neck seam."),
    ("S03", "Fork L005 shortcut", scene("S03-L005-B01-I02_end_shortcut_entrance_r003_candidate.png"), scene("S03-L005-B01-I02_locked_local_head_r004_candidate.png"), "Head pitch; exact exterior background; check projection and neck seam."),
    ("S03", "Fork L007 long-route reconsideration", scene("S03-L007-B01-I02_end_decision_locked_background_r003_candidate.png"), scene("S03-L007-B01-I02_locked_local_head_r004_candidate.png"), "Screen-left turn; fixed body/root; compare against accepted L006 anchor."),
    ("S03", "Fork L008 shortcut reconsideration", scene("S03-L008-B01-I02_end_decision_locked_background_r003_candidate.png"), scene("S03-L008-B01-I02_locked_local_head_r004_candidate.png"), "Screen-right turn; fixed body/root; check final wide-to-portrait cut."),
    ("S05", "Before rear-paw catch", scene("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png"), scene("S05-L008-B01-I01_grounded_approach_r002_candidate.png"), "Check Milo is grounded and approaching Leo's rear paw, with a possible next contact."),
    ("S05", "Rear-paw catch contact", scene("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png"), scene("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r006_candidate.png"), "Targeted toe-to-rear-paw contact before the forward pitch. Check contact and Leo's four-paw topology at native size; r004 remains selected."),
    ("S05", "Forward pitch", scene("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png"), scene("S05-L008-B01-I03_forward_pitch_r002_candidate.png"), "Check contact/support loss and trajectory. A source still is not a motion pass."),
    ("S05", "Grounded nose landing", scene("S05-L009-B01-I04_grounded_nose_landing_r002_candidate.png"), scene("S05-L009-B01-I04_grounded_nose_landing_r004_candidate.png"), "Owner rejected the prior distorted Milo body. New proposal keeps a compact, grounded Milo beside Leo's nose; check full anatomy and roll-to-landing geography."),
    ("S06", "Leo raises head", scene("S06-L001-B01-I01_start_rest_nose_r001_candidate.png"), scene("S06-L001-B01-I02_head_raised_r005_candidate.png"), "Targeted revision retains one Milo at Leo's nose and exact exterior pixels. Check head/mane seam, actor scale and actual rise."),
    ("S06", "Milo scrambles down", scene("S06-L001-B02-I01_scramble_descent_r003_candidate.png"), scene("S06-L001-B02-I01_scramble_descent_r006_candidate.png"), "Owner rejected prior body. New bounded stepping pose excludes Leo's face and protects the exterior. Check Milo's limbs, tail and path from nose to arrival."),
    ("S06", "Front paw ready", scene("S06-L002-B01-I01_front_paw_ready_r002_candidate.png"), scene("S06-L002-B01-I01_front_paw_ready_r004_candidate.png"), "Owner rejected prior body. New one-foreleg pose keeps Leo lying and Milo at the same root; check four Leo paws and arm attachment."),
    ("S06", "Front paw descending", scene("S06-L002-B01-I02_front_paw_descending_r002_candidate.png"), scene("S06-L002-B01-I02_front_paw_descending_r004_candidate.png"), "Owner rejected prior body. New one-foreleg intermediate moves toward the selected block; check attachment, contact and Milo anatomy."),
    ("S06", "Milo freezes", scene("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"), scene("S06-L003-B01-I02_frozen_r002_candidate.png"), "Face-only proposal with fixed actor roots; a same-raster hold remains an honest fallback if reaction is indistinct."),
    ("S06", "Milo worried", scene("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"), scene("S06-L004-B01-I02_worried_r002_candidate.png"), "Face-only proposal; inspect crop and ear/head continuity."),
    ("S06", "Milo humbled", scene("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"), scene("S06-L005-B01-I02_humbled_r002_candidate.png"), "Face-only proposal; inspect continuity and no extra limb."),
    ("S08", "Leo top-right paw repair", scene("S08-L016-B01-I01_single_gentle_clear_r002_candidate.png"), scene("S08-L016-B01-I01_single_gentle_clear_r004_candidate.png"), "Owner found the far front paw still missing in r002. New candidate has a separately visible image-top-right paw; inspect attachment and four-paw count. L016/L017/L018 remain bound to historical r001."),
    ("Mouth", "Milo toothless speech calibration", expression("Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png"), expression("Milo/expressions/milo_portrait_base_3q_default_tiny_open_toothless_r002_candidate.png"), "Auxiliary mouth-only reference, not a dialogue endpoint or selected calibration for every view."),
    ("Mouth", "Leo toothless speech calibration", expression("Leo/expressions/leo_portrait_base_3q_r001_candidate.png"), expression("Leo/expressions/leo_portrait_base_3q_tiny_open_toothless_r002_candidate.png"), "Auxiliary mouth-only reference, not a dialogue endpoint or selected calibration for every view."),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return os.path.relpath(path, REVIEW)


def main() -> None:
    feedback = json.loads((REVIEW / "OWNER_FEEDBACK_20261027.json").read_text())
    accepted = {row["candidate_sha256"] for row in feedback["cards"] if row["owner_feedback"] == "accepted_visual_proposal"}
    rows = []
    body = []
    for group, title, before, after, note in CARDS:
        if not before.is_file() or not after.is_file():
            raise FileNotFoundError(before if not before.is_file() else after)
        before_sha, after_sha = sha(before), sha(after)
        status = "owner_accepted_visual_proposal_pending_technical_binding" if after_sha in accepted else "new_redo_pending_owner_review"
        rows.append({"group": group, "title": title, "before": str(before.relative_to(ROOT)), "before_sha256": before_sha, "candidate": str(after.relative_to(ROOT)), "candidate_sha256": after_sha, "status": status, "note": note})
        body.append(
            f"<section class='{'accepted' if after_sha in accepted else 'pending'}'><h2>{html.escape(group)} · {html.escape(title)}</h2>"
            f"<p>{html.escape(note)}</p><div class='pair'>"
            f"<figure><a href='{html.escape(relative(before))}'><img src='{html.escape(relative(before))}' loading='lazy'></a>"
            f"<figcaption>Current/reference · {before_sha[:12]}</figcaption></figure>"
            f"<figure><a href='{html.escape(relative(after))}'><img src='{html.escape(relative(after))}' loading='lazy'></a>"
            f"<figcaption>{'Owner accepted visual proposal' if after_sha in accepted else 'Revised candidate, awaiting review'} · {after_sha[:12]}</figcaption></figure></div></section>"
        )
    document = """<!doctype html><html lang='en'><meta charset='utf-8'><title>V7 S01–S08 image repair candidates</title>
<style>body{font:16px system-ui;background:#151817;color:#f2efe5;margin:2rem auto;max-width:1500px;padding:0 1rem}a{color:#f6c879}button{padding:.6rem 1rem;font:inherit;border:1px solid #f6c879;background:#30382f;color:#f2efe5;border-radius:6px;cursor:pointer}section{margin:2rem 0;padding:1rem;background:#222724;border-radius:12px}body:not(.show-all) section.accepted{display:none}.pair{display:grid;grid-template-columns:1fr 1fr;gap:1rem}figure{margin:0}img{max-width:100%;height:auto;background:#111}figcaption{color:#bbb;font-size:.85rem;padding:.3rem}p{line-height:1.4}@media(max-width:850px){.pair{grid-template-columns:1fr}}</style>
<h1>Feltwillow V7 · S01–S08 source-image repair candidates</h1>
<p>The owner accepted 19 prior visual proposals and rejected five exact hashes. Those five have new revisions below. Existing selection ledgers have not been rebound, and no generated video or connected-motion join is approved by this board. Connected groups require the same camera/background and stable character identity, root, scale, anatomy and contacts. Click an image for native size.</p>
<p><button type='button' onclick='document.body.classList.toggle("show-all");this.textContent=document.body.classList.contains("show-all")?"Show only five new revisions":"Show all 24 cards"'>Show all 24 cards</button></p>
<p><a href='START_REVIEW.html'>Opening video diagnosis</a> · <a href='CONNECTED_PIXEL_AUDIT.json'>Raw connected still pixel audit</a> · <a href='REPAIR_REVIEW.json'>Machine-readable card hashes</a></p>
""" + "\n".join(body) + "</html>\n"
    (REVIEW / "REPAIR_REVIEW.html").write_text(document)
    (REVIEW / "REPAIR_REVIEW.json").write_text(json.dumps({"schema": "feltwillow.repair-review.v1", "cards": rows}, indent=2) + "\n")
    print(f"wrote {len(rows)} comparison cards")


if __name__ == "__main__":
    main()
