# Lion and Mouse v6 second image-audit remediation

**Date:** 13 October 2026
**Branch:** `working-cloud-branch`
**Starting commit:** `ce821fc1573c05215fae84ae6672ccf0d32f4645`
**Implementation state:** validation completed; the resulting commit is recorded in the repository history and final handoff.
**Starting tree:** clean; branch was checked out at the task start and already matched the requested `working-cloud-branch` after fast-forward to this starting SHA.

## Result

The pipeline remediation and review records are implemented. All 96 current PNG candidates are hash-inventoried below. One active candidate remains rejected, four are stale against the current camera plan, and 91 await full-size owner review. Ten versioned replacements across Scenes 6, 8, 10 and 15 are now generated and hash-recorded; all remain pending owner review. The owner approved the current Milo canonical and hunter-net hashes for replacement generation and selected six of the nine required anchor families. Three fresh calibration candidates are staged with exact hashes and remain pending owner review; five of the 14 replacement targets remain blocked on those anchors. Video rendering remains blocked.

The six owner-liked frames (`s01_p04`, `s05_p01`, `s06_p03`, `s12_p03`, `s07x_p01`, `s07x_p02`) were preserved without modifying their PNG bytes. The six selected setup-anchor candidates remain byte-identical; stable anchor snapshots were added without replacing the originals. Approved Leo canonical and location masters were preserved.

## Implemented

- Current character identity and the same-depth cast ratio are rendered from the story-local `visual_bible.json`. V6 Milo’s identity explicitly says no mane, crest or tuft; the active target ratio is 0.25 with a 0.22–0.28 review range. Historical v4 0.55/1:3 language is clearly labeled v4-only.
- Candidate-era prompt/reference fields are migrated to historical provenance fields. The current generation contract derives fresh prompts and sources from the bible and staging plan; missing historical cache inputs now appear as warnings separate from live blockers.
- Every active frame has a hash-bound freshness and disposition record. The visual gate requires complete human review evidence and per-visible-actor paw-count, no-missing-or-duplicated-limbs and support-contact fields. Stale frames remain supersession work, not visual rejections.
- Candidate revision requires a newer revision and an existing replacement PNG before stale state can clear; it preserves the old hash and review history.
- Added tests for bible-authoritative identity/scale, historical warnings versus live authority blockers, explicit dispositions, anatomy evidence, stale-candidate handling and replacement revision checks.
- Added the [29-family setup-anchor selection packet](lion-and-mouse-v6-size-anchor-review-2026-10-13.md), with exact staged target geometry and current candidate path/hash for each family.

### Owner-reported failures and hash history

| Frame | Rejected/current candidate SHA-256 | Prior rejected SHA-256 | Replacement SHA-256 | Finding |
|---|---|---|---|---|
| `s08_p04` | `7f4ef9495bfc52d53f50d8fbc4701ecf98d5c69a50575f0c6f38e9e72886c440` | `7f4ef9495bfc52d53f50d8fbc4701ecf98d5c69a50575f0c6f38e9e72886c440` | `s08_p04_r03_candidate.png` — `859b4f14f9f48749cc44afec73a9a8440568f685e4a41cd74fcb6edfd2e33e4a` | Carry-over owner-reported failure: global orange cast and character drift; local full-resolution inspection also confirms broad orange grading and an open production-boundary mouth. The new candidate uses closed-mouth canonical layers and the registered plate crop; it remains pending owner review. |
| `s10_p02` | `06c36996b0be638615e37cc3d7a698baa3243daccf8246e1021d6d653a1446fa` | `06c36996b0be638615e37cc3d7a698baa3243daccf8246e1021d6d653a1446fa` | `s10_p02_r03_candidate.png` — `c241a6b3e7a90884422a066249dfbd007a0079a3ab36473de95adf0e3e72c606` | Rebuilt all four paws and connected overhead net/rope/ground loop on the approved plate; pending owner review. |
| `s14_p06` | `f6e6b1503858a1aa4ca5475e4cbcdecc224038ba68f749a092addbefba627680` | `f6e6b1503858a1aa4ca5475e4cbcdecc224038ba68f749a092addbefba627680` | **Not generated** | Owner-confirmed scale failure: Milo visibly jumps in size against the same trap_morning:wide family; s13_p01 and s14_p06 both stage Milo at depth 0.794 and height 0.119. |
| `s15_p04` | `cb630afdcf65bf290aa7a5fc660bd91ace281e43f69eecdb9934ed2287d3da4f` | `cb630afdcf65bf290aa7a5fc660bd91ace281e43f69eecdb9934ed2287d3da4f` | `s15_p04_r03_candidate.png` — `bf36806e7441bba98793a68a1a845ce30765ead3ea28d50dc6081e6891a84549` | Rebuilt from character canonicals and the approved medium-two anchor, with the net as a separate layer; pending owner review. |
| `s06_p02` | [r04 history](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/history/s06_p02_r04_candidate.png) — `1893f30c89cdc4e7acbcc1ef256faa2e910395113bfe3a46ec0501d57239ade1` | — | `s06_p02_r05_candidate.png` — `4ee2c6bba346cdf83d1c390fdc8f6101ffe6546ec24b410a6e6fed43b23d6115` | Owner-reported extra rear arm on Milo. Removed within a bounded local edit patch; r04 remains hash-preserved under review history as the correction target. r05 is pending owner visual review. |

