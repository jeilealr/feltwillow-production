"""Refine the preserved native Leo scaffold; never builds S05 or calls providers.

Blender --background --disable-autoexec --python-exit-code 1 --python THIS
Use -- --review-only to reopen the saved candidate and render its review suite.
"""
import bpy, math, random, json, hashlib, sys, time, bisect
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / 'blender'
SOURCE = AREA / 'assets/characters/leo/leo_canonical_candidate.blend'
OUTPUT = SOURCE.with_name('leo_canonical_candidate_r02.blend')
REVIEW = AREA / 'renders/leo_canonical_r02'
REVIEW.mkdir(parents=True, exist_ok=True)
RNG = random.Random(18102602)
BINDINGS = json.loads((AREA/'config/leo_pass_r02_sources.json').read_text())['sources']
sys.path.insert(0, str(AREA/'scripts'))
import build as helpers

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def verify_sources():
    for path, expected in BINDINGS.items():
        if sha(ROOT/path) != expected: raise RuntimeError('Changed source: '+path)

def head_map(p): return Vector((p.x*1.10, -.43+(p.y+.43)*1.08, .96+(p.z-.96)*1.10))
def body_map(p): return Vector((p.x, -.43+(p.y+.43)*.85, p.z))

def bind(o, bone, rig):
    if o.type == 'MESH':
        o.vertex_groups.clear()
        g=o.vertex_groups.new(name=bone);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
        m=o.modifiers.new('Candidate skeletal attachment','ARMATURE');m.object=rig;o.parent=rig
    else:
        world=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=bone
        b=rig.data.bones[bone]
        o.matrix_parent_inverse=(b.matrix_local @ Matrix.Translation((0,b.length,0))).inverted()
        o.matrix_basis=world

def weld(objects, name, voxel):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
    o=bpy.context.object;o.name=name
    m=o.modifiers.new('Continuous felt volume','REMESH');m.mode='VOXEL';m.voxel_size=voxel
    bpy.ops.object.modifier_apply(modifier=m.name)
    m=o.modifiers.new('Needle felt smoothing','SMOOTH');m.factor=.65;m.iterations=5
    bpy.ops.object.modifier_apply(modifier=m.name)
    for f in o.data.polygons:f.use_smooth=True
    return o

