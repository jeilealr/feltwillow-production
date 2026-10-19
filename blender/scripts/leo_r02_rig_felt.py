"""Bind Leo's refined r02, attach stable wool, apply the approved PATINA trial.
Run after leo_tripo_refine_r02.py. Does not call any external service.
"""
import bpy,math,json,sys,random,bisect,hashlib,shutil,time
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender';sys.path.insert(0,str(AREA/'scripts'))
import leo_tripo_refine_r02 as refine
import leo_tripo_canonical_pass as prior
OUT=refine.OUT;P=refine.P;MAT=AREA/'assets/materials/leo_felt_patina_trial';RNG=random.Random(18102606)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def smooth(a,b,x):return refine.smoothstep(a,b,x)
def normalize(d):
    d={k:v for k,v in d.items() if v>.00001};s=sum(d.values());return {k:v/s for k,v in d.items()}
def segment_distance(p,a,b):
    d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));return (p-a-d*t).length,t

def rig_surface(o,paws,asset):
    arm=bpy.data.armatures.new('Leo_r02_skeleton');rig=bpy.data.objects.new('Leo_RIG_R02',arm);asset.objects.link(rig)
    rig.parent=bpy.data.objects['Leo_ASSET_ROOT'];rig.show_in_front=True;rig.display_type='WIRE'
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
    def bone(name,h,t,parent=None,deform=True):
        b=arm.edit_bones.new(name);b.head=h;b.tail=t;b.use_deform=deform
        if parent:b.parent=arm.edit_bones[parent]
        return b
    bone('ROOT',(0,0,0),(0,0,.12),deform=False)
    bone('hips',(0,.30,.61),(0,.07,.63),'ROOT');bone('spine',(0,.07,.63),(0,-.17,.67),'hips')
    bone('chest',(0,-.17,.67),(0,-.34,.77),'spine');bone('neck',(0,-.34,.77),(0,-.44,.96),'chest')
    bone('head',(0,-.44,.96),(0,-.75,1.09),'neck')
    chains={}
    for key,foot in paws.items():
        end,side=key.split('.');x,y,z=foot['center'];ankle=Vector((x,y+.015,.095))
        hip=Vector((x*.65,y+(.18 if end=='front' else -.015),.63))
        knee=Vector((x*.87,y+(.22 if end=='front' else -.10),.33))
        tag=end+'_'+side;parent='chest' if end=='front' else 'hips'
        bone(tag+'_upper',hip,knee,parent);bone(tag+'_lower',knee,ankle,tag+'_upper')
        bone(tag+'_paw',ankle,(x,y-.12,.095),tag+'_lower')
        bone('CTRL_'+tag,ankle,(x,y-.12,.095),'ROOT',False)
        chains[tag]=(hip,knee,ankle)
    tail=[Vector((-.30,.54,.63)),Vector((-.49,.77,.60)),Vector((-.53,.90,.86)),Vector((-.49,.90,1.11))]
    for i in range(3):bone('tail_'+str(i+1),tail[i],tail[i+1],'hips' if i==0 else 'tail_'+str(i))
    bpy.ops.object.mode_set(mode='POSE')
    for tag in chains:
        p=rig.pose.bones[tag+'_lower'];ik=p.constraints.new('IK');ik.name='Planted paw / bounded trial';ik.target=rig;ik.subtarget='CTRL_'+tag;ik.chain_count=2;ik.use_stretch=False
        rig.pose.bones[tag+'_upper'].ik_stretch=0;p.ik_stretch=0
        c=rig.pose.bones[tag+'_paw'].constraints.new('COPY_ROTATION');c.target=rig;c.subtarget='CTRL_'+tag;c.target_space='WORLD';c.owner_space='WORLD'
    bpy.ops.object.mode_set(mode='OBJECT')
    weights=[]
    for v in o.data.vertices:
        p=v.co;h=max(smooth(.75,.91,p.z),smooth(.56,.75,p.z)*(1-smooth(-.65,-.52,p.y)))*(1-smooth(-.20,.04,p.y))
        tailw=smooth(.51,.68,p.y)*smooth(.38,.50,p.z)*(1-smooth(-.30,-.15,p.x))
        # Choose the actual fitted limb, blending into torso above the elbow/hip.
        distances={tag:min(segment_distance(p,a,b)[0],segment_distance(p,b,c)[0]) for tag,(a,b,c) in chains.items()}
        tag=min(distances,key=distances.get);distance=distances[tag]
        leg=(1-smooth(.34,.65,p.z))*math.exp(-(distance/.17)**4)
        if p.z<.15:leg=1
        d={}
        if h>0:d['head']=h
        remaining=1-h
        if tailw>0:
            td=[segment_distance(p,tail[i],tail[i+1])[0] for i in range(3)];k=min(range(3),key=lambda i:td[i]);d['tail_'+str(k+1)]=remaining*tailw
        remaining*=1-tailw
        if leg>0:
            paw=1-smooth(.12,.23,p.z);upper=smooth(.25,.44,p.z)
            d[tag+'_paw']=remaining*leg*paw;d[tag+'_upper']=remaining*leg*(1-paw)*upper;d[tag+'_lower']=remaining*leg*(1-paw)*(1-upper)
        torso=remaining*(1-leg);hip=smooth(.0,.34,p.y);chest=1-smooth(-.30,-.07,p.y)
        d['hips']=torso*hip;d['chest']=torso*(1-hip)*chest;d['spine']=torso*(1-hip)*(1-chest)
        weights.append(normalize(d))
    for b in arm.bones:
        if b.use_deform:o.vertex_groups.new(name=b.name)
    for v,w in zip(o.data.vertices,weights):
        for name,value in w.items():o.vertex_groups[name].add([v.index],value,'REPLACE')
    mod=o.modifiers.new('Leo r02 controlled deformation','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
    bpy.context.view_layer.update()
    # Six cream whiskers follow the rigid head; curve shape stays editable.
    for ob in list(asset.objects):
        if ob.name.startswith('Leo_whisker_'):
            world=ob.matrix_world.copy();ob.parent=rig;ob.parent_type='BONE';ob.parent_bone='head'
            b=rig.data.bones['head'];ob.matrix_parent_inverse=(b.matrix_local@Matrix.Translation((0,b.length,0))).inverted();ob.matrix_basis=world
    rig['status']='Initial fitted quadruped rig; small head/plant test only; not locomotion-ready';rig['mouth_policy']='closed, no teeth'
    return rig,weights

def patina_material(source):
    m=source.copy();m.name='Leo_Felt_r02_PATINA';n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    coord=n.new('ShaderNodeAttribute');coord.attribute_name='felt_rest';coord.label='Stable rest coordinates / no swimming'
    scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=4.0;l.new(coord.outputs['Vector'],scale.inputs[0])
    maps={}
    for kind in ('height','roughness'):
        im=bpy.data.images.load(str(MAT/(kind+'.png')),check_existing=True);im.colorspace_settings.name='Non-Color';im.pack()
        t=n.new('ShaderNodeTexImage');t.image=im;t.label='Approved PATINA '+kind;t.projection='BOX';t.projection_blend=.25;t.extension='REPEAT';l.new(scale.outputs[0],t.inputs['Vector']);maps[kind]=t
    bump=n.new('ShaderNodeBump');bump.label='PATINA compressed felt height';bump.inputs['Strength'].default_value=.34;bump.inputs['Distance'].default_value=.0020;l.new(maps['height'].outputs['Color'],bump.inputs['Height'])
    # Keep only the source normal baseline below PATINA; don't stack noisy maps.
    base=next((x for x in n if x.type=='NORMAL_MAP'),None)
    if base:l.new(base.outputs['Normal'],bump.inputs['Normal'])
    l.new(bump.outputs['Normal'],p.inputs['Normal'])
    rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.86;rough.inputs['To Max'].default_value=.98;l.new(maps['roughness'].outputs['Color'],rough.inputs['Value']);l.new(rough.outputs['Result'],p.inputs['Roughness'])
    m['source']='PATINA approved trial 01a14f67-38b6-75c2-a13d-7bbacd6ce06c';m['usage']='height/roughness at .25 BU tile; original Leo color unchanged; normal map preserved for UV-specific experiments'
    return m

def add_wool(o,rig,weights,asset):
    import numpy as np
    me=o.data;me.calc_loop_triangles();tris=list(me.loop_triangles);acc=[];area=0
    for t in tris:area+=t.area;acc.append(area)
    uv=me.uv_layers.active.data;verts=[];faces=[];vertex_uv=[];bindings=[];group_assignments={g.name:[] for g in o.vertex_groups}
    # Short loops sit on the felt; few longer flyaways define the soft outline.
    for k in range(46000):
        tr=tris[bisect.bisect_left(acc,RNG.random()*area)];u=RNG.random();v=RNG.random()
        if u+v>1:u=1-u;v=1-v
        bary=(1-u-v,u,v);vs=[me.vertices[i] for i in tr.vertices];root=sum((x.co*w for x,w in zip(vs,bary)),Vector())
        normal=sum((x.normal*w for x,w in zip(vs,bary)),Vector()).normalized()
        # Keep sensitive facial shapes clear; PATINA supplies their fine relief.
        if root.y<-.70 and abs(root.x)<.32 and .79<root.z<1.28:continue
        tangent=normal.cross(Vector((RNG.random(),RNG.random(),RNG.random()))).normalized();side=normal.cross(tangent)
        fly=(k%11==0);length=RNG.uniform(.008,.016) if not fly else RNG.uniform(.012,.024)
        height=RNG.uniform(.0010,.0028) if not fly else RNG.uniform(.002,.006)
        radius=RNG.uniform(.00030,.00048);N=7;S=3;start=len(verts)
        points=[]
        for j in range(N):
            t=j/(N-1);a=t*math.pi*1.7
            points.append(root+normal*(.00045+math.sin(t*math.pi)*height)+tangent*(length*t)+side*(math.sin(a)*length*.25))
        for j,p in enumerate(points):
            direction=(points[min(j+1,N-1)]-points[max(0,j-1)]).normalized();ex=direction.cross(normal).normalized();ey=direction.cross(ex).normalized()
            for s in range(S):
                a=math.tau*s/S;verts.append(tuple(p+(ex*math.cos(a)+ey*math.sin(a))*radius))
        for j in range(N-1):
            for s in range(S):a=start+j*S+s;b=start+j*S+(s+1)%S;faces.append((a,b,b+S,a+S))
        uvc=sum((uv[idx].uv*w for idx,w in zip(tr.loops,bary)),Vector((0,0)))
        vertex_uv.extend([tuple(uvc)]*(N*S))
        w={}
        for idx,factor in zip(tr.vertices,bary):
            for name,value in weights[idx].items():w[name]=w.get(name,0)+value*factor
        w=normalize(w);ids=list(range(start,start+N*S))
        for name,value in w.items():group_assignments[name].append((ids,value))
        bindings.append({'start':start,'triangle':list(tr.vertices),'bary':bary,'rest_root':list(root)})
    mesh=bpy.data.meshes.new('Leo_r02_short_loop_wool');mesh.from_pydata(verts,[],faces);mesh.update()
    wool=bpy.data.objects.new('Leo_attached_wool_r02',mesh);asset.objects.link(wool);wool.parent=bpy.data.objects['Leo_ASSET_ROOT']
    layer=mesh.uv_layers.new(name='Source_palette_UV');vuv=np.array(vertex_uv,dtype=np.float32);li=np.empty(len(mesh.loops),dtype=np.int32);mesh.loops.foreach_get('vertex_index',li);layer.data.foreach_set('uv',vuv[li].reshape(-1))
    mesh.polygons.foreach_set('use_smooth',np.ones(len(mesh.polygons),dtype=bool))
    for name,groups in group_assignments.items():
        vg=wool.vertex_groups.new(name=name)
        for ids,value in groups:vg.add(ids,value,'REPLACE')
    mod=wool.modifiers.new('Wool inherits source triangle skin weights','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
    m=o.data.materials[0].copy();m.name='Leo_Wool_r02_Palette';pp=m.node_tree.nodes.get('Principled BSDF')
    for link in list(pp.inputs['Normal'].links):m.node_tree.links.remove(link)
    pp.inputs['Roughness'].default_value=.97;pp.inputs['Sheen Weight'].default_value=.20;wool.data.materials.append(m)
    # Store a sparse deterministic independent attachment check sample.
    sample=bindings[::max(1,len(bindings)//80)]
    (P/'groom_bindings_sample.json').write_text(json.dumps(sample,indent=2)+'\n')
    print('GROOM',len(bindings),'strands',len(mesh.vertices),'vertices',flush=True)
    return wool,len(bindings)

def reset_pose(rig):
    for b in rig.pose.bones:b.location=(0,0,0);b.rotation_mode='QUATERNION';b.rotation_quaternion=(1,0,0,0);b.scale=(1,1,1)

def animate(rig):
    reset_pose(rig)
    for frame,angle,lift in [(1,0,0),(9,12,0),(17,0,0),(25,-12,0),(33,0,0),(41,0,.02),(49,0,0)]:
        reset_pose(rig);head=rig.pose.bones['head'];q=head.bone.matrix_local.to_quaternion();head.rotation_quaternion=q.inverted()@Quaternion(Vector((0,0,1)),math.radians(angle))@q
        hips=rig.pose.bones['hips'];hips.location=hips.bone.matrix_local.to_3x3().inverted()@Vector((.006 if lift else 0,0,lift))
        head.keyframe_insert(data_path='rotation_quaternion',frame=frame);hips.keyframe_insert(data_path='location',frame=frame)
    if rig.animation_data and rig.animation_data.action:rig.animation_data.action.name='Leo_R02_Controlled_HeadTurn_Plant_Trial'
    s=bpy.context.scene;s.frame_start=1;s.frame_end=49;s.render.fps=24;s.frame_set(1)

def build():
    checkpoint=OUT.with_name('leo_tripo_r02_mesh_checkpoint.blend')
    if not checkpoint.exists():shutil.copy2(OUT,checkpoint)
    bpy.ops.wm.open_mainfile(filepath=str(checkpoint),use_scripts=False)
    o=bpy.data.objects['Leo_surface'];asset=bpy.data.collections['LEO_TRIPO_CANDIDATE_R02'];paws=refine.feet(o)
    rig,weights=rig_surface(o,paws,asset)
    local=o.data.materials[0];local.use_fake_user=True;patina=patina_material(local);o.data.materials[0]=patina
    wool,count=add_wool(o,rig,weights,asset);animate(rig)
    # Open in a useful camera and color display, with nothing selected.
    prior.neutral();prior.camera('front_three_quarter');s=bpy.context.scene;s.cycles.seed=18102606
    for screen in bpy.data.screens:
        for a in screen.areas:
            if a.type=='VIEW_3D':
                a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=False
                a.spaces.active.region_3d.view_perspective='CAMERA'
    bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=o
    s['approval_status']='r02 rig/felt candidate; controlled test pending';s['groom_strands']=count;s['material_trial']='PATINA_01';s.frame_set(1)
    for im in bpy.data.images:
        if not im.packed_file and im.has_data:im.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
    (P/'rig_build.json').write_text(json.dumps({'candidate_sha256':sha(OUT),'mesh_stats':refine.stats(o.data),'bones':len(rig.data.bones),'groom_strands':count,'weight_max_sum_error':max(abs(sum(w.values())-1) for w in weights),'mouth':'closed','initial_rig_only':True},indent=2)+'\n')
    print('RIG_FELT_BUILD_COMPLETE',sha(OUT),flush=True)

if __name__=='__main__':build()
