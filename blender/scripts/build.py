"""Blender 5.2.2: deterministic Feltwillow candidate libraries and s05 scene.
Run: blender --background --factory-startup --python blender/scripts/build.py
"""
import bpy
import math
import random
import json
import hashlib
import sys
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / 'blender'
CFG = json.loads((AREA / 'config/authority.json').read_text())
RNG = random.Random(CFG['seed'])
CHAR = AREA / 'assets/characters/leo/leo_canonical_candidate.blend'
ENV = AREA / 'assets/environments/great_tree/great_tree_dusk_candidate.blend'
SCENE = AREA / 'scenes/lion_and_mouse_v6/s05.blend'
COL = None
PARTS = []


def reset(name):
    global COL
    bpy.ops.wm.read_factory_settings(use_empty=True)
    COL = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(COL)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = CFG['unit_scale_m']
    bpy.context.scene['approval_status'] = 'prototype_needs_owner_review'
    bpy.context.scene['seed'] = CFG['seed']


def register(obj, name, mat=None, bone=None):
    obj.name = name
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    COL.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    if bone:
        PARTS.append((obj, bone))
    return obj


def felt(name, color, fiber_scale=180, bump=.12):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    p = n.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = .91
    p.inputs['Sheen Weight'].default_value = .18
    p.inputs['Sheen Roughness'].default_value = .8
    tex = n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = fiber_scale
    tex.inputs['Detail'].default_value = 3
    coord = n.new('ShaderNodeTexCoord'); l.new(coord.outputs['Object'], tex.inputs['Vector'])
    b = n.new('ShaderNodeBump'); b.inputs['Strength'].default_value = bump
    b.inputs['Distance'].default_value = .006
    l.new(tex.outputs['Fac'], b.inputs['Height']); l.new(b.outputs['Normal'], p.inputs['Normal'])
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*[v * .78 for v in color], 1)
    ramp.color_ramp.elements[1].color = (*[min(v * 1.12, 1) for v in color], 1)
    l.new(tex.outputs['Fac'], ramp.inputs[0]); l.new(ramp.outputs['Color'], p.inputs['Base Color'])
    return m


def ell(name, loc, scale, mat, bone=None, irregular=.012, segments=32, rings=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = register(bpy.context.object, name, mat, bone)
    # Apply deterministic low-frequency irregularity in the editable base mesh.
    for v in o.data.vertices:
        p = v.co
        f = 1 + irregular * (math.sin(7*p.x + 3*p.z) + .5*math.sin(11*p.y-4*p.z))
        v.co = (p.x*scale[0]*f, p.y*scale[1]*f, p.z*scale[2]*f)
    for f in o.data.polygons:
        f.use_smooth = True
    return o


def curve(name, points, radius, mat, bone=None, radii=None):
    c = bpy.data.curves.new(name, 'CURVE'); c.dimensions = '3D'; c.resolution_u = 3
    c.bevel_depth = radius; c.bevel_resolution = 2
    sp = c.splines.new('BEZIER'); sp.bezier_points.add(len(points)-1)
    for i, (p, co) in enumerate(zip(sp.bezier_points, points)):
        p.co = co; p.handle_left_type = 'AUTO'; p.handle_right_type = 'AUTO'
        if radii: p.radius = radii[i]
    o = bpy.data.objects.new(name, c); COL.objects.link(o); c.materials.append(mat)
    if bone: PARTS.append((o, bone))
    return o


def fibers(objects, material, count=100):
    """Bounded surface-following short poly curves; one object per body part."""
    bpy.context.view_layer.update()
    for o, bone in objects:
        if o.type != 'MESH' or not o.name.startswith(('Leo_coat','Leo_mane','Leo_paw','Leo_face','Leo_ear')):
            continue
        c = bpy.data.curves.new(o.name+'_fiber_data', 'CURVE'); c.dimensions='3D'
        c.bevel_depth=.00065; c.bevel_resolution=0
        for _ in range(count):
            face=RNG.choice(list(o.data.polygons))
            tri=list(face.vertices)[:3]
            va,vb,vc=[o.data.vertices[i] for i in tri]
            u=RNG.random();v=RNG.random()
            if u+v>1:u=1-u;v=1-v
            point=va.co*(1-u-v)+vb.co*u+vc.co*v
            norm=va.normal*(1-u-v)+vb.normal*u+vc.normal*v
            normal=(o.matrix_world.to_3x3() @ norm).normalized()
            tangent=normal.cross(Vector((RNG.random(),RNG.random(),RNG.random()))).normalized()
            start=o.matrix_world @ point+normal*.001
            length=RNG.uniform(.008,.021)
            s=c.splines.new('POLY');s.points.add(3)
            for j,p in enumerate(s.points):
                t=j/3; pos=start+tangent*(length*t)+normal*(math.sin(t*math.pi)*length*.45)
                p.co=(*pos,1)
        ob=bpy.data.objects.new(o.name+'_fibers',c);COL.objects.link(ob);c.materials.append(o.data.materials[0])
        PARTS.append((ob,bone))


def camera(name, loc, target, lens=48, ortho=None):
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);COL.objects.link(o)
    o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    data.lens=lens;data.clip_start=.01;data.clip_end=300
    if ortho: data.type='ORTHO';data.ortho_scale=ortho
    bpy.context.scene.camera=o
    return o


