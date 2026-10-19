"""Actual r02 deformation measurements, stills and sampled short-motion frames."""
import bpy,math,json,sys,time,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender';sys.path.insert(0,str(AREA/'scripts'))
import leo_tripo_refine_r02 as refine
import leo_tripo_canonical_pass as prior
OUT=refine.OUT;P=refine.P
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def open_candidate():
    bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);prior.neutral();bpy.context.scene.frame_set(1)

def audit():
    open_candidate();s=bpy.context.scene;rig=bpy.data.objects['Leo_RIG_R02'];surface=bpy.data.objects['Leo_surface'];groom=bpy.data.objects['Leo_attached_wool_r02']
    paws=refine.feet(surface);plant={}
    for name,paw in paws.items():
        ids=sorted(paw['ids'],key=lambda i:surface.data.vertices[i].co.z)[:12];plant[name]=ids
    kd=KDTree(len(surface.data.vertices))
    for v in surface.data.vertices:kd.insert(v.co,v.index)
    kd.balance();faceids=[kd.find(Vector(p))[1] for p in [(-.12,-.90,1.10),(.15,-.87,1.10),(0,-.97,.96),(-.06,-.93,.88),(.08,-.93,.88)]]
    bindings=json.loads((P/'groom_bindings_sample.json').read_text());sample=bindings[:80]
    frames=[];baseline=None;face_ref=None;max_attachment=0;neutral_delta=0
    for frame in range(1,50):
        s.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();me=surface.evaluated_get(deps).data;gm=groom.evaluated_get(deps).data
        points={name:[me.vertices[i].co.copy() for i in ids] for name,ids in plant.items()}
        fp=[me.vertices[i].co.copy() for i in faceids];fd=[(fp[a]-fp[b]).length for a in range(len(fp)) for b in range(a)]
        if frame==1:
            baseline=points;face_ref=fd;neutral_delta=max((v.co-me.vertices[v.index].co).length for v in surface.data.vertices)
        paw_drift={name:max((p-q).length for p,q in zip(points[name],baseline[name])) for name in plant}
        attach=[]
        for binding in sample:
            target=sum((me.vertices[i].co*w for i,w in zip(binding['triangle'],binding['bary'])),Vector());root=gm.vertices[binding['start']].co;attach.append((root-target).length)
        error=max(attach);max_attachment=max(max_attachment,error)
        face_error=max(abs(x-y)/max(y,.001) for x,y in zip(fd,face_ref))
        frames.append({'frame':frame,'paw_max_drift_bu':paw_drift,'groom_root_max_distance_bu':error,'face_landmark_pair_max_relative_change':face_error,'min_plant_z_bu':{name:min(p.z for p in values) for name,values in points.items()}})
    max_drift=max(d for f in frames for d in f['paw_max_drift_bu'].values());max_face=max(f['face_landmark_pair_max_relative_change'] for f in frames)
    topology=refine.stats(surface.data);expected=refine.SOURCE
    checks={'main_surface_manifold':topology['nonmanifold_edges']==0,'main_surface_closed':topology['boundary_edges']==0,
      'skin_weights_normalized':max(abs(sum(g.weight for g in v.groups)-1) for v in surface.data.vertices)<1e-5,
      'four_paw_regions_resolved':len(paws)==4,'paw_drift_below_0_0015_bu':max_drift<.0015,
      'face_landmark_distances_stable_within_0_5_percent':max_face<.005,
      'sampled_groom_roots_within_0_003_bu':max_attachment<.003,
      'rest_pose_mesh_max_change_below_0_002_bu':neutral_delta<.002,
      'source_r01_hash_unchanged':sha(expected)=='69d4c29d2b6442eee9bb8de9cfb2289657aeec315bf99790756a2be5a67b0ac9',
      'six_pale_whisker_curves_head_bound':len([o for o in bpy.data.objects if o.name.startswith('Leo_whisker_') and o.parent_bone=='head'])==6,
      'all_file_images_packed':all(im.packed_file for im in bpy.data.images if im.source=='FILE')}
    report={'candidate':str(OUT.relative_to(ROOT)),'sha256':sha(OUT),'blender':bpy.app.version_string,'topology':topology,'bones':len(rig.data.bones),
      'test':'49-frame small +/-12 degree head turn and .02 BU pelvis lift / .006 BU side shift; no locomotion',
      'limits':{'paw_drift_bu':.0015,'groom_root_distance_bu':.003,'face_relative_distance_change':.005},
      'maximums':{'paw_drift_bu':max_drift,'groom_root_distance_bu':max_attachment,'face_relative_distance_change':max_face,'rest_pose_mesh_change_bu':neutral_delta},
      'checks':checks,'frames':frames,'not_validated':['walk/crouch/lie poses','advanced facial deformation','all groom roots, sampled 80 only','self-collision clearance over full performance range','production animation readiness'],
      'visual_review':'requires inspection of rendered motion and multi-angle stills'}
    (P/'controlled_rig_audit.json').write_text(json.dumps(report,indent=2)+'\n');s.frame_set(1)
    print('CONTROLLED_RIG_AUDIT',json.dumps({'checks':checks,'maximums':report['maximums']}),flush=True)

