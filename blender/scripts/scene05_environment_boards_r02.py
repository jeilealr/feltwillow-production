"""Assemble real environment review renders and source-bound delivery receipt."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/scene05_environment_r02';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def f(n):return ImageFont.truetype(FONT,n)
def board(size,title,note):
 im=Image.new('RGB',size,'#18302b');d=ImageDraw.Draw(im);d.text((24,16),title,font=f(30),fill='white');d.text((24,60),note,font=f(18),fill='#c6d4ca');return im

def panel(im,path,xy,label,size=(936,527)):
 x,y=xy;src=ImageOps.contain(Image.open(path).convert('RGB'),size);im.paste(src,(x,y));ImageDraw.Draw(im).text((x,y-32),label,font=f(22),fill='white')
plate=ROOT/'character/locations/lion_and_mouse_v6/great_tree/tree_dusk_r02.png'
im=board((1944,700),'Great Tree — approved plate and first reusable 3D environment','Broad landmark arrangement, not a calibrated pixel match. Candidate surface/sky/foliage fidelity remains open.')
panel(im,plate,(24,134),'Approved dusk r02 geography');panel(im,P/'environment_wide.png',(984,134),'Environment r02 — actual Cycles render');im.save(P/'plate_comparison.png')
im=board((1944,1340),'Scene 05 — environment review','Empty set / contact area / provisional crop / diagnostic overview. No character performance is shown.')
for path,xy,label in [('environment_wide.png',(24,134),'Wide set — permanent landmarks'),('root_contact_detail.png',(984,134),'Low approach root and visible ground'),('interaction_crop_study.png',(24,784),'Current proposed p02 crop study — unapproved camera'),('overview_diagnostic.png',(984,784),'Overview outside matte beauty envelope')]:panel(im,P/path,xy,label)
im.save(P/'environment_review_board.png')
im=board((1944,700),'Scene 05 — geometric interaction reserve','Blue shapes are proxies only. Leo rest volume is conceptual; no lie-down pose or real Milo model is validated.')
panel(im,P/'route_proxy_overlay.png',(24,134),'.375 BU Milo height / 1.5 BU neutral Leo reference');panel(im,P/'root_proxy_detail.png',(984,134),'Approach route around the fixed low root');im.save(P/'interaction_proxy_board.png')
im=board((1944,700),'Great Tree — limited background view envelope','Fixed scenery, fixed mattes; primary camera shifted ±.25 BU and retargeted. Larger/reverse views remain unqualified.')
panel(im,P/'envelope_left.png',(24,134),'Left envelope extreme');panel(im,P/'envelope_right.png',(984,134),'Right envelope extreme');im.save(P/'camera_envelope_board.png')
# Label the small static route overview with landmarks, without altering source renders.
im=Image.open(P/'route_proxy_overlay.png').convert('RGB');d=ImageDraw.Draw(im);labels=[((655,250),'OAK_MAIN'),((98,379),'ROOT_APPROACH_A'),((390,349),'Leo rest PROXY'),((606,401),'Milo PROXY'),((645,444),'clear route')]
for xy,label in labels:
 box=d.textbbox(xy,label,font=f(16));d.rectangle((box[0]-4,box[1]-3,box[2]+4,box[3]+3),fill='#18302b');d.text(xy,label,font=f(16),fill='white')
im.save(P/'route_landmark_overlay.png')
# Bind actual final files. Source image/production-plan checks are independent of art review.
ENV=ROOT/'blender/assets/environments/great_tree/great_tree_environment_r02.blend';SHOT=ROOT/'blender/scenes/lion_and_mouse_v6/s05_environment_r02.blend';eh=sha(ENV);sh=sha(SHOT)
validation=json.loads((P/'validation.json').read_text());assert validation['environment_sha256']==eh and validation['scene_sha256']==sh;assert all(validation['checks'].values()),validation['checks']
records=[]
for name in ['render_manifest.json','proxy_render_manifest.json']:
 rows=json.loads((P/name).read_text());rows=[r for r in rows if r['environment_sha256']==eh and (r['scene_sha256'] is None or r['scene_sha256']==sh)]
 (P/name).write_text(json.dumps(rows,indent=2));records.extend(rows)
 for r in rows:assert sha(P/r['path'])==r['sha256'] and list(Image.open(P/r['path']).size)==r['size']
assert len(records)==9,len(records)
auth=json.loads((ROOT/'blender/config/scene05_environment_r02_authority.json').read_text())
for r in auth['records']:assert sha(ROOT/r['path'])==r['sha256'],r['path']
old=json.loads((P/'existing_asset_inventory.json').read_text())
for r in old['files']:assert sha(ROOT/r['path'])==r['sha256']
files=[x for x in P.iterdir() if x.is_file() and x.suffix in ['.png','.json'] and x.name!='delivery_manifest.json']+[ROOT/'blender/docs/scene05_environment_contract.md',ROOT/'blender/docs/scene05_environment_r02_report.md',ROOT/'blender/config/scene05_environment_r02_authority.json',ROOT/'blender/config/great_tree_ambient_presets_r02.json',ROOT/'blender/README.md']+list((ROOT/'blender/scripts').glob('*scene05_environment*r02*.py'))+[ROOT/'blender/scripts/scene05_environment_inspect.py']
receipt={'status':'first reusable environment prototype, art match incomplete, owner review pending','environment_sha256':eh,'scene_sha256':sh,'final_render_count':9,'all_10_limited_checks_pass':True,'sources_unchanged':True,'prior_prototypes_unchanged':True,'external_requests':0,'additional_cost_usd':0,'files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)]};(P/'delivery_manifest.json').write_text(json.dumps(receipt,indent=2));print('ENV_DELIVERY_VERIFIED',json.dumps({'environment_sha256':eh,'scene_sha256':sh,'renders':len(records),'checks':validation['checks']}))
