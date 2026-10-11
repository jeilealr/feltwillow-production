# Feltwillow Spatial Staging and Grounding Consistency Guidelines

**Date:** 2026-10-10  
**Scope:** `lion_and_mouse_v6` and all future Feltwillow image/video projects  
**Status:** Adopted permanent production rule (owner instruction, 2026-10-10)  
**Purpose:** Define a systematic, reusable rule set so characters remain physically believable inside their environments, especially when moving between foreground, middle ground, and background, and when interacting with ground surfaces and objects.

---

## 1. Why this file exists

The repository already contains rules for character identity, scale, references, prompts, timing, and approvals. What also needs to be permanently systematized is **spatial staging consistency**:

1. **Depth consistency** — how a character moves from front/foreground to middle ground and background.
2. **Grounding consistency** — whether the character is standing, walking, sitting, landing, climbing, or resting on a physically believable support surface.

These rules apply to:

- still image generation,
- image approval,
- video prompt preparation,
- runtime clip generation,
- lip-sync and edit handoff reviews,
- future stories beyond v6.

This document is intended to become a **standing production policy**, not a one-off reminder.

---

## 2. Core principle

A Feltwillow scene is not only judged by whether the character *looks good* in isolation. It must also be judged by whether the character is **physically believable in the scene**.

That means:

- the character must occupy a sensible place in the environment,
- the character must appear supported by a valid surface,
- the size must make sense for the documented depth,
- the pose must make sense relative to terrain,
- the occlusion and overlap with scene objects must be coherent,
- movement across shots must not feel like teleportation or arbitrary rescaling.

---

## 3. Two permanent consistency requirements

## 3.1 Requirement A — Depth and distance consistency

When a character appears in the **foreground**, **middle ground**, or **background**, the following must remain coherent:

- apparent scale,
- body placement,
- camera relationship,
- perspective,
- silhouette clarity,
- contact with the environment,
- relation to landmarks.

### Required interpretation

- **Foreground:** character appears larger, with clearer body detail and stronger local interaction with the ground and nearby props.
- **Middle ground:** character remains readable but smaller, still clearly grounded, and positioned relative to major landmarks.
- **Background:** character is smaller and less detailed, but must still remain physically placed in a believable traversable zone.

### What must not happen

- a character keeps the same scale while supposedly moving far back into the scene,
- a character becomes tiny or huge without a documented camera/depth change,
- a character jumps between depth planes without transitional logic,
- a character changes depth but shadows, contact, or surrounding object scale do not match,
- a character appears behind one object in one frame and in front of it in the next without narrative movement.

---

## 3.2 Requirement B — Grounding and walkable-surface consistency

A character must be supported by a **valid physical surface** appropriate to the action.

### Valid support examples

Depending on the scene, valid support may include:

- path,
- dirt road,
- grass lane,
- flat rock,
- tree root,
- branch,
- nest or den surface,
- ground beside a prop,
- Leo’s body or paw **only when intentionally specified and physically shown**.

### Invalid support examples

Unless explicitly designed and physically justified, the character must **not** appear to stand or move on:

- open water,
- floating leaves,
- bush crowns,
- flower tops,
- empty air,
- impossible edge points,
- props with no visible support logic,
- disconnected net strands,
- decorative foreground elements that are not part of the walkable plane.

### Clarification

A leaf **on the ground/path** is not automatically invalid.  
If the leaf is part of the path surface and the character is clearly stepping on the path, that is fine.  
What is invalid is treating an isolated leaf like a weight-bearing platform.

---

## 4. Operational definitions for production

## 4.1 Walkable surface
A walkable surface is a surface where the character can plausibly stand, walk, sit, land, or push off, given the scene design and species anatomy.

## 4.2 Support contact
Support contact means the visible paws, feet, body, or resting surface visibly connect to the support plane with correct overlap, alignment, and implied weight.

## 4.3 Depth plane
A depth plane is the approximate distance layer within a composition: foreground, middle ground, or background.

## 4.4 Landmark anchoring
Landmark anchoring means the character’s placement can be described relative to stable scene elements, such as:

- path edge,
- feeding stone,
- tree trunk,
- root,
- rock,
- doorway,
- net,
- stream bank.

---

## 5. Mandatory rules for all projects

## Rule 1 — Every setup must define walkable areas
Each recurring setup or location should document:

- what area is traversable,
- what area is decorative only,
- what area is hazardous or invalid,
- what objects may be stepped on,
- what objects may only be touched or passed by.

**Example:**
- Stream scene: Milo may stand on the bank, path, or flat stone if specified.
- Milo may not stand on the water surface.
- Milo may not stand on the top of a bush unless the story explicitly places him there.

## Rule 2 — Every character placement must be depth-aware
Whenever a character is placed in a scene, the prompt or layout instruction must imply:

- approximate depth plane,
- relative size,
- relation to nearby landmarks,
- orientation and contact direction.

## Rule 3 — Apparent size must follow depth unless the camera changes
A character placed deeper into the scene must generally appear smaller.  
A size change without a depth or camera explanation is a defect.

