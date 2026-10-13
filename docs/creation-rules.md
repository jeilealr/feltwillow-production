# Creation rules: scripts, images and video

Spatial placement, depth, support surfaces and contact review follow the canonical [spatial staging and grounding policy](spatial-staging-consistency.md). CR-27 below is the concise production gate; setup-level exceptions and metadata live in each story visual bible.

Reusable policy for active stories. The detailed examples below preserve the v4-era
history and must be interpreted within each story's own current visual bible and
approved assets. For Lion and Mouse v6, its story-local bible and approved v6
canonicals are authoritative; v4 paths and identity roots are not active inputs.
Historical experiments in [prompting.md](prompting.md) remain evidence, but do not
override a story's current versioned rules.

Prompts alone cannot guarantee correct anatomy or motion. Production requires
specific prompts, approved references, registered pairs, persistent state records
and visual review before downstream use. A completed job is not approval.

For the native v6 keyframe pipeline, follow
[`keyframe-regeneration.md`](keyframe-regeneration.md): each revision starts
from the approved plate/crop, includes the identity roots for every visible
actor and a hash-bound same-setup scale anchor, and keeps camera cuts and closed
production-boundary mouths explicit. The reference and runtime gates remain
closed while canonicals, anchors, props or full-size keyframes await owner
approval.

## CR-01. Production order and owner selection

1. Write the script, proposed shot order and cause-and-effect state table. Plan
   dialogue durations; generate audio only when requested.
2. Owner reviews the sequence before its images, especially revised contact,
   trap and rescue beats. A written storyboard is sufficient for this gate.
3. Freeze the visual bible; create and approve neutral canonicals, scale
   calibration, expression/mouth references, plates and prop states.
4. Create a separate prompt record for every image, edit, reused asset, endpoint
   and mouth variant. Follow [prompt-records.md](prompt-records.md). Review each
   image before using it as another image's reference.
5. Register and inspect start/end pairs and adjacent-shot handoffs using
   [v4-preflight.md](v4-preflight.md).
6. Render a small pilot of individual clips; review it before expanding the batch.
7. Give the owner individual clips, contact sheets and a selection ledger. Record
   the exact selected file, revision, seed, mouth mode, trim and order.
8. **After owner take selection and an instruction to assemble, run the animatic
   as a separate job.** Never append assembly/post to a clip task file. Never
   build an animatic automatically after each batch.
9. Post-process selected material and inspect it again. Upscaling/interpolation
   cannot repair identity, impossible contact or prop causality.

Preserve earlier-version inputs and reviews. An active production request may
authorize image work; video and assembly remain separately scoped.

## CR-02. Freeze one versioned character identity

An explicit owner redesign precedes the next canonical. For v4 **Milo has a
smooth felt crown with no separate top-hair tuft**. This supersedes all earlier
attempts to shrink the tuft. Retain ordinary felt fibres, eyebrows and whiskers.
First revise the neutral canonical; once approved, derive the pack and every
interaction from that v4 root. Independently erasing hair in many old images
is not proof that their faces and bodies agree.

