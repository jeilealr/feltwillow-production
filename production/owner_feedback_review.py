"""Build r004 owner feedback evidence from the authored plan; CPU only.

Creates display-only indexes and a grouped review page. It never changes media,
selection ledgers, historical evidence or external operation states.
"""
from __future__ import annotations
import argparse,html,json,os,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production.sequence_plan import selection_catalog,resolve_sequence,digest,fingerprint,audio_intervals
from production.visual_grammar import classification_matrix
from production.sequence_readiness import evaluate
from production.v7_dialogue import inventory
from feltwillow import wan
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]


def build(root,out):
    root=Path(root).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    folder=root/'stories/lion_and_mouse_v7';plan=json.loads((folder/'audio_visual_plan.json').read_text());lib=json.loads((folder/'character_performance_library.json').read_text())
    def write(name,value):
        (out/name).write_text(json.dumps(value,indent=2)+'\n')
    catalog=selection_catalog(folder);packets={};readiness={};cards=[];fits={};h=html.escape
    matrix=classification_matrix(plan);write('CLASSIFICATION_MATRIX.json',matrix)
    write('DIALOGUE_INVENTORY.json',inventory(plan,lib.get('mouth_references',{})))
    audio=audio_intervals(plan,root);write('AUDIO_AND_FRAME_ALLOCATIONS.json',{'schema':'feltwillow.sample-review.v1','scenes':audio,'word_and_action_markers':'pending reviewed alignment; offsets do not locate physical events','render_allocations':'not approved; no uniform/equal edge division inferred'})
    for uid,unit in plan['visual_units'].items():
        sid=unit['sequence_id'];p=resolve_sequence(plan,sid,root,catalog)
        packets[sid]=p;readiness[sid]=evaluate(p,'realization')
        anchors=[];seen=set()
        for u in p['resolved_images']:
            source=u.get('source');media=''
            if source:
                native=root/source['path'];sha=source['sha256']
                if native.is_file() and digest(native)==sha:
                    fit=out/'fits'/f'{sha}.png'
                    if sha not in fits:
                        fit.parent.mkdir(exist_ok=True)
                        with Image.open(native) as im:
                            record=wan.fitted_record(im,1280,720);wan.fit(im,1280,720).save(fit)
                        fits[sha]=dict(source=source,fit=record,path=str(fit.relative_to(out)))
                    if sha not in seen:
                        media=f'<a href="{h(os.path.relpath(native,out))}"><img loading="lazy" src="{h(os.path.relpath(fit,out))}" alt="Fitted reviewed-source preview; selection does not certify transition"></a>'
                    else:media='<p>Same raster as a preceding anchor; no duplicate image or alias model job.</p>'
                    seen.add(sha)
            anchors.append(f'<section><b>{h(u["id"])}</b> · {h(u["status"])}{media}<small>{h(source["sha256"] if source else "No selected bytes")}</small></section>')
        lines=[]
        for line in p.get('audio_lines',[]):
            path=root/line['wav'];player=''
            if path.is_file() and digest(path)==line['sha256']:
                player=f'<audio controls preload="none" src="{h(os.path.relpath(path,out))}"></audio>'
            lines.append(f'<p>{h(line["line_id"])} · {h(line["speaker"])} · {h(line["text"])}</p>{player}')
        classification=' · '.join(unit[k] for k in ('editorial_relationship','composition','mouth_policy'))
        cards.append(f'<article id="{h(uid)}"><h2>{h(uid)}</h2><p class="classification">{h(classification)}</p><p>{h(unit.get("visible_action_requirement") or "Intentional hold/single-shot coverage")}</p><p class="pending">Source motion, joins, mouth and owner video selection remain separate pending gates.</p>{"".join(lines)}<details><summary>{len(p["resolved_images"])} ordered logical anchors · {len(seen)} local distinct rasters</summary>{"".join(anchors)}<pre>{h(json.dumps(p["edges"],indent=2))}</pre></details><details><summary>Current dependencies</summary><pre>{h(json.dumps(readiness[sid],indent=2))}</pre></details></article>')
    aliases={k:v['alias_of_sequence'] for k,v in plan['production_sequences'].items() if v.get('alias_of_sequence')}
    index={'schema':'feltwillow.sequence-index.v1','source_plan_sha256':fingerprint(plan),'derived_from':'audio_visual_plan.json + scoped selection records','execution_sequence_ids':list(packets),'review_aliases':aliases,'sequences':packets}
    write('SEQUENCE_REALIZATION_INDEX.json',index);write('READINESS.json',readiness);write('FIT_RECORDS.json',fits)
    # Current derived data is regenerated, while old review/sequence_readiness_r001 stays immutable.
    (folder/'derived/sequence_realization_index.json').write_text(json.dumps(index,indent=2)+'\n')
    gaps=[dict(sequence_id=sid,use_id=u['id'],status=u['status'],source=u.get('source'),blockers=u.get('blockers',[])) for sid,p in packets.items() for u in p['resolved_images'] if u['status'] not in {'selected_exact','selected_alias','selected_hold'}]
    write('SHOT_GAPS.json',{'active_missing_or_blocked_uses':gaps,'retired_production_placeholders':'See authoritative owner_editorial_direction and EDITORIAL_MIGRATION_BEFORE.json; historical planned slots remain unchanged','aliases_do_not_request_duplicate_generation':True})
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Feltwillow v7 — owner feedback r004</title><style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 18px;color:#28322b;background:#f3f0e8}article{background:white;border:1px solid #cbcbbc;border-radius:10px;padding:20px;margin:18px 0}img{max-width:100%;height:auto}section{padding:12px;border-bottom:1px solid #ddd}small,pre{overflow-wrap:anywhere;white-space:pre-wrap}small{display:block;font-size:12px}audio{width:100%}.classification{font-weight:bold;color:#365f45}.pending{color:#805529}summary{cursor:pointer;padding:10px}a{color:#215e41}</style><h1>Connected sequences, individual shots & portraits</h1><p>One card per intended output unit. Expand the ordered anchors to inspect internal states; repeated aliases are bookkeeping, not extra films. No new Wan or image-provider work has run.</p><p>The first narration line is forest-only. s01_opening links to s01_empty_hold; it is not a second film entry.</p><p><a href="art/REVIEW.html">Native art comparisons, missing paw and exact operation proposals</a> · <a href="S01_FOREST_STATIC_PREVIEW.html">CPU-only forest hold preview</a> · <a href="BLOCKERS.md">Remaining blockers</a></p>'''+''.join(cards)+'</html>'
    (out/'OWNER_REVIEW.html').write_text(page)
    return dict(units=len(cards),canonical_sequences=len(packets),review_aliases=aliases,distinct_fitted_rasters=len(fits),active_blocked_uses=len(gaps),audio_scenes=len(audio))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(json.dumps(build(a.root,a.out),indent=2))
if __name__=='__main__':main()