## Rule 4 — Contact must be visible or strongly implied
The character’s paws/body must visibly connect to the ground or support plane unless the action is a jump, fall, or deliberate suspension.

## Rule 5 — Occlusion must respect depth
If a character is behind a rock, trunk, or prop, that overlap must stay consistent with the stated depth plane.

## Rule 6 — Action must match support
The support surface must make sense for the action:

- walking → path/ground/root/branch as appropriate,
- sitting → stable support plane,
- lying → stable support plane,
- landing → visible landing plane,
- climbing → explicit climbable structure,
- biting/pulling/holding → body placement must allow the action.

## Rule 7 — Environmental continuity matters across shots
If the character moves from one frame to the next:

- position change must be plausible,
- scale shift must match movement in depth,
- body orientation should not randomly flip,
- landmark relation should progress logically,
- contact should stay believable.

## Rule 8 — Video inherits still-image grounding rules
A clip is not acceptable just because the first and last frames are good.  
Motion between them must preserve:

- grounding,
- support contact,
- depth continuity,
- landmark coherence,
- believable approach/recession.

## Rule 9 — Physical size must be checked against the set

Before dependent scene frames, approve one same-ground-plane cast lineup and one character-on-plate size anchor for each recurring location/camera family. Record each anchor's image hash, camera crop, contact point, anatomical dimensions and a nearby landmark **at the same depth**. Keep the character-to-landmark ratio stable as the camera crops or zooms; a crop magnifies both. Do not use a distant tree crown or horizon object as a ruler for a foreground character. Sitting, lying and running change pose height but not head, torso, ear, mane or paw anatomy. A numerical size target in a staging file is a plan, never proof of visual compliance.

For a fixed camera, compare adjacent measured character size with the depth-derived target. A discrepancy over 10% requires correction or an explicitly documented camera/depth cause. A camera crop defaults to a cut; a continuous zoom requires a recorded camera path and endpoint checks. Check the actual image at full resolution against the approved plate and adjacent frame before using it as a video endpoint.

## Rule 10 — Video boundaries must be explicit

For each audio scene, record its chronological first and last candidate images and the intended join to the next scene. Reuse the **same image file** as the previous end and next start only for an explicitly designated continuous join with compatible plate, camera crop, geography, cast and world state. Otherwise mark a cut or a separately designed transition. A shared file removes the boundary-pixel jump but does not excuse drift in the next target image. A shot with a different crop is not automatically a zoom animation.

---

## 6. What must be checked in v6 specifically

For `lion_and_mouse_v6`, every active setup should be reviewed using these rules, including but not limited to:

- stream afternoon / sunset,
- fork sunset,
- shortcut dusk,
- great tree dusk / day / sky,
- home night,
- trap morning,
- forest run.

Every setup should explicitly answer:

1. Where can Milo stand?
2. Where can Leo stand / lie / move?
3. What parts are walkable ground?
4. What parts are landmarks only?
5. What parts are invalid for support?
6. If a character moves backward or forward in depth, how should scale change?
7. What occlusions are expected at each depth zone?

---

## 7. Approval checklist for still images

The following checklist should be applied during image review.

### 7.1 Grounding checklist
- [ ] Character is supported by a valid surface.
- [ ] Paws/body contact the support plane correctly.
- [ ] Contact shadow/overlap is coherent.
- [ ] Character is not floating.
- [ ] Character is not standing on water, decorative foliage, or an implausible object.
- [ ] If perched or climbing, the structure clearly supports that pose.

### 7.2 Depth checklist
- [ ] Character size matches the intended depth plane.
- [ ] Character position relative to landmarks is coherent.
- [ ] Occlusion with foreground/background objects makes sense.
- [ ] Perspective and pose match camera distance.
- [ ] No unexplained size jump relative to adjacent frames or setup anchors.

### 7.3 Action checklist
- [ ] The pose is possible on the chosen support surface.
- [ ] Props and body interaction make sense.
- [ ] The action can plausibly transition to prior/next frames.

### 7.4 Continuity checklist
- [ ] Relative location is consistent with nearby frames.
- [ ] Depth movement is believable.
- [ ] No teleportation, clipping, or support inconsistency.

---

## 8. Approval checklist for video / animated shots

For any rendered clip or candidate take:

- [ ] First frame is grounded correctly.
- [ ] Middle of the clip remains grounded correctly.
- [ ] Final frame remains grounded correctly.
- [ ] Character does not slide unrealistically across a non-walkable area.
- [ ] Character does not drift in scale without story/camera cause.
- [ ] Character does not pass through or ignore scene obstacles.
- [ ] Contact with net, rope, tree roots, stones, path, or props remains coherent.
- [ ] Motion between depth planes appears intentional and physically plausible.

---

## 9. Required documentation changes for future consistency

To keep this systematic, this rule should not live in only one place.

## 9.1 Primary authoritative home
Create or maintain one central rules document for this topic, for example:

