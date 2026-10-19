# v7 technical coverage and review report

## Verified

- 52 chronological visual units exist across all 16 audio scenes.
- All 161 authoritative audio line IDs are assigned exactly once; no line is missing or duplicated.
- All 52 planned keyframe paths exist, including the environment-only exact sunset plate.
- Milo and Leo v7 canonical files match their approved v6 source files byte-for-byte.
- All registered v7 audio line and scene files match their manifest SHA-256 hashes; registered location plates exist and match their hashes.
- Scene images use the registered v7 location plates and deterministic foreground composition. No rejected regenerated background is used.
- Milo’s environment scale direction and the corrected Leo paw description appear in the review rules and prompts.

## Still needs visual approval

- All scene frames are candidates, not approved video frames.
- Leo appears in 29 candidate units. Compare each full-size image to the v6 canonical for face, mane silhouette, palette, body shape, and rounded golden-cream paws. The owner flagged identity drift; reject any frame that departs from the canonical, including grey or sharp nail shapes.
- The v7 action atlases, generated props, and generated character layers remain pending owner review.
- Inspect transparent edges, anatomy, contact, same-depth 1:4 scale, and adjacent-frame continuity before promotion.

See [the full sequence](../VISUAL_SEQUENCE.md), [contact sheet](contact_sheets/v7_sequence_review.svg), [character staging rules](../CHARACTER_STAGING.md), and [source of truth](../SOURCE_OF_TRUTH.md).
