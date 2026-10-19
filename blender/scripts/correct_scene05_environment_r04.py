"""Correction 1: designed depth/canopy and craft continuity, no new world rebuild."""
import bpy,sys,math,random,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];A=R/'blender';P=A/'renders/scene05_environment_r04';E=A/'assets/environments/great_tree/great_tree_environment_r04.blend';sys.path.insert(0,str(A/'scripts'));import craft_scene05_r04 as c
bpy.ops.wm.open_mainfile(filepath=str(E),use_scripts=False);s=bpy.context.scene;assert not s.get('r04_correction_1');r=random.Random(510410)
hero=bpy.data.collections['GT_R04_HERO_CRAFT'];dress=bpy.data.collections['GT_R04_AUTHORED_PLANTS'];far=bpy.data.collections['GT_R04_LAYERED_DISTANCE'];m={key:bpy.data.materials[name] for key,name in [('bark','R04_WOOL_GROWTH_FOLDS'),('moss','R04_SOFT_OLIVE_CUSHION'),('mosslight','R04_SUNLIT_MOSS_TIPS'),('leaf','R04_SAGE_FELT_LEAF'),('deep','R04_BLUEGREEN_FELT_LEAF')]};base=bpy.data.objects['ANCHOR_OAK_BASE'].location.copy()
# Existing mid trees become genuinely middle-distance; nonuniform depth and scale.
centers=[(-7,12,1.5),(-4.8,14,1.7),(-2.7,16,1.4),(.1,18,1.6),(5.8,13,1.9),(8,16,1.8),(10,20,1.7),(-9,21,2.0),(-5.5,23,2.0),(4,24,2.1)]
for i,(x,y,size) in enumerate(centers):
 factor=[.65,.60,.74,.58,.72,.62,.7,.57,.62,.68][i];origin=Vector((x,y,0));dest=origin+Vector((0,5+(i%3)*2,0))
 for o in list(far.objects):
  belongs=o.name.startswith(('R04_MID_WOOD_%02d'%i,'R04_MID_BRANCH_%02d_'%i,'R04_MID_UNIFIED_CROWN_%02d'%i,'R04_MID_LEAF_%02d_'%i))
  if not belongs:continue
  if o.type=='MESH' and o.name.startswith('R04_MID_LEAF_'):
   o.location=dest+(o.location-origin)*factor;o.scale*=factor
  else:
   # Meshes/tubes carry real-world coordinates; translate in world space.
   if o.type=='MESH':
    inv=o.matrix_world.inverted()
    for v in o.data.vertices:v.co=inv@(dest+(o.matrix_world@v.co-origin)*factor)
# Hero canopy frames at visible branch shoulders, not solely above the camera.
for o in list(dress.objects):
 if o.name.startswith(('R04_HERO_CROWN_','R04_CANOPY_LEAF_','R04_canopy_felt_edge_')):o.location.z-=1.15
# Attach more substantial softly curled leaf clusters to those branches.
protos=[bpy.data.objects['R04_KIT_LEAF_%d'%i] for i in range(3)]
for i,(dx,dy,z) in enumerate([(-3.15,-.1,3.9),(-2.5,-.4,4.25),(-1.6,-.6,4.05),(2.8,-.3,3.8),(3.8,.5,4.0)]):
 center=base+Vector((dx,dy,z))
 for j in range(70):
  a=r.random()*math.tau;q=center+Vector((r.gauss(0,.43),r.gauss(0,.25),r.gauss(0,.28)));sz=r.uniform(.25,.40);c.instance(protos[(j+i)%3],'R04_SHOULDER_LEAF_%02d_%03d'%(i,j),q,(sz*.85,sz,sz),(r.uniform(.2,1.2),r.uniform(-.4,.4),a),dress)
# Recessed broad wool folds replace smooth rubbery faces without floating strips.
oak=bpy.data.objects['OAK_MAIN']
for v in oak.data.vertices:
 p=v.co-base;z=p.z
 if .15<z<3.0:
  weight=min(1,(z-.15)/.5)*min(1,(3-z)/.6);a=math.atan2(p.y,p.x);rad=math.hypot(p.x,p.y)
  if rad<1.45:
   d=.035*math.sin(a*11+.28*math.sin(z*1.4))*weight;v.co.x+=math.cos(a)*d;v.co.y+=math.sin(a)*d
