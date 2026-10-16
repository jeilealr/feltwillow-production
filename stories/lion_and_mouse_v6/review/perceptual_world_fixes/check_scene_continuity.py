#!/usr/bin/env python3
"""Check screen-size/axis continuity and build a scene-order viewing page."""
import hashlib
import html
import json
import os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HOME=Path(__file__).resolve().parent
ROOT=HOME.parents[3]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def head_band(c):
    a=np.asarray(Image.open(ROOT/c['still_source']['label']).convert('RGBA'))[:,:,3]>127
    y,x=np.nonzero(a);a=a[y.min():y.max()+1,x.min():x.max()+1]
    y,x=np.nonzero(a[:int(a.shape[0]*.44)])
    return c['h']*1080*int(x.max()-x.min()+1)/a.shape[0]
def main():
    plan=load(HOME/'complete_replacement_plan.json');replacements={f['id']:f for f in plan['frames']}
    active={f['id']:f for f in load(HOME.parent.parent/'keyframe_plan.json')['images']}
    groups={'scene04_action':['s04_p01','s04_p02','s04_p03','s04_p04'],
      'scene06_08_shared':['s06_p01','s06_p02','s06x_p01','s07_p01','s08_p04','s08_p06'],
      'scene16_shared':['s16_p01','s16_p04','s16_p05','s16x_p01','s16x_p02','s16x_p03']}
    results=[]
    for name,ids in groups.items():
        rows=[]
        for fid in ids:
            f=replacements[fid];r=load(ROOT/f['composition_receipt']);c=next(c for c in r['characters'] if c['actor']=='milo')
            rows.append({'id':fid,'sha256':f['sha256'],'head_band_width_px':round(head_band(c),3),'pose_height_fraction':c['h'],'crop_rect_on_plate':f['crop_rect_on_plate']})
        widths=[r['head_band_width_px'] for r in rows];spread=max(widths)/min(widths)-1
        assert spread<.01,(name,spread)
        results.append({'group':name,'screen_head_size_spread_fraction':spread,'frames':rows,'scope':'Screen-size proxy, not anatomical calibration. Camera families compared separately from portraits.'})
    axes=[]
    for fid,f in replacements.items():
        if fid.startswith(('s15_','s15x_')):
            r=load(ROOT/f['composition_receipt'])
            for c in r['characters']:
                assert (c['x']<.5 if c['actor']=='milo' else c['x']>.5),(fid,c['actor'])
                if c['actor']=='milo':assert c['flip']==False
                axes.append({'id':fid,'actor':c['actor'],'screen_center_fraction':c['x'],'face_direction':'right' if c['actor']=='milo' else 'left'})
            if len(r['characters'])>1:
                for c in r['characters']:
                    x,y,w,h=c['box'];assert x>0 and x+w<1920 and y>0 and y+h<1080,(fid,'clipped actor')
    assert 's12_p04' not in replacements
    exception=active['s12_p04'];assert sha(ROOT/exception['candidate_path'])==exception['sha256']
    # Effective frames include unchanged neighboring portraits/context, not only fixes.
    preview=HOME/'sequence_previews';preview.mkdir(exist_ok=True)
    sections=[]
    for scene in [4,6,7,8,13,14,15,16]:
        ids=[f for f in active if f.startswith(('s%02d_'%scene,'s%02dx_'%scene))]
        ids.sort();cards=[]
        sheet=Image.new('RGB',(1440,310*((len(ids)+2)//3)),'#202020');draw=ImageDraw.Draw(sheet)
        for i,fid in enumerate(ids):
            f=replacements.get(fid);path=ROOT/(f['output_path'] if f else active[fid]['candidate_path']);im=Image.open(path).convert('RGB').resize((480,270),Image.Resampling.LANCZOS)
            target=preview/(fid+'.jpg');im.save(target,quality=93)
            label='corrected candidate' if f else 'retained original'
            cards.append('<figure><a href="'+html.escape(os.path.relpath(path,HOME))+'"><img width="480" height="270" src="sequence_previews/'+fid+'.jpg" loading="lazy" alt="'+fid+'"></a><figcaption>'+fid+' — '+label+'</figcaption></figure>')
            x=i%3*480;y=i//3*310;sheet.paste(im,(x,y+30));draw.text((x+8,y+8),fid+' '+label,fill='white')
        diagnostic=Path('/scratch/project_465002727/jelealro/tmp/perceptual-world')/('final_scene_%02d.jpg'%scene);sheet.save(diagnostic,quality=95)
        sections.append('<section><h2>Scene %02d</h2><div class="sequence">'%scene+''.join(cards)+'</div></section>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Scene continuity review</title><style>body{background:#171b1c;color:#edf1ed;font:17px/1.5 system-ui;max-width:1100px;margin:30px auto;padding:0 20px}a{color:#b8dfbb}.sequence{display:flex;flex-wrap:wrap;gap:20px}figure{margin:0 0 16px;max-width:480px}img{max-width:100%;height:auto}section{border-top:1px solid #526057;margin:30px 0}</style><h1>Scene continuity review</h1><p>Effective candidate sequence, including neighboring retained images. Every preview is 480×270; click for native size. Compare shared views with shared views and portraits with portraits. Scene15 keeps Milo left / Leo right; s12_p04 remains the explicit distant-wide exception.</p><p><a href="owner_review.html">Before/after review</a> · <a href="scene_continuity_verification.json">Size and axis checks</a></p>'''+''.join(sections)+'</html>'
    (HOME/'scene_continuity.html').write_text(page)
    report={'schema':'feltwillow.scene-continuity-check.v1','scope':'Screen-size and composition checks; visual selection/anatomy approvals remain separate','screen_size_groups':results,'scene15_axis_checks':axes,'owner_exception_preserved':{'id':'s12_p04','sha256':exception['sha256']},'supplemental_closing_hold_identical':replacements['s16x_p01']['sha256']==replacements['s16x_p02']['sha256']==replacements['s16x_p03']['sha256']}
    assert report['supplemental_closing_hold_identical']
    (HOME/'scene_continuity_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: three matched size groups (<1% head-band spread), all Scene15 axes/margins, identical closing x01–03, and untouched s12_p04 exception.')
if __name__=='__main__':main()
