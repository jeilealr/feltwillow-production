# Risk register and experiment review

**Completed test results:** [2026-10-16 report](RESULTS_2026-10-16.md).
The original plan/assessment below is retained as context.

No results are recorded yet. A blank field means **not evaluated**, never pass.

## Stop/go matrix

| Risk / detection | Stop condition | Resume evidence |
|---|---|---|
| ROCm/attention/precision incompatibility | Import/kernel error or no compatible path | Pinned isolated stack completes one control example on allocated MI250X |
| HBM or host RAM exhaustion | OOM or cap exceeded | Revised offload/resolution/resource estimate approved; no edits to baseline environment |
| Storage or quota uncertainty | Download budget/headroom unverified | File-size manifest plus project/user byte and inode headroom; one weight set |
| Debug partition misuse | Routine renders, sweep, repeated long attempts or second ordinary dev job | Move to small/standard as appropriate; explicitly bounded diagnostic only |
| Guide domain mismatch | Motion ignores controls or outlines damage animal identity | Control ablation follows intended movement and visual review passes |
| Geometry/cut mismatch | Different plate/view/crop, hard cut, or contact/scale drift | Responsible owner reconciles endpoints; regenerate hashes; no local policy workaround |
| Unsupported end-image behavior | Endpoint is required but capability unknown/fails | Empirical combined-control endpoint proof, or restrict to start-only independent experiments |
| Style/identity/anatomy loss | Face, ears, mane, actor count, paws or background materially regress | Owner-reviewed improvement without critical regressions |
| Unverified LoRA | Unsupported keys/expert pairing or unexplained effect | Exact adapter/backend match and separate loading/visual test |
| No measurable benefit | Control equals/worsens baseline, or overhead outweighs gain | New hypothesis approved before spending more; retain I2V for this shot |
| Governance failure | Source changed, false review, no runtime readiness | Fresh evidence through existing workflow; experiment never promotes itself |
| Blender complexity | Backend unproven or proxy is sufficient | Proxy A/B gain plus a specific depth/camera need; bounded CPU/headless smoke proof |

## Comparison template (`compare.md` in each run)

```markdown
# <run_id>: baseline vs controlled vs control ablation
Status: not evaluated
Production eligible: false
Reviewer/date: pending
Manifest SHA-256: pending
Input and result receipt paths/hashes: pending
Source image roles (fixed-start / reference / end conditioning or evaluation): pending
Resolution, frames, FPS and experimental duration: pending
Settings differing across models and reason: pending
Control-ablation change (all other settings held fixed): pending

| Criterion | Baseline 0–4 | Controlled 0–4 | Frame/time evidence | Pass/fail |
|---|---|---|---|---|
| Intended movement / trajectory | | | | |
| Paw/support contact and grounding | | | | |
| Camera/crop/landmark stability | | | | |
| Milo identity, face, ears, anatomy | | | | |
| Leo identity, mane, face, paw count | | | | |
| Background, props and visual style | | | | |
| Consistency with selected start bytes | | | | |
| End-image coherence (or explicitly not tested) | | | | |
| Temporal smoothness / flicker | | | | |
| Dialogue-region stability before lip-sync (when relevant) | | | | |

Peak host RAM / HBM, wall time, allocated GCD-hours: pending
Guide preparation time / engineering time / output bytes: pending
Control ablation: motion changed in expected direction? pending
Decision: hold / stop / next bounded test (never production approval)
Critical regressions, failure frames and next hypothesis: pending
```

Scoring anchors: 0 unusable; 1 major errors; 2 mixed; 3 acceptable for the stated
experiment; 4 consistently strong. Use N/A with reason for absent actors or
unsupported endpoints. Do not average away identity, anatomy, cut, grounding,
or governance failures. Inspect full clips plus actual first/middle/last frames;
record file hashes and frame indices. Metadata does not constitute visual review.

Predeclare the main failure to improve and measurable target before rendering.
For P1, annotate a small set of silhouette/contact samples and compare achieved
movement, stationary-ground contact and landmark displacement. Provisional
review tolerance: planted support drift ≤2% of frame height and fixed landmark
drift ≤1% of frame width, unless a documented action accounts for it. These
are experiment diagnostics, not new staging rules. Record normalized distances
and uncertainty; silhouettes cannot validate paw anatomy automatically.
For P2/P3 prioritize stable identity/framing and no invented actors or face loss.

Advance beyond the first comparison only if control visibly responds to the
ablation, motion improves by at least one rubric point over baseline, and no
critical criterion regresses; disclose preparation and compute cost. A second
seed checks repeatability only after that first success. Stop if results remain
equal/worse or complexity is unjustified. An owner-reviewed experimental pass
permits proposing a next test, not production integration or v6 approval.
