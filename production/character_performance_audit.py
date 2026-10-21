"""Existing-image-only comparison pack; automatic metrics never grant visual approval."""
import html
import json
import os
from pathlib import Path

try:
    from . import audio_visual_plan as av
    from . import character_performance as cp
except ImportError:
    import audio_visual_plan as av
    import character_performance as cp


def build(root,folder,plan,library):
    from PIL import Image, ImageDraw
    import numpy as np
    target=folder/cp.AUDIT;target.mkdir(parents=True,exist_ok=True)
    manifest=av.read(folder/'scene_composition_candidates.json')
    manual_path=target/'VISUAL_OBSERVATIONS.json'
    manual=av.read(manual_path) if manual_path.exists() else {'observations':[],'landmarks':{}}
    observations={r['image_id']:r for r in manual['observations']}
    images={r['image_id']:r for r in manifest['images']}
    inspected=[]
    for iid,record in images.items():
        path=cp.checked_file(root,record)
        with Image.open(path) as image:
            image.load();dimensions=list(image.size)
        observation=observations.get(iid)
        if not observation or observation['sha256']!=record['sha256']:
            observation={'image_id':iid,'sha256':record['sha256'],'inspection':'not_inspected','verdict':'not_inspected','observation':'No hash-bound native-resolution visual observation available.','reason':'A decoded image or automatic metric is not a visual verdict.','owner_verdict':None,'camera_status':'camera_unknown'}
        inspected.append({**observation,'dimensions':dimensions,'path':record['path']})
    canonical=av.read(folder/'character_library.json')['characters']['Milo']['canonical']
    groups={
        'walking':['S01-L001-B01-I02','S01-L002-B03-I02','S01-L003-B01-I02'],
        'head_route':['S03-L004-B01-I02','S01-L002-B03-I02','S03-L002-B01-I02'],
        'portrait':['S02-L003-B01-I01','S03-L009-B01-I01','S03-L010-B01-I01'],
        'fixed_fork':['S03-L006-B01-I02','S03-L007-B01-I02','S03-L008-B01-I02']}
    sheets=[]
    for name,ids in groups.items():
        sheet=Image.new('RGB',(1800,415),(28,32,28));draw=ImageDraw.Draw(sheet)
        for n,iid in enumerate(ids):
            with Image.open(root/images[iid]['path']) as source:
                image=source.convert('RGB');image.thumbnail((590,340))
            x=n*600;sheet.paste(image,(x,35));draw.text((x+5,8),iid,fill='white')
            draw.text((x+5,380),'Whole frame fit; no actor-size normalization',fill='white')
        out=target/(name+'_comparison.jpg');sheet.save(out,quality=94);sheets.append(str(out.relative_to(root)))
    # Native top strip is free of actors/contacts in these three inspected frames.
    roi=[0,0,1672,200]
    with Image.open(root/'character/locations/lion_and_mouse_v7/fork/fork_sunset_r01.png') as src:
        master=np.asarray(src.convert('RGB'))[:200]
    arrays={}
    metrics=[]
    for iid in groups['fixed_fork']:
        with Image.open(root/images[iid]['path']) as src:arrays[iid]=np.asarray(src.convert('RGB'))[:200]
        delta=np.abs(arrays[iid].astype(float)-master.astype(float))
        metrics.append({'image_id':iid,'reference':'fork_sunset_r01.png','roi_xyxy':roi,'changed_pixel_fraction':float(np.mean(np.any(delta!=0,axis=2))),'mean_absolute_channel_difference_0_255':float(np.mean(delta)),'verdict':'confirmed_defect','scope':'exact protected-background pixels differ; no inference about geometry, visual severity or anatomy'})
    first=groups['fixed_fork'][0]
    for iid in groups['fixed_fork'][1:]:
        delta=np.abs(arrays[iid].astype(float)-arrays[first].astype(float))
        metrics.append({'image_id':iid,'reference':first,'roi_xyxy':roi,'changed_pixel_fraction':float(np.mean(np.any(delta!=0,axis=2))),'mean_absolute_channel_difference_0_255':float(np.mean(delta)),'scope':'same-canvas, no alignment/resampling; confirms exact pixel mismatch'})
    report={'schema':'feltwillow.performance-audit-evidence.v1','source_manifest_sha256':av.digest(folder/'scene_composition_candidates.json'),'original_png_count':len(images),'decoded_existing_files':len(inspected),'manually_inspected':sum(r['inspection']=='inspected_native_resolution' for r in inspected),'normalization':'contact sheets fit complete frames to equal panel width; no body/face-size normalization or physical distance inference','landmarks':manual.get('landmarks',{}),'manual_tolerance_pixels':manual.get('measurement_tolerance_pixels'),'metrics':metrics,'observations':inspected,'sheets':sheets,'owner_approval':None}
    av.write(target/'AUDIT.json',report)
    text=['# Existing-image character consistency audit','','All 24 original PNGs decoded and opened at native resolution in this review; image hashes identify the inspected bytes. Original PNGs, sidecars, operation and receipts remain untouched. Findings are advisory; only the owner selects artwork.','','Starting branch/HEAD and all pre-change hashes: BEFORE.json. VISUAL_OBSERVATIONS.json contains appended manual evidence; AUDIT.json contains measured pixel evidence and file bindings.','','## Findings','','- Walking L001 / winding-path / deeper-trail: compactness and leg extension differ, with different gait and oblique projection. Suspected proportional drift in L001 needs matched-view review; camera_unknown prevents a confirmed size verdict. Shared three-quarter screen-right lightstep family is proposed, not approved.','- S03-L004: large head impression is suspected, confounded by projection; stepping also suggests early route commitment. Bind proposed stationary consideration instead of maximizing walk reuse.','- S02-L003: useful startled portrait inspiration, minimal far-ear top clearance confirmed; larger frame occupancy is consistent with portrait framing and does not prove changed anatomy. No portrait-master approval.','- Fixed-fork: approximate foot-root shifts and body extents are visible against a common background. Shared-root contract is unmet. Head turn changes projected extent, so anatomy/scale suspicion remains separate from the confirmed placement/pixel failures.','- No v6 performance atlas was adopted or used as authority.','','## Comparable fixed-camera evidence','','Manual body+ears boxes exclude tail and whiskers, tolerance about 15 px; foot-root is approximate support midpoint. These are review landmarks, not calibrated anatomy. No metric camera distance is known.','','| Image | Body+ears box xyxy | Root xy |','|---|---|---|']
    for iid,marks in report['landmarks'].items():text.append(f"| {iid} | {marks['body_ears_bbox']} | {marks['root_contact']} |")
    text+=['','Pixel ROI: native `[0,0,1672,200]`, away from actors/contact shadows. No resize or registration. Against the master, about 99% of pixels differ with mean channel differences only about 5–6/255. This proves lack of byte-identical background pixels, not a large perceptual/geographic change.','','## Per-image observations','','| Image | Verdict | Evidence / limitation |','|---|---|---|']
    for row in inspected:text.append(f"| {row['image_id']} | {row['verdict']} | {row['observation']} {row['reason']} |")
    text+=['','## Review pack','','Open review.html using the local loopback server. Full-line WAV controls remain unchanged. Toggle native size or overlays; browser verdict selectors are unsaved discussion placeholders and grant no approval. Contact sheets use complete-frame fit, never normalized actor height. The original canonical is shown separately; a crop/lighting match is not owner acceptance.','', 'Performance requirements: ../../derived/PERFORMANCE_REQUIREMENTS.md. All current registry references are planned; zero generated/approved performance assets.']
    (target/'REVIEW.md').write_text('\n'.join(text)+'\n')
    def url(path):return html.escape(os.path.relpath(root/path,target),quote=True)
    page=['<!doctype html><meta charset="utf-8"><title>V7 character consistency review</title><style>body{font:17px system-ui;background:#20241d;color:#eee;margin:25px}a{color:#c7edab}figure{margin:25px 0}img{max-width:100%;height:auto}.frame{position:relative;display:inline-block;max-width:100%}.frame img{display:block}.frame svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;display:none}body.overlay svg{display:block}body.native .frame{max-width:none}body.native img{max-width:none}audio{width:min(650px,100%)}.note{color:#ffd88c}section{border-top:1px solid #777;margin-top:35px}code{font-size:14px}</style>',
          '<h1>V7 character performance consistency</h1><p>Read-only existing-image audit. Zero new performance images; all proposed references are planned, with no owner approval. Distinguish anatomy from camera-relative size. Independent shots: camera_unknown. Fixed fork: shared root/scale required.</p>',
          '<p><a href="../scene_compositions/s01_s03_r001/review.html">Original 24-image audio gallery</a></p><label><input type="checkbox" onchange="document.body.classList.toggle(\'native\',this.checked)">Native image size (scroll horizontally)</label> <label><input type="checkbox" onchange="document.body.classList.toggle(\'overlay\',this.checked)">Show approximate fixed-fork landmarks</label><p class="note">Landmarks ±15 px, not anatomy segmentation. Verdict controls are unsaved placeholders; no approval ledger is written.</p>',
          '<h2>Approved identity reference (identity scope only)</h2><img style="max-height:480px;width:auto" alt="Milo canonical, identity only" src="'+url(canonical['path'])+'">']
    by_id={r['image_id']:r for r in inspected};lookup={im['id']:(line,beat,im) for line in plan['lines'] for beat in line['beats'] for im in beat['image_sequence']['images']}
    for name,ids in groups.items():
        page.append('<section id="'+name+'"><h2>'+name.replace('_',' ').title()+'</h2><p>Compare complete frames at equal canvas scale. No common physical distance assumed across independent shots.</p>')
        page.append('<img alt="Existing-image comparison sheet" src="'+url(str((target/(name+'_comparison.jpg')).relative_to(root)))+'">')
        for iid in ids:
            row=by_id[iid];line,beat,im=lookup[iid];b=im['performance'].get('Milo',{})
            page.append('<figure><h3>'+iid+'</h3><p>'+html.escape(line['text'])+'</p><audio controls preload="none" src="'+url(line['audio']['wav'])+'"></audio><p class="note">'+html.escape(row['verdict']+': '+row['observation']+' '+row['reason'])+'</p><p>'+html.escape(row['camera_status'])+'; proposed '+html.escape(b.get('pose_id',''))+':'+html.escape(b.get('pose_variant',''))+' / '+html.escape(b.get('expression_id',''))+' — planned, no available/approved performance bytes.</p>')
            page.append('<div class="frame"><img loading="lazy" alt="'+iid+'" src="'+url(row['path'])+'">')
            if iid in report['landmarks']:
                mark=report['landmarks'][iid];x,y,x2,y2=mark['body_ears_bbox'];rx,ry=mark['root_contact']
                page.append(f'<svg viewBox="0 0 1672 941"><rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="none" stroke="cyan" stroke-width="3"/><path d="M {rx-18} {ry} h 36 M {rx} {ry-18} v 36" stroke="yellow" stroke-width="3"/><rect x="0" y="0" width="1672" height="200" fill="none" stroke="magenta" stroke-width="3"/></svg>')
            page.append('</div><p>Owner verdict (unsaved): <select><option>Pending owner review</option><option>Needs matched-view comparison</option><option>Accept for discussion</option><option>Needs revision</option></select></p></figure>')
        page.append('</section>')
    page.append('<script>document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})))</script>')
    (target/'review.html').write_text('\n'.join(page)+'\n')
    return {'audit':str((target/'REVIEW.md').relative_to(root)),'native_pngs_inspected':report['manually_inspected'],'contact_sheets':len(sheets),'new_character_assets_generated':0,'owner_approval':None}
