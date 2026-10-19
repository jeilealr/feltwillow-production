# Leo imported r01: structure assessment and bounded rig plan

This is an **unbound development candidate**, not an animation asset. There is
no deforming armature or facial system in the delivered file. Non-rendering
`LEO_RIG_PLAN_GUIDES` empties are approximate planning landmarks, not fitted
joints or proof of anatomy. The earlier native prototype rig is a different
mesh and must not be presented as this mesh's deformation evidence.

## Actual intake findings

The imported surface retains 48,753 vertices and 48,742 faces: 48,713 quads,
23 triangles and 6 n-gons. There are 41 non-manifold edges, including 40 boundary
edges. A connected-component audit finds one large component of 48,694 vertices
and five tiny components totaling 59 vertices. Those tiny islands are not six
anatomical parts. Their bounds are in the technical audit: most sit near the
rear/tail region, with a small muzzle fragment. No automatic deletion or hole
filling was applied. First identify what each represents under wireframe.

Four paws and one tail are visible across the review views. Coordinate-region
ground diagnostics are not paw-count proof: the imported stance is asymmetric,
so a rectangular region can include the adjacent leg. Lowest paw-region vertices
range from approximately 0.00054 to 0.00899 BU above the common ground datum;
at .2 m/BU this is about 0.11–1.80 mm. Do not confuse the overall lowest vertex
with all four plantar surfaces being perfectly planted. No stance correction
was made because it would change the imported shape without a fitted rig.

The UV atlas and four 2048-square maps are preserved. Eyes, eyelid lines and
much of the color detail belong to one combined surface/material; no independent
eye aim, eyelids, jaw or mouth shapes have been established. A high quad count
does not demonstrate useful shoulder/hip loops or a clean mane/neck boundary.
Self-intersections, UV overlap and wall thickness are untested.

## Next controlled sequence

1. Preserve this revision; make a separate mesh-refinement candidate. Inspect
   the five tiny islands and 41 problem edges in context. Repair confirmed
   debris/holes only, recording before/after topology and UV changes.
2. Refine posterior mane bead rows into thick irregular rolled felt locks,
   without changing the approved front forelock, face or outer silhouette.
   Improve the four toe lobes and shoulder transitions against the canonical.
3. Fit a quadruped skeleton: asset root -> pelvis/spine/chest -> neck/head;
   separate scapular/upper/lower/paw chains in front, hip/stifle/hock/paw chains
   behind; three tail segments and four planted IK paw controls with poles.
   Guides are starting hypotheses; fit from actual mesh cross-sections.
4. Keep visible mane rolls largely head-bound, with a restrained neck transition.
   Skin the continuous body with smooth joint gradients. Separate eyes for aim
   only after checking their geometry and preserving current texture alignment.
   Neutral closed mouth/no teeth; advanced facial shapes remain deferred.
5. Rebind every wool strand and whisker root to the refined surface/weights.
   Current added wool/whiskers are parented to the asset root for static review;
   **they would not follow skin deformation**. Topology changes invalidate their
   present nearest-surface/UV attachment assumptions.
6. Test neutral -> 12-degree head yaw -> neutral, then a 0.02-BU pelvis/chest
   shift with four planted paws, viewed from the face and both sides. Inspect
   intermediate frames, neck penetration and mane/whisker attachment. Only after
   those pass attempt a short walk/contact test and lie-down transition.

Current verdict: useful sculpt/retopology starting point; **needs targeted mesh
refinement before a controlled rig test**. No new paid generation is warranted
by the present evidence. Temporal wool stability and deforming performance stay
untested until an actual bound rig and short sequence exist.
