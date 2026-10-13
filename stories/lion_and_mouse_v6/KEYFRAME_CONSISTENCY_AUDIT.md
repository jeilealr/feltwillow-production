# v6 keyframe continuity audit

**11 October 2026. Status: corrective plan; no candidate image is approved for video by this audit.** The original 92 PNGs were unchanged when this audit was first written. Later revisions replaced several active candidates; their old bytes were removed from the working tree after revision; Git history and the hash ledger preserve provenance. Only the current contact sheets in `keyframes/.review/contact_sheets/current/` should be used for review. This audit compares the contact sheets, named full-size images, canonicals, `staging_plan.json`, `keyframe_plan.json`, and the video sequence. It identifies failures that a valid planning file cannot detect in generated pixels.

## Second image-audit implementation (13 October 2026)

The second audit's user-reported failures were recorded against the exact active PNG hashes in `keyframe_visual_reviews.json`: `s10_p02` (Leo missing a front-left paw), `s14_p06` (Milo's visible size jumps against the same-depth `trap_morning:wide` target), `s15_p04` (global color and character identity drift), and `s08_p04` (carry-over orange cast and identity drift; full-size inspection also observed an open mouth at a production boundary). These four current candidates remain rejected. Historical rejected hashes for `s14_p04`/`s14_p05` remain preserved.

Ten camera-plan-stale records are marked `supersede_for_camera_plan`, not visually rejected: `s08_p02`, `s08_p03`, `s08_p05`, `s12_p02`, and `s15x_p01` through `s15x_p06`. Their current bytes cannot be used as fresh-camera candidates. The other 82 active candidates are pending review. The six owner-liked frames listed in `KEYFRAME_REVIEW.md` remain preserved. The [second-audit implementation report](../../docs/audits/lion-and-mouse-v6-second-image-audit-remediation-2026-10-13.md) records every active candidate hash and disposition; the [setup-anchor packet](../../docs/audits/lion-and-mouse-v6-size-anchor-review-2026-10-13.md) records six approved replacement anchors and three new-calibration requests; other families remain unselected.

No replacement keyframes have been generated yet. The owner has hash-approved the current Milo canonical and hunter-net prop as replacement-generation inputs, and six required setup anchors. Three additional target families need fresh calibration candidates before their five dependent replacement frames can be generated. The consolidated atlases remain pending and are not direct inputs to these replacements. Video rendering is unsafe until the stale frames are replaced, all active endpoints receive complete hash-bound visual/anatomy review, and all reference/runtime gates pass.

## Findings and disposition

| Evidence | Finding | Disposition before video |
|---|---|---|
| `s01_p01` → `s01_p03` | Both use the full `stream_afternoon` plate. Milo's planned standing-equivalent heights are 0.171 and 0.159 of frame height: about a 7% decrease for a modest depth move. In the prior images, `s01_p01` was visibly much larger than `s01_p03`. The new `s01_p01` r03 brings the two closer, but its pixel scale and independently generated grass, stones and light still require full-size comparison. | Review both current PNGs at the same crop; verify that a modest walk does not create a large apparent shrink. For a moving clip, use the exact same approved plate/crop under both endpoints. |
| `s03_p03` → `s03_p04` | Both are 1.6× medium views of the fork, with planned heights 0.292 and 0.280. The shift should be small. These are a useful fixed-camera pair for checking Milo's ear/head/torso proportions. | Measure both at the registered crop and compare the boulder/path scale. A pose change cannot resize Milo's head. |
| `s04_p02`, `s04x_p02`, `s09_p01` | The first and last are full-plate shortcut views; their planned Milo heights are 0.167 and 0.150. `s04x_p02` is a 1.6× crop of the same location and has a planned height of 0.267, exactly 1.6× `s04_p02`. The older candidates made Milo too large against the branch, rock, tree geometry and stump. New active revisions are `s04_p02` r03, `s04x_p02` r03 and `s09_p01` r02; these remain unapproved. A crop can make him occupy more screen space; it cannot change his size relative to objects at the same depth. | Measure the actual silhouettes and same-depth landmarks across the revised frames. Use a single approved physical Milo scale anchor; do not infer scale from frame fraction alone. |
| `s09_p02` | Milo in the original wide home view was larger than the glowing burrow entrance, so he could not plausibly enter it. A smaller r02 candidate now places him below the entrance height on the same path. | Compare the new r02 with the approved home plate, doorway opening and adjacent movement before approving. |
| Scenes 04–06 action chain | Scene 04 p02 made Milo too large, and p04 appeared to turn him back toward a different path. Scene 05 lacked a readable trip-to-roll bridge, while Scene 06 p01 had an extra arm and p03 cropped Leo's mane. Current revisions and three new bridge images correct those specific compositions. | Review the full-size current Scene 04–06 PNGs in the order of `video_boundary_plan.json`. Confirm one rightward path, stable physical scale, exactly two Milo arms, complete mane, and clear paw-to-nose contact before animation. |
| Scenes 05 and 07 dialogue views | The earlier Scene 05 Leo close view kept a sharp background; Scene 07 had only medium two-shots despite dialogue close-up direction in the creation rules. Current Scene 05 close r03 and the two new Scene 07 speaker portraits use the established Great Tree setting with strong background blur and complete ears/mane. | Treat each portrait as an intentional camera cut. Compare facial identity with canonicals and keep its closed-mouth boundary fixed during later character-only lip-sync. The medium shots continue to establish shared physical scale. |
| `s12_p01` → `s12_p04` | The planned 0.286 medium view becomes a 0.141 wide view, combining a camera change with a real move farther down the path. The wide-to-wide `s12_p03` → `s12_p04` target goes 0.176 → 0.141 (about 20% smaller). | This larger reduction is narratively justified only if Milo visibly travels into depth. Do not interpolate directly across the medium-to-wide camera cut. |
| Scene 13 storyboard and `s13_p01` | The six-panel storyboard draws Milo too large in its establishing view beside the trapped lion and path landmarks. The old `s13_p01` r01 was roughly twice its 0.191 wide-frame standing-equivalent target; its r02 replacement is closer to that target but unapproved. Leo is lying, so his flattened pose height cannot validate the ratio; the closer two-shots need a head/mane/paw comparison at the registered crop. | Reject the storyboard as a scale reference. Review new `s13_p01` r02 against the approved plate and adjacent shots; measure the closer frames against a pose-aware lion anchor before deciding whether they need revision. Keep the storyboard only for beat and camera composition. |
| `s14_p04`/`s14_p05` r01 | The original one-character rope-detail PNGs visibly include Leo. His longer-muzzled face and loose mane differ from the accepted curly felt canonical and adjacent trapped-lion views. | **Rejected r01 hashes remain blocked.** New r02 one-animal inserts keep Leo off camera. Old PNG bytes were removed from the working tree; their hashes remain in the plan's `superseded` ledger. The r02 pair still needs full-resolution owner review for Milo identity, strand state, scale, plate/crop and adjacent continuity. |
| Scenes 05–08, 10–11, 13–15 | Continuous locations and actor relationships are planned, but individually generated backgrounds and faces may redraw. Scene 14 shows that prompt/reference presence alone does not prove exact identity. | Compare adjacent endpoints on the same plate/crop, including tree roots, trap net, paw contact and character head size. A scene number or audio track boundary does not itself justify a spatial jump. |

