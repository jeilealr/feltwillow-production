# Anatomy and motion profiles for future fables

## Compose capabilities, not a single species switch

Each character declares support surfaces, structural appendages, locomotion modes, facial mechanisms, stylized exaggerations, mass reference and interaction capabilities. A duck combines walking, swimming, flight and a beak; a bear may switch between four-legged and upright action; a dragon may combine quadruped legs, wings and a long tail. A profile describes the approved design, not an anatomical rule the owner must obey.

Use explicit IDs such as `leg.front.L`, `wing.R`, `antenna.L`, `tail`, `hand.L`. Define parentage, control mode, expected count and allowed occlusion. Add or omit structures only from canon. A deliberately one-eyed fantasy creature must not fail a universal two-eye test. Distinguish ordinary animal behavior from anthropomorphic performance; a human-like smile, hand gesture or gait is a conscious story choice.

## Profile matrix

| Family/capability | Rig requirements | Minimum tests | Typical failures |
|---|---|---|---|
| Human / humanoid biped | Pelvis/spine balance, feet, hands, shoulders, eyes/jaw as designed | Stand, sit, turn, reach, grasp/release, walk and stop | Foot sliding, knee inversion, shoulder collapse, fingers inside props |
| Upright small animal | Biped base adapted to short limbs, big head/ears, tail balance | Crouch, small gesture, stumble recovery, face close-up | Human proportions imposed; torso stretches for reach |
| Quadruped | Scapular/shoulder motion, spine, fore/hind distinction, paw contacts | Walk/turn, plant, lie down/rise, head turn, low obstacle | Front/back limbs treated identically; elbow/knee/hock confusion |
| Ungulate | Hoof contact/roll, appropriate distal joints, neck balance | Walk/trot if needed, stop, bend to ground | Dog-like paws and wrong foot articulation |
| Bird | Wing root/fold, feather fan or felt wing shapes, legs/toes, beak, head | Perch, land/takeoff, flap/glide, fold, walk | Wings treated as human hands, backwards leg joint, clipping folded feathers |
| Waterfowl | Bird profile plus waterline/body float and paddle action | Enter/exit water, turn, swim hold, shore contact | Feet on water surface, floating above water, arbitrary bobbing |
| Fish / aquatic mammal | Species-appropriate spine and tail propulsion, fins/flukes | Turn, slow/stop, surface transition if needed | Mammal fluke moved like fish tail; eyes/material made realistic without approval |
| Snake / worm / eel | Continuous backbone, contact-aware curves, distributed bend | Coil/uncoil, path follow, obstacle bend | Length changes, tube intersections, body floats between supports |
| Arthropod / spider / insect | Per-limb IDs, staged support groups, antennae/mandibles/wings as designed | Slow gait, stop, turn, climb if needed | Generic biped gait, leg phase chaos, incorrect appendage count |
| Turtle / snail / shelled character | Rigid shell and protected volume, limb/head exits or foot body | Turn, retract if required, obstacle clearances | Shell squash, neck penetrating shell, impossible doorway fit |
| Bat / membrane-wing animal | Membrane supports, fold and tension controls | Fold, extend, flap, perch/hang if needed | Feather-style wing rig, membrane inversion/tearing |
| Hybrid / fantastical character | Explicit composition of approved capabilities | Transitions between each supported mode | Auto-rig guesses incoherent skeleton; unreviewed anatomy inventions |

This matrix is an original planning checklist, not a validated rig implementation or a zoological database. Study species-specific movement reference with usable rights before choosing joint ranges or gait phase. Review design exaggeration with the owner, especially where realistic anatomy would harm the miniature-felt identity.

## Locomotion specification

Define grounded contacts by interval: which paw/foot/toe/body segment supports weight, its support object, and whether it may slip or lift. Define travel direction and speed before cycle timing. Root displacement and planted-foot travel must agree. Turning requires different inside/outside paths; simply rotating a straight walk cycle may skate.

For flight, define takeoff impulse, airborne interval and landing contact, then wing action. Not every wing motion should move the whole body sinusoidally. For swimmers, define a world-space waterline and heading before secondary body roll. For crawlers, define support/contact distribution rather than forcing discrete foot controls. For changing modes, test the transition, not just each loop in isolation.

## Speech and expression

Separate voice speaker identity from rig anatomy. A bird can express speech with beak articulation and eyes; an insect may use posture/antennae and a small designed mouth; an animal may have a soft lip crease without teeth. Use the existing canonical mouth design. Do not infer realistic tongues, teeth or human lips from a generic speech tool. Silent listeners and narration shots remain appropriately still.

For stylized children, elders and different body proportions, preserve the approved age impression and silhouette without a stock adult rig stretching the body. Accessories and clothing are their own deformation/contact problem, not a reason to modify anatomy.

## Rig discovery

Rigify has modular components including different limb types [B01](sources.md#b01); choose and fit, do not assume generation equals correct skinning. Mesh2Motion is an optional open-source candidate worth investigating across body families [A01](sources.md#a01). Mixamo's documented auto-rigging scope is bipedal humanoids [A02](sources.md#a02), so do not route Leo, fish or birds through it by default. Third-party auto-rig outputs are diagnostic candidates until local motion tests pass.

## Future-proofing checks

Keep skeleton and control specifications independent of English actor names. Allow left/right asymmetry, missing/extra limbs when canonical, multiple locomotion modes and per-character facial strategies. Version a rig's capabilities so shot planning cannot request a perch, grasp or flight from a rig that does not support it. A new species usually needs calibration, not just another YAML label.
