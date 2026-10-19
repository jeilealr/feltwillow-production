"""Assemble actual saved images only; no image synthesis or source modification.
Run with Python + Pillow after leo_tripo_canonical_pass.py completes.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'blender/renders/leo_tripo_canonical_r01'
CANON=ROOT/'character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png'
ATLAS=ROOT/'character/characters/lion_and_mouse_v6/Leo/references/l_complete_reference_r01_candidate.png'
try:
 FONT=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',19)
 TITLE=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',27)
except OSError:FONT=TITLE=ImageFont.load_default()
receipts=[]
def board(name,entries,columns=3,cell=450):
 rows=(len(entries)+columns-1)//columns
 out=Image.new('RGB',(columns*cell,rows*(cell+44)+65),(238,236,232));d=ImageDraw.Draw(out)
 d.text((18,15),'Leo — imported candidate r01 / unapproved prototype',font=TITLE,fill=(30,30,30))
 inputs={}
 for i,(label,path) in enumerate(entries):
  im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(cell-14,cell-14))
  x=(i%columns)*cell;y=(i//columns)*(cell+44)+65
  out.paste(im,(x+(cell-im.width)//2,y+(cell-im.height)//2));d.text((x+10,y+cell+4),label,font=FONT,fill=(20,20,20))
  inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 dest=P/name;out.save(dest)
 receipts.append({'path':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'inputs':inputs})

board('comparison.png',[
 ('Approved 2D canonical',CANON),('Normalized import / original shader',P/'import_before_front_three_quarter.png'),
 ('Candidate / same camera and lighting',P/'front_three_quarter.png'),('Candidate face / neutral light',P/'portrait.png')],columns=2,cell=590)
views=['front','left','right','rear','front_three_quarter','rear_three_quarter','elevated_three_quarter','portrait']
board('turnaround.png',[('Approved 2D canonical',CANON)]+[(v.replace('_',' '),P/(v+'.png')) for v in views])
board('shape_diagnostics.png',[(v.replace('_',' '),P/(v+'.png')) for v in ['clay_three_quarter','clay_rear','wire_right','silhouette_three_quarter','story_light_study','import_before_rear']])
board('atlas_comparison.png',[('Supporting atlas / pending approval',ATLAS),('Candidate left',P/'left.png'),('Candidate right',P/'right.png'),('Candidate rear',P/'rear.png')],columns=2,cell=590)
(P/'board_manifest.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('Created four review boards from saved images')
