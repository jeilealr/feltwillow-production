# V6 focused integration finish — in progress

The owner preferred trial C for Scene 04 p03 and authorized applying that finish to every v6 keyframe needing it. The active goal covers all 96 images, their scene continuity, successful adoption, selection records and contact sheets. This folder is a new scoped review; the completed perceptual-world review stays closed.

`audit.json` records a decision for every current source hash. All 16 current scene sheets were screened. Initial findings select 51 slots (39 distinct source images) for finishing and retain 45. These are integration decisions, not anatomy/scale or render approvals. Sources that deliberately share identical bytes receive identical finished bytes.

Open `owner_review.html` for current prepared pairs and remaining work. `frames/<id>/` stores the exact prompt, raw built-in ImageGen output, bounded finish, edit/protected-feature masks and hash-bound receipt. The original selected composite stays active until the finish and adjacent sequence pass inspection. Original composites are also recoverable from the pre-finish Git commit; adoption must preserve their hashes and recovery locators.

The current bounded workflow replays selected actor alpha/placement and restores original scenery, other actors and central facial features. For portraits where the generator shifts shoulder/head details, only its smooth bounded lighting field is transferred to original pixels. This preserves selected anatomy/material detail while using model-suggested integration lighting. Raw generated backgrounds are never accepted as a new plate.

`finish_frame.py` replays a selected RGBA composition receipt. `update_review.py` refreshes audit counts and the comparison page. Exact historical selected composition metadata for older images was recovered from Git into `legacy_selected_compositions.json`; it does not restore rejected PNGs or grant new approvals. Some older composites and net-contact views still need a scoped mask/receipt path before finishing. They remain pending, not silently retained.

Remaining work: finish all selected distinct images; inspect native results and every affected scene/duplicate group; reject or correct any face, silhouette, palette, net/contact or lighting drift; preserve original composites and adopted finish provenance; update all hash-bound plans/owner-delegated finish selection records and current scene sheets; run focused verification and commit. Video-control implementation remains unchanged.

Temporary runs use `/scratch/project_465002727/jelealro/tmp/integration-finish`. Image libraries are available in `/scratch/project_465002727/jelealro/tmp/perceptual-world/image-env`. No API fallback was used.