## Why the errors passed

`production/staging_contract.py` checks the **metadata equation**, walkable-zone coordinates, cast ratio and file references. It does not inspect the rendered PNG, count visible animals, compare Leo's facial anatomy, or measure Milo against a branch or boulder. The earlier `production/keyframe_plan.py` also multiplied solo-shot height prompts by 0.55 while leaving a different QA target in parentheses. That undocumented correction made one record contain two size instructions. It has been removed for future prompts; existing generated-image prompts remain as immutable provenance.

The Scene 14 insert prompts said “exactly ONE animal” but also described Leo trapped under the net. Leo's canonical was not attached because the staging record contained only Milo. This gave the model contradictory content and no Leo identity authority. Future one-animal insert prompts now explicitly keep Leo off camera. Current PNGs and their historical prompts are not silently rewritten.

The dialogue close-up format was documented, but the first keyframe pass favored action coverage and its generator did not encode strong plate blur for dialogue portraits. That let medium two-shots stand in for speaker portraits and left the Scene 05 close background sharp. The current generator includes explicit portrait framing and strong blur when a close view has a recorded character speaker. It still cannot prove the resulting pixels match; the owner must inspect each face.

The contact sheets are indexed by record ID, with supplemental `x` frames appended after overview frames. That is **not** always playback order. Long voice lines also need word-level cut placement. The [video boundary plan](video_boundary_plan.json) now names chronological frame order, scene start/end images and every camera-cut versus same-view transition. It is a planning contract, not a render-ready clip manifest.

## Mandatory acceptance rules for v6 and later stories

