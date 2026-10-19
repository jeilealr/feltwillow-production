"""Assemble real renders for review; no generated or repainted imagery."""
from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/leo_tripo_canonical_r03';OLD=P.with_name('leo_tripo_canonical_r02');C=ROOT/'character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def f(n):return ImageFont.truetype(FONT,n)
def panel(canvas,path,box,label,crop=None):
 im=Image.open(path).convert('RGB')
 if crop:im=im.crop(crop)
 x,y,w,h=box;im=ImageOps.contain(im,(w,h));canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2));ImageDraw.Draw(canvas).text((x,y-32),label,font=f(22),fill='#e7eceb')
def board(w,h,title,subtitle):
 im=Image.new('RGB',(w,h),'#182c2c');d=ImageDraw.Draw(im);d.text((24,18),title,font=f(30),fill='white');d.text((24,62),subtitle,font=f(18),fill='#b9cfca');return im
im=board(1336,1520,'Leo — old whisker-root repair','Actual color and clay renders; matching camera / neutral light. Groom hidden to expose the repair.')
for path,box,label in [(P/'muzzle_before_color.png',(24,132,632,632),'r02 — incorrect color-atlas sampling'),(P/'muzzle_after_color.png',(680,132,632,632),'r03 — corrected cream patch'),(P/'muzzle_before_clay.png',(24,832,632,632),'r02 — slight root pinch in clay'),(P/'muzzle_after_clay.png',(680,832,632,632),'r03 — local fairing in clay')]:panel(im,path,box,label)
im.save(P/'muzzle_repair_comparison.png')
im=board(1620,730,'Leo — felt before / after','Matched body camera, neutral light, 896 px / 48 samples. Reused PATINA maps; no additional generation.')
panel(im,OLD/'patina_felt_body_detail.png',(24,132,774,570),'r02 — sparse short curls')
panel(im,P/'body_detail.png',(822,132,774,570),'r03 — finer overlapping fibers')
im.save(P/'felt_refinement_comparison.png')
im=board(1550,1080,'Leo — canonical reference and r03','Different pose/view and lighting: a qualitative material/identity comparison, not a calibrated reconstruction.')
panel(im,C,(24,132,640,900),'Approved 2D canonical')
panel(im,P/'front_three_quarter.png',(690,132,836,900),'r03 Blender candidate — actual render')
im.save(P/'canonical_comparison.png')
if '--static' in sys.argv:sys.exit(0)
frames=[Image.open(P/('motion/frame_%03d.png'%i)).convert('RGB') for i in range(1,50,4)]
frames[0].save(P/'controlled_rig_preview.gif',save_all=True,append_images=frames[1:],duration=167,loop=0,disposal=2,optimize=False)
im=board(1336,1130,'Leo — controlled rig preview','13 rendered samples from the 49-frame head-turn / body-lift trial. All 49 frames measured.')
for k,frame in enumerate(frames):
 x=24+(k%5)*260;y=132+(k//5)*320;im.paste(frame.resize((248,248)),(x,y));ImageDraw.Draw(im).text((x,y+254),'Frame %02d'%(1+k*4),font=f(18),fill='white')
im.save(P/'motion_contact_sheet.png')
# Separate obsolete trial previews from the current final render inventory.
asset=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ch=sha(asset)
mp=P/'render_manifest.json';records=json.loads(mp.read_text());final=[r for r in records if r['candidate_sha256']==ch];old=[r for r in records if r['candidate_sha256']!=ch]
if old:(P/'superseded_preview_records.json').write_text(json.dumps({'status':'Historical output hashes; original preview paths were overwritten by later trials. Preserved first-trial images are under material_trial_01/. These records are not current render evidence.','records':old},indent=2))
mp.write_text(json.dumps(final,indent=2))
assert len(final)==23,(len(final),'final renders')
for r in final:
 p=P/r['path'];assert sha(p)==r['sha256'];assert list(Image.open(p).size)==r['size']
a=json.loads((P/'controlled_rig_audit.json').read_text());assert a['sha256']==ch and all(a['checks'].values())
sourcehashes={
'blender/assets/characters/leo/leo_canonical_tripo_candidate_r02.blend':'7d60fb0c9aa96c89458152d09e5e6c88e7566507d58ff9e2a8daef0042a5768a',
'character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png':'6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545',
'blender/assets/characters/leo/imports/tripo_owner_model/model.fbx':'3ccead17de1785f9c0d0fa8b3d1f3d531ad8b0d433fba31091f601bda883b9b2'}
for name,expected in sourcehashes.items():assert sha(ROOT/name)==expected,name
receipt={'candidate':str(asset.relative_to(ROOT)),'candidate_sha256':ch,'bytes':asset.stat().st_size,'sources_preserved':sourcehashes,'final_render_count':23,'motion_rendered_frames':list(range(1,50,4)),'measured_frames':list(range(1,50)),'external_generation_requests':0,'additional_cost_usd':0,'owner_approval':'pending','files':[]}
receipt['implementation_files']=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted([*(ROOT/'blender/scripts').glob('*r03*.py'),*(ROOT/'blender/docs').glob('*r03*.md'),ROOT/'blender/README.md'])]
receipt['reused_material_files']=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted((ROOT/'blender/assets/materials/leo_felt_patina_trial').iterdir()) if p.is_file() and p.suffix in ['.png','.json']]
for p in sorted(P.rglob('*')):
 if p.is_file() and p.suffix in ['.png','.gif','.json'] and p.name!='delivery_manifest.json':receipt['files'].append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})
(P/'delivery_manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'candidate_sha256':ch,'final_renders':23,'source_checks':'passed','audit_checks':'11 passed'}))