def renders(preview=False):
    open_candidate();s=bpy.context.scene;records=[];s.cycles.seed=18102606
    manifest=P/('preview_render_manifest.json' if preview else 'render_manifest.json')
    if '--resume' in sys.argv and manifest.exists():records=json.loads(manifest.read_text())
    def render(name,size=768,samples=40):
        dest=P/(name+'.png');dest.parent.mkdir(exist_ok=True,parents=True);s.render.filepath=str(dest);s.render.resolution_x=size;s.render.resolution_y=size;s.cycles.samples=samples
        if any(r['path']==str(dest.relative_to(ROOT)) and r['candidate_sha256']==sha(OUT) and dest.exists() and r['sha256']==sha(dest) for r in records):return
        t=time.perf_counter();bpy.ops.render.render(write_still=True)
        records.append({'path':str(dest.relative_to(ROOT)),'sha256':sha(dest),'candidate_sha256':sha(OUT),'seconds':round(time.perf_counter()-t,3),'frame':s.frame_current,'engine':'CYCLES','device':'CPU','size':[size,size],'samples':samples,'camera_matrix':[list(r) for r in s.camera.matrix_world],'ortho_scale':s.camera.data.ortho_scale,'material':bpy.data.objects['Leo_surface'].data.materials[0].name,'color_transform':'Standard / None / exposure 0 / gamma 1'})
        (P/('preview_render_manifest.json' if preview else 'render_manifest.json')).write_text(json.dumps(records,indent=2)+'\n')
    for view in (['front_three_quarter','portrait','rear'] if preview else list(prior.VIEWS)):
        prior.camera(view);render(('preview_' if preview else '')+view)
    if preview:return
    surface=bpy.data.objects['Leo_surface'];patina=surface.data.materials[0];local=bpy.data.materials.get('Leo_Felt_r02_PaletteLocked')
    if local is None:
        checkpoint=OUT.with_name('leo_tripo_r02_mesh_checkpoint.blend')
        with bpy.data.libraries.load(str(checkpoint),link=False) as (src,dst):dst.materials=['Leo_Felt_r02_PaletteLocked']
        local=dst.materials[0]
    # A/B keeps geometry, pigment, groom, camera and light fixed.
    prior.camera('portrait');surface.data.materials[0]=local;render('local_felt_portrait')
    surface.data.materials[0]=patina;render('patina_felt_portrait')
    # Body macro from the left side, with a visible wool silhouette.
    c=s.camera;c.location=(-3,-1.9,1.2);target=Vector((-.15,.05,.54));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.75
    surface.data.materials[0]=local;render('local_felt_body_detail',896,48)
    surface.data.materials[0]=patina;render('patina_felt_body_detail',896,48)
    prior.camera('portrait');c.data.ortho_scale=.76;c.location=(-1.8,-5,1.13);target=Vector((0,-.78,.97));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();render('whiskers_final_close',896,48)
    prior.camera('front_three_quarter');bpy.data.objects['Neutral_key'].data.color=(1,.79,.57);bpy.data.objects['Neutral_rim'].data.color=(.62,.74,1);render('story_light_study')
    prior.neutral();prior.camera('front_three_quarter')
    for frame in range(1,50,4):s.frame_set(frame);render('motion/frame_%03d'%frame,512,16)
    s.frame_set(41);prior.camera('right');render('rig_body_shift_right',768,32)
    s.frame_set(9);prior.camera('portrait');render('rig_head_turn_portrait',768,32)
    print('R02_REVIEW_COMPLETE',len(records),flush=True)

if __name__=='__main__':
    if '--preview' in sys.argv:renders(True)
    elif '--audit-only' in sys.argv:audit()
    elif '--render-only' in sys.argv:renders()
    else:audit();renders()