Historical rejection chain preserved:

| Frame | Rejected r01 SHA-256 | Current active r02 SHA-256 | Replacement in this pass |
|---|---|---|---|
| `s14_p04` | `93abc605530d0c61f777d7c11f066fe416d0794bb6484ae2baeb9fa9d1a504cc` | `92066afa75a3ba884ece2e567bded4415e689d0406fa031141057e17f67deff8` | Not generated; active r02 remains pending review. |
| `s14_p05` | `4d61b32eada6e4fbec9ad9c7dad7258948280c371b21a37a52454821ffb2bf12` | `5361b04c1f6dc1748afb07ad0eb267c0f99c21e762c044594ad4b7d786045f08` | Not generated; active r02 remains pending review. |

These prior rejections remain in `known_rejections`; the current r02 candidates have not been changed in this pass.

### Explicit disposition of every active frame

Inventory counts: 91 current/pending review; 4 stale/supersede for camera plan; 1 current/rejected.

| Frame | Freshness | Visual disposition | Active candidate SHA-256 |
|---|---|---|---|
| `s01_p01` | `current` | `pending_review` | `6d51bad2cc8bf0c906a78f0569d8038551b5071e5378b9c367bdf863fb11da0e` |
| `s01_p02` | `current` | `pending_review` | `ef6a1c389e1b7f915d3707a98cc9c86d03c3ed4b8345da92146e8b36c9d9d372` |
| `s01_p03` | `current` | `pending_review` | `bd263f472822c1c25bb89cd4342ea16b43d723c1d67394d2a3a1443af177551d` |
| `s01_p04` | `current` | `pending_review` | `bdbd5175e4cd86ca2313290dd727da794a924b2215c10dfeb95338b94e94581f` |
| `s02_p01` | `current` | `pending_review` | `492df6934222464468a4f697b449c78f74868bcde05e73b1e0dbce9bafbf9186` |
| `s02_p02` | `current` | `pending_review` | `e890692698af2e5ecd60b4728862dcee6872ce8ab8bd02a9250556be4e45cac7` |
| `s02_p03` | `current` | `pending_review` | `6cf9f93e8ed9b713555f54f6a5f6c2d22ad1655a09ae0144b6b1e82a821c333b` |
| `s03_p01` | `current` | `pending_review` | `82f23e9edd68eab25286f0a109bf96741079009ac1c5af1493df01b94f183fe2` |
| `s03_p02` | `current` | `pending_review` | `24d7b5a3ccc49a7eee53cdf109b72013f0d8222944f5b62f24d449b4ae7cd53b` |
| `s03_p03` | `current` | `pending_review` | `7cb12ef07cb04ef2f2fe7a700abe3d297cff09c8c8a6251631527eb846de7357` |
| `s03_p04` | `current` | `pending_review` | `527ec61eb3afcb9838612d3f9532a7457cd6e90ca7169df7d508ad31ef2046f2` |
| `s04_p01` | `current` | `pending_review` | `2457b0ec290bc87beb512adb8cb9d2d94bce637908728ad0f88bd696f0680695` |
| `s04_p02` | `current` | `pending_review` | `ed00c0774149038c8f8b60013632a2f23a79209ddcde7e12bca649500800072b` |
| `s04_p03` | `current` | `pending_review` | `a1ab23ebd695c7666957e327fbb400b814aca24bbddb2749011929c75b0c7414` |
| `s04_p04` | `current` | `pending_review` | `f1be68117caeac38915ba96b4985afec0ef2f5a8ab15a9391a762bb3156defa2` |
| `s05_p01` | `current` | `pending_review` | `0009c8ce44fb26cb9f67a87b30346d740612a495bbfa6ef469b01783d67f27d6` |
| `s05_p02` | `current` | `pending_review` | `1b05ac5a975a4d6b0e52c467810cefa9e5d7ab2836bb6aec6fa68eb5c9f63684` |
| `s05_p03` | `current` | `pending_review` | `b2e5744a0e4c6ce5fb4a6ec0e9916109cbece0026e9f27fccfce6bb8885a272e` |
| `s05_p04` | `current` | `pending_review` | `7b5b1e0dcae0969458e1768eccc4ae0f1b372047a7d64c8a7a51fdda7bb44657` |
| `s06_p01` | `current` | `pending_review` | `294084f831ab4a4538e262f7e7938f3959e064868ba75b453ea56fa53cac946d` |
| `s06_p02` | `current` | `pending_review` | `1893f30c89cdc4e7acbcc1ef256faa2e910395113bfe3a46ec0501d57239ade1`; replacement r05 `4ee2c6bba346cdf83d1c390fdc8f6101ffe6546ec24b410a6e6fed43b23d6115` |
| `s06_p03` | `current` | `pending_review` | `41567d053a3298bd6201785e27b25dbe04e7172306b3077e8fb07ddfdc353f24` |
| `s07_p01` | `current` | `pending_review` | `3c92a374460695e5e0d5de20a54406252f5e3bbc816bdb52a58da7ee456271bc` |
| `s07_p02` | `current` | `pending_review` | `204c3464bc51fcace6af28037d068b3fc0845236efc8763fc0b9d2f1e608f039` |
| `s07_p03` | `current` | `pending_review` | `cb331f9cf4464acd8811be8b566c6fb1058b081fd68165bd4e1ea3842fa8e240` |
| `s07_p04` | `current` | `pending_review` | `ec98c425d417d86a252e0daa3f5d660ac7af516ad9f5c843b9ff959a20b62c7d` |
| `s08_p01` | `current` | `pending_review` | `add1e8fd434aacb94f5f79ed7a3a4a737a62ae440d148d96877e8cb1f8cce925` |
| `s08_p02` | `current` | `pending_review` | `6897037efcb63903e98e7d5d7a87ffdd6267a1932cd5fec4a5f746e8faba7b55` |
| `s08_p03` | `current` | `pending_review` | `92310192480c53b3107a0541958fa3c96bf1e2ab63a5f5277f18a44ee8073f51` |
| `s08_p04` | `current` | `pending_review` | `859b4f14f9f48749cc44afec73a9a8440568f685e4a41cd74fcb6edfd2e33e4a` |
| `s08_p05` | `current` | `pending_review` | `5760c002310bea3a96ce8686b6c5718d744f03523dc04076216162dec11bec32` |
| `s08_p06` | `current` | `pending_review` | `1a0e23c896c9da566eacfd13660a073207a8e9527c01a0138efaf2014190173a` |
| `s09_p01` | `current` | `pending_review` | `c256b2517af3ff12b168d88ebbce58ca37f4faae9a28e9dbf9f1844148239dd2` |
| `s09_p02` | `current` | `pending_review` | `d390b4a09af028e928833e7eafff63fbbe2b36120a2f861f2a9be3e8d78dc610` |
| `s09_p03` | `current` | `pending_review` | `9704f3940833d8edbcd8e695a50ca241702c52abee7263d2099dcb917b141442` |
| `s09_p04` | `current` | `pending_review` | `f374683976a52e0d0a4135e1417ceb78a763fcc34ecb70b194cb87fe10ef7d4f` |
| `s10_p01` | `current` | `pending_review` | `90748469654d581229463e18f722866f95f8a458cbfd998526419903b91b6290` |
| `s10_p02` | `current` | `pending_review` | `c241a6b3e7a90884422a066249dfbd007a0079a3ab36473de95adf0e3e72c606` |
| `s10_p03` | `current` | `pending_review` | `c8f382e3ef0a32b56a62e58a6d6d4503ff799fef61107d1be01f7203f63519a1` |
| `s11_p01` | `current` | `pending_review` | `63a4de7ea19a3ff1ceac99e42163bc57020cb4e60e2294a9f25b6b927ff4d43e` |
| `s11_p02` | `current` | `pending_review` | `cce4f43fbe82578e24c9458d0c6716812d0c745030a6aebffdbc3085993d526b` |
| `s11_p03` | `current` | `pending_review` | `e1fbfb5b8f92fa861e58bb1f0dc8ce3bb795b1c77910d8b818953cae4d12f7fc` |
| `s11_p04` | `current` | `pending_review` | `8df10cd86d2b5b5331bf9ab77220cddc978105cb01d5694ab51a880a00aebe6a` |
| `s12_p01` | `current` | `pending_review` | `0c550226c6631fc6706fa9b28a06fc637fbfb98bafff8a41d30b182ca4d15ded` |
| `s12_p02` | `stale` | `supersede_for_camera_plan` | `c84a102886b105e4aa96bef7e9d1987e85af2b3198c6edea04c6672525e17566` |
| `s12_p03` | `current` | `pending_review` | `fa222dd7257c6d7a2975bb12eba0014be3a9b7ecf2123ace30a75a529c07aef3` |
| `s12_p04` | `current` | `pending_review` | `32a83222c248b6265b10c0d1ce53c7fcc9ae278594a70545d47b3963fce43ed7` |
| `s13_p01` | `current` | `pending_review` | `ca92c68e425b0ed7c5ccf16b198e7ba11461146c6031ae4d89bd730513f10be3` |
| `s13_p02` | `current` | `pending_review` | `2081e3b199b91dd44802102eccc823062f212bbc4ad03316ea84d00d831c6857` |
| `s13_p03` | `current` | `pending_review` | `68f87262eca56d3d2483e9fd0a963ce615d534a097f9b95e707458acae09dc81` |
| `s13_p04` | `current` | `pending_review` | `152c2de6fed9a89872aab9c477f487eefad7c1a7a86df2152d5ee53840b1319b` |
| `s13_p05` | `current` | `pending_review` | `1cfaca7d5d8f07d13c40d7c6afa5fc7600ce0e692f7e86a06ae11c1722925584` |
| `s13_p06` | `current` | `pending_review` | `4d4df233dd9c140810313d986d9e7eb62b53d78e19f15f0e1072255a87f95e7d` |
| `s14_p01` | `current` | `pending_review` | `47f71cdc18ef74539bea0f2fcd178b203b4a3d652830579d343a15ff375198a3` |
| `s14_p02` | `current` | `pending_review` | `819044f9f0801830b4ef7071f575f60ca1c143f760a34705afe4ca587257517b` |
| `s14_p03` | `current` | `pending_review` | `2a9a948ef6b56a43896eb604700d033c7b193241ce61431896055f1b3c548ec5` |
| `s14_p04` | `current` | `pending_review` | `92066afa75a3ba884ece2e567bded4415e689d0406fa031141057e17f67deff8` |
| `s14_p05` | `current` | `pending_review` | `5361b04c1f6dc1748afb07ad0eb267c0f99c21e762c044594ad4b7d786045f08` |
| `s14_p06` | `current` | `rejected` | `f6e6b1503858a1aa4ca5475e4cbcdecc224038ba68f749a092addbefba627680` |
| `s15_p01` | `current` | `pending_review` | `5a0dc89bc2c02864e8f3a4de4d14133eca7f39cf53383a5c97cf28d2fe47a649` |
| `s15_p02` | `current` | `pending_review` | `80cf3a4a4879ae7143ff63b1f33499bcec2ef26b0c92f24475659980f56d8358` |
| `s15_p03` | `current` | `pending_review` | `8da43b2f1462f98f6af91d1fe95da8a1333dfd60c3920763ce10a1a22841af96` |
| `s15_p04` | `current` | `pending_review` | `bf36806e7441bba98793a68a1a845ce30765ead3ea28d50dc6081e6891a84549` |
| `s15_p05` | `current` | `pending_review` | `39e9563baf98a94576f4cd231e766cfde6d1657152f1219c880d6543286e0b4b` |
| `s15_p06` | `current` | `pending_review` | `4a766e4a2396a29a60eafd034462290eaad624740f508c2acdd680e8293f6dc5` |
| `s16_p01` | `current` | `pending_review` | `1ecb933c000c970cf9c3e639d736784223dcc4fc5b6e45486352014766020887` |
| `s16_p02` | `current` | `pending_review` | `ffbeb30e4e624a462fd255deadd531b65fa54031b76cc079ecb7cb24258d2c00` |
| `s16_p03` | `current` | `pending_review` | `73a7031bf0163007f6a9ae535034df5145c31610295230b04b7b3842924f37ac` |
| `s16_p04` | `current` | `pending_review` | `5ba1c460a5e1685ab02fe24af76f3b8652dcec3bb3f2ed27fd67ca9644cc1db3` |
| `s16_p05` | `current` | `pending_review` | `04420f7b89b2add2b2fa88c7de3a39188757d0f0c26709f351feb13f0a434984` |
| `s01x_p01` | `current` | `pending_review` | `47412d1463a362f79de00134865840d2c3ff1f60355219a9f8bef9e611306207` |
| `s01x_p02` | `current` | `pending_review` | `1188dfc2e42f3b90671141ae2e9e8d88c05bfa64e0a2fd0a8983fc728a87250b` |
| `s01x_p03` | `current` | `pending_review` | `880c498038eac6f3546c55100aad041a32839f01050b3e0c23dc67d20b33d982` |
| `s04x_p01` | `current` | `pending_review` | `e18ec1720d3b38f0063d3a74c6f12cf276a0449df1beb0c3ea6a3b2b5357f689` |
| `s04x_p02` | `current` | `pending_review` | `5c628905e2bbfbffd6ba86f0e63b3aa8a47d2d641cefc7cfbe441f048ab570d3` |
| `s04x_p03` | `current` | `pending_review` | `8c8aaa628a1c0b77d93424acd118dfed1083639b10f26b713746156f8a10b909` |
| `s05x_p01` | `current` | `pending_review` | `b93713aec61e69dcb5d0289955bb9bd87e5876393492595e654e86e04b9d8978` |
| `s05x_p02` | `current` | `pending_review` | `37a3e46df80f7919a6c7f0b3273d8f7ab3d28dabf363753d4fa93b8fcf3ffb28` |
| `s05x_p03` | `current` | `pending_review` | `c039b93adc92c28820b67f76a9ed518c207acbde1584cbb1ad787424fe36e208` |
| `s05x_p04` | `current` | `pending_review` | `ec424d43dc523fdcb744ca0bb67abca2b9ab7dfa4e67dadeb5cc1a141ed46aa3` |
| `s12x_p01` | `current` | `pending_review` | `cdb37b208825a4dbc28bddeabfe06596bde3c084f088bca59300282e03892f89` |
| `s12x_p02` | `current` | `pending_review` | `a86f73be02ee4b7d1ea7392538160be22c0af788b09b17b041fbf00092613ad3` |
| `s12x_p03` | `current` | `pending_review` | `56c09fa6bb963a1b4dbb9c9db3d0d7740fdc00d34625716d61f378ee3c6707ab` |
| `s15x_p01` | `current` | `pending_review` | `59e0ee3763a036ae62ac5115b9daffe41881a9db14ac4b33c3c6765422936b0f` |
| `s15x_p02` | `stale` | `supersede_for_camera_plan` | `f063e0009509d5b407533f4311f193eab251da6435e9a0feb788b195088ea75d` |
| `s15x_p03` | `current` | `pending_review` | `b397a3ace66f2a8300406b3e51fb7a416d7ed33456a89d0a5e48778d5f8ffa10` |
| `s15x_p04` | `stale` | `supersede_for_camera_plan` | `d0c9e7ddde3913d6f6a435053021c0c13e3447e35f603e60e66a61ca64817d04` |
| `s15x_p05` | `current` | `pending_review` | `5810119e9fdaeac98410e3ba63294c9864bf3b9ad1270a18cdd46fb620146a36` |
| `s15x_p06` | `stale` | `supersede_for_camera_plan` | `bfd423453230e8253a408c0ea0d07d3305299c8df4f54c81bf6deb767899400d` |
| `s16x_p01` | `current` | `pending_review` | `62ebb26270520b9afd3cfffebf725a035f90c63d2fa4b1d4f4902027c0572669` |
| `s16x_p02` | `current` | `pending_review` | `5a6465a898fc95fc52861358873f8dc694b6a134b773a4120f13fb0c8aa26214` |
| `s16x_p03` | `current` | `pending_review` | `93f5858883350b2bcb4eb2f776ff77e148bc342cae11b64c47cba073d1dd04c1` |
| `s05x_p05` | `current` | `pending_review` | `9194731d9f5f6a27444f4f44ff6f2b51348cdb2b9577ff5c0741f16d1ef95783` |
| `s06x_p01` | `current` | `pending_review` | `e1ae4959f017a16266c9d049a03a7df6ce9d182f699069f998a29e89cf508ca6` |
| `s07x_p01` | `current` | `pending_review` | `b94460063f02a834cfdf575bb4d0f508bc364f889b5c63896bc4da449435e827` |
| `s07x_p02` | `current` | `pending_review` | `b0f96a63971bab2baed44b0b95a0d91a68a3a88fdb5747c021de414ab7829034` |