def area(name,loc,target,power,color,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o


def settings():
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24
    s.cycles.use_denoising=True;s.cycles.seed=CFG['seed']
    s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
    s.view_settings.gamma=1;s.render.film_transparent=False
    w=bpy.data.worlds.new('Neutral_world');w.use_nodes=True
    w.node_tree.nodes['Background'].inputs[0].default_value=(.27,.30,.37,1)
    w.node_tree.nodes['Background'].inputs[1].default_value=.35;s.world=w


def save(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True,relative_remap=False)


def create_leo():
    global PARTS, RNG
    RNG=random.Random(CFG['seed'])
    PARTS=[];reset('LEO_CANDIDATE');settings()
    coat=felt('Leo_honey_cream',(.55,.27,.085));cream=felt('Leo_cream',(.78,.60,.34))
    mane=felt('Leo_chestnut_wool',(.085,.024,.006));curl=felt('Leo_golden_lock',(.28,.105,.022))
    inner=felt('Leo_apricot_inner_ear',(.58,.235,.13));dark=felt('Leo_dark_brown',(.055,.027,.017))
    white=felt('Leo_sclera',(.9,.83,.65));amber=felt('Leo_amber_iris',(.42,.18,.018))
    pupil=felt('Leo_pupil',(.009,.007,.005));glint=felt('Leo_eye_glint',(.98,.98,.98))
    for mat in [amber,pupil]:
        p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.26;p.inputs['Sheen Weight'].default_value=0
    ell('Leo_coat_torso',(0,.29,.65),(.285,.61,.31),coat,'spine')
    ell('Leo_cream_chest',(0,-.22,.58),(.245,.22,.27),cream,'chest')
    ell('Leo_coat_rump',(0,.72,.62),(.28,.29,.29),coat,'hips')
    # Armature with four planted IK targets and explicit poles.
    d=bpy.data.armatures.new('Leo_skeleton');rig=bpy.data.objects.new('Leo_RIG',d);COL.objects.link(rig)
    bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    def bone(n,h,t,parent=None,deform=True):
        b=d.edit_bones.new(n);b.head=h;b.tail=t;b.use_deform=deform
        if parent:b.parent=d.edit_bones[parent]
        return b
    bone('ROOT',(0,0,0),(0,0,.15),deform=False)
    bone('hips',(0,.7,.58),(0,.4,.65),'ROOT')
    bone('spine',(0,.4,.65),(0,-.1,.69),'hips')
    bone('chest',(0,-.1,.69),(0,-.35,.78),'spine')
    bone('neck',(0,-.35,.78),(0,-.48,.99),'chest')
    bone('head',(0,-.48,.99),(0,-.85,.99),'neck')
    limb={}
    for end,y in [('front',-.30),('hind',.72)]:
        for side,x in [('L',-.22),('R',.22)]:
            tag=f'{end}_{side}';h=(x,y,.64);k=(x,y+(.075 if end=='front' else -.14),.34);a=(x,y,.115)
            limb[tag]=(h,k,a)
            parent='chest' if end=='front' else 'hips'
            bone(tag+'_upper',h,k,parent);bone(tag+'_lower',k,a,tag+'_upper')
            bone(tag+'_paw',a,(x,y-.16,.10),tag+'_lower')
            bone('CTRL_'+tag,a,(x,y-.16,.10),'ROOT',False)
            bone('POLE_'+tag,(x,y+(1 if end=='front' else -1),.35),(x,y+(1 if end=='front' else -1),.5),'ROOT',False)
    bone('tail_01',(0,.90,.66),(0,1.22,.66),'hips')
    bone('tail_02',(0,1.22,.66),(-.02,1.47,.91),'tail_01')
    bone('tail_03',(-.02,1.47,.91),(-.03,1.51,1.13),'tail_02')
    bpy.ops.object.mode_set(mode='POSE')
    for tag in limb:
        c=rig.pose.bones[tag+'_lower'].constraints.new('IK');c.name='Planted_paw_IK';c.target=rig;c.subtarget='CTRL_'+tag;c.chain_count=2
        c.pole_target=rig;c.pole_subtarget='POLE_'+tag;c.pole_angle=0;c.use_stretch=False
        rig.pose.bones[tag+'_upper'].ik_stretch=0;rig.pose.bones[tag+'_lower'].ik_stretch=0
        # Paw orientation follows the ground control independently of leg bend.
        c=rig.pose.bones[tag+'_paw'].constraints.new('COPY_ROTATION');c.target=rig;c.subtarget='CTRL_'+tag;c.target_space='WORLD';c.owner_space='WORLD'
    bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True;rig.display_type='WIRE'
    for tag,(h,k,a) in limb.items():
        for suffix,start,end,rad in [('upper',h,k,.12),('lower',k,a,.09)]:
            mid=(Vector(start)+Vector(end))/2
            o=ell('Leo_coat_'+tag+'_'+suffix,mid,(rad,rad,(Vector(start)-Vector(end)).length*.65),coat,tag+'_'+suffix)
            o.rotation_euler=(Vector(end)-Vector(start)).to_track_quat('Z','Y').to_euler()
        x,y,z=a
        ell('Leo_paw_'+tag,(x,y-.07,.085),(.135,.175,.085),cream,tag+'_paw')
        for t in [-1,0,1]:
            curve('Leo_toe_'+tag+str(t),[(x+t*.057,y-.235,.07),(x+t*.057,y-.22,.112),(x+t*.057,y-.17,.15)],.0025,dark,tag+'_paw')
    # Head large enough to read as the canon's youthful needle-felt face.
    ell('Leo_mane_mass',(0,-.43,.96),(.41,.245,.45),mane,'head',.035)
    ell('Leo_face',(0,-.645,1.005),(.265,.185,.278),coat,'head')
    # 2 rings of unequal chestnut locks and highlighted frontal spirals.
    for ring in range(2):
        total=15 if ring==0 else 13
        for i in range(total):
            t=2*math.pi*i/total+.08*ring
            x=math.sin(t)*(.32 if ring==0 else .36)
            z=.97+math.cos(t)*(.35 if ring==0 else .32)
            y=-.55 if ring==0 else -.36
            size=RNG.uniform(.087,.12)
            ell('Leo_mane_lock_%d_%02d'%(ring,i),(x,y,z),(size,size*.85,size*1.2),mane,'head',.04,24,16)
            if ring==0:
                pts=[]
                for j in range(30):
                    a=j/29*math.pi*1.8;r=size*(1-.78*j/29)
                    pts.append((x+r*math.cos(a),y-.078-.008*math.sin(a),z+r*math.sin(a)))
                curve('Leo_mane_curl_%02d'%i,pts,.026,curl,'head')
    for side,sign in [('L',-1),('R',1)]:
        x=sign*.235
        ell('Leo_ear_'+side,(x,-.655,1.225),(.105,.052,.115),coat,'head')
        ell('Leo_ear_inner_'+side,(x,-.699,1.229),(.071,.018,.078),inner,'head')
        x=sign*.119
        ell('Leo_eyelid_'+side,(x,-.803,1.064),(.09,.033,.104),dark,'head')
        ell('Leo_sclera_'+side,(x,-.825,1.064),(.078,.024,.09),white,'head')
        ell('Leo_iris_'+side,(x+sign*.006,-.848,1.059),(.049,.012,.061),amber,'head')
        ell('Leo_pupil_'+side,(x+sign*.006,-.858,1.064),(.031,.009,.042),pupil,'head')
        ell('Leo_glint_'+side,(x-.012,-.867,1.088),(.012,.006,.014),glint,'head',0,16,12)
        sleep=curve('Leo_sleep_lid_'+side,[(x-.065,-.822,1.07),(x,-.841,1.045),(x+.065,-.822,1.07)],.006,dark,'head')
        sleep.hide_render=True
        curve('Leo_brow_'+side,[(x-sign*.067,-.811,1.172),(x,-.828,1.192),(x+sign*.055,-.802,1.172)],.014,mane,'head')
        ell('Leo_face_muzzle_'+side,(sign*.073,-.824,.913),(.09,.065,.067),cream,'head')
        for n in range(3):
            ell('Leo_whisker_dot_'+side+str(n),(sign*(.065+n*.022),-.883,.925-.013*(n%2)),(.003,.002,.003),mane,'head',0,12,8)
        for n in range(2):
            curve('Leo_whisker_'+side+str(n),[(sign*.10,-.878,.916-n*.02),(sign*.24,-.90,.93-n*.04),(sign*.32,-.88,.94-n*.06)],.0008,cream,'head')
    ell('Leo_face_chin',(0,-.79,.851),(.11,.064,.058),cream,'head')
    # Soft triangular dark felt nose, closed lip seam.
    verts=[(-.065,-.886,.967),(.065,-.886,.967),(0,-.91,.911),(0,-.85,.95)]
    mesh=bpy.data.meshes.new('nose');mesh.from_pydata(verts,[],[(0,1,2),(0,3,1),(1,3,2),(2,3,0)])
    o=bpy.data.objects.new('Leo_nose',mesh);COL.objects.link(o);mesh.materials.append(dark);PARTS.append((o,'head'))
    mod=o.modifiers.new('Soft felt nose','BEVEL');mod.width=.015;mod.segments=3
    curve('Leo_closed_mouth',[(0,-.892,.923),(0,-.89,.892),(-.04,-.872,.872)],.0028,dark,'head')
    curve('Leo_closed_mouth_R',[(0,-.89,.892),(.04,-.872,.872)],.0028,dark,'head')
    curve('Leo_tail_base',[(0,.90,.66),(0,1.05,.60),(0,1.22,.66)],.038,coat,'tail_01')
    curve('Leo_tail_mid',[(0,1.22,.66),(-.01,1.39,.74),(-.02,1.47,.91)],.033,coat,'tail_02')
    ell('Leo_tail_tuft',(-.025,1.50,1.02),(.075,.075,.13),mane,'tail_03',.04)
    # Weld torso, rump and chest; blend skin weights along the spinal axis.
    torso=[o for o,b in PARTS if o.name in {'Leo_coat_torso','Leo_coat_rump','Leo_cream_chest'}]
    bpy.ops.object.select_all(action='DESELECT')
    for o in torso:o.select_set(True)
    bpy.context.view_layer.objects.active=torso[0];bpy.ops.object.join()
    body=bpy.context.object;body.name='Leo_coat_body'
    rem=body.modifiers.new('Native voxel welded torso','REMESH');rem.mode='VOXEL';rem.voxel_size=.018
    bpy.ops.object.modifier_apply(modifier=rem.name)
    smooth=body.modifiers.new('Soft handmade weld','SMOOTH');smooth.factor=.7;smooth.iterations=4
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    PARTS[:]=[(o,b) for o,b in PARTS if o not in torso]
    PARTS.append((body,'spine'))
    fibers(list(PARTS),curl,1200)
    for o,b in PARTS:
        if o.type=='MESH':
            g=o.vertex_groups.new(name=b);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
            if o.name=='Leo_coat_body':
                hips=o.vertex_groups.new(name='hips')
                for v in o.data.vertices:
                    y=(o.matrix_world@v.co).y
                    w=max(0,min(1,(y-.30)/.50))
                    g.add([v.index],1-w,'REPLACE');hips.add([v.index],w,'REPLACE')
            mod=o.modifiers.new('Leo skeletal deformation','ARMATURE');mod.object=rig
            o.parent=rig
        else:
            # Bone parenting with inverse matrix preserves rest coordinates.
            world=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=b
            rest=rig.data.bones[b]
            rest_parent=rest.matrix_local @ Matrix.Translation((0,rest.length,0))
            o.matrix_parent_inverse=rest_parent.inverted();o.matrix_basis=world
    rig['status']='articulated prototype; overlapping component topology; not final animation topology'
    rig['mouth_policy']='closed';rig['mane_shape']='rigid head-bound locks; no dynamic hair'
    rig['pose_presets']='neutral, walk, lie, struggle, head_turn'
    bpy.context.view_layer.update()
    rig['neutral_height']=max((o.matrix_world @ Vector(corner)).z for o in COL.objects if o.type in {'MESH','CURVE'} for corner in o.bound_box)
    # Standalone asset has a removable studio collection outside asset collection.
    asset=COL
    studio=bpy.data.collections.new('DIAGNOSTIC_STUDIO');bpy.context.scene.collection.children.link(studio)
    globals()['COL']=studio
    mat=felt('Studio_matte',(.68,.70,.73),50,.035)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003))
    register(bpy.context.object,'Studio_floor',mat)
    area('Neutral_key',(-3,-4,5),(0,0,.7),180,(1,.94,.86),4)
    area('Neutral_fill',(3,-2,3),(0,0,.7),90,(.86,.92,1),3)
    area('Neutral_rim',(0,3,4),(0,0,.7),120,(1,1,1),3)
    camera('CAM_Leo_front_three_quarter',(2.5,-4,1.7),(0,.12,.72),ortho=2.65)
    bpy.context.scene.render.resolution_x=640;bpy.context.scene.render.resolution_y=640
    bpy.context.scene['asset_collection']=asset.name
    save(CHAR)


