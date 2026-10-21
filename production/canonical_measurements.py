"""Derive projected canonical surface ratios from explicit manual landmarks."""
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def place_label(draw,xy,text,font,color,occupied,preferred=(5,3)):
    """Keep native coordinates unchanged; move only overlapping text labels."""
    x,y=xy
    offsets=[preferred,(5,-22),(-28,3),(-28,-22),(24,20),(-40,20),(24,-40),(-40,-40),(45,3),(5,40)]
    for dx,dy in offsets:
        pos=(x+dx,y+dy);box=draw.textbbox(pos,text,font=font,stroke_width=1)
        padded=(box[0]-2,box[1]-2,box[2]+2,box[3]+2)
        if padded[0]<0 or padded[1]<0:continue
        if any(padded[0]<b[2] and padded[2]>b[0] and padded[1]<b[3] and padded[3]>b[1] for b in occupied):continue
        break
    occupied.append(padded)
    if abs(dx)>20 or abs(dy)>25:draw.line((x,y,pos[0],pos[1]+7),fill='#666666',width=1)
    draw.text(pos,text,fill=color,font=font,stroke_width=1,stroke_fill='white')


def quantity(record,points):
    pts=[points[name] for name in record['points']]
    if len(pts)<2:raise ValueError('A measurement needs two or more points')
    xy=[p['xy'] for p in pts]
    if record['method']=='horizontal_span':
        if len(pts)!=2 or xy[0][1]!=xy[1][1]:
            raise ValueError('A horizontal span needs exactly two points at the same registered height')
        value=abs(xy[1][0]-xy[0][0]);error=pts[0]['uncertainty_pixels']+pts[1]['uncertainty_pixels']
    elif record['method']=='vertical_span':
        value=abs(xy[-1][1]-xy[0][1]);error=pts[0]['uncertainty_pixels']+pts[-1]['uncertainty_pixels']
    elif record['method'] in {'distance','polyline'}:
        value=sum(math.dist(a,b) for a,b in zip(xy,xy[1:]))
        error=sum(a['uncertainty_pixels']+b['uncertainty_pixels'] for a,b in zip(pts,pts[1:]))
    else:raise ValueError('Unknown quantity method')
    result={'value_pixels':value,'uncertainty_pixels':error,'scope':record.get('scope','')}
    if 'station' in record:result['station']=record['station']
    return result


def measure_actor(actor):
    quantities={k:quantity(v,actor['points']) for k,v in actor['quantities'].items()}
    ratios={}
    for name,formula in actor['ratios'].items():
        n=quantities[formula['numerator']];d=quantities[formula['denominator']]
        if d['value_pixels']<=d['uncertainty_pixels']:raise ValueError('Denominator insufficiently measured')
        low=max(0,n['value_pixels']-n['uncertainty_pixels'])/(d['value_pixels']+d['uncertainty_pixels'])
        high=(n['value_pixels']+n['uncertainty_pixels'])/(d['value_pixels']-d['uncertainty_pixels'])
        ratios[name]={'value':n['value_pixels']/d['value_pixels'],'interval':[low,high],
            'definition':formula['numerator']+' / '+formula['denominator'],
            'comparability':formula['comparability'],'source':actor['source'],
            'identity_status':actor['identity_status'],'measurement_type':'manual_projected_surface','owner_measurement_approval':False}
    return {'source':actor['source'],'identity_status':actor['identity_status'],'quantities':quantities,'ratios':ratios,'unavailable':actor['unavailable']}


