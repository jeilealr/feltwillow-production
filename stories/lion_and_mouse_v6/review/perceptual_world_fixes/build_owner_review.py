#!/usr/bin/env python3
"""Build the complete owner comparison page and small viewing previews."""
import hashlib
import html
import json
import os
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[4]
HOME=Path(__file__).resolve().parent

def main():
    plan=json.loads((HOME/'complete_replacement_plan.json').read_text())
    closer=json.loads((HOME/'closer_review_22.json').read_text())
    reasons={r['id']:r['reason'] for r in closer['frames']}
    captions={
      's04_p01':'Local running view with a readable gesture and planted foot.',
      's04_p02':'Contextual branch passage: preserve the actual overhead branch. Adjacent tighter views supply facial detail.',
      's04_p03':'Pass the stump on the clear lane; preserve screen-right travel.',
      's04_p04':'Continue right past the stump, with local ground magnified together with Milo.',
      's06_p01':'Compact shared scramble beside resting Leo’s paw.',
      's06x_p01':'Leo pushes onto four paws while Milo continues right; both remain in frame.',
      's07_p02':'Apologetic Milo portrait with stable ears, shoulders and camera.',
      's07_p03':'Explaining Milo portrait; the composition you already selected.',
      's09_p01':'Readable careful steps on the local dirt lane.',
      's15_p06':'Released Leo and readable Milo beside the existing collapsed net.',
      's16_p01':'Shared closing hold in the composition you selected for p05.',
      's16_p04':'Happy closing expressions within the same shared composition.',
      's16_p05':'Shared closing composition you already selected.',
      's16x_p01':'Intentional shared closing hold; no invented pose change for narration.',
      's16x_p03':'Intentional shared closing hold; no invented pose change for narration.'}
    rows=[]
    for f in plan['frames']:
        rows.append(dict(f,reason=captions.get(f['id'],reasons.get(f['id'],''))))
    for f in closer['frames']:
        if f['decision']=='retain':
            rows.append({'id':f['id'],'category':'retained','output_path':f['source_path'],
                'sha256':f['source_sha256'],'reason':f['reason']})
    rows.sort(key=lambda f:f['id'])
    previews=HOME/'previews';previews.mkdir(exist_ok=True)
    def picture(path,fid,label,suffix):
        p=ROOT/path
        preview=previews/(fid+'_'+suffix+'.jpg')
        with Image.open(p) as im:
            im.convert('RGB').resize((480,270),Image.Resampling.LANCZOS).save(preview,quality=93)
        return '<figure><a href="'+html.escape(os.path.relpath(p,HOME))+'"><img width="480" height="270" loading="lazy" src="'+html.escape(os.path.relpath(preview,HOME))+'" alt="'+html.escape(fid+' '+label)+'"></a><figcaption>'+html.escape(label)+'</figcaption></figure>'
    sections=[]
    for f in rows:
        approved=bool(f.get('owner_visual_selection'))
        group='retained' if f['category']=='retained' else ('approved' if approved else 'new')
        status='Retain existing image' if group=='retained' else ('Previously selected composition' if approved else 'New replacement — review pending')
        pair=''
        if group!='retained':pair=picture(f['source_candidate']['path'],f['id'],'Current active image','before')
        pair+=picture(f['output_path'],f['id'],'Retained image' if group=='retained' else 'Corrected candidate','after')
        sections.append('<article id="'+f['id']+'" data-group="'+group+'" data-category="'+f['category']+'"><h2>'+f['id']+' <small>'+html.escape(status)+'</small></h2><p>'+html.escape(f['reason'])+'</p><div class="pair">'+pair+'</div><details><summary>Image record</summary><p>'+html.escape(f['output_path'])+'</p><code>'+f['sha256']+'</code></details></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perceptual-world image review — all 36 decisions</title>
<style>body{max-width:1200px;margin:32px auto;padding:0 20px;background:#171b1c;color:#edf1ed;font:17px/1.5 system-ui}a{color:#b8dfbb}h1{font-size:30px}h2{font-size:23px}small{font-size:14px;color:#c5d6c7}article{padding:20px 0;border-top:1px solid #526057;scroll-margin-top:80px}.pair{display:flex;flex-wrap:wrap;gap:20px}figure{margin:0;max-width:480px}img{display:block;width:480px;max-width:100%;height:auto}figcaption{margin:5px 0 14px;color:#cbd5ca}nav{position:sticky;top:0;background:#171b1c;padding:12px 0;z-index:2}button{padding:8px 12px;margin:3px;background:#344b3c;color:white;border:1px solid #789c80;border-radius:4px;cursor:pointer}code{overflow-wrap:anywhere;font-size:12px}details p{overflow-wrap:anywhere}[hidden]{display:none!important}</style>
<h1>Perceptual-world image review</h1><p><strong>14 priority replacements. 22 closer reviews: 9 replacements and 13 retained.</strong></p>
<p>The 23 replacement slots include the four compositions you already liked and 19 additional candidates. Images below are exactly 480×270; click for the 1920×1080 PNG. The active production selection still points to the original images while these candidates await adoption and technical validation.</p>
<p><a href="REVIEW.md">Review notes</a> · <a href="complete_replacement_plan.json">Replacement records</a> · <a href="closer_review_22.json">All 22 review decisions</a> · <a href="batch_verification.json">Verification</a> · <a href="followup_layers.json">Generation prompts and sources</a></p>
<nav aria-label="Filter images"><button data-filter="all">All 36</button><button data-filter="new">19 new candidates</button><button data-filter="priority">14 priority</button><button data-filter="closer_review_fix">9 additional fixes</button><button data-filter="approved">4 already selected</button><button data-filter="retained">13 retained</button></nav>
'''+ '\n'.join(sections)+'''
<script>document.querySelectorAll('button[data-filter]').forEach(b=>b.addEventListener('click',()=>{const v=b.dataset.filter;document.querySelectorAll('article').forEach(a=>{a.hidden=!(v==='all'||a.dataset.group===v||a.dataset.category===v)});}));</script></html>'''
    (HOME/'owner_review.html').write_text(page)
    print('Review page: 36 decisions, 23 before/after pairs, 13 retained images.')

if __name__=='__main__':main()