def create_environment():
    global RNG
    RNG=random.Random(CFG['seed']+1)
    reset('GREAT_TREE_CANDIDATE');settings()
    bark=felt('Oak_handcrafted_bark',(.13,.072,.044),38,.45)
    barklight=felt('Oak_ridges',(.19,.10,.055),95,.2)
    grass=felt('Ground_olive_wool',(.17,.21,.068),90,.22)
    moss=felt('Moss_loops',(.23,.29,.065),95,.3)
    leaf=felt('Leaf_felt',(.11,.18,.065),120,.2)
    dirt=felt('Path_ochre_cloth',(.28,.16,.09),130,.24)
    stone=felt('Crafted_stone',(.22,.23,.24),75,.3)
    for mat in [bark,barklight,grass,moss,leaf,dirt,stone]:
        for node in mat.node_tree.nodes:
            if node.type=='BUMP':node.inputs['Distance'].default_value=.035
    water=felt('Stream_blue_cloth',(.16,.23,.30),90,.05)
    ell('SUPPORT_clearing_ground',(0,4,-.16),(25,25,.16),grass,irregular=0)
    # Winding path, explicit surface mesh with sewn irregular edges.
    verts=[]
    for y,x,width in [(-12,4.7,5),(-5,3.7,4),(0,2.0,3.4),(3,-.5,2),(6,-3.4,1.25),(11,-6,.65),(18,-7,.3)]:
        verts.extend([(x-width,y,.012),(x+width,y,.012)])
    m=bpy.data.meshes.new('Path_mesh');m.from_pydata(verts,[],[(2*i,2*i+1,2*i+3,2*i+2) for i in range(6)])
    o=bpy.data.objects.new('SUPPORT_dirt_path',m);COL.objects.link(o);m.materials.append(dirt)
    # Trunk/root fan camera-calibrated to approved plate's center-right oak.
    base=Vector((3.5,5.2,0))
    curve('Great_oak_trunk',[base,base+Vector((-.2,0,2)),base+Vector((-.1,.25,4)),base+Vector((.3,.3,7)),base+Vector((.6,.5,10))],1.05,bark,radii=[1.65,1.1,.95,.8,.5])
    for i,(dx,dy) in enumerate([(-4,-1),(-2.5,-2),(0,-3.3),(3,-2),(5,.5),(-3,2)]):
        curve('Root_fan_%02d'%i,[base+Vector((0,0,.8)),base+Vector((dx*.35,dy*.35,.32)),base+Vector((dx*.75,dy*.75,.12)),base+Vector((dx,dy,.05))],.33,bark,radii=[2,1.2,.6,.12])
    for i in range(36):
        t=i*math.tau/36
        points=[]
        for z,r,cx,cy in [(.35,1.62,0,0),(2,1.12,-.2,0),(4,1.0,-.1,.25),(7.7,.72,.4,.35)]:
            points.append((base.x+cx+math.cos(t)*r,base.y+cy+math.sin(t)*r,z))
        curve('Bark_raised_seam_%02d'%i,points,.025,barklight)
    for i,(dx,dy,dz) in enumerate([(-5,0,6),(-3,2,7),(4,0,7),(6,2,6)]):
        curve('Oak_branch_'+str(i),[base+Vector((0,0,4)),base+Vector((dx*.45,dy*.4,dz-.8)),base+Vector((dx,dy,dz))],.43,bark,radii=[1.5,.8,.2])
    ell('Left_moss_mound',(-5,-.8,.35),(2.5,1.5,.65),moss,irregular=.06)
    curve('Foreground_stumble_root',[(-6,1,.7),(-4,-.1,.35),(-2,-1,.12),(-.7,-1.5,.045)],.20,bark,radii=[2,1.4,.65,.1])
    ell('Stone_center_left',(-3,2,.27),(.68,.48,.39),stone,irregular=.08)
    ell('Rock_right',(5.6,1,.52),(1.30,.9,.75),stone,irregular=.08)
    ell('Stream_far_left',(-8,10,.025),(3.6,6,.025),water,irregular=.05)
    # Moss patches on roots; leave the acting area and path clear.
    for i in range(70):
        a=RNG.uniform(0,math.tau);r=RNG.uniform(1.1,3.5)
        x=base.x+math.cos(a)*r;y=base.y+math.sin(a)*r
        ell('Root_moss_%03d'%i,(x,y,.12+max(0,2-r)*.23),(RNG.uniform(.13,.4),.25,.15),moss,irregular=.06,segments=16,rings=10)
    # Background hills and fabric sky: no projected plate in beauty render.
    hillmats=[felt('Hill_'+str(i),c,15,.08) for i,c in enumerate([(.13,.13,.22),(.19,.17,.27),(.25,.22,.31)])]
    for i in range(3):
        ell('Distant_ridge_'+str(i),(-7+i*5,24+i*6,1.1+i*.4),(16,5,2.2),hillmats[i],irregular=.07)
    sky=bpy.data.materials.new('Dusk_sky_fabric_gradient');sky.use_nodes=True
    n=sky.node_tree.nodes;l=sky.node_tree.links;n.clear()
    out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');ramp=n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position=.05;ramp.color_ramp.elements[0].color=(.25,.19,.32,1)
    ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(.115,.095,.23,1)
    l.new(tex.outputs['Generated'],sep.inputs[0]);l.new(sep.outputs['Z'],ramp.inputs[0])
    sunset=n.new('ShaderNodeValToRGB')
    sunset.color_ramp.elements[0].position=.35;sunset.color_ramp.elements[0].color=(.72,.26,.075,1)
    sunset.color_ramp.elements[1].position=.49;sunset.color_ramp.elements[1].color=(.14,.115,.25,1)
    l.new(sep.outputs['X'],sunset.inputs[0])
    mix=n.new('ShaderNodeMixRGB');mix.inputs[0].default_value=.55
    l.new(sunset.outputs[0],mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2])
    l.new(mix.outputs[0],em.inputs[0]);em.inputs[1].default_value=.7;l.new(em.outputs[0],out.inputs[0])
    ell('Dusk_sky', (0,65,12),(100,1,25),sky,irregular=0)
    for i in range(42):
        x=RNG.uniform(-16,18);y=RNG.uniform(11,23);z=RNG.uniform(1.4,3.8)
        curve('Background_trunk_'+str(i),[(x,y,0),(x,y,z)],.10,bark)
        if i%3==0:
            for j in range(3):
                bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=.7-j*.15,radius2=0,depth=1.5,location=(x,y,z*.5+j*.55))
                register(bpy.context.object,'Distant_pine_'+str(i)+'_'+str(j),leaf)
        else:
            ell('Background_foliage_'+str(i),(x,y,z),(.8,.7,1),leaf,irregular=.09,segments=16,rings=12)
    for i in range(110):
        x=RNG.uniform(-3.6,9);y=RNG.uniform(4.3,8);z=RNG.uniform(5,7.5)
        ell('Canopy_cluster_'+str(i),(x,y,z),(.5,.45,.32),leaf,irregular=.1,segments=16,rings=12)
    # Repeated leaf blades in clumps: bounded budget, controlled seed.
    for i in range(420):
        x=RNG.uniform(-11,11);y=RNG.uniform(-5,13)
        if (-2<x<3 and -3<y<3) or (y<3 and abs(x-(2-y*.25))<2.5):continue
        for j in range(3):
            o=ell('Ground_leaf_%03d_%d'%(i,j),(x+j*.06,y,.06),(.035,.11,.075),moss if i%2 else leaf,irregular=.04,segments=8,rings=6)
            o.rotation_euler=(RNG.uniform(-.5,.5),RNG.uniform(-.6,.6),RNG.uniform(0,math.tau))
    # Hidden in render image reference, used only for manual calibration.
    ref=bpy.data.objects.new('REFERENCE_tree_dusk_r02_NOT_RENDERED',None);COL.objects.link(ref)
    ref.empty_display_type='IMAGE';ref.data=bpy.data.images.load(str(ROOT/CFG['location']['plate']))
    ref.data.filepath='//' + str(Path('../../../..')/CFG['location']['plate'])
    ref.hide_render=True;ref.hide_viewport=True
    area('Dusk_cool_sky',(-1,3,10),(0,2,0),900,(.53,.60,1),10)
    area('Dusk_neutral_fill',(0,-5,7),(1,3,0),650,(.82,.86,1),9)
    area('Sunset_far_left',(-12,6,4),(2,4,1),1100,(1,.60,.27),5)
    camera('CAM_s05_wide',(0,-13,3.5),(0,4,1.55),lens=39)
    bpy.context.scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.19,.18,.32,1)
    save(ENV)


