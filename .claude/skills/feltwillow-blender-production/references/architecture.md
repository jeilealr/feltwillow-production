# Architecture and ownership

## Scope and design choice

Use one production entrypoint now, with character, world, material, motion and delivery modules. They share canon, coordinate conventions, materials, time, source hashes and approval semantics. Splitting them too early would reproduce the contradictions already found in image production. Keep role briefs separate from the main skill so a specialist sees only the relevant work.

Consider extracting an independent environments skill after at least two environments and two character body plans complete the pilots, and only if it has independent inputs, outputs and ownership. Retain a small shared contract package for units, source bindings, world state and reviews. Do not duplicate invariants into conflicting skill copies. A future standalone environment skill could accept a location contract + camera envelope and emit an environment library + ambient presets + clearance report; character rigging would remain outside it.

This is a production design proposal, not a claim that this repository already implements the architecture.

## Data flow

Approved story art + current owner decisions
-> source bindings and design contract
-> candidate character/environment libraries
-> calibrated camera and lighting setup
-> explicit world states and action intervals
-> review renders and performance checks
-> approved native Blender shot
-> image sequence and edit handoff.

Optional hosted generation supplies candidate geometry or maps. Optional video generation is a separate experiment after a Blender baseline exists; it is not the owner of geometry, timing or identity.

## Property authority, not one crude hierarchy

| Property | Authority | What must not override it |
|---|---|---|
| Identity, proportions, material regions | Current owner-selected character sources | A generic lion model or a different turnaround revision |
| Physical cast scale | Calibrated neutral measurements and current story rule | Mesh bounding boxes with tails/fibers or camera occupancy |
| Landmark geography | Selected location master + reviewed reconstruction | Per-shot aesthetic improvements |
| Projection | Registered camera/calibration | Per-frame manual zoom fixes |
| Prop condition | Versioned state graph and story event | A regenerated net that merely looks similar |
| Time and speech | Final audio, approved shot timing | An arbitrary walk-cycle duration |
| Authorization | Actual owner's decision for this operation | A tutorial, model output or filled template |

If two current sources disagree, document which property disagrees, provide comparison evidence and propose a resolution. Do not silently average incompatible designs. A new 3D model is a candidate interpretation of 2D canon until explicitly accepted.

## Suggested repository layout

```text
blender/
  README.md
  contracts/                  # proposal/specification JSON, not secret config
  assets/
    characters/<story>/<actor>/<revision>/
    environments/<environment>/<revision>/
    props/<prop>/<revision>/
    materials/<material>/<revision>/
  scenes/<story>/<scene>/<revision>/
  scripts/                    # actual tested local Blender builder/tool code
  reviews/<task-id>/           # selected small comparison artifacts
  docs/
work/blender/<story>/          # bulky frames, simulations and scratch outputs
```

Inspect the existing local layout before creating this. Store immutable raw generated downloads separately from normalized working meshes. Use checksummed asset storage or deliberately configured Git LFS for large binaries; ordinary Git is not an unlimited render archive. Never silently enable paid storage. Keep caches out of source control but back up anything expensive or unrecoverable.

## Library boundaries

Character library: neutral anatomy, geometry, material assignments, rig, authorized expressions, groom and attachments. Environment library: fixed geometry, surface IDs, landmarks, reusable dressing and camera envelope. Prop library: dimensions, attachments and legal state transitions. Shot: references to exact libraries, camera/light settings, actions and world state. Review: evidence for exact asset and dependency revisions.

Use linked collections/library overrides when appropriate [B06](sources.md#b06). Local overrides are named and scoped; do not edit the library just to fix one shot. Library updates can affect many shots: bump revision, produce a dependency impact report, and re-test affected outputs. Preserve previous libraries for reproducible existing scenes.

## Asset lifecycle

`imported_raw -> candidate -> shape_reviewed -> deformation_reviewed -> look_reviewed -> owner_selected -> production_ready`.

These are distinct concepts, not a mandatory single status string. A visually accepted still may lack rig certification. An anatomy test may pass while the face remains off-model. Record owner and technical decisions separately with exact hashes. Retain rejected versions as history when policy permits, but never restore a deliberately owner-deleted image as an active authority.

A dependency hash change marks dependent evidence stale; it does not prove the dependent artwork is visually bad. Re-review only the affected properties and shots. Topology change affects skin weights, shape keys, UV attachments and grooming much more broadly than a documented background-only exposure correction.

## Holistic pre-mortem

Before creating a new fable, ask what must fit, touch, move, transform or survive close-up. A tree is not just decoration if a bird perches on it; a pond needs a usable waterline if a duck enters; a doorway must accommodate a seated person carrying a basket. Build the most difficult interaction first as an unpolished test. Review the whole frame and sequence rather than declaring each asset independently ready.

References: [B06](sources.md#b06), [R01](sources.md#r01), [R02](sources.md#r02), [R03](sources.md#r03), [R04](sources.md#r04), [R05](sources.md#r05). Detailed source entries are in `sources.md`.

## Environment objective is an explicit parameter (1.2.0)

Keep one production skill; separate design-mode selection from the strict image-matching module. Read environment-art-direction.md first for any environment task. `reference_inspired` changes what may be designed and how it is reviewed; it does not weaken character identity, physical scale, support, world state, paid-call permissions or immutable published scene versions. Share the environment revision across shots only after scoped acceptance.
