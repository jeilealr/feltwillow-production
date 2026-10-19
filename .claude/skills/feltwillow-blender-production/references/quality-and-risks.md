# Whole-frame quality, risk anticipation and independent review

**Select the design mode first:** Read [environment direction](environment-art-direction.md). Use [environment image matching](environment_image_matching.md) only for `plate_match`; evaluate `reference_inspired` and `original_design` against their authorized brief. A blockout can be structurally valid while failing the handmade look.

## Evidence levels

Label every assertion: **source-verified**, **metadata-tested**, **visually observed**, **owner-selected**, **hypothesis**, or **not tested**. A creator's demo is a source observation, not a Feltwillow benchmark. A successful script proves only its tested properties. Selection is not all technical approvals; a historical warning is not a current rejection.

Use a task-specific risk register before expensive work. For each risk record trigger, affected assets/shots, severity, likelihood, detection method, mitigation owner and stop condition. Use high/medium/low judgments rather than invented statistical probabilities. Reassess after the first actual render and motion trial.

## Anticipatory matrix

| Risk | Detection | Mitigation / stop condition |
|---|---|---|
| Wrong current canonical or superseded audit | Compare current owner ledger, hashes and README | Stop identity edits until authority resolved |
| Pretty front, unusable back | Multi-angle clay/texture review | Mark unseen forms inferred; repair before approval |
| Missing feature or limb confused with occlusion | Semantic part map + orbit + mesh inspection | Fix existence only when confirmed, never duplicate hidden limb |
| Good mesh, poor joint topology | Extreme-pose and mid-motion tests | Retopo/weights before expensive groom |
| Mane, feather or fiber sliding | Deformation render with markers | Rebind UV/rest surface; invalidate stale groom evidence |
| Paws/toes skating or floating | Contact tracks relative to support | Repair root travel, IK, surface alignment |
| Wing/antler/tail intersects plants | Swept motion envelope + diagnostic views | Adjust route/dressing explicitly, not anatomy scale |
| Human/animal cannot fit doorway or bridge | Actor plus prop clearance test | Revise set or blocking with owner intent preserved |
| Bird perch or duck waterline implausible | Side-view contact and enter/exit test | Build valid support/water surface and rig transition |
| Net topology changes between poses | Knot/edge IDs + visual overlay | Preserve graph until explicit cut event |
| Prop changes hands by teleporting | Parent-switch world transform audit | Keyframe matched handoff; correct custody state |
| 2.5D scenery exposed | Envelope extremes and moving camera | Restrict camera or replace failing card with geometry |
| Grass/tree landmark drift | Compare library/camera signatures | Lock landmarks; isolate scatter/ambient masks |
| Material wrong scale or painted shadows | Neutral swatch and UV review | Rework mapping/inferred maps; keep canonical region colors |
| Plastic fur or realistic CG look | Canonical style comparison at delivery size | Reduce gloss/long hairs; review macro felt construction |
| Flickering fibers/alpha/denoise | Short animated render | Reduce unstable detail, fix attachments/sampling |
| Global orange cast | Neutral versus scene lighting A/B | Separate color transform, material and light diagnosis |
| Over-animation competes with narration | Playback with/without ambient | Reduce layers; keep primary action legible |
| Ambient phase resets at cuts | Global clock / preset state comparison | Evaluate absolute time; no per-shot reseed |
| Shared pose but velocity jump | Boundary derivative + playback review | Match approach/departure or choose deliberate cut |
| Mouth moves for narrator / double sync | Speaker timeline plus final rendered face | One approved facial pipeline per take |
| New rig breaks old actions | Dependency and capability regression | Pin versions; retest affected action library |
| Hero revision silently enters every scene | Library hash diff / impact report | Candidate revisions; explicit shot migration |
| Paid job repeats after timeout | Request ledger and provider status | Poll same ID; reserve unknown charge |
| Parallel agents overspend or overwrite | Single coordinator, file ownership, budget reservation | Serialized mutations; enforced executor before autonomy |
| Untrusted `.blend` executes code | Isolated import, autoexec disabled | Review code before enabling trusted drivers |
| Missing textures/cache on HPC | Dependency inventory + destination smoke test | Package/restore and hash-check before batch |
| GPU backend unavailable or out of memory | Actual device and worst-shot test | Local/CPU fallback; reduce complexity; no blind Slurm reruns |
| Asset or motion lacks commercial rights | Source/license receipt | Block publication, not silently assume rights |
| Metric pass hides recognizable wrong face | Independent canonical comparison | Human/owner decision remains required |

## Review presentation

Keep identical camera, resolution and color settings for before/after. Include front and rear views for characters, a clean plate comparison for sets, and the hardest contact/pose for animation. Provide enough sequence frames and a real playback artifact to detect temporal problems. A contact sheet is an index, not a substitute for full-resolution inspection.

Every finding names file/revision/hash, frame/time, exact defect, affected contract and recommended bounded action. Distinguish wrong source data from wrong output, staging versus physical scale, and historical versus current. Do not issue vague "improve quality" tasks that let another agent redesign the project.

## Acceptance rubric

Owner reviews recognizable identity and felt style. Technical reviewer checks file bindings, anatomy/contact evidence, camera/world continuity, timing, stability, performance and portability. Both must refer to the same revision. A failed critical identity, support, state or timing check blocks the affected output. A missing check stays missing; it is not false failure evidence and not a pass.

Use `review-report.md` and `risk-register.csv`. For requests to relax standards, state the visible trade-off, proposed limit and affected shots. Do not quietly lower the bar to make the validator green.

## Regression expansion

After Leo/S05, add a bird with perch/fold/swim-or-flight, then a human hand/prop/seated test, then a shell/serpentine/arthropod case as future stories require. These are validation obligations, not already-tested rigs. Include cross-asset regressions: a new rock size should not break a paw contact; a changed grass shader should not alter all characters; a shared night light preset should not shift a daytime setup.

## External-library risks (1.3.0)

Use external-assets.md for acquisition and adaptation. Anticipate: free preview but paid source tier; conflicting pack/site license; permissive mesh with separately licensed maps; embedded restricted textures inside a shared .blend; expired source URLs; untrusted drivers; unsupported game-engine shaders; huge texture memory; repeated foliage silhouettes; photoreal/low-poly style mixing; texture-density mismatch; inappropriate stand/perch surfaces. A metadata pass cannot waive these risks or grant permission.
