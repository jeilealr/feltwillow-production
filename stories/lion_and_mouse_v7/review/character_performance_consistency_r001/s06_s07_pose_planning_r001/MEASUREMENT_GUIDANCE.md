# Per-character ratio guidance for S06/S07

These are projected visible-surface baselines from each selected canonical, with annotation uncertainty. They are not automatically design targets. Milo requested upright projected head fraction is 0.39 ±0.01 at comparable head pitch; never apply it to a crouch, a raised/lying Leo or a portrait crop. Keep paw colors, cream-patch boundaries and horizontal widths as well as heights.

S05 selected setup measurements are a staging anchor, not a standing-height calibration: do not infer a physical Milo/Leo ratio from lying Leo. Camera/depth remain camera_unknown. A previously stated same-depth 0.25 standing-equivalent design guide is not a measured value in S05.

## Milo

| Visible surface ratio | Canonical observation | Comparability |
|---|---:|---|
| projected_head_fraction | 0.3947 · interval [0.3728, 0.4173] | same upright pose and head pitch |
| head_to_torso | 1.0646 · interval [0.9319, 1.2248] | same pose; torso is explicitly a surface-axis proxy |
| ear_to_skull | 0.8106 · interval [0.7211, 0.9109] | near ear only, same yaw/pitch |
| far_ear_to_skull | 0.6599 · interval [0.5696, 0.7613] | far ear only, same yaw/pitch |
| eye_to_skull | 0.2374 · interval [0.2018, 0.2774] | near open eye, same yaw/pitch |
| far_eye_to_skull | 0.0935 · interval [0.0658, 0.1247] | far open eye, same yaw/pitch |
| eye_spacing_to_skull | 0.4376 · interval [0.3956, 0.4846] | same yaw/pitch |
| visible_arm_path_to_torso | 0.6237 · interval [0.3911, 0.9043] | surface proxy, not anatomical arm chain or elbow calibration |
| torso_to_visible_standing_leg_height | 1.8736 · interval [1.513, 2.3348] | upright surface proxy; invalid for bent legs |
| tail_arc_to_torso | 1.6839 · interval [1.0725, 2.4218] | visible tail in this projection only |
| tail_thickness_to_torso | 0.1608 · interval [0.1055, 0.2276] | same registered tail segment/projection |
| upper_torso_panel_to_head_width | 0.4388 · interval [0.3605, 0.5267] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match |
| belly_panel_to_head_width | 0.5276 · interval [0.4444, 0.6209] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match |
| lower_belly_panel_to_head_width | 0.4868 · interval [0.3923, 0.5929] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match |
| belly_panel_to_torso_height | 0.6246 · interval [0.5088, 0.7643] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| belly_panel_to_head_height | 0.5867 · interval [0.5013, 0.6797] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match |
| lower_to_upper_torso_panel_width | 1.1093 · interval [0.8357, 1.4654] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| pelvis_band_to_head_width | 0.7434 · interval [0.6395, 0.8601] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match; limb support/roll must match |
| near_thigh_band_to_head_width | 0.2902 · interval [0.22, 0.369] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match; limb support/roll must match |
| near_thigh_band_to_pelvis_band | 0.3903 · interval [0.287, 0.5142] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; limb support/roll must match |
| near_arm_band_to_head_width | 0.2038 · interval [0.1383, 0.2774] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; head yaw/pitch must also match; limb support/roll must match |
| cream_upper_to_torso_panel_width | 0.6120 · interval [0.4541, 0.8176] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| cream_belly_to_torso_panel_width | 0.6136 · interval [0.4795, 0.7806] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| cream_lower_to_torso_panel_width | 0.6305 · interval [0.4635, 0.8555] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| cream_patch_width_to_height | 0.3581 · interval [0.2918, 0.4334] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| cream_patch_height_to_torso_height | 1.0703 · interval [0.9163, 1.2561] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges |
| pelvis_band_to_belly_panel_width | 1.4091 · interval [1.1557, 1.7245] | same upright three-quarter body yaw/lean and registered surface station; no arms/props substituted for torso edges; limb support/roll must match |
| near_closed_hand_to_head_width | 0.2206 · interval [0.1678, 0.2799] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| far_closed_hand_to_head_width | 0.1631 · interval [0.1134, 0.2188] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| near_foot_front_span_to_head_width | 0.3813 · interval [0.3197, 0.4504] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| far_foot_side_span_to_head_width | 0.5108 · interval [0.4376, 0.5929] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| near_foot_projected_aspect | 2.1781 · interval [1.5843, 3.1053] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| far_foot_projected_aspect | 2.7308 · interval [2.0532, 3.7581] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| near_closed_hand_height_to_head_height | 0.2133 · interval [0.1535, 0.2786] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| near_foot_span_to_pelvis_band | 0.5129 · interval [0.4172, 0.6277] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |
| near_closed_hand_to_arm_band | 1.0824 · interval [0.6789, 1.8033] | same named near/far hand/foot, orientation, load and support; near frontal breadth and far side heel-to-toe span are not interchangeable; head-normalized metrics also require compatible head yaw/pitch |