Until approved, the new canonical is pending; v3 is reference material for the
unchanged traits, not an approved v4 asset. (Status 2026-10-02: the v4 roots
exist, `character/characters/lion_and_mouse_v4/{Milo,Leo}/canonical/full-body_*_neutral_pose_r01.png`,
accepted from the owner's list on 2026-10-01.) Freeze and review:

- Milo: slender taupe-grey torso, elongated cream belly, youthful rounded head,
  two large circular ears with dusty-rose interiors, dark-brown irises with cream
  sclera, small brown nose, slim bipedal limbs, one thin rosy-taupe tail.
- Leo: compact golden-ochre quadruped, cream muzzle/chest, dark-brown irises with
  cream sclera, four paws, one golden tail with rust tuft; full circular
  burnt-orange/rust mane with the canonical volume and lock pattern.
- Head/torso ratio, muzzle width, ear diameter/spacing, eye spacing, torso width,
  limb thickness and tail root. Chubby Milo, different eyes, extra tails and a
  thinner/crimson mane fail even if the scene looks attractive.
- Lighting may change brightness/shadows, not intrinsic identity colours. Compare
  neutral references as well as the scene light; never recolour the cast to fit
  a background.
- Count anatomical parts, and specify which are visible versus hidden. An
  occluded tail has a recorded location; it is not permission to create another.

The v1 black stitched eyes and 1:6 size ratio are historical. The current cast
has brown eyes. Milo is **one third of Leo's neutral standing height at the
same depth**; this ratio does not use a lying lion's shorter silhouette.

## CR-03. Canvas size, anatomical scale and scene scale

Equal PNG dimensions do not imply equal characters. Equal silhouette heights
also do not imply equal body scale across sitting, standing and running poses.

1. Lock dimensions and camera for each family: square studio canonicals/views,
   matched portrait expressions, exact 16:9 scene endpoints. Record any pad/crop
   transform; never stretch an image to force a ratio.
2. Calibrate neutral standing height and stable anatomical landmarks: head width
   excluding ears/hair, eye spacing, torso length and ground contacts. Measure
   comparable views; a head turn needs perspective-aware review.
3. Maintain anatomical scale through pose changes. Sitting reduces the pose's
   height; the skull does not shrink on standing. Keep ground contacts separate
   from the top of the pose's silhouette.
4. `production/keyframe.py` mattes and tightly crops the entire silhouette, then
   scales it to `h * frame_height`. Its `h` is pose-box height, not anatomical
   calibration. Reusing `h: 0.36` for sitting and standing can cause S02's shrink.
   After registering the poses to equal anatomical scale, compute
   `h_pose = h_neutral * B_pose / B_neutral`, where B is the pose/neutral box
   height in that registered space. Ratios of unaligned source files are invalid.
   Save head scale and foot/contact placement alongside the resulting `h`.
5. Inside a fixed-camera shot use the same plate, crop, focal framing, light,
   depth plane and layer order. Actor depth motion changes actor scale smoothly;
   trees and rocks do not zoom with the actor.
6. Overlay both endpoints at the actual video input size. Inspect after all
   resize/pad/crop operations, not only at original image resolution.

Initial review tolerances (proposed, not measured model guarantees): unchanged
view head/eye spacing within 2%; planted ground contact within 0.5% of frame
height; static landmarks within 0.2% of frame dimensions after a common camera
transform. Visible identity/scale jumps fail regardless of tolerance. Intentional
motion uses its recorded trajectory; do not compare moving feet as planted feet.

## CR-04. Registered start and end images

Every v4 character shot needs approved start AND end images. Derive the end from
the approved start using the same canonical roots and plate. Unrelated attractive
stills are not a pair.

- Record pair ID, camera profile, dimensions, crop, colour treatment, depth and
  exactly what may change. Everything else is protected. Use local image edits,
  masks or composition where supported. Restore protected regions from the base
  or reject a candidate if whole-image regeneration moves them.
- Endpoints reduce drift; inspect the middle too. A perfect last frame cannot
  excuse a distorted paw, eye, tail or prop halfway through.
- For state changes, the end depicts the actual result. Identical start/end is
  allowed for an explicitly planned hold/loop, never to depict a rope breaking.
- Exits have a clean end plate and a continuous visible path through a frame
  boundary. An empty endpoint alone may cause disappearance. If necessary cut
  from a validated pre-exit frame to the empty scene instead of accepting a fade.
- The owner accepts slight close-up reframing (S07). Make it intentional, record
  start/end crop and transform, keep anatomy and blurred context consistent.
  Prefer a controlled digital crop in post to a generative camera move.

## CR-05. Expression, mouth and gesture controls

Before speech alternatives, approve closed, slightly open and moderately open
mouth references in identical face framing. Freeze jaw hinge, muzzle, lip
outline, mouth interior, tongue and dentition. Create Leo's just-woken surprised
reference from his asleep pose; opening the eyes must reveal the same brown eyes.

For **every speaking or expressive character beat**, render separate named modes:

- `closed`: preferred edit-safe baseline when no mouth animation is intended.
  Hold the approved mouth pose steady, whether the audio is narrator voice-over
  or character dialogue over a distant wide shot. Paws and tail stay anchored.
- `mouth`: only for audio lines explicitly assigned to the visible character. The
  video render supplies body, face and subtle head/eye motion; timed mouth movement
  is composited afterward from that character's forced word alignment (`production/lip_sync.py`).
  Narrator lines never drive a character's mouth, including lines that describe
  what the character says or does. During narration, use a silent hold/reaction
  and keep the approved mouth pose still.
  The current compositor uses one approved open shape and broad syllable pulses,
  so it is word-timed but not phoneme/viseme-accurate. Record the speaker and
  endpoint states. Review every processed close-up against the narration.

A different seed is not a different mode. Both modes need compatible endpoint
images: a closed clip cannot end on an open mouth. Sleep, silent locomotion and
empty scenery remain silent. Gnawing needs functional mouth contact; its safe
backup is a separate closed observing/reaction shot, not sealed-mouth chewing.
The closed alternative to a call is a worried reaction with off-screen audio.

Default body control: paws lowered/resting, shoulders and torso steady, tail
settled in its recorded position. A smile does not authorise waving, pointing,
hand clasping, arm lifts or tail flicks. An essential gesture gets its own shot,
contact path and endpoints. Simplifying unreliable decoration in any future
character requires a versioned canonical decision, as with Milo's hair.

V4 proposes two small rounded cream upper incisors for Milo's gnaw reference,
subject to mouth-design approval. Keep that tooth design whenever visible.
Leo never acquires fangs. Avoid a global `visible teeth` negative when approved
teeth are required, or a global `mouth open` negative for a speech variant.

## CR-06. Locations and ambient motion

One approved plate per place/camera/light. New lighting preserves its geometry.
Close-ups use the same scene state; blurring a wrong place or old net state does
not fix it. Freeze trunk centres, roots, rocks, horizon, path edges, ground plane
and light direction. Record at least three static landmarks. Preserve identical
protected background pixels in still pairs where possible.

**Seed plate and variants:** For a new location and camera, the first plate is a
seed: generate it without a location-image reference only because no approved
plate exists yet. Review and approve that seed before creating variants. Register
its record ID in `visual_bible.json` as `composition_master_record`; its target path
is the location's composition master. Every later plate
for that same location and camera—including another time of day—must attach that
master explicitly in `ordered_references` as `edit_base` and change only the
registered light/time/weather delta. Generate each variant directly from the
master, not from the previous variant, so small differences do not accumulate.
A written `{{plate:...}}` description is not an attached visual reference. If a
master exists but is missing from the reference list, do not generate; fix the
record first. If a prompt has no attached reference, treat it as a new scene,
never as an implicit continuation of the first image. Inspect each variant next
to the master and compare the fixed landmarks before accepting it. If a new
season or camera intentionally changes the geometry, register that as a distinct
profile and state the permitted changes explicitly.

Each place has an ambient profile reused across its shots:

- Gentle leaf/grass-tip movement; stems, roots and trunk bases stay fixed. Canopy
  leaves may flutter; the tree skeleton does not bend or slide.
- Visible water continuously ripples/flows in the approved direction. It cannot
  freeze between S01 and S02; banks, rocks and water level stay fixed.
- Visible clouds drift slowly in one consistent direction; stars may twinkle
  softly in a cutaway. Sun and time of day remain fixed within a shot.
- Soft leaf shadows may shift slightly with the same breeze; no global flicker
  or relighting. Inspect amplitude/direction continuity across adjacent cuts.

Keep the main action dominant. Add a short frozen ambient clause rather than
another story about clouds. In empty scenery, ambient motion is the main action.
A difference of location/light may justify another profile; record that change.

## CR-07. Prop permanence, contact and net topology

Give each prop an ID and start/event/end state: count, holder, position, attachment
points, layer order and visibility. Carry it into the next shot. Hidden, off-screen
and removed are different states.

- One acorn stays in Milo's paws while he notices the time in the proposed v4
  plan. A separate placement shot leaves it at a recorded ground point before he
  travels. A falling object follows a visible path to a resting place; it never
  disappears. Later views retain it if that place is visible.
- Leo stays asleep until Milo contacts his paw. Contact precedes waking. A fast
  tumble/nose aftermath can be an explicit editorial cut, not a morph from a wide
  scene to a close-up under a supposedly fixed camera.
- One net: suspended -> falling -> draped -> frayed -> severed -> opening ->
  slipping behind Leo -> fallen behind him. After release the overhead branch
  is empty in all later frames, including close-up backgrounds.
- Establish why cutting the selected strand opens the net. The v4 proposal uses
  a closure strand securing an existing fold; releasing it cannot delete other
  mesh strands. Review this topology in the intact state before any bite image.
- Annotate the selected strand, two neighbouring knots and bite point outside
  the generated picture. Cut at the bite point. Track the resulting two ends
  and their occlusions. A single cut does not delete a length of rope. Any
  detached fragment gets an ID, a falling path and a resting location.
- A broken strand remains broken. Additional breaks require distinct strand IDs
  and visible work or a planned time-ellipsis cut with cumulative damage. Never
  return to an intact net for a second magical snap.
- Preserve rope/leaf/paw/body occlusion order. Leaves cannot pass through intact
  netting. The net slips behind Leo by gravity, without teleporting sideways or
  reforming around him after release.
- Milo remains present or has an explicit off-screen place/entrance. A Leo-only
  start cannot simply gain Milo at the endpoint.

The proposed S14 order in the v4 packet needs owner review before images.
(Status 2026-10-02: S14 images for this order exist at r02 and the owner chose
two of them as the size reference, CR-14; an explicit approval of the order is
not recorded.) Narration must match the chosen number/order of visible breaks
and trap motion.

## CR-08. Readable locomotion and source quality

Use an approved side-view running pose, upright bipedal Milo, a fixed camera,
one direction and a clear ground lane. Specify start/end position, depth, gait
and ground contacts. Exactly one mouse follows one continuous path; his single
tail stays attached. Avoid combining a run, glance back, jump and camera track.
For S09 use a forward-looking careful run; a glance back can be a separate hold.
Depth movement (S10) changes actor scale, not background scale.

Sharp source images need enough actual subject pixels, legible eyes/face, intact
paws and silhouette separation. Inspect at 1280x720. An initial planning floor
for solo running Milo is about 180 pixels of upright-equivalent height at 720p
(25% of frame height), subject to visual review, not a guarantee. If correct
cast scale makes him too small, give him a separate closer shot. Do not enlarge
him relative to Leo. Avoid smear, foreground obstruction and detail crossing
his face. Upscaling cannot restore missing original features.

## CR-09. Exhaustive records and focused model prompts

Every image record includes ordered reference paths and roles, purpose, counts,
geometry, state, full positive text, exclusions, edit scope, protected areas and
acceptance checks. Submit complete frozen identity/style descriptions; do not
submit only “same as before”. Record exact submitted prompts, output location,
tool/model/seed where exposed, reference hashes and selected output hash. Mark
unknown settings `unknown`; never invent provenance for earlier images.

Every video record adds paired dependencies, event timeline, camera/ambient
clauses, prop transitions, mouth mode, candidate naming and reject criteria.
The runtime instruction focuses on one action; exhaustive planning must not
become a pile of conflicting requests to the model. Keep the full specification
and a separately recorded, complete runtime candidate. Measure its actual token
length against the deployed text encoder before submission; never silently lose
critical constraints to truncation. Fast Lightning runs at CFG 1 with no negative
pass, so desired states must be present positively and in the approved images;
negative lists alone do not control this mode.

Use explicit local reference paths when supported. Inspect the actual files and
confirm ordered roles. Filenames alone did not catch I-07's wrong sleeping scene.
Reopen the saved output; a preview or save command is not visual verification.

## CR-10. Revisions and downstream invalidation

Use the active story's own paths and revision IDs; preserve earlier versions as
history. For v6, use v6-local identifiers and approved canonical records. Never
use a v4 path or revision ID as a current v6 instruction. Approved-image edits produce a new
revision. Identity, plate, prop or prompt changes make dependent prompts,
installed packs, mattes/crops, keyframes and renders stale. Rebuild in dependency
order. Current scripts may skip existing outputs; use new revisioned paths and
shot names, or explicitly rebuild affected files. Do not trust stale caches.

Documentation states: `draft`, `needs_reference`, `ready_for_image_review`,
`approved_image`, `ready_for_pair_review`, `approved_pair`, `render_candidate`,
`owner_selected`, `rejected`, `stale`. Current scripts do not enforce these gates.

## CR-11. Anatomy readability and prop layers

Keep identity references prop-free. Acorns, nets and other story objects belong
to separate prop references and scene passes; an action-pose guide may show a
character's hands or mouth contacting an object, but must not replace the
character's canonical anatomy reference. For a held object, preserve a clean
grip pose and composite the approved prop at the contact point so the fingers
or paws visibly meet it.

A prop that crosses a character in depth remains one continuous world object.
For compositing, derive front and rear occlusion masks from that same approved
prop source; do not redraw it as multiple objects or change its mesh, count,
scale, knots or state. In particular, an intact net over Leo may have strands
behind his body and strands in front, with a continuous path through the
occlusion. Preserve all broken ends and the net's state across cuts.

For Milo, the pale belly ends above the crotch. Keep a visible taupe-grey gap
between the two slim legs from the crotch down; do not let the cream belly form
a white bridge or wedge between them. Keep both legs distinct and planted, with
the feet separated enough to read clearly. Retain his approved slim waist,
softly rounded cheeks, fine visible whiskers on both sides, smooth crown,
brown eyes, two large ears and one attached tail. Do not compensate for a
cropped or incomplete body by stretching or enlarging the head.

For full-body or medium shots, state the complete visible anatomy in the prompt:
Milo's crown through both feet and entire tail; Leo's full mane, torso, four
paws and tail. Keep a margin around ears, mane, paws and tail. Place solo
characters at the established lower-centre/screen position unless the approved
shot plan specifies otherwise. Close portraits are intentional only when the
shot plan calls for a face crop; preserve a complete body in all other shots.
When using a composited character pass, match contact shadows, edge softness,
light direction, depth blur and ground contact to the locked plate so the
character does not read as a pasted cutout.

Before accepting an image, inspect leg separation, whiskers, cheek volume,
whole-body visibility and character-to-plate integration at full resolution
and at delivery size. Reject any white belly bridge between Milo's legs, missing
whiskers, visibly clipped anatomy, floating feet, hard cutout edges, or altered
plate landmarks.

## CR-12. Expression references and face seams

Keep expression references as clean, prop-free face or head studies with the
canonical skull, muzzle, cheek width, ear spacing, eye spacing and whiskers.
Use them to guide only the eyes, brows and mouth in a scene. Anchor every scene
to an approved full-body character and the locked plate; a face study alone
must never supply an entire scene actor or replace the torso, paws or tail.

Milo and Leo may retain their subtle central felt stitching, but it should
read as a material seam, not a dark line cutting across the face. In close
shots, keep the seam low contrast and consistent with the canonical reference.
Inspect the forehead, muzzle and silhouette at delivery size for a strong
or misaligned seam before acceptance.

## CR-13. Generated-image gates (lessons from the Gemini r02/r03 pass, 2026-10-02)

Each rule names the defect that made it necessary. When the owner asks the agent
to generate, use the built-in OpenAI `image_gen` tool by default; Gemini through
`character/gemini_image.py` is optional when the owner selects it
(`docs/gemini-images.md`). These rules apply to any image model.

1. **Whole bodies unless the shot is a face close-up.** In a wide, medium or
   two-shot, every character's body stays in frame and attached: a lying lion
   shows mane, torso, paws and tail. A head with no body is a reject.
   (s05 r02: Leo became a floating head.) Anchor contact shots on the
   previous shot's camera and pose, and say "no part of the body is cut by the
   frame edge".
2. **Side-by-side identity gate.** Before accepting a frame with a face,
   compare it at full size beside the canonical (the review sheet puts the
   identity roots first in every row). Check colour temperature (warm taupe,
   not cool grey), iris size and colour, face seam, cheek width and the
   head-to-body ratio. (s08 r02: off-model Milo face accepted at thumbnail size.)
3. **Reuse an approved frame from the same setup.** When a character
   reappears in a setup the owner has already approved, edit that frame and
   change only the expression or pose; do not generate the character afresh.
   (s08 r03 was fixed as an edit of the approved s07 frame. The same approach
   held Milo's face across S13 and S15.)
4. **Scale as frame fractions and comparisons.** "Same size as reference 1"
   is ignored. Write "from ear tips to feet y=0.55 to y=0.87, centred
   x=0.55" and relative statements such as "Milo's whole body is as tall as
   Leo's head" or "his head is smaller than Leo's muzzle", plus depth ("at
   the same depth as Leo"). (s02, s05, s13 grew Milo to twice his size.)
5. **Staging references are staging only.** An older-version image used for
   composition leaks its identity (the V3 references gave Leo a red, short
   mane). Name the reference's role and restate the identity explicitly.
6. **Spell out small props.** "A small plain round felt disc with no markings,
   half hidden under leaves". (Unspecified, the trigger got an "X".) A prop
   whose state is fixed (a net with the lion inside) is named in every
   frame where it appears. (One s13 take showed the net empty.)
7. **Name the expression parts.** Image models default to a smile. Write
   brows, eyes and mouth explicitly: "brows high, eyes wide, mouth closed in
   a small neutral line, no smile".
8. **Continuity cascades.** When an upstream world state changes (the net
   staging), mark every downstream frame that shows the old state `stale` and
   redo the chain in dependency order. Redo a start and its end together, and
   generate each end from its accepted start.
9. **Plate check per take.** A model can silently replace the locked plate
   (Pro did, on several takes). Compare background landmarks with the
   previous frame before judging the character.
10. **Record every take.** Each API call is logged in
    `stories/lion_and_mouse_v4/revisions/gemini_ledger.csv`; each accepted take
    in the manifest stores its prompt, references, model and review note, and
    the replaced result stays under `superseded`.

## CR-14. Character scale and expression close-ups

Use each story version's own approved canonicals, expression studies, location plates and setup
anchors. Never borrow an earlier version's image to define current identity or scale. Record
standing-equivalent cast ratios at the same depth, then record apparent frame fractions for each
setup and depth plane. A seated or lying pose changes silhouette height while head, mane and limb
anatomy stays fixed. For Lion and Mouse v6 the current values are in its `visual_bible.json`
(CR-28); the former experimental measurements are historical and are not active rules.

Dialogue close-ups follow their own setup crop: a single sharp face and upper chest against the
same location, strongly blurred. Use the approved current-version expression image for brows,
eyelids, gaze and mouth only; the canonical remains the identity authority. Review the face and
background beside their approved sources before accepting the frame.

## CR-15. Which shots are face close-ups (dialogue format) and which are scene shots

Every scene image record in `prompt_manifest.json` now has a `framing` field.
Decide it before writing a prompt; it controls everything else.

| `framing` | When | Look | Size rule |
|---|---|---|---|
| `dialogue_close_up` | One character speaks, listens or reacts alone; the line is about feelings | Head and upper chest centred in 16:9 (ear tips or mane top y≈0.05, chin y≈0.70), facing the camera, the scene's plate strongly blurred behind, nothing in front (except the net when the character is inside it) | Close-up; no size relation needed |
| `close_two_shot` | A contact action needs both characters readable (nose contact, gnawing) | Both characters on the setup's locked plate; blur only if that setup specifies it | Preserve each actor's measured setup size and depth |
| `scene_wide` | Arrivals, exits, travel, actions, any shot that shows where we are | Whole bodies on the sharp plate, fixed normal-height camera | Use the approved setup and depth anchor in CR-16; the CR-14 0.30–0.36 range applies to its measured solo/closer setup |
| `empty_plate` | Establishing or time-passing shots | Plate only | n/a |

**Recipe for a `dialogue_close_up` (what fixed s07 and S15):**
1. References, in order: the approved current-version edit base where applicable, the locked
   current-version plate, the current-version canonical (`identity_root`), and one approved
   current-version expression study. A framing reference may be attached only when it shares
   the intended crop and cannot replace the canonical or plate.

2. The prompt names the location plate and asks for it "very strongly
   blurred (like a portrait lens at f/1.4)". Without that phrase Nano Banana 2
   kept the background half sharp.
3. Name the expression in words as well as by reference (CR-13 rule 7), and
   say "exactly two eyes and two brows".
4. The end frame changes only the expression: "keep framing, head size and
   background exactly as in reference image 1".
5. Review: framing numbers, blur strength, face side by side with the
   canonical, two brows.

## CR-16. Apparent size across adjacent scene shots (owner, 2026-10-02)

For every wide or medium shot, record the plate, camera crop, ground baseline,
character depth plane, and visible bounding box (normalized `x0,y0,x1,y1`)
for the head or mane and for the complete body. Choose an approved shot of the
same setup as the size anchor. Compare the next shot at equal image size before
acceptance; changes in pose may change the silhouette but must keep the head,
mane, torso and paw size consistent at the same depth. A close-up with a blurred
plate is a deliberate editorial cut and uses its separate close-up framing.

For an independent version, every setup anchor must be an approved image from that same version.
Lion and Mouse v6 has no approved sharp-background anchor yet; review and approve a
valid same-setup anchor before accepting existing candidate frames or making more
dependent frames. Its owner-selected numeric targets remain in
`stories/lion_and_mouse_v6/visual_bible.json`. Compare both start and end of each pair.

When an actor moves forward or backward, annotate the initial and final depth
and resulting size in the active plan or manifest. A scale jump with no visible depth move or
camera cut fails review. Prefer a measured bounding-box comparison to broad
instructions such as “same size.” Do not apply the solo Milo 0.30–0.36 frame
fraction to a farther-away two-character shot; use the chosen shot's depth
anchor and Leo-to-Milo anatomical ratio instead.

## CR-17. Reusable setup and acceptance contract for every story

Complete this setup **before the first scene image**, including stories with
only one character. Save its measurements in the story's visual bible and
repeat the applicable facts in each individual image prompt. Repetition is
deliberate: a tool call must be understandable without earlier chat or prompts.

| Freeze first | Record and use for every relevant image |
|---|---|
| Character identity | One approved, prop-free neutral root per character; front, side and back when needed; intrinsic colours; head, eyes, brows, nose, muzzle, cheeks, ears or mane, torso, limbs, tail root, material seams and feature counts. List forbidden drift (for example hair, extra limbs, changed nose). |
| Action and emotion coverage | Before generating scenes, list every recurring walk, run, crouch, roll, rest, prop-contact and dialogue pose in the shot plan. Give each staged actor a version-local pose reference and each story-specific emotional state an expression reference. Keep neutral turnarounds as identity masters; a pose sheet guides anatomy and action, never background, camera or size. Validate that every staged actor has a mapping, and review the actual pose cells visually before reusing them. |
| Shared cast scale | A same-depth lineup with neutral standing-equivalent heights and head/mane widths. Store ratios between every pair of characters. Repose or lie down without scaling skulls, manes or limbs. |
| Location camera | One approved plate per place, camera and light state; image size, crop, lens/framing, horizon, ground plane, light direction and at least three fixed landmarks. Reuse it or derive an explicitly registered close-up. |
| Shot size and depth | For each scene setup, choose an approved size anchor. Store each actor's normalized head/mane and whole-body box, screen centre, feet/baseline and depth plane in start and end frames. For two or more actors, compare them **in one frame at the same depth** and record their relative scale. |
| Persistent world state | Prop count, holder, contact, damage, attachment, front/back occlusion, and off-screen location; current state comes from the latest accepted shot, never from an older attractive image. |

Every scene prompt repeats the complete frozen identity of **each visible
character**, even if the same words appeared in the previous prompt. It also
states character counts, anatomical counts, the size anchor and measured frame
fractions, depth, foot/contact positions, plate landmarks, expression parts,
prop state, and the only allowed change from the accepted parent. A face
expression reference controls brows, eyes and mouth; it cannot replace the
canonical head, body or prop state. Prop-bearing images are action references,
not neutral identity roots.

At review, compare (1) each face and body against its canonical, (2) every
character against the shared lineup and the setup's previous shot, (3) the
background against its locked plate, and (4) the pair's start and end at final
delivery size. Inspect nose/muzzle shape, whiskers, cheek width, eyes, ears,
seams, mane, all visible paws and tails, ground shadows, scale, occlusion and
object counts. Review close-ups at full resolution and wide shots both full
size and delivery size. A pleasing composition does not excuse identity,
scale or plate drift. A rejected or unreviewed output cannot become a later
reference.

If a model changes protected geometry, make a focused edit from the approved
parent, use a reviewed isolated actor/prop layer on the locked plate, or reject
the take. A request for transparent output is not proof of transparency:
inspect the actual alpha channel and edges, especially whiskers, ears and
tail, before any composite. Reject a matte with background gradients, colour
fringing, clipped parts or leftover objects; never feed that rejected image
into the next generation call. Record the exact tool, prompt, ordered reference paths and hashes,
output hash, inspection note and any unresolved defect. A new result is accepted
only when the actual saved file has been reopened and checked. Maintain one
active target per manifest record where the owner requests replacement; retain
earlier provenance in the record instead of accumulating unnecessary active
`r**` files. Invalidate dependent frames when an upstream identity, plate,
scale or prop state changes, then repair them in dependency order.

**Never mix framings inside one shot.** Wan animates between the start and
end frames; a wide start with a close-up end becomes an unwanted zoom.
(The first `s08_leo_softens` r01 pair had exactly this problem: a wide start
and a close-up end. Both endpoints were remade as close-ups on 2026-10-02.)

**Edits must not add characters.** When the reference images contain the
same character more than once (an approved frame plus a second frame of the
same character), the model may draw that character twice: s05 r05 got two
Milos. For a change of expression or eyes, send only the frame being edited
plus the canonical, and state "exactly one Milo".

## CR-18. One source of truth for every prompt (2026-10-02)

**Why:** the v4 audit of 2026-10-02 found the same character described in many slightly
different ways across 140 image prompts, 62 video prompts and five revision files, size numbers
that contradicted the accepted frames, and references attached without the prompt saying what
they were for. Image models follow the words they are given, so word drift became image drift.

**Rule:** for every story, all prompt text that describes a character, a place, a camera setup,
a size relation, the light or the style lives once in `stories/<slug>/visual_bible.json`.
Prompts are templates (`prompt_template` in `prompt_manifest.json`) that pull it in through
placeholders and add only frame-specific words: pose, position, expression, action, prop state.

- Write each character's `identity` from its approved canonical image, never from memory or an
  older version. Colours are named with the hex sampled from the canonical; proportions as
  ratios; every feature counted. `short`/`sheet` may only reuse its colour words.
- Never write a character's colour or body feature in a record: `lint` rejects a sentence
  that pairs a colour word with a body feature outside the canonical blocks.
- Every attached reference is listed in the prompt (`{{refs}}`) with its role in plain words,
  and every visible character's canonical is attached; a canonical is never attached for a
  character that is not in the frame.
- Sizes come from the setup (`setups.<id>.size`, measured on its `anchor_record`, which every
  start frame attaches as its size anchor) and the lineup (`blocks.cast_scale`); never estimate
  them per record. A frame states only the sizes of the characters in it.
- A reference that shows a character who is not in the frame is not attached (it can draw that
  character in); the edit base comes first, then plate, canonicals, poses, faces, props, size anchor.
- Nothing is appended at generation time: no revision fix text, no `--extra`. The prompt sent is
  the rendered prompt.
- After any change: `python3 production/image_prompts.py build`, then `lint` (0 errors), then
  `md`. The rendered prompt is the only text sent to a tool.

Reference: [`image-prompts.md`](image-prompts.md); workflow: the repo skill
`.claude/skills/consistent-image-prompts/SKILL.md`.

**Decision (owner, 2026-10-02): one Leo-to-Milo lineup for the whole story.** Milo standing is
0.55 of Leo's mane height and his head with ears about 0.4 of Leo's face height, as in
`s05_nose_aftermath_start` (Milo 0.20 of the frame, mane 0.36). This replaces the per-setup
ratios of CR-14 and CR-16 (great tree about 0.47, trap path about 0.85): sizes still come from each
setup, but every setup now applies this one ratio (`visual_bible.json` `cast_scale`).

## CR-19. A separate open-mouth image calibrates dialogue (owner, 2026-10-05; revised 2026-10-09)

For each character dialogue close-up, create one approved open-mouth calibration image by editing
an approved closed-mouth endpoint. Only the mouth differs: pose, head size and position, gaze,
background, camera and light remain identical. Attach the closed frame as `edit_base`, the location
plate, the character canonical, and the approved `*_OPEN` mouth study. Keep one speech-mouth design
per character throughout the story.

Both video boundaries must use approved closed-mouth images. Record the separate open image as
`mouth_open_image` on the `mode: mouth` variant, with one explicit audio `speaker`; map its visual
character ID to that speaker via `characters.<id>.voice_speaker` in the bible. `production/lip_sync.py`
uses the image only during that character's aligned words. It rejects open-mouth boundaries,
which would otherwise open during silent gaps while preserving chain continuity. Narrator-only
close-ups receive only a `closed` variant. `production/story_packet.py` applies this to new stories;
the retired `production/chain_packet.py` applied it to historical inherited packets. Review every open image against its
closed edit base and the `*_OPEN` study before rendering.

Earlier Lion and Mouse versions used an open image as a video endpoint. Those existing media are
historical; future packets use closed endpoints and post-render mouth animation (CR-23/24).

Reference: [`image-prompts.md`](image-prompts.md); workflow: the repo skill
`.claude/skills/consistent-image-prompts/SKILL.md`.

## CR-20. Scene keyframe file names carry the per-scene chronological order (owner, 2026-10-08)

**Why:** within one scene a file browser sorts shots alphabetically, which is not story order
(`s01_acorn_…` sorted before `s01_explores_…` even though "explores" comes first). Baking the
chronological position into the file name makes the stills sort in story order on disk, which is
how the owner reviews them.

**Rule (opt-in per story via `visual_bible.json` `"keyframe_chrono_naming": true`):** each scene
keyframe **file** is named

```
sNN_CC_<shot-name>_<start|end|open>_rNN.png
```

where `CC` is a two-digit counter that **restarts at 01 inside each scene** and counts the scene's
shots in story order (the manifest `shots[].order`; a `bridge` shot has no images and is not
counted). Only the **file name** changes: the manifest record `id` stays `<shot>_<which>` and all
cross-references resolve by id, so ids, `start_image`/`end_image` and prose shot names are
untouched.

- `production/story_packet.py` sets the flag and emits chrono file names for every **new** story
  automatically. Stories generated before 2026-10-08 (Tortoise and Hare, Boy Who Cried Wolf, Ugly
  Duckling) are **grandfathered**: they keep the old `<shot>_<which>_rNN.png` names and the flag is
  off, so the check does not fire. To adopt it in one of them, rename its keyframe files, update
  every reference (manifest `target`/`output_path`/`ordered_references[].path`, the embedded
  `[file.png]` in prompts, the per-story README tables, `story.yaml`, `runtime_inputs.json`,
  `timing_plan.json`, `TIMING_SHEET.md`), then set the flag; file bytes are unchanged, so stored
  `sha256` stay valid.
- `image_prompts.py lint` enforces the convention only when the flag is on: it recomputes the
  expected `sNN_CC_` prefix from the shot order and flags any scene keyframe whose file name does
  not match.
- Lion and Mouse v5 was converted on 2026-10-08 (the first story to use it); videos under `work/`
  (git-ignored) and per-line narration audio (`SNN-LNNN.wav`, already in order) are out of scope.

Reference: [`image-prompts.md`](image-prompts.md); workflow: the repo skill
`.claude/skills/consistent-image-prompts/SKILL.md`.


## CR-22. Lock the visible silhouette in dialogue close-up video (owner, 2026-10-09)

Dialogue close-ups must preserve the approved head-and-shoulders crop for the full clip. Their video
prompts use a portrait-only character description, then explicitly lock the approved crop and visible
silhouette from the start and end frames. They do not repeat full-body identity text, because details
outside the frame can prompt the video model to invent those parts. Lint requires the portrait
placeholder and crop lock for every newly generated dialogue close-up variant. Approved reused
renders keep their original prompt and provenance.


## CR-21. Audio-driven chained coverage (owner, 2026-10-08)

**Why:** Lion and Mouse v5 has 11:23.7 of narration but 43 shots of 5.06 s, about 3.5 min of
picture; the timing sheet filled 7.9 min with slow-downs and stills, and the clips are too short
for the audio. The shot list was written from the story's actions, not from the narration. From
v6 on the narration is the timeline: plan enough visual coverage for every
spoken span and pause, and register every cut or exact shared boundary.

**Current v6 implementation (2026-10-11):** Lion and Mouse v6 has 52 visual
units, 97 candidate keyframes and 16 scene boundary plans in its story-local
`visual_sequence_plan.json`, `keyframe_plan.json` and
`video_boundary_plan.json`. It does **not** have a `prompt_manifest.json`,
`timing_plan.json` or `story.yaml`. Run
`production/staging_contract.py --story lion_and_mouse_v6`,
`production/keyframe_visual_gate.py --story lion_and_mouse_v6`, and
`production/v6_runtime.py --story lion_and_mouse_v6 --preflight` before any
runtime export. The visual and runtime gates must fail while a required image
is unreviewed, stale or rejected. Exact v5 English audio reuse is allowed only
through the v6-local audio manifest and runtime namespace; no v5 visual asset,
clip or render is a v6 input. Speaker-specific mouth motion follows CR-23/24.

The numbered manifest-piece rules below document the earlier CR-21
implementation. Apply them only to a story with the corresponding manifest
schema; their `chain_plan.py`, `export_runtime.py` and `image_prompts.py`
commands are not direct v6 instructions.

**Historical manifest implementation (opt-in via `"chained_coverage": true`):**

1. **Audio first.** The rendered narration (`work/stories/<slug>/audio/<lang>/timing.json`) is the
   timeline. Every second of it (lines, pauses and the scene tail) is covered by exactly one
   **piece**, in order. A piece is a manifest shot with one video variant.
2. **One piece, one clip, 49 to 81 frames.** Clips longer than 81 frames cost quadratically and
   drift more (`docs/lumi.md`), so a long line is covered by several pieces, never by one long
   clip. `production/chain_plan.py` gives each piece its seconds from the lines it lists and
   picks the frame count (4k+1, 49 to 81 at 16 fps) closest to them; the small rest is a retime
   between 80% and 125% speed (RIFE in post). A piece shorter than 2.45 s or longer than 6.33 s
   is an error: merge or split lines. Pieces are never trimmed, because the trimmed part would
   be the shared end image.
3. **Chain.** A piece with `"join_in": "chain"` starts on exactly the image record its
   predecessor ended on (same record id, same file). So every handoff is an approved still that
   both clips are pinned to.
4. **Marked cuts only.** A piece that cannot chain says `"join_in": "cut"` and why, in
   `cut_reason`; lint checks that the reason is true:
   - `film_start`: the first piece of the film.
   - `close_up`: a cut into or out of a `dialogue_close_up` or `close_two_shot` setup.
   - `camera_change`: another setup at the same place (place = the plate's folder, e.g. the
     great tree's wide, close-up and upward sky views).
   - `time_change`: the same place in another light (day, dusk, night, another season).
   - `location_change`: another place.
   - `dissolve`: time passes; needs `transition` `crossfade` or `dip`, and is the only cut
     allowed inside one setup (e.g. the empty tree after the friends rested there).
   Any other cut between two pieces of the **same setup** is an error: on a fixed camera it is
   a jump cut (a character pops in or out). A cut may carry `transition` (`cut`, `crossfade`,
   `dip`) for the edit; time changes read best as a crossfade.
5. **Landscape pieces** cover narration that has no action, e.g. the opening of Lion and Mouse
   over the empty stream plate or the season plates of The Ugly Duckling. Mode `ambient`, no
   cast; start and end are the location's approved plate record (`PL_<loc>`), or an approved
   empty scene frame of that setup when a prop belongs in the view (the trap path with the net
   bundled in the branches), so start = end and only the ambient motion of CR-06 moves (water,
   leaves, clouds, light). To bring a character
   in on the same camera, chain an **entrance** piece: start = the empty plate, end = the
   character just inside the frame edge. Never cut from the empty plate to the same camera with
   the character already there.
6. **Holds and living pieces.** Start = end is allowed only for a planned hold (`"hold": true`
   or mode `ambient`): breathing, a blink, ears, tail tip, ambient motion. It must not depict a
   state change (CR-04).
7. **Talking chains.** A run of dialogue close-up pieces alternates the closed frame and its
   `<shot>_open` key frame (CR-19): closed → open, open → closed, and so on. Every hand-off is
   one of the two approved images.
8. **Boundary images** are reviewed against both pieces that use them: the end of the earlier
   piece and the start of the later one (identity, size, plate, prop state, pose that a single
   action can reach from both sides). A boundary image first created as an end frame is an edit
   of its piece's start frame (`edit_base`); later uses do not change that.
9. **Reuse (historical policy only).** An earlier manifest design allowed a piece whose
   endpoints and prompt matched an earlier version to name it in `"reuse"`.
   This does not authorize cross-version visual or render reuse for independent v6.
10. **Join test.** Before the full render, `production/chain_preview.py --stills` plays the
    planned images against the narration (no GPU) to check pacing and the chain. After a pilot
    of the first scenes is rendered and the owner has chosen takes, use
    `chain_preview.py --require-takes --fail-on-flagged-joins` to assemble only exact-length chosen takes and measure
    joins on the retimed preview frames. A bad join can be repaired with
    `production/chain_repair.py --story <slug> --piece <later> --previous-piece <earlier>`;
    this records the chosen source clip and hash, and `export_runtime.py` adds a separately named
    candidate whose first frame comes from that clip. The original candidate and take remain
    untouched. Choose the repair in `takes.yaml` and run the strict join test again.
11. **Image approval.** After visual review, record approval for the exact manifest target with
    `production/image_prompts.py --story <slug> approve <image-id> --reviewed-by <name>`.
    The approval records the image hash, rendered prompt/specification hash, and hashes of ordered references.
    Runtime export refuses v6-owned scene images with missing or stale approvals.
12. **Edit handoff.** When every piece has an owner-chosen take, run
    `production/edit_manifest.py --story <slug>`. It writes a hash-bound film-order manifest for
    DaVinci or another editor; it does not assemble or render the final film.
13. **Historical migration note.** The retired `production/chain_packet.py` copied every resolved base-story image
    asset used by the new packet into the matching versioned character/location folders, rewrites
    the new bible and manifest paths, and leaves the base story untouched. Accepted inherited
    expression studies are indexed in `prompt_manifest.json` and generated as
    `prompts/expressions.md`; they are references, not new image jobs. Carried assets keep their
    source filenames and `carried_from` provenance, while chronology and edit-base checks apply to
    newly created images.

Tools: `production/chain_plan.py` (timing, frame counts, coverage checks, `TIMING_SHEET.md`),
`production/image_prompts.py lint` (chain, cut and landscape rules when the flag is on),
`production/chain_preview.py` (strict join test), `production/chain_repair.py` (hash-bound
continuation repair), `production/edit_manifest.py` (chosen-take handoff), and the image `approve`
command (hash-bound approval). Workflow: the repo skill
`.claude/skills/audio-chained-coverage/SKILL.md`. Current Lion and Mouse v6
implements audio-driven coverage with a separate keyframe/boundary plan.

## CR-23. Dialogue mouth motion is timed in post (owner, 2026-10-09)

For every new narrated project, retain the exact line audio and transcript, create
word timings with the isolated WhisperX aligner, and apply mouth animation only
after a take is selected. The compositor may only use reviewed, matched closed/open
endpoint frames and must preserve the source clip's first and last frames exactly
so the scene chain remains continuous. Final edit export rejects dialogue mouth
variants without a current hash-bound lip-sync output. Use `docs/lip-sync.md` for
the commands, review steps and limitations. This implementation approximates
syllabic opening within word intervals; it does not claim phoneme-level visemes.

## CR-24. Narration never drives character lip sync (owner, 2026-10-09)

A character's mouth moves only for audio explicitly assigned to that character in
`dialogue_coverage.json`. `NARRATOR` lines are voice-over: they never produce
character mouth cues, even when the narration describes a call, speech or reaction.
Every `mode: mouth` variant must carry one explicit character speaker, and the
compositor must ignore narrator/other-character lines and fail closed if that speaker
is missing or mismatched. During voice-over, hold the character's approved mouth
pose still. If two visible characters speak in one piece, split the coverage into
speaker-specific shots (or use a reviewed multi-speaker compositor); never apply one
character's timing to another character. A non-verbal vocalization is lip-synced only
when its audio is separately assigned to that character.

## CR-25. Scene scale requires an attached anchor and measured review (owner, 2026-10-10)

For every scene frame with visible characters against a sharp or recognizable background,
attach the setup's approved same-camera `anchor_record` with role `size_anchor` to both
start and end frames. The anchor must show each character whose scale it is meant to lock;
it cannot be the frame being generated, a blurred portrait, or a known scale-defective frame.
When a setup begins with single-character frames before its first shared-cast anchor, list those
specific earlier frames as `bootstrap_records`. Measure them against the setup's numeric targets
and approve them before making the shared-cast anchor; do not attach the future anchor to them.
Reference cycles and self-anchors fail the generation-order check.
Keep the anchor in the references actually sent after provider limits are applied, dropping
optional staging references first. Before staging, measure each character's silhouette against
the setup's frame-fraction target and anchor, and compare the shared-cast ratio. Missing anchors
or material scale mismatches block staging and downstream use. Numeric prompt instructions alone
do not count as a scale check.

## CR-26. Lion and Mouse v6 revised scale and trapped-net composition (owner, 2026-10-10)

The v6 `visual_bible.json` is the source of truth for its current numeric size targets (CR-28).
Close-ups retain their own crop. Measure against the approved v6 setup anchor once it exists.

For trapped-Leo close-ups, the net must conform to Leo's mane, head and shoulders and read as
supported by his body, not as a flat web between Leo and the viewer. Leave a clear opening over
both eyes, nose and muzzle. Remove the central vertical strand that crossed the forehead and nose;
do not leave a loose end. Every remaining strand must join the continuous mesh at a knot or crossing.

In `.review`, keep one PNG candidate per record. Preserve prompt and source hashes in the Markdown
sidecar when the redundant source PNG is removed; do not leave visually redundant source/candidate
copies in the review folder.

## CR-27. Walkable ground and supported character contact (owner, 2026-10-10; see [spatial-staging-consistency.md](spatial-staging-consistency.md))

Before generating or reviewing a scene frame, identify the walkable surface and ground baseline at
that character's position and depth from the locked plate. Record the support surface and normalized
foot/contact point. A character's planted feet or paws must meet continuous visible ground with
matching shadow and occlusion. Do not stand a character on water, flowers, bush canopies, or other
decorative foliage unless the story explicitly establishes stable footing or perching there. For
sitting, lying, climbing, jumping, or prop contact, verify the stated contact is physically supported.
Reject floating, sinking, or implausible plant-top placements before staging.

## CR-28. Lion and Mouse v6 scale reset (owner, 2026-10-10)

The owner reset Milo's scene-wide size to 0.21 of the frame height from ear tips to planted feet
in wide and two-character shots. Apply this target
to all scene-wide setups, with pose-height adjusted for sitting while preserving head size. Keep
portrait close-ups at their established framing. In start/end pairs, hold Leo's size and position
steady unless the prompt explicitly moves him, and keep Milo on the same walkable depth plane unless
the story action changes depth. This owner decision supersedes the half-size target recorded in
CR-26; update the bible, rendered prompts and candidates together.

**Current interpretation:** CR-29 and CR-30 apply this 0.21 value as Milo's
wide-plate **near-foreground base**, then derive each shot's screen fraction from
documented depth and camera crop. The sentence above is historical owner direction,
not an instruction to force 0.21 into every cropped frame.

## CR-29. Character staging contract and depth progression (owner, 2026-10-11)

Before generating scene images for a new story, complete its `staging_plan.json`. For
manifest-backed stories, `new-story` creates this file and registers it in
`visual_bible.json`; `image_prompts.py lint` rejects scene image records without
corresponding staged frame entries. Current v6 uses its own plan directly. Run
`python3 production/staging_contract.py --story <slug>` to check the plan itself. This contract
records a same-depth cast lineup, an approved plate and walkable zone for each location, a camera
view/crop for each frame, and each actor's ground contact point, depth and apparent size. A scene
image record's ID must match its staging frame ID. Numeric plans still require visual review of
the actual images against a same-setup approved size anchor and the locked plate (CR-17, CR-25).

For a fixed camera, apparent size changes continuously with the actor's movement in depth. Derive
size from the approved plate's ground geometry and the story's depth model; interpolate size
between key poses. A small depth move may only cause a small size change. A larger move toward or
away from camera may cause a larger change, but the walkable path, contact shadow and occlusion
must also show that travel. Record a camera cut/crop separately; it may alter frame fraction but
must not change character anatomy or the same-depth cast ratio.

Current Lion and Mouse v6 targets are in `stories/lion_and_mouse_v6/CHARACTER_STAGING.md` and
`staging_plan.json`. They retain Milo's 0.21 wide-foreground height from CR-28, but apply it to
the **full approved plate at foreground depth**, not blindly to every cropped two-character
frame. The chosen same-depth upright Milo to quadrupedal Leo height ratio is 0.40, pending a
measured shared-cast anchor review. The owner-favored Scene 06 medium and closer two-shots guide
their camera crops and left/right staging.

## CR-30. Measured image scale and explicit scene boundaries (owner, 2026-10-11)

CR-28 and CR-29 define **planning targets**; generated images pass only after their actual pixels
are reviewed. Before making dependent frames, approve a same-depth cast lineup and one measured
character-on-plate anchor for each recurring camera/location family. Record its file hash,
camera crop, ground contact, anatomical size and a nearby landmark at the same depth. Compare
adjacent frames against that anchor and the depth equation. A crop enlarges character and
landmark together; it does not change physical size. Sitting or lying changes pose height, not
head, mane, torso or paw anatomy. A same-camera size discrepancy over 10% from the predicted
standing-equivalent value needs correction or a documented depth/camera explanation.

Every audio scene must name a start and end image and its entry join. A continuous join may
reuse the exact previous end PNG as the next start only when plate, crop, cast and world state
allow it. Otherwise use a cut or a designed transition; do not morph across independent camera
views by default. Full-resolution identity, plate, animal-count, landmark scale and grounding
review is required for **both** video endpoints. The canonical [spatial staging policy](spatial-staging-consistency.md)
defines this gate for future stories. For v6, see the [keyframe consistency audit](../stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md)
and [boundary plan](../stories/lion_and_mouse_v6/VIDEO_BOUNDARIES.md). Run
`python3 production/keyframe_visual_gate.py --story <slug>` before video export
when the story uses an individual `keyframe_plan.json`; the hash-bound visual
review record must pass for every candidate endpoint. `new-story` scaffolds
`video_boundary_config.json` and `keyframe_visual_reviews.json`; fill the former
with chronological insert order, explicit cut reasons and only justified shared
joins before building a boundary plan. Never infer these from filename order.