## Validation

| Check | Result |
|---|---|
| Python unit suite (`python3 -m unittest discover -s tests -v`) | **76 tests passed**, including owner-correction-target provenance and revision-path regressions. |
| Python compile check | `python3 -m compileall -q production tests` passed. |
| Staging contract | 0 errors; 96 staged frames. |
| Pose coverage | 0 errors; 23 pose definitions cover 96 staged frames. |
| Markdown links | `python3 production/check_markdown_links.py`: all repository-relative links resolve; 0 broken links. |
| Reference gate | **67 current-authority blockers**, 57 historical-provenance warnings, 96 regeneration contracts. Pending owner approvals and unresolved stale/rejected candidates remain live blockers; historical warnings do not count as current readiness failures. All ten new candidate files now have durable Git locators. |
| Visual gate | **102 blockers** across current review and disposition checks for the 96 candidates. |
| Runtime preflight | **169 blockers**, combining reference and visual-review requirements; it writes no files. |
| Composite reproducibility | All nine Scene 8, 10 and 15 candidates regenerated from saved transparent layers and registered crop inputs with matching hashes. The s06_p02 local correction compositor also reproduced the r05 candidate byte-for-byte from the archived r04 correction target and saved edit source. |

The authority blockers include setup-anchor selection/approval, pending prop approvals where required, one unreplaced rejected frame, and four stale frames. Full-size hash-bound review is still required. The gates remain fail-closed; do not bypass them or use the current candidate set for video.

