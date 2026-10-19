# Rigging and deformation workflow

## Choose the rig from actions

List the hardest required poses and contact changes before choosing a rig. A narrative character is judged during a head turn, crouch, landing or emotional hold, not only in a neutral turntable. Decide deforming versus rigid parts, control spaces, attachment logic and how facial expressions preserve identity. Use the anatomy matrix; keep the current Leo test narrow without defining every later animal as a lion.

Create a clean control hierarchy: asset root for placement and invariant scale, locomotion/root-motion layer, body controls, appendage controls, then secondary motion. Give animator-facing controls meaningful names and safe limits. Keep deformation bones distinct from controls where appropriate. Never make world placement depend on an arbitrary mesh origin.

## Transform preparation

Inspect scale, mirrored transforms, bone roll, rest pose, object origins and mesh parents before binding. Do not blindly apply all transforms after a rig/shape-key/groom stack exists. Preserve an unrigged normalized source and a pre-binding checkpoint. Work in an agreed forward/up convention; import orientation corrections are recorded once rather than reintroduced in every shot.

Fit the skeleton to approved anatomical landmarks. For Leo, preserve shoulder mass and the fore/hind limb distinction; for birds, build foldable wing geometry and appropriate leg/toe articulation. Skin regions that must bend; rigid-bind a hat or appropriately rigid accessory only when the resulting attachment looks correct. Automatic weights are a first pass, not acceptance.

## Weight review

Test weights at the actual deformation zones: shoulders, hip/leg folds, neck-to-head transition, cheek/jaw, wing fold, tail root, shell openings. Inspect volume loss, pinch, creases, islands left behind and penetration. Use corrective shapes or local weight repair where necessary; do not hide a bad deformation with fur. Keep paint/weight evidence and neutral bounds for regression.

Shape-key edits depend on stable topology [B03](sources.md#b03). Test facial keys in combination, not only one at a time: blink + head turn, smile + jaw opening, eye aim + brow. Preserve the muzzle, ear/head attachment and owner-selected chest silhouette during expression-only shots.

## Contacts and controls

Use IK when stable contact is the priority and FK or blended control where arcs matter; verify snapping and blend transitions. IK is a constraint mechanism, not a guarantee of plausible balance [B02](sources.md#b02). A foot's world-space position must remain approximately fixed while planted relative to its moving support. For perching, toes contact a branch with plausible wrap; for gripping, hand/prop transforms agree without teleporting.

Record intentional compression, squash or stretch as bounded style controls. Keep the asset's physical scale invariant; do not use root scaling to fake body compression or fit through a doorway. A large-head character may need a custom balance solution rather than a human retarget.

## Mane, fibers and attachments

Decide whether mane locks follow head, neck or mixed deformation. Keep the characteristic outer mane silhouette stable during expression-only work. Bind whisker roots to the correct muzzle region, permit small controlled motion, and test both sides. Verify eyelashes/feathers/fibers remain attached after deformation. Deforming surface-curves use stable surface/UV relationships; UV or topology changes need revalidation [B04](sources.md#b04).

## Three-level test suite

**Static extremes:** neutral, maximum required head yaw/pitch, crouch/lie/sit or folded-wing state, reach/grasp, contact pose. Avoid unrealistic joint extremes beyond the story simply to obtain dramatic thumbnails.

**Short motion:** head turn plus blink; locomotion with start/stop; most important pose transition; one prop or terrain interaction. Render or playblast from story camera and a diagnostic side view. Sample motion between keyframes; collisions often occur mid-interval.

**Shot-distance test:** wide, medium and upper-body portrait. A rig that passes distant motion may reveal eyelid or muzzle distortion in a close-up. Test motion blur and felt fibers only after the plain mesh passes.

Proposed initial QA tolerances must be calibrated to character size and shot. For example, flag planted contact drift as a fraction of foot length and inspect it, rather than declaring an arbitrary fixed number of millimeters universally acceptable. Report measurements plus visual judgment; metadata alone cannot validate weight or acting.

## Reuse and retargeting

Save reviewed actions with rig revision, rest pose, root-motion convention and required controls. Retarget only between compatible profiles, then fix contact and proportions. Do not scale a human walk wholesale onto a quadruped. A useful library includes quiet breathing, blink, look, walk-start/stop, turn, sit/lie transitions, and anatomy-specific actions, each bounded and reviewed.

Keep animation editable in native Blender. A provider's FBX/GLB can be an interchange asset but does not replace the full native rig, constraints, procedural groom and shader graph. Verify export/import round trips before committing to a format.

## Escalation

After the bounded repair budget is exhausted, report the specific failure with frame numbers and alternate methods: targeted retopology, a different skeleton, simpler shot staging, or specialist help. Do not claim an hour-long tutorial implies a film-ready hero in an hour. Full actor quality is proven by the deformation and visual tests, not generation speed.
