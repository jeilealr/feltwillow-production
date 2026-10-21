"""Read-only, reusable performance-library cards and local audio review."""
import argparse
import html
import json
import os
from pathlib import Path

try:
    from . import character_performance as cp
except ImportError:
    import character_performance as cp


def comparison_is_current(library, report):
    """Old comparison pixels must not appear to describe replacement assets."""
    for row in report.get('rows',[]):
        variant=library['assets'].get(row['asset_id'],{}).get('variants',{}).get(row['variant'],{})
        current=variant.get('file') or {}
        if current.get('path')!=row['source']['path'] or current.get('sha256')!=row['source']['sha256']:
            return False
    return bool(report.get('rows'))


def build(root,story):
    folder,plan,chars,locs,library=cp.load(root,story)
    errors=cp.validate(library,plan,chars,root,folder=folder)
    if errors:raise ValueError('\n'.join(errors))
    target=folder/cp.AUDIT/'pose_library'
    target.mkdir(parents=True,exist_ok=True)
    def url(path):
        # Resolve trusted registry paths through the existing repository boundary.
        return html.escape(os.path.relpath(cp.av.local(root,path),target),quote=True)
    h=html.escape
    rows=cp.usage_report(library,plan)['uses']
    profiles=[]
    canonical_panels=[]
    for actor,policy in library.get('anatomy_policies',{}).items():
        profile=policy.get('ratio_profile',{})
        table=[]
        for name,metric in profile.get('ratios',{}).items():
            label='No adopted target yet' if metric['target'] is None else f"{metric['target']} ± {metric['tolerance']} (absolute ratio units)"
            observation=metric.get('reference_measurement')
            measured=(f"{observation['value']:.2f} (interval {observation['interval'][0]:.2f}–{observation['interval'][1]:.2f})" if observation else 'Not measurable / pending')
            table.append('<tr><td>'+h(name)+'</td><td>'+h(label)+'</td><td>'+h(measured)+'</td><td>'+h(metric['definition'])+'</td><td>'+h(metric['comparability'])+'</td></tr>')
        profiles.append('<details><summary>'+h(actor+' · '+profile.get('calibration_status','pending'))+'</summary><p>Own canonical SHA-256: <code>'+h(policy['canonical']['sha256'])+'</code></p><p>Observation identity: '+h(profile.get('observation_identity_status','pending'))+'. Baselines are projected surface measurements; they do not automatically become design targets.</p><table><thead><tr><th>Ratio</th><th>Target</th><th>Measured baseline</th><th>Definition</th><th>Comparable when</th></tr></thead><tbody>'+''.join(table)+'</tbody></table></details>')
        annotation=folder/cp.AUDIT/'canonical_measurements_r001'/(actor.lower()+'_combined_annotated.jpg')
        if annotation.is_file():
            canonical_panels.append('<section><h2>'+h(actor)+' · all canonical measurements</h2><p>'+h(profile.get('observation_identity_status','pending'))+'</p><a href="'+url(str(annotation.relative_to(root)))+'"><img class="comparison" loading="lazy" src="'+url(str(annotation.relative_to(root)))+'" alt="'+h(actor)+' combined canonical height width face and paw measurements"></a><p>All previous landmarks and new widths, cream patch, hands and paws in one image. Numbered dots are coordinates; W labels are horizontal spans. No hidden joints inferred. <a href="../canonical_measurements_r001/review.html">Full coordinate/width legends, native pixels, ratio tables and uncertainty</a></p></section>')
    cards=[]
    history=[]
    for aid,asset in library['assets'].items():
        for variant_name,variant in asset['variants'].items():
            file=variant.get('file')
            if not file:continue
            for previous in variant.get('superseded_candidates',[]):
                history.append({'asset_id':aid,'variant':variant_name,**previous})
            cp.checked_file(root,file)
            matched=[r for r in rows if (r.get('pose_id')==aid and r.get('pose_variant')==variant_name) or (r.get('expression_id')==aid and r.get('expression_variant')==variant_name)]
            image_ids=sorted({r['image_id'] for r in matched})
            scenes=sorted({r['line_id'].split('-')[0] for r in matched})
            # Current owner review is S01-S03; future uses remain text links/IDs.
            audio={r['line_id']:r['audio_wav'] for r in matched if r['line_id'].startswith(('S01-','S02-','S03-'))}
            players=[]
            for lid,wav in sorted(audio.items()):
                if cp.av.local(root,wav).is_file():
                    players.append('<label>'+h(lid)+'<audio controls preload="none" src="'+url(wav)+'"></audio></label>')
            side=cp.av.read(cp.av.local(root,file['sidecar']['path']))
            note=side.get('technical_review','No visual verdict recorded')
            if not isinstance(note,str):note=json.dumps(note,ensure_ascii=False)
            blockers=cp.anatomy_blockers(library,asset['actor'],variant)
            anatomy=variant.get('anatomy_review',{}).get('status','pending')
            category='portrait' if asset['asset_type']=='portrait_base' else 'expression' if asset['asset_type']=='expression' else 'body'
            cards.append('<article data-kind="'+category+'" data-scenes="'+' '.join(scenes)+'" data-search="'+h((aid+' '+variant_name+' '+' '.join(image_ids)).lower(),quote=True)+'"><h2>'+h(aid+':'+variant_name)+'</h2><p class="badge">Pose/acting: '+h(variant['status'])+'</p><p>Anatomy: '+h(anatomy)+'</p><a href="'+url(file['path'])+'" target="_blank"><img loading="lazy" src="'+url(file['path'])+'" alt="'+h(aid+':'+variant_name,quote=True)+'"></a><p class="filename">'+h(Path(file['path']).name)+'</p><p>'+h(note)+'</p><p class="warning">'+h('; '.join(blockers) or 'No anatomy evidence blockers; scene/prop review remains separate')+'</p><details><summary>Audio-linked image uses ('+str(len(image_ids))+')</summary><p>'+h(', '.join(image_ids) or 'Reusable angle-base dependency; no direct scene assignment')+'</p>'+''.join(players)+'</details><details><summary>Source evidence</summary><p>Image SHA-256: <code>'+h(file['sha256'])+'</code></p><p>Canonical SHA-256: <code>'+h(asset['canonical']['sha256'])+'</code></p><p>View / head: '+h(asset['view']+' / '+variant['head_orientation'])+'</p><p>Card fit is a display choice, not a common anatomical pixel scale.</p></details></article>')
    comparison=folder/cp.AUDIT/'milo_anatomy_r001/normalized_comparison.jpg'
    comparison_report=folder/cp.AUDIT/'milo_anatomy_r001/PROJECTED_LANDMARKS.json'
    current_comparison=comparison_report.is_file() and comparison_is_current(library,cp.av.read(comparison_report))
    pending=[]
    for aid,asset in library['assets'].items():
        if asset['asset_type']!='expression':continue
        if any(r['line_id'].startswith(('S01-','S02-','S03-')) and r.get('expression_id')==aid for r in rows):
            for name,v in asset['variants'].items():
                if not v.get('file'):pending.append('<li>'+h(aid+':'+name)+' — planned; no image generated</li>')
    summary='<section><h2>Current review status</h2><p><strong>'+str(len(cards))+' current generated performance assets</strong>. The registry supplies one current file per pose/variant. '+str(len(history))+' superseded versions are excluded from these cards and preserved as history; current candidates remain marked by their own approval/readiness state.</p><p><strong>Milo upright projected head fraction: 0.39 ±0.01 (0.38–0.40).</strong> Canonical measured baseline is approximately 0.39 with annotation uncertainty. Target tolerance is not measurement precision.</p><p>Pose/acting approval does not establish anatomy congruence or acorn fit. Known body-facing/contact concerns remain on the relevant cards. Leo observations use the actual local bytes; his canonical ledger mismatch is unresolved.</p><details><summary>Missing S01–S03 expressions ('+str(len(pending))+')</summary><ul>'+''.join(pending)+'</ul></details></section>'
    next_stage=folder/'review/scene_compositions/s01_s03_performance_r002/review.html'
    if next_stage.is_file():
        summary+='<p><a href="../../scene_compositions/s01_s03_performance_r002/review.html">S01–S03 composed scene candidates · audio and comparisons</a></p>'
    if canonical_panels:
        summary+='<details open><summary>Combined annotated canonical images: Milo and Leo · all measurements</summary><p>Height, face, widths, cream patch and paws are shown together. Width and height must both agree in compatible views. Current candidates require matched-view measurements; generation guidance does not establish a proportion pass. Portraits use applicable head/ear/eye ratios; a cropped belly is not measurable.</p><div class="grid">'+''.join(canonical_panels)+'</div></details>'
    compare='<details open><summary>Current annotated comparison</summary><p>Uniform crown-to-sole normalization; manual ±20 px; head pitch differs. Screening only. Source images unchanged.</p><img class="comparison" src="'+url(str(comparison.relative_to(root)))+'"></details>' if comparison.is_file() and current_comparison else '<p>Earlier anatomy comparison is archived; it does not describe all current replacement bytes.</p>'
    style='body{font:17px system-ui;background:#252821;color:#eee;margin:26px}a{color:#c7edab}header{max-width:1100px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px}article{background:#343a31;padding:16px;min-width:0;border-radius:8px}h2{font-size:18px;overflow-wrap:anywhere}article img{display:block;width:100%;height:auto;background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 50% / 24px 24px}body.native article{overflow:auto}body.native article img{width:auto;max-width:none}code,.filename{font-size:12px;overflow-wrap:anywhere}.badge,.warning{color:#ffdb91}audio{width:100%;margin:6px 0 14px}details{margin:14px 0}summary{cursor:pointer}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #697160;padding:8px;text-align:left}nav{display:flex;gap:15px;flex-wrap:wrap;align-items:center;margin:20px 0}input,select{font:inherit}.comparison{max-width:100%;height:auto}article[hidden]{display:none}'
    script="""const search=document.querySelector('#search'),kind=document.querySelector('#kind');function filter(){document.querySelectorAll('article').forEach(c=>c.hidden=!(c.dataset.search.includes(search.value.toLowerCase())&&(kind.value==='all'||c.dataset.kind===kind.value)))}search.addEventListener('input',filter);kind.addEventListener('change',filter);document.querySelector('#native').addEventListener('change',e=>document.body.classList.toggle('native',e.target.checked));document.querySelectorAll('audio').forEach(p=>p.addEventListener('play',()=>document.querySelectorAll('audio').forEach(q=>{if(q!==p)q.pause()})));"""
    page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Character pose library review</title><style>'+style+'</style></head><body><header><h1>Character pose library · '+h(story)+'</h1><p>Reusable read-only review. Pose/acting selection, anatomy evidence and scene/prop readiness are separate. Original PNGs and receipts remain unchanged.</p><p>Each character owns its canonical-bound ratios; current targets and measured baselines appear separately below. Portraits and bent/foreshortened poses use applicable local ratios, not whole-body fraction.</p><p><a href="../canonical_measurements_r001/review.html">Canonical annotations and measured ratios for Milo and Leo</a></p></header>'+summary+''.join(profiles)+compare+'<nav><label>Find pose or image ID <input id="search" type="search"></label><label>Type <select id="kind"><option value="all">All</option><option value="body">Body poses</option><option value="portrait">Portrait bases</option><option value="expression">Expressions</option></select></label><label><input id="native" type="checkbox"> Native size (scroll)</label></nav><main class="grid">'+''.join(cards)+'</main><script>'+script+'</script></body></html>'
    (target/'review.html').write_text(page+'\n')
    cp.av.write(target/'HISTORY_INDEX.json',{'scope':'superseded files; excluded from active pose cards','files':history})
    return {'gallery':str((target/'review.html').relative_to(root)),'generated_assets_shown':len(cards),'source_image_changes':0,'provider_calls':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--story',required=True);args=p.parse_args()
    import json
    print(json.dumps(build(cp.ROOT,args.story),indent=2))


if __name__=='__main__':main()