Unmeasured/occluded quantities stay unavailable; no hidden joints inferred.

## Leo

| Visible surface ratio | Canonical observation | Comparability |
|---|---:|---|
| mane_to_visible_face_width | 1.9888 · interval [1.7848, 2.2222] | same three-quarter local image; visible face proxy, not skull |
| mane_height_to_visible_face_height | 2.3231 · interval [2.0714, 2.6167] | same local image; forehead partly hidden |
| muzzle_to_visible_face_width | 0.5994 · interval [0.5092, 0.7027] | same head yaw/pitch |
| near_eye_to_visible_face_width | 0.2381 · interval [0.1969, 0.2853] | near open eye same head angle |
| far_eye_to_visible_face_width | 0.1513 · interval [0.1155, 0.1922] | far open eye same head angle |
| eye_spacing_to_visible_face_width | 0.4573 · interval [0.4075, 0.5143] | same head yaw/pitch |
| near_ear_to_visible_face_width | 0.3994 · interval [0.3217, 0.4882] | near visible ear same head angle |
| far_ear_to_visible_face_width | 0.3744 · interval [0.2983, 0.4614] | far visible ear same head angle |
| near_forepaw_to_visible_face_width | 0.6583 · interval [0.5643, 0.7658] | same standing three-quarter projection/depth; not universal paw ratio |
| near_hindpaw_to_visible_face_width | 0.5546 · interval [0.4672, 0.6547] | same standing three-quarter projection/depth |
| visible_tail_shaft_to_face_width | 0.6696 · interval [0.3544, 1.0301] | shaft only; not complete anatomical tail length |
| tail_tuft_to_visible_face_width | 0.5462 · interval [0.4488, 0.6577] | same tuft projection |
| visible_flank_to_face_width | 0.9384 · interval [0.7743, 1.1261] | surface proxy only; same standing view |
| mane_height_to_standing_silhouette | 0.6927 · interval [0.6532, 0.7336] | standing Leo only, height includes mane |
| near_hind_thigh_to_visible_face_width | 0.5434 · interval [0.4147, 0.6907] | same standing quadruped view, yaw, support and occlusion; actual local bytes only, pending owner hash reconciliation |
| near_foreleg_to_visible_face_width | 0.4342 · interval [0.3333, 0.5495] | same standing quadruped view, yaw, support and occlusion; actual local bytes only, pending owner hash reconciliation |
| near_hind_thigh_to_hindpaw_width | 0.9798 · interval [0.7248, 1.2921] | same standing quadruped view, yaw, support and occlusion; actual local bytes only, pending owner hash reconciliation |
| visible_cream_chest_to_face_width | 0.4006 · interval [0.2808, 0.5375] | same standing quadruped view, yaw, support and occlusion; actual local bytes only, pending owner hash reconciliation |
| visible_hindquarter_panel_to_face_width | 0.5070 · interval [0.3806, 0.6517] | same standing quadruped view, yaw, support and occlusion; actual local bytes only, pending owner hash reconciliation |
| far_forepaw_to_visible_face_width | 0.6078 · interval [0.5066, 0.7237] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| exposed_far_hindpaw_to_face_width | 0.3529 · interval [0.2572, 0.4625] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| near_forepaw_projected_aspect | 2.1963 · interval [1.6929, 2.931] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| near_hindpaw_projected_aspect | 1.9223 · interval [1.4472, 2.6265] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| far_forepaw_projected_aspect | 2.0093 · interval [1.5078, 2.7386] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| near_forepaw_to_hindpaw_span | 1.1869 · interval [0.9862, 1.4326] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| exposed_foreleg_to_visible_face_height | 0.6923 · interval [0.54, 0.87] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| mane_width_to_near_forepaw | 3.0213 · interval [2.6667, 3.4419] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| visible_tail_thickness_to_face_width | 0.1457 · interval [0.084, 0.2162] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |
| near_foreleg_to_forepaw_width | 0.6596 · interval [0.498, 0.8512] | same named quadruped limb/paw, yaw, standing support/load and mane/leg occlusion; partial far hindpaw remains partial; actual local-byte observation only pending canonical hash reconciliation |

Unmeasured/occluded quantities stay unavailable; no hidden joints inferred.

