**Update, owner direction 19 October 2026:** Both existing canonicals and location masters are approved. This proposed extraction is deferred, not an identity-approval prerequisite. Preserve canonical backgrounds; a separately reviewed Leo matte may be derived when composition needs it.

# Next image operation — awaiting approval

One built-in `image_gen.imagegen` request: extract Leo’s studio background to a transparent candidate. The approved canonical bytes remain unchanged. Model, seed and current price are not exposed by the built-in tool; estimated total cost is **unknown**, never assumed free. No API fallback or retry is authorized.

Input: `character/characters/lion_and_mouse_v7/Leo/canonical/full-body_leo_neutral_pose_r01.png`

SHA-256: `6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545`

Setting: `transparent_background=true`; use that exact local reference.

Exact prompt:

```text
Use case: background-extraction
Asset type: Leo neutral canonical transparent source candidate for Feltwillow v7 foundation; not a redesigned canonical.
Input image 1: approved Leo full-body neutral identity master. It controls every existing visible pixel, pose, proportions, face, mane, rounded paws and felt pigment.
Primary request: remove only the plain studio background and its floor shadow. Preserve the full lion exactly as in the supplied reference, including soft thin mane fibers, whiskers, tail and all four paws. Preserve the current neutral pose, view, eye direction and closed mouth. Deliver one full-body RGBA cutout with a genuinely transparent background and clean alpha around the fibers. Do not add scenery, cast shadows, labels, objects or a different pose. Do not invent hidden anatomy. Preserve warm golden-cream rounded felt toes without nails. This candidate will be compared against the original at full resolution before any use. Keep the entire existing visible silhouette inside the image.
```

Output candidate: `stories/lion_and_mouse_v7/sources/Leo/neutral_matte_r001_candidate.png`. Inspect against the canonical and retain the actual tool receipt and hashes before using it. This is foundation source work, not approval of a scene pair.