## Files changed

Pipeline code: `production/keyframe_plan.py`, `production/keyframe_reference_gate.py`, `production/keyframe_visual_gate.py`, `production/revise_keyframe_candidate.py`, `production/compose_transparent_keyframe.swift`, `production/compose_owner_correction_patch.swift`, `production/staging_contract.py`, `production/v6_runtime.py`, and `production/check_keyframe_review.py`. Tests cover the changed authority, visual, scale and revision behavior. Story records changed: `visual_bible.json`, `keyframe_plan.json`, `keyframe_regeneration_contract.json`, `keyframe_visual_reviews.json`, and `video_boundary_plan.json`. New versioned Scene 8, 10 and 15 candidates, the s06_p02 anatomy correction, preserved prior revisions under `.review/history/`, generated transparent source layers, registered crop receipts, and exact prompts are linked from the [generated-frame review packet](lion-and-mouse-v6-generated-frame-review-2026-10-13.md). Guidance and status documentation are listed in `git status`; this report is the durable record of this implementation pass.

## Regeneration and rendering decision

Regeneration is partially exercised end to end. Nine replacement candidates use already approved setup anchors; each is versioned, hash-recorded, and pending owner review. The three newly generated calibration anchors still need exact-hash approval before five dependent replacement targets can be generated. Four stale and one rejected target remain. Inspect every new frame at full resolution, record complete review/anatomy evidence, and rerun the gates. Video remains blocked until the current candidate set has no stale/rejected frames and every endpoint and authority passes.

## 14 October owner correction

The owner reported that Milo has an extra arm behind his body in `s06_p02_r04`. A localized correction produced `s06_p02_r05` without changing the source PNG; the prior revision is retained under [review history](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/history/s06_p02_r04_candidate.png). The source image was used only as a correction target, and the exact prompt, source/output hashes, generated edit layer, bounded patch rectangle and compositor hash are recorded in [`s06_p02_r05_correction_manifest.json`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/s06_p02_r05_correction_manifest.json). The candidate is pending owner review and is not approved for video.

The [generated-frame review packet](lion-and-mouse-v6-generated-frame-review-2026-10-13.md) contains ten previews, their exact hashes, the three pending calibration candidates, and the reproducible layer/composite manifests. `production/compose_transparent_keyframe.swift` reproduces the nine Scene 8/10/15 candidates; `production/compose_owner_correction_patch.swift` reproduces the localized s06_p02 correction.
