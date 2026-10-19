# Research synthesis and adoption decisions

## What this research establishes

This package consolidates current repository rules, selected creator workflows, official Blender documentation, Blender Studio production/training material and provider/client documentation. It is a research-grounded first version of a production skill, not a claim that reading tutorials creates a perfect artist or that all recommendations have been tested on the user's meshes.

Direct YouTube audiovisual playback was unavailable. For `VeOU0FnTjjc`, an indexed mirror of the published captions was inspected [Y01](sources.md#y01). For `nHBNa2IKWvk`, the relevant first-party tools companion article was inspected [Y02](sources.md#y02). Public pages from the same creator expanded the workflow context. No full transcript, paid course or downloadable creator asset is redistributed.

## The one-hour section: the useful lesson

The captioned workflow starts with generated parts, assembles and repairs them in Blender, rigs the result and tests motion in a game engine. The shorter pass lacks later refinement; the longer pass adds more material and rig polish. It uses Tripo P2 rather than necessarily the H3.1 endpoint selected for Feltwillow. [Y01](sources.md#y01)

Our adaptation is **bounded feasibility first**: preserve the promising H3.1 Leo, repair targeted features, test actual deformation, and only then invest in felt grooming and full scene work. The time box measures progress and exposes blockers; it does not promise a complete film-ready character in one hour. Separate meaningful parts, but do not fracture continuous deforming skin simply to copy a humanoid workflow.

## The tools video: useful loop, unsafe shortcut

The creator's companion article emphasizes giving an agent application tools and preview feedback, then asking it to build, inspect, repair and verify against a concrete brief. It describes several Blender and game-engine integrations, not a mandatory stack for every artist. [Y02](sources.md#y02)

Adopt the measurable brief and feedback loop. Reject blanket approval/sandbox bypass, automatic paid iterations and installing everything because it appeared in a demo. For Feltwillow, existing Blender MCP plus optional fal is a sufficient initial integration target. More integrations are a response to a demonstrated missing capability, not a route to guaranteed quality.

## More from the creator that actually helps

The full-character article provides a useful stage ordering: prepare references, work on geometry, establish UV/materials, then rig and animate [Y03](sources.md#y03). The animal-rigging article helps identify non-humanoid services to test [Y04](sources.md#y04). The animated-film article separates generation from animation and assembly [Y05](sources.md#y05). The environment article supports modular set construction rather than treating a full generated scene as a finished navigable world [Y06](sources.md#y06). The reference-preparation article is useful only when it strengthens existing canonical consistency, not when it prompts fresh redesign [Y07](sources.md#y07). These are creator demonstrations, not independent reliability or time benchmarks for this project.

## Why non-YouTube sources matter more for the rules

Blender's manual establishes how rigs, shape keys, curve attachments, caches, linked libraries and color/normal handling actually work [B01](sources.md#b01), [B02](sources.md#b02), [B03](sources.md#b03), [B04](sources.md#b04), [B05](sources.md#b05), [B06](sources.md#b06), [B07](sources.md#b07), [B08](sources.md#b08), [B09](sources.md#b09), [B10](sources.md#b10), [B11](sources.md#b11), [B12](sources.md#b12), [B13](sources.md#b13), [B14](sources.md#b14), [B15](sources.md#b15), [B16](sources.md#b16). Those constraints are more reliable than a polished showreel. Blender Studio's Sprite Fright production account is especially relevant: the artists deliberately chose controlled, simplified construction and authored motion instead of assuming more simulation meant better style [S01](sources.md#s01). We borrow that decision discipline, not its visual designs.

For deeper study, use Blender Studio's public Toon Character Workflow, Humane Rigging and Animation Fundamentals curricula, and Pierrick Picaut's public rigging/animation course descriptions [S02](sources.md#s02), [S03](sources.md#s03), [S04](sources.md#s04), [S05](sources.md#s05). Full paid lessons were not inspected. These are learning paths, not evidence that their entire expertise has been reproduced in this archive.

## Holistic conclusion

A dependable felt film needs agreement across character design, anatomy, rig, materials, set scale, camera, lighting, motion, prop state and audio. Optimizing them in isolation can make the whole shot worse. A beautiful wing rig may collide with a beautiful tree; a sharper wool texture may flicker; a well-formed doorway may be too small for a human carrying a prop. The specialist briefs therefore share one world contract and an independent whole-frame review.

Use anatomy capabilities rather than a universal skeleton. Use full 3D where interactions/parallax require it and 2.5D within a tested camera envelope. Separate ambient from primary action and evaluate both from the same story clock. Keep the acorn, net graph, waterline and contact history explicit. More movement is not automatically better storytelling.

## Corrections to earlier assumptions in this conversation

- Successful object generation does not establish usable topology, rigging, felt appearance or production time.
- Current repository decisions supersede the earlier "all images pending" state. The new skill preserves owner selection and asks for missing technical evidence rather than restarting cleanup.
- Equal object-scale values do not imply equal anatomical sizes across meshes. Screen targets cannot directly become world-space meters.
- A broad camera-family name is insufficient to prove an exact view match.
- Standard Wan I2V is not a guaranteed video-to-video polish stage for a Blender animation.
- Normal/AO baking is optional; PATINA cannot generate actual silhouette fibers or guarantee canonical color.
- A compatible ROCm machine does not automatically establish Blender Cycles support for its GPU.
- An MCP connection is not a secure spending limiter, and a role brief is not an actually running specialist agent.

These corrections are deliberate safeguards against overconfident automation, not reasons to abandon the Blender experiment.

## Architecture decision

Ship **one production skill with modular references and nine specialist role briefs**. It supports both characters and reusable worlds without repeating a conflicting core policy. Environments get their own substantial reference module and ownership boundary now. Split into separately installable skills only after actual use shows independent triggers and a stable shared contract.

## What remains empirical

The user's actual Leo mesh, selected material maps, local Blender version, available GPU, prototype scene and rig must be inspected and tested locally. This release did not create or approve a character, generate a texture, run Blender, inspect every repository image, or render a film. Its portable helper tests are documented separately. The first success criterion is one faithful S05 still plus a stable short movement; the second is generalization to a bird and a human/upright character. Only those results can justify broader production commitments.