1. **One physical scale per character and setup.** Establish a neutral same-depth lineup and at least one owner-approved character-on-plate anchor for each recurring location/camera family before dependent images. Record the anchor image hash, contact point, view/crop and measured ear-to-foot (Milo), mane-top-to-front-paw (Leo), head width and one nearby **same-depth** landmark size. Distant tree crowns or horizon objects are not valid same-depth rulers. Until an anchor is accepted, planned numeric heights are targets, not evidence that the images pass.
2. **Fixed camera and modest movement.** For the same plate/crop, compute the next standing-equivalent height from the recorded contact depth. Adjacent frames should match that value within 10% after allowing for measurement uncertainty; a larger observed change requires a documented depth move or camera change. Check stable head, mane, ear and paw dimensions even when sitting, lying or running changes the pose box. `s01_p01`/`s01_p03` is the model for a modest move; a dramatic recession such as `s12_p03`/`s12_p04` needs visible travel along the path.
3. **Camera moves are explicit.** A crop changes apparent screen fraction by the registered magnification; it does not enlarge the animal relative to a branch, stone, root or other object on the same ground plane. A wide-to-medium change defaults to a cut. A moving zoom needs a separately recorded camera path, locked plate geometry and reviewed start/end views; never ask a video model to invent the missing view.
4. **Two-character anatomy.** At equal depth/camera, Milo's upright standing-equivalent height now targets 0.25 of Leo's quadrupedal mane-to-front-paw height, with a 0.22–0.28 review range. This supersedes the earlier 0.40 target and requires fresh visual review; a metadata pass does not validate old PNGs. When Leo lies under the trap net, compare his head/mane/paw dimensions with his own standing anchor and the net, then compare Milo with him at their documented depths. Do not compare only the flattened lying silhouette height; do not shrink Leo to make Milo readable.
5. **Environment and identity gate.** Compare each candidate side by side with its canonical, approved plate and adjacent same-setup endpoint at full resolution. Confirm visible animal count; Leo's muzzle, eye placement, ears, curly brown mane and tawny felt texture; Milo's grey felt body, green eyes, ears and torso; fixed landmark/crop/lighting; same-depth landmark ratios; valid support contacts, net state and occlusion. Any failed item blocks that PNG as a video endpoint. A text prompt, reference list, JSON validator or owner review of a contact sheet alone cannot certify those pixels.
6. **Boundary continuity.** Every audio scene has explicit start and end images. Only joins explicitly marked `shared_boundary_candidate` may reuse the exact previous end PNG as the next start PNG. At other joins, use a cut or a separately planned transition. Within a scene, `camera_cut` means a deliberate change of view of the same registered location; `same_view_motion_candidate` still requires image-to-image landmark, character-size and identity approval before animation. Never morph between unrelated camera crops or independently redrawn places as though they were one continuous physical take.

For exact plate pixels, the dependable production method is a locked approved plate/crop with reviewed isolated character/prop layers or a focused edit of an accepted same-setup endpoint. Independently generated whole frames should be treated as candidates until a full-resolution match proves continuity. Narrator audio remains voice-over; lip-sync applies only to Milo or Leo dialogue.

`python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6` is the pre-video gate. It currently fails by design: `keyframe_visual_reviews.json` has no approvals. Its known-rejection ledger preserves the two r01 hashes; the active r02 images are new, unapproved candidates. For each accepted image, the reviewer must record the exact PNG SHA-256, reviewer/date, approved size anchor and measured evidence, plus explicit passes for identity, plate, anatomy/landmark scale, grounding, animal count, world state and adjacent continuity. The script checks evidence and staleness; it cannot decide whether a face truly matches the canonical.

**Next visual work:** review the revised Scene 14 r02 pair and measure/correct any failed scale pairs above, then run the same full-size gate over all 96 active images before rendering. This document does not authorize use of unreviewed frames.

## 13 October 2026 remediation update

The image-generation audit dated 2026-10-13 was applied to the current branch.
Approved character/location masters and the six owner-liked frames were left
unchanged. The current generation contract is described in
[`../../docs/keyframe-regeneration.md`](../../docs/keyframe-regeneration.md).

- **Active inventory:** removed the unreferenced `s07_p03_r03_candidate.png`.
  The declared `s13_p06_r02_candidate.png` bytes were absent from the checkout
  and Git history, so the active record and review index now point to the exact
  recoverable `s13_p06_r01_candidate.png` bytes with a commit/blob locator. The
  missing r02 remains recorded as unavailable history. Contact sheets were
  rebuilt; the root PNG set, active plan and current manifest agree.
- **Historical sources:** current regeneration inputs are now derived from the
  approved plate/crop and actor canonicals rather than recursive generated
  frames. Seven appended generated-image-cache path lines were moved to labeled
  provenance records; no cache path remains an actionable reference. The
  contract now recovers 35 historical inputs through exact Git locators; seven
  old input paths and 51 superseded candidate revisions still lack recoverable
  bytes. They are reported as historical gaps and are never promoted to current
  generation inputs.
- **Source locks:** future prompts include actor-specific identity constraints,
  one staging-derived anatomical height per visible actor, location lighting
  clauses, explicit camera family, and closed boundary-mouth policy. Great Tree
  dusk clauses preserve cool ambient light and the fixed warm rim direction;
  they prohibit global orange grading. The contradictory `tree_day` wording is
  corrected.
- **Approval state:** Milo's revised body canonical and combined atlas remain
  pending owner hash-bound review. Acorn/net prop designs and the 29 distinct
  size-anchor families are not marked approved by this remediation. Regeneration
  stays blocked until required authorities are approved and hash-bound.
- **Camera coverage:** Scene 08 restores speaker portraits, Scene 12 p02 is a
  Milo portrait cut, Scene 15 alternates speaker portraits, and Scene 16 wide
  frames share exact staging and one anchor family ID. Ten active candidates
  whose current crop/view differs from the new staging are marked stale pending
  a separately saved revision.
- **Review and runtime:** all 96 active candidates still need full-size,
  hash-bound visual review. The runtime preflight remains fail-closed; no image
  or video approval was invented. The reference, visual, staging, inventory and
  runtime gates are documented and exercised by tests.