def sculpt_lock(name, center, size, roll, material, axis='front'):
    """Thick tapered wool roll, swept in 3D; rear locks are full volumes too."""
    c=Vector(center); points=[]; n=46; sides=12
    for i in range(n):
        t=i/(n-1);a=roll+t*math.pi*1.73
        r=size*(1-.76*t)
        # Uneven depth avoids a planar ornamental ring.
        if axis=='front':p=c+Vector((r*math.cos(a),-.026*math.sin(t*math.pi)-.026*t,r*math.sin(a)))
        else:p=c+Vector((r*math.cos(a),.055*math.sin(t*math.pi),r*math.sin(a)))
        points.append(p)
    verts=[];faces=[]
    for i,p in enumerate(points):
        t=i/(n-1);tangent=(points[min(i+1,n-1)]-points[max(0,i-1)]).normalized()
        u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u).normalized()
        width=size*.44*(.27+.73*math.sin(math.pi*(.08+.86*t))**.55)*(1-.48*t)
        for j in range(sides):
            a=math.tau*j/sides
            verts.append(p+u*math.cos(a)*width+v*math.sin(a)*width*.88)
    for i in range(n-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.extend([tuple(reversed(range(sides))),tuple((n-1)*sides+j for j in range(sides))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);helpers.COL.objects.link(o);mesh.materials.append(material)
    for f in mesh.polygons:f.use_smooth=True
    return o

def surface_wool(o, bone, rig, count):
    mesh=o.data;mesh.calc_loop_triangles()
    triangles=list(mesh.loop_triangles);weights=[];total=0
    for tr in triangles:total+=tr.area;weights.append(total)
    if total==0:return
    c=bpy.data.curves.new(o.name+'_wool','CURVE');c.dimensions='3D';c.bevel_depth=.00052;c.bevel_resolution=0
    for k in range(count):
        tr=triangles[bisect.bisect_left(weights,RNG.random()*total)]
        a,b,d=[mesh.vertices[i] for i in tr.vertices];u=RNG.random();v=RNG.random()
        if u+v>1:u=1-u;v=1-v
        pos=a.co*(1-u-v)+b.co*u+d.co*v
        normal=(a.normal*(1-u-v)+b.normal*u+d.normal*v).normalized()
        tangent=normal.cross(Vector((RNG.random(),RNG.random(),RNG.random()))).normalized()
        bitan=normal.cross(tangent);length=RNG.uniform(.006,.015)
        s=c.splines.new('POLY');s.points.add(5)
        for j,p in enumerate(s.points):
            t=j/5;ang=t*math.pi*1.5
            q=pos+normal*(.0008+math.sin(t*math.pi)*length*.3)+tangent*length*t+bitan*math.sin(ang)*length*.18
            p.co=(*q,1)
    ob=bpy.data.objects.new(o.name+'_wool',c);helpers.COL.objects.link(ob);c.materials.append(o.data.materials[0])
    # Same deform weights via converted mesh for blended limb/body fibers.
    if len(o.vertex_groups)>1:
        bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
        bpy.ops.object.convert(target='MESH');ob=bpy.context.object
        for g in o.vertex_groups:ob.vertex_groups.new(name=g.name)
        from mathutils.kdtree import KDTree
        kd=KDTree(len(mesh.vertices))
        for v in mesh.vertices:kd.insert(v.co,v.index)
        kd.balance()
        for v in ob.data.vertices:
            _,idx,_=kd.find(v.co)
            for g in mesh.vertices[idx].groups:ob.vertex_groups[g.group].add([v.index],g.weight,'REPLACE')
        m=ob.modifiers.new('Surface matching skeletal weights','ARMATURE');m.object=rig;ob.parent=rig
    else:bind(ob,bone,rig)

def build_candidate():
    verify_sources();bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
    rig=bpy.data.objects['Leo_RIG'];asset=bpy.data.collections['LEO_CANDIDATE'];helpers.COL=asset;helpers.PARTS=[]
    # Operate only on a new in-memory revision, retaining the source file.
    tags={}
    for o in list(asset.objects):
        if o==rig:continue
        if '_fibers' in o.name or o.name.startswith(('Leo_mane','Leo_toe_')):
            bpy.data.objects.remove(o,do_unlink=True);continue
        tag=o.parent_bone if o.parent_type=='BONE' else (o.vertex_groups[0].name if o.type=='MESH' and len(o.vertex_groups) else 'spine')
        tags[o.name]=tag;world=o.matrix_world.copy();o.parent=None;o.matrix_world=Matrix.Identity(4)
        for m in list(o.modifiers):
            if m.type=='ARMATURE':o.modifiers.remove(m)
        fn=head_map if tag=='head' else body_map
        if o.type=='MESH':
            for v in o.data.vertices:v.co=fn(world@v.co)
            o.vertex_groups.clear()
        elif o.type=='CURVE':
            for s in o.data.splines:
                for p in s.bezier_points:
                    for attr in ('co','handle_left','handle_right'):setattr(p,attr,fn(world@getattr(p,attr)))
                for p in s.points:p.co=(*fn(world@Vector(p.co[:3])),1)
    # Bring the existing rig rest landmarks with the shortened body/larger head.
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
    bpy.ops.object.mode_set(mode='EDIT')
    for b in rig.data.edit_bones:
        fn=head_map if b.name=='head' else body_map;b.head=fn(b.head);b.tail=fn(b.tail)
    bpy.ops.object.mode_set(mode='OBJECT')
    palette={'Leo_honey_cream':(.74,.385,.125),'Leo_cream':(.94,.755,.46),
             'Leo_chestnut_wool':(.18,.055,.012),'Leo_golden_lock':(.38,.15,.032),
             'Leo_apricot_inner_ear':(.68,.26,.14),'Leo_dark_brown':(.066,.027,.012)}
    for name,color in palette.items():
        m=bpy.data.materials.get(name)
        if not m:continue
        m.diffuse_color=(*color,1)
        for n in m.node_tree.nodes:
            if n.type=='VALTORGB':
                n.color_ramp.elements[0].color=(*[x*.88 for x in color],1)
                n.color_ramp.elements[1].color=(*[min(x*1.08,1) for x in color],1)
            if n.type=='BUMP':n.inputs['Strength'].default_value=.16;n.inputs['Distance'].default_value=.0025
        p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.94;p.inputs['Specular IOR Level'].default_value=.22
    coat=bpy.data.materials['Leo_honey_cream'];cream=bpy.data.materials['Leo_cream'];dark=bpy.data.materials['Leo_dark_brown']
    # Sink/soften eye layers together, keeping sclera/iris/pupil/glint coherent.
    for side in ('L','R'):
        for stem in ('eyelid','sclera','iris','pupil','glint'):
            o=bpy.data.objects['Leo_'+stem+'_'+side];center=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
            for v in o.data.vertices:v.co=center+(v.co-center)*.91+Vector((0,.026,0))
        o=bpy.data.objects['Leo_face_muzzle_'+side];center=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
        for v in o.data.vertices:
            d=v.co-center;v.co=center+Vector((d.x*1.10,d.y*1.18-.012,d.z*1.18))
    # Broader rounded felt nose, replacing only the candidate's sharp tetrahedron.
    old=bpy.data.objects['Leo_nose'];bpy.data.objects.remove(old,do_unlink=True);tags.pop('Leo_nose')
    nose=helpers.ell('Leo_nose',(0,-.983,.953),(.075,.037,.043),dark,irregular=0,segments=40,rings=24)
    for v in nose.data.vertices:
        zn=v.co.z/.043;v.co.x*=.65+.4*(zn+1)/2
    tags[nose.name]='head'
    # Continuous upper/lower limbs; preserve separate soft cream paws.
    for end in ('front','hind'):
        for side in ('L','R'):
            tag=end+'_'+side
            upper=bpy.data.objects['Leo_coat_'+tag+'_upper'];lower=bpy.data.objects['Leo_coat_'+tag+'_lower']
            tags.pop(upper.name);tags.pop(lower.name)
            leg=weld([upper,lower],'Leo_coat_'+tag+'_continuous',.009)
            bind(leg,tag+'_upper',rig);lo=leg.vertex_groups.new(name=tag+'_lower')
            for v in leg.data.vertices:
                z=v.co.z;w=max(0,min(1,(z-.26)/.17));w=w*w*(3-2*w)
                leg.vertex_groups[0].add([v.index],w,'REPLACE');lo.add([v.index],1-w,'REPLACE')
            paw=bpy.data.objects['Leo_paw_'+tag];tags.pop(paw.name)
            center=sum((v.co for v in paw.data.vertices),Vector())/len(paw.data.vertices)
            for v in paw.data.vertices:
                d=v.co-center;v.co=center+Vector((d.x*1.12,d.y,d.z))
            toes=[]
            for i in range(4):
                x=center.x+(i-1.5)*.067
                toes.append(helpers.ell('Toe_volume_'+tag+str(i),(x,center.y-.111,.076),(.042,.080,.072),cream,irregular=.015,segments=24,rings=16))
            paw=weld([paw]+toes,'Leo_paw_'+tag,.005)
            tags[paw.name]=tag+'_paw'
    # Voluminous collar and staggered sculpted rolls, replacing the shallow disc.
    mane_mats=[helpers.felt('Leo_r02_lock_'+str(i),c,210,.15) for i,c in enumerate(
        [(.22,.068,.014),(.29,.10,.021),(.36,.145,.035),(.16,.043,.008),(.43,.19,.048)])]
    core=helpers.ell('Leo_mane_core_r02',(0,-.39,1.025),(.445,.31,.475),mane_mats[0],irregular=.027,segments=48,rings=32);tags[core.name]='head'
    # Offsets and varied roll directions are fixed design inputs, not frame noise.
    for layer in range(3):
        total=[17,19,14][layer]
        for i in range(total):
            t=math.tau*(i+.34*layer)/total+RNG.uniform(-.055,.055)
            rx=[.383,.369,.29][layer];rz=[.409,.385,.33][layer]
            y=[-.667,-.365,-.137][layer]+RNG.uniform(-.027,.027)
            x=math.sin(t)*rx;z=1.035+math.cos(t)*rz
            # Lower mane tapers softly; no giant flat circle behind the head.
            if z<.85:x*=.90
            size=RNG.uniform(.096,.133)
            mat=mane_mats[[0,1,2,1,3,1,4][(i+layer*2)%7]]
            o=sculpt_lock('Leo_mane_roll_%d_%02d'%(layer,i),(x,y,z),size,RNG.uniform(-1,1)+t,mat,'front' if layer==0 else 'rear');tags[o.name]='head'
    # Hero forelock: central descending sweep with a light rolled tip.
    o=sculpt_lock('Leo_forehead_sweep',(.037,-.766,1.392),.133,1.20,mane_mats[2]);tags[o.name]='head'
    # Tail tuft's edited volume tapers to a softer point rather than an oval cap.
    tuft=bpy.data.objects['Leo_tail_tuft'];center=sum((v.co for v in tuft.data.vertices),Vector())/len(tuft.data.vertices)
    for v in tuft.data.vertices:
        d=v.co-center;t=d.z/.13;v.co=center+Vector((d.x*(1.30-.36*t),d.y*(1.24-.30*t),d.z*1.12))
    # Rebind after rest-space edits. Torso uses a continuous spinal gradient.
    for name,bone in tags.items():
        o=bpy.data.objects.get(name)
        if o:bind(o,bone,rig)
    body=bpy.data.objects['Leo_coat_body'];hip=body.vertex_groups.new(name='hips')
    for v in body.data.vertices:
        w=max(0,min(1,(v.co.y-.16)/.40));w=w*w*(3-2*w)
        body.vertex_groups[0].add([v.index],1-w,'REPLACE');hip.add([v.index],w,'REPLACE')
    bpy.context.view_layer.update()
    for o in list(asset.objects):
        if o.type!='MESH':continue
        name=o.name
        if not name.startswith(('Leo_coat','Leo_paw','Leo_face','Leo_ear','Leo_mane','Leo_forehead','Leo_tail_tuft')):continue
        bone=tags.get(name, 'spine')
        if '_continuous' in name:bone=name.removeprefix('Leo_coat_').removesuffix('_continuous')+'_upper'
        count=550 if 'mane' in name else 2200
        if name=='Leo_coat_body':count=10000
        if name=='Leo_face':count=4000
        surface_wool(o,bone,rig,count)
    s=bpy.context.scene;s['approval_status']='r02_promising_prototype_not_canonical';s['source_blend_sha256']=sha(SOURCE)
    s['source_bindings']='blender/config/leo_pass_r02_sources.json';s['revision']='leo_r02'
    rig['status']='r02 feasibility rig; blended continuous limb sections, unvalidated shoulders and facial deformation'
    rig['mouth_policy']='neutral closed mouth; no teeth';rig['active_pose']='neutral'
    # Neutral white-balanced review setup, identical for before/after.
    configure_studio()
    set_camera('front_three_quarter')
    s.render.resolution_x=768;s.render.resolution_y=768;s.cycles.samples=32;s.cycles.seed=18102602
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT),compress=True,relative_remap=False)
    print('LEO_R02_SAVED',OUTPUT,flush=True)

