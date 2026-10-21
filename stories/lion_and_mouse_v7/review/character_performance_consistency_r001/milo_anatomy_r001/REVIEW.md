# Milo anatomy consistency review r001

Owner approves the depicted poses and acting. Anatomy congruence, prop fit and locked-shot suitability remain separate conditions. Exact PNGs and statement are in OWNER_ACCEPTANCE.json; no source image or creation receipt was altered.

The owner-named images map to `milo.acorn.pick_hold.3q:hold` (S01-L004-B03-I02) and `milo.harvest.berries.3q:default` (S01-L004-B02-I01). Both current sources were opened at native resolution. The acorn-holding image shows a more dominant head relative to the torso. Downward head pitch changes the projected crown/chin and hides the neck; the berry pose has an upward head angle and longer readable chest. Camera/lens/depth is unknown for both, so the difference cannot honestly be certified as zoom alone, nor recovered as a precise three-dimensional anatomical defect.

Verdict: **suspected head/torso inconsistency, needs matched-view review**, rather than a congruence pass. The pose and identity remain liked/selected. No repair generation is authorized or performed.

## Scale-controlled screening

Comparison (comparison image unavailable; no fabricated evidence) uniformly scales each entire source to the same approximate skull-crown-to-sole height, excluding ears from the height definition. Original PNG bytes are untouched. Manual crown/chin/sole landmarks have roughly ±20-pixel uncertainty and are recorded in PROJECTED_LANDMARKS.json. Approximate projected head fractions are about 0.36–0.38 for the berry/reference poses versus 0.43 for the acorn-holding pose. These are screening observations, not a universal anatomical target: head pitch and perspective remain uncontrolled. Ear tips, tail and raised-hand extent do not set actor scale.

Only these four references received the annotated matched-display comparison. Other generated poses retain their existing visual notes but have not received equivalent anatomy measurement/certification. All 22 current performance PNGs are indexed for prospective review; no automatic visual pass is inferred.

## Whole-story enforcement

The authored `character_performance_library.json` now contains one Milo anatomy policy: canonical identity remains unchanged; the owner-preferred berry inspection pose anchors comparable body proportions. The policy forbids independent head/body scaling and allows only uniform whole-actor staging scale. Every proposed/generated view must separately check skull/torso, ears, neck transition, limb lengths and support contacts at compatible angle/articulation. A differently framed portrait may be larger on screen. A shared camera/depth setup must retain root and anatomical scale.

Per-variant `anatomy_review` is bound to exact image and reference hashes. Planning remains valid with reviews pending; image readiness and dry proposals report missing anatomy review even after owner pose/acting selection. A claimed matched review needs an evidence file, method and current exact source hashes. The gate checks review evidence consistency, not anatomy from pixels automatically. Generative guidance cannot guarantee identical anatomy. Reviewed alpha-layer reuse can preserve pixels under uniform scale; new perspective/action variants still need review. Known body-facing errors remain separate technical-use blockers.

## Acorn fit

No isolated approved v7 acorn design was found in the active location props folder (it contains a README). Existing poses contain empty grip spaces, so fit is **unverified**. See PROP_FIT.json. Before scene readiness, bind one exact-hash acorn design and size relative to Milo, test the actual grip/contact/occlusion for each action phase and preserve custody events. Do not enlarge hands or shrink the prop independently from shot to shot to make a pose work. A contact preview or scene image will be a separate concrete authorized operation.
