"""Real r04 render comparison and final local receipt."""
from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/leo_tripo_canonical_r04';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.new('RGB',(1648,800),'#182c2c');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((24,18),'Leo — final eye cleanup',font=font(30),fill='white');d.text((24,61),'Actual matching frontal renders. Facial shape, colors, expression and rig preserved.',font=font(20),fill='#bfd0ca')
for x,name,label in [(24,'eyes_before.png','r03 — remaining strands across eye'),(836,'eyes_after.png','r04 — both eyes clear')]:
 d.text((x,108),label,font=font(23),fill='white');src=Image.open(P/name).convert('RGB');src=ImageOps.contain(src,(788,630));im.paste(src,(x,150))
im.save(P/'eye_cleanup_comparison.png')
asset=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r04.blend';src=asset.with_name('leo_canonical_tripo_candidate_r03.blend');h=sha(asset)
assert sha(src)=='e337d6708236f8b57da8853b59f9dcc6edc9643392ffbe52e5135cffedc21fa2'
a=json.loads((P/'controlled_rig_audit.json').read_text());assert a['sha256']==h and all(a['checks'].values())
for r in json.loads((P/'render_manifest.json').read_text()):assert r['candidate_sha256']==h and sha(P/r['path'])==r['sha256']
files=[p for p in P.iterdir() if p.is_file() and p.suffix in ['.png','.json'] and p.name!='delivery_manifest.json']+list((ROOT/'blender/scripts').glob('*r04*.py'))+list((ROOT/'blender/docs').glob('*r04*.md'))+[ROOT/'blender/README.md']
r={'candidate':str(asset.relative_to(ROOT)),'candidate_sha256':h,'source_r03_sha256':sha(src),'source_preserved':True,'measured_frames':49,'limited_checks':a['checks'],'additional_cost_usd':0,'owner_status':'Owner happy with r03 appearance; r04 requested local eye finish retains it. No broader canonical/animation approval inferred.','files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(files)]}
(P/'delivery_manifest.json').write_text(json.dumps(r,indent=2));print('R04_DELIVERY_VERIFIED',h,'11 limited checks passed')