- `docs/spatial-staging-consistency.md`

This file should be the canonical explanation.

## 9.2 Secondary references
The following files should reference the central rule rather than duplicating it loosely:

1. **Relevant `SKILL.md` files**  
   Add a short section that says agents must enforce spatial staging, depth, and grounding consistency according to the central doc.

2. **Story `visual_bible.json`**  
   Each setup/location should include or maintain:
   - walkable surface description,
   - invalid support zones,
   - depth/scale expectations,
   - key landmarks for placement.

3. **Story README / LUMI handoff / creation docs**  
   Mention that image acceptance requires successful grounding and depth review.

4. **Approval checklists / review prompts**  
   Include explicit pass/fail checks for support surface, contact, depth, and occlusion.

5. **Prompt-building instructions**  
   Ensure prompts state where the character is standing and how that relates to the setup landmarks.

---

## 10. Recommended repository implementation pattern

To keep this consistent across future projects, use this layered structure:

### Layer A — Canonical rule document
A single central document, such as:
- `docs/spatial-staging-consistency.md`

### Layer B — Story-specific setup definitions
Inside each story’s `visual_bible.json`:
- define walkable area,
- invalid areas,
- landmark placement rules,
- scale/depth anchors.

### Layer C — Prompt generation guidance
In prompt-related skills or scripts:
- require explicit support-surface logic,
- require landmark-based placement,
- require depth-aware scale.

### Layer D — Approval gate / human review
Approval materials should explicitly ask:
- Is the character grounded?
- Is the surface valid?
- Is the scale correct for depth?
- Is the environment interaction believable?

This pattern prevents the rule from being forgotten when a new story begins.

---

## 11. Minimum metadata every setup should carry

For each setup, the production documents should ideally capture:

- `walkable_surface`
- `invalid_support_zones`
- `anchor_landmarks`
- `depth_planes`
- `expected_scale_by_depth`
- `occlusion_notes`
- `special_contact_rules`

### Example schema idea

```json
{
  "walkable_surface": "clear dirt path between left rock and tree root",
  "invalid_support_zones": [
    "open water",
    "bush crown",
    "decorative foreground leaf"
  ],
  "anchor_landmarks": [
    "left trunk",
    "flat stone",
    "stream edge"
  ],
  "depth_planes": {
    "foreground": "large readable character, near left trunk",
    "midground": "reduced scale on the center path",
    "background": "small silhouette near stream bend"
  },
  "expected_scale_by_depth": {
    "foreground": "largest",
    "midground": "medium",
    "background": "smallest"
  },
  "occlusion_notes": "character behind right rock must be partially hidden at paw level"
}
```

---

## 12. Common failure patterns to flag

Future agents should automatically watch for these failure patterns:

1. Character appears to stand on water.
2. Character appears to stand on floating decorative leaves.
3. Character is placed on a bush top with no support logic.
4. Character looks detached from the ground.
5. Shadow/contact does not match position.
6. Character changes depth but not scale.
7. Character changes scale but not context.
8. Character crosses an obstacle without passing around/over it.
9. Character placement contradicts the setup’s walkable path.
10. Character is behind an object in one frame and in front of it in the next without explanation.
11. Trap/net interactions do not match rope logic.
12. Character body position makes the intended action impossible.

---

## 13. Required remediation behavior when a defect is found

If a grounding or depth defect is found:

1. Do **not** approve the image/clip just because identity or style is good.
2. Record the exact defect:
   - invalid support,
   - incorrect depth scale,
   - broken occlusion,
   - impossible action,
   - continuity failure.
3. Identify whether the defect is:
   - prompt-level,
   - setup-definition-level,
   - approval-checklist-level,
   - video-motion-level.
4. Fix the source-of-truth instruction before regenerating dependent outputs.
5. Re-check downstream affected images/clips.

---

## 14. Recommended wording for future agent prompts

Use wording like this when instructing agents:

> Ensure every character is physically grounded in the environment. Characters must stand, sit, walk, land, climb, or rest only on surfaces that plausibly support them. Respect walkable areas, landmark positions, occlusion, and depth-aware scale. When a character moves from foreground to middle ground or background, apparent size, placement, and perspective must change consistently. Never allow characters to appear floating, standing on water, or using decorative foliage as a support surface unless that is explicitly intended and visually justified.

---

## 15. Decision for adoption

### Recommended adoption decision
Adopt this document as a **permanent cross-project consistency rule** for Feltwillow.

### Recommended placement in the repository
1. Add this as a central document under `docs/`.
2. Reference it from relevant `SKILL.md` files.
3. Reference it from story creation/review documentation.
4. Encode setup-specific details inside each story’s `visual_bible.json`.
5. Include the checklist items in approval and audit prompts.

---

## 16. Final summary

For v6 and future Feltwillow projects, two things must always be systematically checked:

1. **How characters move through depth** — foreground, middle ground, background.
2. **Whether characters are physically grounded on valid support surfaces**.

This is now treated as a formal consistency requirement, not an optional artistic preference.

