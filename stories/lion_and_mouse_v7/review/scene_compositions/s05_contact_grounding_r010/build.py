"""Local scene staging repair: reviewed actor rasters, contact masks and shadows."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = Path(__file__).resolve().parent
R = D.parents[4]

def read(p):
    return json.loads(p.read_text())

def write(p,x):
    p.write_text(json.dumps(x,indent=2)+'\n')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def record(p):
    return {'path':str(p.relative_to(R)), 'sha256':digest(p)}

def ellipse(size, bounds, opacity, blur):
    m=Image.new('L',size)
    ImageDraw.Draw(m).ellipse(tuple(bounds),fill=opacity)
    return m.filter(ImageFilter.GaussianBlur(blur))

def main():
    assert not (D/'EXECUTION.json').exists(), 'Preserve existing revisions'
    background=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions/S05-L001-B01-I01_single_sleeping_leo_reveal_r001_candidate.png'
    base=Image.open(background).convert('RGBA')
    contact=read(R/'stories/lion_and_mouse_v7/review/scene_compositions/s05_contact_local_composition_r007/COMPOSITION_RECIPE.json')
    continuation=read(R/'stories/lion_and_mouse_v7/review/scene_compositions/s05_local_continuation_r008/COMPOSITION_BATCH.json')
    current=read(R/'stories/lion_and_mouse_v7/review/scene_compositions/s05_contact_local_composition_r007/EXECUTION.json')['outputs'][0]
    rows=read(R/'stories/lion_and_mouse_v7/review/scene_compositions/s05_local_continuation_r008/EXECUTION.json')['outputs']
    lookup={r['image_id']:r for r in [current]+rows}
    old_trip=next(j for j in continuation['jobs'] if j['image_id']=='S05-L008-B01-I04')
    old_roll=next(j for j in continuation['jobs'] if j['image_id']=='S05-L009-B01-I03')
    jobs=[
        {'id':'S05-L008-B01-I02','actor':contact['actor'],'xy':[46,350],
         'output':'S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png',
         'shadows':[[[320,700,390,718],75,4]],'foreground':None,
         'intent':'Milo translated 32 pixels left, same scale/vertical support. Provides forward travel room before I04. Raised foot approaches the paw; review contact-event timing rather than assume contact from metadata.'},
        {'id':'S05-L008-B01-I04','actor':old_trip['actor'],'xy':[200,323],
         'output':'S05-L008-B01-I04_local_trip_r002_candidate.png',
         'shadows':[[[441,662,501,680],90,3]],
         'foreground':[[416,691],[429,674],[452,665],[480,665],[504,670],[534,681],[555,706],[555,735],[433,742]],
         'intent':'Raise whole actor 42 pixels so downward foot meets upper rear-paw rim. Restore Leo paw foreground over lower foot for local contact/occlusion. No leg or body redraw. Review foot-catching edge rather than intentional stepping.'},
        {'id':'S05-L009-B01-I03','actor':old_roll['actor'],'xy':[830,490],
         'output':'S05-L009-B01-I03_local_roll_r002_candidate.png',
         'shadows':[[[965,786,1235,819],62,10],[[1060,797,1180,812],72,3]],'foreground':None,
         'intent':'Move whole rolling actor 50 pixels left and 90 down toward ground in foreground/flank corridor. Soft ground shadow anchors roll; avoids floating directly over face. Review trajectory/depth and later nose landing.'}
    ]
    (D/'masks').mkdir(exist_ok=True)
    (D/'receipts').mkdir(exist_ok=True)
    outputs=[];checks=[];observations=[]
    for index,job in enumerate(jobs,1):
        old=lookup[job['id']]
        assert digest(R/old['path'])==old['sha256']
        side=read(R/old['sidecar']['path'])
        actor_record=job['actor']
        assert digest(R/actor_record['path'])==actor_record['sha256']
        source=Image.open(R/actor_record['path']).convert('RGBA')
        scale=.32
        size=tuple(round(d*scale) for d in source.size)
        resized=source.resize(size,Image.Resampling.LANCZOS)
        layer=Image.new('RGBA',base.size)
        layer.paste(resized,tuple(job['xy']))
        occlusion=Image.new('L',base.size)
        if job['foreground']:
            ImageDraw.Draw(occlusion).polygon([tuple(p) for p in job['foreground']],fill=255)
            occlusion=occlusion.filter(ImageFilter.GaussianBlur(.7))
        visible=layer.copy()
        # Occlusion changes alpha only; no actor RGB or limb geometry is edited.
        alpha=np.asarray(layer.getchannel('A')).astype(np.float64)
        occ=np.asarray(occlusion).astype(np.float64)/255
        visible.putalpha(Image.fromarray(np.rint(alpha*(1-occ)).astype('uint8')))
        shadow=Image.new('L',base.size)
        for bounds,opacity,blur in job['shadows']:
            m=ellipse(base.size,bounds,opacity,blur)
            shadow=Image.fromarray(np.maximum(np.asarray(shadow),np.asarray(m)))
        shade=Image.new('RGBA',base.size,(28,20,12,0))
        shade.putalpha(shadow)
        result=Image.alpha_composite(Image.alpha_composite(base,shade),visible).convert('RGB')
        # Changes are confined to actor + explicitly audited cast/contact-shadow masks.
        effects=(np.asarray(layer.getchannel('A'))>0)|(np.asarray(shadow)>0)
        base_array=np.asarray(base.convert('RGB'))
        image_array=np.asarray(result)
        protected_changes=int(np.count_nonzero(np.any(base_array!=image_array,axis=2)&~effects))
        assert protected_changes==0
        stem=job['id']
        shadow_path=D/'masks'/f'{stem}_shadow.png';shadow.save(shadow_path)
        occlusion_path=D/'masks'/f'{stem}_leo_foreground.png';occlusion.save(occlusion_path)
        effect_path=D/'masks'/f'{stem}_effect_support.png';Image.fromarray(effects.astype('uint8')*255).save(effect_path)
        out=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions'/job['output']
        assert not out.exists() and not out.with_suffix('.json').exists()
        result.save(out)
        with Image.open(out) as saved:
            saved.load();assert saved.size==base.size
        for k,h in [('wav','sha256'),('metadata','metadata_sha256')]:assert digest(R/side['audio'][k])==side['audio'][h]
        creation={'method':'owner-requested local Pillow staging/contact repair','provider_calls':0,'actual_cost':0,
                  'background':record(background),'actor':actor_record,'scale':scale,'translate_pixels':job['xy'],
                  'resampling':'whole-layer Lanczos; actor RGB unmodified after resize',
                  'contact_shadow_specs':job['shadows'],'shadow_mask':record(shadow_path),
                  'leo_foreground_polygon':job['foreground'],'occlusion_mask':record(occlusion_path),
                  'affected_region_mask':record(effect_path),'source_scene':old,'intent':job['intent']}
        side.update(path=str(out.relative_to(R)),sha256=digest(out),creation=creation,
                    inputs=[record(background),actor_record],owner_decision=None,
                    status='candidate_pending_owner_review',production_readiness=False,
                    technical_review=job['intent'],readiness_limitations=['Local manual contact/trajectory and light integration need owner review.','Exact source body/grey-paw raster reused at uniform scale; no new canonical measurements or physical calibration.'])
        side_path=out.with_suffix('.json');write(side_path,side)
        receipt=D/'receipts'/f'{index:03d}.json';write(receipt,side)
        row={'image_id':job['id'],'path':str(out.relative_to(R)),'sha256':digest(out),'sidecar':record(side_path),'receipt':record(receipt),'dimensions':list(base.size),'status':'candidate_pending_owner_review'}
        outputs.append(row)
        checks.append({'image_id':job['id'],'changed_pixels_outside_actor_and_shadow_masks':protected_changes,
                       'effect_mask_pixels':int(effects.sum()),'source_actor_rgb_edits':False,'uniform_scale':scale,
                       'occluded_actor_pixels':int(np.count_nonzero((alpha>0)&(occ>0))),
                       'source_audio_hashes':'verified','png_decode':'pass','physical_contact_pass':None})
        observations.append({'image_id':job['id'],'image_sha256':row['sha256'],'observation':job['intent']+' Selected body/paw colors retained; no recoloring. Shadows and occlusion are explicit local layers. Background unchanged outside actor/shadow effect mask. New staging pending owner review.','owner_decision':None,'camera':'camera_unknown'})
    write(D/'EXECUTION.json',{'completed':3,'outputs':outputs,'provider_calls':0,'actual_cost':0})
    write(D/'COMPOSITION_VALIDATION.json',{'images':checks,'full_suite':'not run per owner cadence'})
    write(D/'VISUAL_OBSERVATIONS.json',{'images':observations})
    write(D/'OWNER_FEEDBACK.json',{'scope':'staging/contact repairs only; preserve canonical and prepared poses','statement':'Move Milo a bit left in L008-I02; I04 left foot must contact Leo paw; roll I03 looks stuck on; L009-I01/I02 poses are okay','revised_inputs':[lookup[j['id']] for j in jobs],
          'retained_pose_depictions':[lookup['S05-L009-B01-I01'],lookup['S05-L009-B01-I02']],
          'retention_scope':'pose depictions liked; no new full scene/video approval inferred'})
    # Side-by-side review uses saved outputs only.
    sheet=Image.new('RGB',(1200,1100),(35,39,32));draw=ImageDraw.Draw(sheet)
    for k,(job,new) in enumerate(zip(jobs,outputs)):
        for c,row in enumerate([lookup[job['id']],new]):
            tile=Image.open(R/row['path']).convert('RGB');tile.thumbnail((590,332))
            x=c*600;y=k*365;sheet.paste(tile,(x,y+26));draw.text((x+5,y+5),job['id']+(' before' if c==0 else ' revised'),fill='white')
    sheet.save(D/'comparison.jpg',quality=95)
    print('Created 3 local revised candidates; all protected-region checks passed.')

if __name__=='__main__':
    main()