def build(root,story):
    from PIL import Image,ImageDraw,ImageFont
    try:from . import character_performance as cp
    except ImportError:import character_performance as cp
    folder,plan,chars,locs,library=cp.load(root,story)
    source=folder/'canonical_proportion_landmarks.json'
    data=json.loads(source.read_text());out=folder/cp.AUDIT/'canonical_measurements_r001';out.mkdir(exist_ok=True)
    report={'schema':'feltwillow.canonical-projected-measurements.v1','landmark_source':{'path':str(source.relative_to(root)),'sha256':cp.av.digest(source)},'actors':{},'approval':False}
    pages=[];md=['# Canonical projected proportion measurements','','Manual surface landmarks, not a recovered skeleton or 3D anatomy. Intervals include annotation uncertainty. Original canonical bytes/approval records unchanged. Milo current design head target is 0.39 ±0.01; other measurements are baselines, not new owner art approvals. Leo observations remain non-authoritative pending canonical hash reconciliation.','']
    for actor,record in data['actors'].items():
        cp.checked_file(root,record['source'])
        result=measure_actor(record);report['actors'][actor]=result
        policy=library['anatomy_policies'][actor];profile=policy['ratio_profile']
        # Observation provenance is distinct from canonical approval; never replace identity hashes.
        profile['observation_source']=record['source'];profile['observation_identity_status']=record['identity_status']
        for name,obs in result['ratios'].items():
            row=profile['ratios'].setdefault(name,{'definition':obs['definition'],'comparability':obs['comparability'],'target':None,'tolerance':None,'calibration_status':'pending_reference_measurement'})
            row['reference_measurement']=obs
            if name=='projected_head_fraction' and actor=='Milo':
                row['canonical_measurement']=obs
        for name,reason in record['unavailable'].items():profile['ratios'][name]['measurement_limitation']=reason
        profile['measurement_evidence']={'path':str((out/'MEASUREMENTS.json').relative_to(root))}
        im=Image.open(cp.av.local(root,record['source']['path'])).convert('RGBA');base=Image.new('RGBA',im.size,'#dddddd');base.alpha_composite(im);draw=ImageDraw.Draw(base)
        try:font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14)
        except OSError:font=ImageFont.load_default()
        palette=['#0066cc','#bb2299','#008844','#cc6600']
        for idx,(key,q) in enumerate(record['quantities'].items()):
            pts=[record['points'][name]['xy'] for name in q['points']];draw.line([tuple(p) for p in pts],fill=palette[idx%4],width=2)
        legend=[];number_labels=[]
        for idx,(name,p) in enumerate(record['points'].items(),1):
            x,y=p['xy'];draw.ellipse((x-4,y-4,x+4,y+4),fill='yellow',outline='black');place_label(draw,(x,y),str(idx),font,'black',number_labels);legend.append(f'{idx}: {name} ({x}, {y}), ±{p["uncertainty_pixels"]} px')
        base.convert('RGB').save(out/(actor.lower()+'_annotated.jpg'),quality=95)
        # Keep the earlier derived width-only image for provenance, while the
        # active review uses one combined diagram with every measurement.
        width_base=Image.new('RGBA',im.size,'#dddddd');width_base.alpha_composite(im)
        combined=base.copy();wd=ImageDraw.Draw(width_base);cd=ImageDraw.Draw(combined);width_legend=[];combined_labels=list(number_labels)
        for idx,(key,q) in enumerate(((k,v) for k,v in record['quantities'].items() if v['method']=='horizontal_span'),1):
            pts=[tuple(record['points'][name]['xy']) for name in q['points']]
            color=palette[(idx-1)%4];wd.line(pts,fill=color,width=3)
            for x,y in pts:wd.line((x,y-7,x,y+7),fill=color,width=3)
            x,y=pts[-1];label_y=y+9 if key.startswith('cream_patch') else y-22
            wd.text((x+7,label_y),'W'+str(idx),fill=color,font=font,stroke_width=2,stroke_fill='white')
            cd.line(pts,fill=color,width=3)
            for px,py in pts:cd.line((px,py-7,px,py+7),fill=color,width=3)
            place_label(cd,(x,y),'W'+str(idx),font,color,combined_labels,preferred=(17,label_y-y))
            width_legend.append('W'+str(idx)+': '+key+'; '+q['scope'])
        width_base.convert('RGB').save(out/(actor.lower()+'_widths_annotated.jpg'),quality=95)
        combined.convert('RGB').save(out/(actor.lower()+'_combined_annotated.jpg'),quality=95)
        md+=['## '+actor,'','Source actual SHA-256: `'+record['source']['sha256']+'`','',record['identity_status'],'','| Ratio | Projected baseline | Conservative interval |','|---|---:|---:|']
        table=[]
        for name,obs in result['ratios'].items():
            lo,hi=obs['interval'];label=f'{obs["value"]:.2f}';interval=f'{lo:.2f}–{hi:.2f}';md.append(f'| {name} | {label} | {interval} |');table.append('<tr><td>'+html.escape(name)+'</td><td>'+label+'</td><td>'+interval+'</td><td>'+html.escape(obs['definition'])+'</td></tr>')
        pending=''.join('<li>'+html.escape(name+': '+reason)+'</li>' for name,reason in record['unavailable'].items())
        md+=['','Unmeasurable from this view: '+', '.join(record['unavailable'])+'.','']
        quantities_table=''.join('<tr><td>'+html.escape(k)+'</td><td>'+f'{v["value_pixels"]:.1f} ±{v["uncertainty_pixels"]:.1f}'+'</td><td>'+html.escape(v['scope'])+'</td></tr>' for k,v in result['quantities'].items())
        diagram='<h3>Combined canonical measurements</h3><p>One diagram contains all previous and new measurements. Numbered dots identify native-pixel landmarks; W labels identify horizontal spans, including paws. Body, cream patch, closed hands and feet remain separate. No hidden circumference or joint inferred.</p><a href="'+actor.lower()+'_combined_annotated.jpg"><img src="'+actor.lower()+'_combined_annotated.jpg"></a><details><summary>W-label width legend</summary><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in width_legend)+'</ul></details>'
        pages.append('<section><h2>'+actor+'</h2><p>'+html.escape(record['identity_status'])+'</p><p>Actual image SHA-256: <code>'+record['source']['sha256']+'</code></p>'+diagram+'<table><thead><tr><th>Ratio</th><th>Baseline</th><th>Interval</th><th>Visible quantities</th></tr></thead><tbody>'+''.join(table)+'</tbody></table><details><summary>Native-pixel quantities and surface definitions</summary><table><tr><th>Quantity</th><th>Pixels ± uncertainty</th><th>Scope</th></tr>'+quantities_table+'</table></details><details><summary>Landmark coordinates and uncertainty</summary><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in legend)+'</ul></details><details><summary>Hidden/ambiguous anatomy: not invented</summary><ul>'+pending+'</ul></details></section>')
    cp.av.write(out/'MEASUREMENTS.json',report)
    for policy in library['anatomy_policies'].values():
        policy['ratio_profile']['measurement_evidence']['sha256']=cp.av.digest(out/'MEASUREMENTS.json')
    cp.av.write(folder/cp.LIBRARY,library)
    (out/'MEASUREMENTS.md').write_text('\n'.join(md)+'\n')
    (out/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Canonical ratio measurements</title><style>body{font:16px system-ui;background:#252821;color:#eee;margin:25px}a{color:#c7edab}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(450px,1fr));gap:25px}section{min-width:0;background:#343a31;padding:15px}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #777;padding:6px;text-align:left}code{overflow-wrap:anywhere}</style><h1>Milo and Leo: canonical projected measurements</h1><p>Manual native-image annotations with uncertainty. Surface proxies are identified; hidden joints remain unmeasured. No source image edits or new generation. Leo actual-byte observations do not resolve his canonical approval mismatch.</p><div class="grid">'+''.join(pages)+'</div>')
    return {'actors':{a:len(x['ratios']) for a,x in report['actors'].items()},'source_images_changed':0,'owner_approvals_added':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--story',required=True);args=p.parse_args()
    print(json.dumps(build(ROOT,args.story),indent=2))


if __name__=='__main__':main()
