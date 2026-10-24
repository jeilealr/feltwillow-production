# L008 local composition proposal

Two guided scene generations failed to retain the reviewed body. Use the original owner-selected L001 as the unchanged full background/Leo layer, with the selected r004 transparent Milo as foreground. This avoids repainting the incorrect Milo and avoids AI redrawing the replacement.

[Exact sources/hashes and transform](COMPOSITION_RECIPE.json): scale 0.32 uniformly, translation (78,350) on the 1672×941 scene. Proposed leading-foot contact is approximately (473,653), manually observed; camera/depth and body ratios remain unmeasured. No part warps, recoloring, face replacement or new generation. The r004 face replaces the failed scene face along with the whole actor. Preserve old images and receipts.

**One local Pillow composition, zero provider requests, zero generation cost.** Review contact/scale/edges/lighting before propagation. No synthesized shadow in this first local candidate; any later finishing is separate. No output composed yet: current image-tool instructions require explicit selection of a non-imagegen editing method before using local image editing.