VIEWS={'front':((0,-8,.80),(0,.12,.80),2.25),
 'left':((-8,.2,.80),(0,.2,.80),2.75),'right':((8,.2,.80),(0,.2,.80),2.75),
 'rear':((0,8,.80),(0,.2,.80),2.25),
 'front_three_quarter':((2.5,-4,1.7),(0,.12,.80),2.65),
 'rear_three_quarter':((-3,4,1.8),(0,.2,.80),2.65),
 'elevated_three_quarter':((2.8,-4,3),(0,.12,.78),2.8),
 'portrait':((0,-4,1.12),(0,-.55,1.08),1.36)}

def configure_studio():
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.7,.7,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
    for name,power in [('Neutral_key',230),('Neutral_fill',135),('Neutral_rim',150)]:
        o=bpy.data.objects[name];o.data.color=(1,1,1);o.data.energy=power
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'

def set_camera(name):
    loc,target,scale=VIEWS[name];c=bpy.context.scene.camera;c.location=loc
    c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale;c.data.dof.use_dof=False

def review():
    records=[]
    def render(name):
        s=bpy.context.scene;s.render.resolution_x=768;s.render.resolution_y=768;s.render.resolution_percentage=100
        p=REVIEW/(name+'.png');s.render.filepath=str(p);start=time.perf_counter();bpy.ops.render.render(write_still=True)
        records.append({'image':str(p.relative_to(ROOT)),'sha256':sha(p),'seconds':round(time.perf_counter()-start,3),
          'input_blend':str(Path(bpy.data.filepath).relative_to(ROOT)),'input_blend_sha256':sha(bpy.data.filepath),
          'camera_matrix':[list(r) for r in s.camera.matrix_world],'ortho_scale':s.camera.data.ortho_scale,
          'engine':s.render.engine,'device':s.cycles.device,'samples':s.cycles.samples,'resolution':[768,768],
          'view_transform':s.view_settings.view_transform,'exposure':s.view_settings.exposure,'blender':bpy.app.version_string,
          'status':'diagnostic_candidate_not_approved'})
        (REVIEW/'render_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    # Directly comparable old revision in the same review lighting/camera.
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);configure_studio()
    for view in ('front_three_quarter','portrait','right','rear'):
        set_camera(view);render('before_'+view)
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT),use_scripts=False);configure_studio()
    for view in VIEWS:set_camera(view);render(view)
    # Shape diagnostics: all character materials replaced, fibers hidden.
    asset=bpy.data.collections['LEO_CANDIDATE'];saved=[];hidden=[]
    clay=bpy.data.materials.new('Diagnostic_clay');clay.diffuse_color=(.45,.45,.45,1);clay.use_nodes=True
    clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.45,.45,.45,1)
    clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9
    for o in asset.objects:
        if o.type in {'MESH','CURVE'}:
            saved.append((o,list(o.data.materials)));o.data.materials.clear();o.data.materials.append(clay)
        if o.name.endswith('_wool'):hidden.append(o);o.hide_render=True
    set_camera('front_three_quarter');render('clay_three_quarter');set_camera('right');render('clay_right')
    for o,mats in saved:
        o.data.materials.clear()
        for m in mats:o.data.materials.append(m)
    for o in hidden:o.hide_render=False
    set_camera('front_three_quarter')
    # Controlled small head-turn diagnostic only, no claim of rig acceptance.
    rig=bpy.data.objects['Leo_RIG'];rig.pose.bones['head'].rotation_mode='XYZ';rig.pose.bones['head'].rotation_euler.z=math.radians(12)
    bpy.context.view_layer.update();render('head_turn_12deg')
    rig.pose.bones['head'].rotation_euler.z=0;bpy.context.view_layer.update()
    bpy.data.objects['Neutral_key'].data.color=(1,.77,.52);bpy.data.objects['Neutral_rim'].data.color=(.65,.76,1)
    render('story_light_study')
    # Leave disk file in its saved neutral state, never save review changes.
    print('LEO_R02_REVIEW_COMPLETE',len(records),flush=True)

if __name__=='__main__':
    if '--review-only' not in sys.argv:build_candidate()
    if '--build-only' not in sys.argv:review()
