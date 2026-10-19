"""Assemble real r02 evidence and a short sampled rig preview with Pillow."""
from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/leo_tripo_canonical_r02';OLD=ROOT/'blender/renders/leo_tripo_canonical_r01'
try:FONT=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18);TITLE=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
except OSError:FONT=TITLE=ImageFont.load_default()
receipts=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def board(filename,entries,columns=2,cell=500):
    rows=(len(entries)+columns-1)//columns;out=Image.new('RGB',(columns*cell,rows*(cell+40)+60),(238,236,232));d=ImageDraw.Draw(out);d.text((16,15),'Leo r02 — refinement, felt and controlled rig trial',font=TITLE,fill=(25,25,25));inputs={}
    for i,(label,path) in enumerate(entries):
        im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(cell-12,cell-12));x=(i%columns)*cell;y=(i//columns)*(cell+40)+60
        out.paste(im,(x+(cell-im.width)//2,y+(cell-im.height)//2));d.text((x+8,y+cell+3),label,font=FONT,fill=(25,25,25));inputs[str(path.relative_to(ROOT))]=sha(path)
    dest=P/filename;out.save(dest);receipts.append({'path':str(dest.relative_to(ROOT)),'sha256':sha(dest),'inputs':inputs})

board('whisker_repair_comparison.png',[("Imported dark geometry / before",P/'imported_whiskers_before.png'),('Imported branches removed / six cream retained',P/'whiskers_final_close.png')])
board('refinement_comparison.png',[('r01 / before',OLD/'front_three_quarter.png'),('r02 / current candidate',P/'front_three_quarter.png'),('r01 rear',OLD/'rear.png'),('r02 rear / restrained surface refinement',P/'rear.png')])
board('felt_material_comparison.png',[('Local felt / same geometry, wool and light',P/'local_felt_body_detail.png'),('PATINA height + roughness / original Leo colors',P/'patina_felt_body_detail.png'),('Local felt face',P/'local_felt_portrait.png'),('PATINA felt face',P/'patina_felt_portrait.png')])
views=['front','left','right','rear','front_three_quarter','rear_three_quarter','elevated_three_quarter','portrait']
board('turnaround.png',[(v.replace('_',' '),P/(v+'.png')) for v in views],columns=4,cell=360)
board('controlled_rig_comparison.png',[('Neutral / frame 1',P/'motion/frame_001.png'),('Head turn / frame 9',P/'motion/frame_009.png'),('Opposite head turn / frame 25',P/'motion/frame_025.png'),('Planted body shift / frame 41',P/'motion/frame_041.png'),('Body shift / side',P/'rig_body_shift_right.png'),('Head turn / portrait',P/'rig_head_turn_portrait.png')],columns=3,cell=400)
images=[];inputs={}
for frame in range(1,50,4):
    path=P/('motion/frame_%03d.png'%frame);im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,0,512,30),fill=(238,236,232));d.text((8,5),'Rig trial — frame %d / sampled every 4 frames'%frame,font=FONT,fill=(25,25,25));images.append(im);inputs[str(path.relative_to(ROOT))]=sha(path)
gif=P/'controlled_rig_preview.gif';images[0].save(gif,save_all=True,append_images=images[1:],duration=167,loop=0,disposal=2)
receipts.append({'path':str(gif.relative_to(ROOT)),'sha256':sha(gif),'fps_approx':6,'source_frames':list(range(1,50,4)),'inputs':inputs})
(P/'board_manifest.json').write_text(json.dumps(receipts,indent=2)+'\n');print('Created five boards and sampled rig GIF')
