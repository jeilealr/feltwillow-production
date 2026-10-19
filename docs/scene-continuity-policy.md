# Scene/location continuity policy

V7 is authored from audio lines and visual beats. An audio chapter is not one physical location or one camera. Choose the background relationship deliberately for each beat; character identity and causal world/prop state persist in every case.

| Choice | What stays consistent | What may change |
|---|---|---|
| `independent_scene` | Forest world/style, character identity/anatomy, narrative time and prop custody | Local forest place, camera, composition and visible landmarks; no inherited master panorama |
| `same_place_new_view` | Particular place/geographic relationships, physical staging and light | Camera height, angle, framing, focus; no automatic pixel lock |
| `locked_background` | One declared background asset, camera/crop, landmarks, support plane and light | Actor pose/gaze/expression and explicitly recorded story events |

These describe relationships between beats. A pair or multi-key action inside one beat still requires a coherent local setup. An exact background lock does not imply reusing the whole actor image or forcing shared start/end boundaries between lines.

## Current opening direction

- S01-L001 establishes the wide peaceful forest and Milo as an explorer.
- S01-L002 has independent berry-thicket, hollow-log-clearing and winding-woodland-path compositions. The log need not sit across the canonical stream.
- S01-L003 uses a distinct deeper woodland setting to communicate distance from home.
- S01-L004 cuts between seeds beneath tall grass, berries beside water, and an acorn glade. Only the berry clause requires a stream. Do not force the river on the right, mountains, opposite-bank trunk or master framing into the other shots.
- S02 can use independent forest/evening compositions, while light progresses consistently and Milo retains the same acorn until placing it beside a stone at a stream. A cut never creates a second acorn or changes custody early.
- S03-L001–L005 may cut between route emphasis views. Preserve left safe meadow/right shortcut identity; L004/L005 no longer require shared background or boundary.
- S03-L006–L008 are the first explicit `locked_background` group, `fork_decision`: one fork composition/camera, Milo looks sky → long path → shortcut. Generate/select one shared background; do not separately invent three backgrounds. AI image references do not guarantee identical pixels, so inspect protected background drift before accepting endpoints.
- S03-L009/L010 are Milo close-ups with blurred fork-world backgrounds; the preceding fixed-camera requirement does not automatically extend into them.

Later S05/S06 staging, rear-paw-to-face logic and other causal state groups remain intact unless the owner revises them. Same-place consistency does not silently become an exact-pixel lock.

## Reference-image roles

Declare whether a location reference supplies **style/material only**, **geography/light**, or **exact background/camera**. A style reference does not require its river, mountains, trunk arrangement, crop or landmarks. For the revised opening, no stream-bank image is attached to the independent scene-composition proposal; Milo's approved canonical supplies identity and the prompts describe the felt forest settings.

A planned location view is a camera/world intent, not automatically a separate empty-background generation request. An independent setting may be created directly inside the complete scene image. Generate a separate plate when reuse, an explicit lock or compositing benefits from it. Do not convert the count of planned views into a spending target.

Exact approvals remain scoped to their bytes and original use. Earlier generated outputs and approvals are preserved in the previous-assets index; they do not select images for the revised direction. Background generation, complete scene composition, finished key-image sequences and video approval are separate stages.

## Camera-relative size

Milo's apparent size is camera-relative: greater viewing distance makes him smaller, and closer distance, lens/zoom or cropping can make him larger. Compare size only after accounting for camera distance, lens/zoom, crop, subject depth and pose. At the same camera setup and subject depth, anatomical dimensions and scale relative to local landmarks must remain consistent; pose may change his bounding box. Independent wide shots and portraits do not require the same frame fraction. Record intentional camera/depth changes; do not invent measured distances or diagnose drift from screen size alone.

S03-L006–L008 locks camera and standing depth, so compare stable head/body landmarks against that shared setup. A mismatch there remains a review issue, not a confirmed anatomical defect without this comparison.