def link_asset(path,name):
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[name]
    c=dst.collections[0];bpy.context.scene.collection.children.link(c)
    return c


def create_scene():
    reset('S05_CONTROLS');settings()
    env=link_asset(ENV,'GREAT_TREE_CANDIDATE')
    # Relative linked library paths survive repository relocation.
    # Keep absolute runtime paths until first scene save establishes its base.
    # Append Leo once for pose editing; provenance retained in custom properties.
    with bpy.data.libraries.load(str(CHAR),link=False) as (src,dst):dst.collections=['LEO_CANDIDATE']
    leo=dst.collections[0];bpy.context.scene.collection.children.link(leo)
    rig=leo.objects['Leo_RIG'];rig['source_library']='//../../assets/characters/leo/leo_canonical_candidate.blend'
    rig.location=(.4,.3,0);rig.rotation_euler[2]=math.radians(65)
    # Sleeping pose driven by the same skeleton, no independent geometry rescale.
    sys.path.insert(0,str(AREA/'scripts'))
    from poses import apply_pose
    apply_pose(rig,'lie')
    # Turn the existing head toward the plate-facing camera, retaining body scale.
    from mathutils import Quaternion
    head=rig.pose.bones['head'];basis=head.bone.matrix_local.to_quaternion()
    head.rotation_mode='QUATERNION'
    head.rotation_quaternion=basis.inverted() @ Quaternion((0,0,1),math.radians(-48)) @ basis
    bpy.context.view_layer.update()
    registered=bpy.data.objects.get('CAM_s05_wide')
    wide=registered.copy();wide.data=registered.data.copy();COL.objects.link(wide)
    wide.name='CAM_s05_wide_review';bpy.context.scene.camera=wide
    wide.data.show_background_images=True
    background=wide.data.background_images.new()
    background.image=bpy.data.images.get('tree_dusk_r02.png')
    background.alpha=.35;background.display_depth='BACK'
    wide['reference_usage']='Viewport camera-aligned plate overlay; never in beauty render'
    # Registered 2D crops become lens/shift variants of the same optical center.
    # One camera per view + crop center (the selected medium view has two centers).
    seen=set()
    for f in CFG['s05_frames']:
        rect=f['crop_rect_on_plate'];x,y,w,h=rect
        key=(f['view'],round(x+w/2,3),round(y+h/2,3))
        if f['view']=='wide':continue
        if key in seen:continue
        seen.add(key)
        name='CAM_s05_'+f['view']+'_'+f['id']
        o=wide.copy();o.data=wide.data.copy();COL.objects.link(o);o.name=name
        o.data.lens=wide.data.lens/w
        o.data.shift_x=((x+w/2)-.5)/w
        o.data.shift_y=(.5-(y+h/2))*(540/960)/w
        o['source_frame']=f['id'];o['crop_rect_on_plate']=rect;o['match_status']='provisional_landmark_fit'
        if f['view']=='owner_s05x_p04_camera':
            o.data.dof.use_dof=True;o.data.dof.focus_distance=14.7;o.data.dof.aperture_fstop=4
    # Non-production proxy measures standing anatomy, never the lying pose box.
    m=felt('Milo_PROXY_neutral',(.30,.30,.30))
    ratio=CFG['cast_scale']['milo_to_leo']['standing_equivalent_height']
    height=rig['neutral_height']*ratio
    proxy=ell('Milo_SCALE_PROXY',(1.8,.3,height/2),(.09,.065,height/2),m,irregular=0)
    proxy.hide_render=True;proxy['production_asset']=False;proxy['neutral_height']=height
    proxy['ratio_to_leo']=ratio;proxy['note']='Scale calibration only; not canonical Milo'
    bpy.context.scene['representative_frame']='s05_p01; sleeping pose approximation'
    save(SCENE)
    # After saving, fix image references and library path against actual saved file.
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath)
    save(SCENE)


if __name__=='__main__':
    for path,expected in CFG['sources'].items():
        source=ROOT/path
        if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
            raise RuntimeError('Authority changed or missing; review and update extraction/config before rebuilding: '+path)
    create_leo();create_environment();create_scene()
    print('FELTWILLOW_BUILD_OK')