bpy.context.view_layer.update();oak.data.calc_loop_triangles();bt=BVHTree.FromPolygons([oak.matrix_world@v.co for v in oak.data.vertices],[t.vertices for t in oak.data.loop_triangles],all_triangles=True)
# Replace circular root pads by three connected irregular wool strips.
for o in hero.objects:
 if o.name.startswith(('R04_MOSS_ROOT_CUSHION_','R04_moss_root_loops_')):o.hide_render=True
for strip,(dx,dy) in enumerate([(-2.6,-1.9),(-.15,-2.1),(2.3,-1.3)]):
 pieces=[]
 for j in range(12):
  t=.22+j*.052;point=base+Vector((dx*t,dy*t,0));hit,n,_,_=bt.ray_cast(point+Vector((0,0,4)),Vector((0,0,-1)))
  if hit is None:continue
  sz=r.uniform(.17,.28);o=c.ell('R04_moss_strip_part',hit+n*.015,(sz,sz*.9,sz*.42),m['moss'],hero,strip*30+j,3);o.rotation_euler=n.to_track_quat('Z','Y').to_euler();pieces.append(o)
 if pieces:
  mos=c.fuse(pieces,'R04_ROOT_UNIFIED_MOSS_STRIP_%d'%strip,.024);c.fibers('R04_root_connected_wool_%d'%strip,mos,m['mosslight'],hero,2200,.022,.0012,510420+strip)
# Ground at shot distance: larger mottling and lower relief, short anchored fibers.
ground=bpy.data.objects['SURF_CLEARING'];mat=ground.data.materials[0];n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF');tc=n.get('REST_OBJECT_COORDINATES')
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=70;noise.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],noise.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.4;bump.inputs['Distance'].default_value=.009;l.new(noise.outputs['Fac'],bump.inputs['Height']);old=p.inputs['Normal'].links[0].from_socket;l.new(old,bump.inputs['Normal']);l.new(bump.outputs[0],p.inputs['Normal'])
# Curled loops lie flush on broad ground regions; no disks/chips or obstacle carpet.
data=bpy.data.curves.new('R04_matted_ground_short_wool','CURVE');data.dimensions='3D';data.bevel_depth=.0014;data.bevel_resolution=0
for i in range(14000):
 x=r.uniform(-5,5);y=r.uniform(-3,8)
 if -1.6<x<1.5 and -.85<y<1.55:continue
 center=.25+1.1*math.sin(y*.36)
 if abs(x-center)<.62 and r.random()>.22:continue
 length=r.uniform(.014,.034);a=r.random()*math.tau;sp=data.splines.new('POLY');sp.points.add(3)
 for j,pt in enumerate(sp.points):
  t=j/3;pt.co=(x+math.cos(a)*length*t,y+math.sin(a)*length*t,.009+.007*math.sin(math.pi*t),1)
o=bpy.data.objects.new('R04_CONTINUOUS_GROUND_MATTED_WOOL',data);dress.objects.link(o);data.materials.append(m['mosslight'])
# Front accents make a real foreground/quiet-clearing transition.
for i,(x,y,sz) in enumerate([(-3.5,-1.8,.38),(-2.9,-.5,.23),(3.2,-1.5,.35),(3.8,.3,.30),(-2.9,2.2,.25),(2.6,2.3,.23),(-3.5,4.8,.3)]):
 for j in range(14):
  a=j*2.399;size=sz*r.uniform(.7,1.2);c.instance(protos[j%3],'R04_EDGE_SPRIG_%02d_%02d'%(i,j),(x+r.uniform(-.15,.15),y+r.uniform(-.12,.12),.025),(size*.75,size,size),(.55+r.uniform(0,.4),0,a),dress)
s['r04_correction_1']='reduced and deepened mid crowns; lowered hero canopy; coherent root moss; matted ground wool'
bpy.ops.wm.save_as_mainfile(filepath=str(E),compress=True)
(P/'correction_1.json').write_text(json.dumps({'environment_sha256':hashlib.sha256(E.read_bytes()).hexdigest(),'changes':s['r04_correction_1'],'paid_requests':0},indent=2))
