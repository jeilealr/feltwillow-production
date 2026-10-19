"""Bounded reference-inspired r04 from r03. Sole environment writer; no services."""
import bpy,sys,math,random,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'blender';P=A/'renders/scene05_environment_r04';sys.path.insert(0,str(A/'scripts'));import craft_scene05_r04 as c
R=random.Random(510400);E=A/'assets/environments/great_tree/great_tree_environment_r04.blend';S=A/'scenes/lion_and_mouse_v6/s05_environment_r04.blend'
assert not E.exists() and not S.exists(),'Next revision is occupied'
bpy.ops.wm.open_mainfile(filepath=str(A/'assets/environments/great_tree/great_tree_environment_r03.blend'),use_scripts=False);s=bpy.context.scene
env=bpy.data.collections['ENV_GreatTree_R02'];hero=c.collection('GT_R04_HERO_CRAFT',env);dress=c.collection('GT_R04_AUTHORED_PLANTS',env);far=c.collection('GT_R04_LAYERED_DISTANCE',env);sky=c.collection('GT_R04_DUSK_SKY',env);templates=c.collection('GT_R04_KIT_TEMPLATES',env);templates.hide_render=True;templates.hide_viewport=True
lights=c.collection('GT_DUSK_LIGHT_R04',s.collection);cams=c.collection('GT_CAMERAS_R04',s.collection)
# Preserve but explicitly retire previous failed dressing; all original inputs remain on disk.
for name in ['GT_FELT_DRESSING','GT_FAR_RELIEF','GT_SKY_CLOUDS','GT_R03_CLUSTERED_UNDERSTORY','GT_R03_DISTANCE_SKY','GT_R03_HERO_REFINEMENT','GT_DUSK_LIGHT_R02']:
 bpy.data.collections[name].hide_render=True
for o in bpy.data.collections['GT_PERMANENT_HERO'].objects:o.hide_render=True
m=c.palette();base=bpy.data.objects['ANCHOR_OAK_BASE'].location.copy()
source=bpy.data.objects['OAK_MAIN'];source.name='OAK_MAIN_SOURCE_R03';source.hide_render=True
def loc(x,y,z):return tuple(base+Vector((x,y,z)))
parts=[c.tube('GT_R04_trunk', [loc(0,0,.12),loc(-.12,.05,.8),loc(.02,.08,2.0),loc(.19,.18,3.5),loc(.05,.30,5.5),loc(.36,.5,7)],[1.2,.98,.76,.66,.50,.29],m['bark'],hero,9)]
rootdefs=[(-3.25,-2.15,.36),(-1.8,-2.65,.44),(-.25,-2.4,.47),(1.75,-2.10,.43),(3.2,-.8,.34),(2.7,1.5,.30),(-2.4,1.8,.31)]
for i,(x,y,r) in enumerate(rootdefs):
 parts.append(c.tube('GT_R04_buttress_%02d'%i,[loc(x*.03,y*.03,.95),loc(x*.28,y*.25,.46),loc(x*.65,y*.63,.16),loc(x,y,.025)],[r*1.45,r,r*.65,.018],m['bark'],hero,5))
branches=[(-3.8,.25,5.2),(-2.4,.8,6.2),(2.7,.6,5.4),(4.0,1.1,4.8)]
for i,(x,y,z) in enumerate(branches):
 parts.append(c.tube('GT_R04_branch_%d'%i,[loc(.10,.12,2.8),loc(x*.36,y*.3,3.6),loc(x*.70,y*.7,z-.3),loc(x,y,z)],[.50,.33,.19,.065],m['bark'],hero))
 for j in [-1,1]:parts.append(c.tube('GT_R04_branch_tip_%d_%d'%(i,j),[loc(x*.67,y*.7,z-.35),loc(x*.85+j*.25,y*.75+.2,z+.2),loc(x+j*.5,y+.35,z+.55)],[.17,.09,.025],m['bark'],hero))
oak=c.fuse(parts,'OAK_MAIN',.035);oak['revision']='R04 continuous compressed-wool tree';oak['role']='hero fixed landmark; roots not substituted for Leo forepaw'
c.fibers('R04_bark_short_edge_wool',oak,m['bark'],hero,5500,.016,.0012,510401)
# Preserve the safe root and support coordinate system; revise appearance, not contact function.
approach=bpy.data.objects['ROOT_APPROACH_A'];approach.hide_render=False;approach.data.materials.clear();approach.data.materials.append(m['bark'])
for col in list(approach.users_collection):col.objects.unlink(approach)
hero.objects.link(approach)
for name in ['SURF_CLEARING','SURF_PATH']:
 o=bpy.data.objects[name]
 if name=='SURF_CLEARING':o.data.materials.clear();o.data.materials.append(c.ground_material(m['path'],m['moss']));o.hide_render=False
 else:o.hide_render=True;o['r04_role']='legacy path support retained; continuous ground shader supplies visible path'
def tree_bvh(o):
 bpy.context.view_layer.update();o.data.calc_loop_triangles();return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[t.vertices for t in o.data.loop_triangles],all_triangles=True)
bt=tree_bvh(oak)
# Coherent root-shoulder cushions. Larger shared masses replace flat flakes.
for i,(x,y,t,sz) in enumerate([(-2.3,-1.4,.2,.42),(-1.7,-1.0,.3,.48),(-1.1,-.65,.4,.38),(-.55,-1.6,.2,.37),(.2,-1.15,.4,.45),(.6,-.6,.7,.35),(1.4,-1.2,.3,.5),(2.3,-.7,.2,.37),(-.65,.5,.9,.36),(.7,.3,1.1,.32)]):
 hit,n,_,_=bt.ray_cast(base+Vector((x,y,4)),Vector((0,0,-1)))
 if hit is None:continue
 cushion=c.ell('R04_MOSS_ROOT_CUSHION_%02d'%i,hit+n*.025,(sz,sz*.73,sz*.28),m['mosslight'] if i%4==0 else m['moss'],hero,i,4);cushion.rotation_euler=n.to_track_quat('Z','Y').to_euler();c.fibers('R04_moss_root_loops_%02d'%i,cushion,m['mosslight'],hero,550,.020,.0013,510450+i)
# Rocks: preserve landmark IDs while replacing only candidate surface geometry.
for i,name in enumerate(['ROCK_RIGHT','STONE_CENTER_LEFT']):
 old=bpy.data.objects[name];p=old.location.copy();dims=old.dimensions.copy();old.name=name+'_SOURCE_R03';old.hide_render=True
 ob=c.ell(name,p,(dims.x*.50,dims.y*.53,dims.z*.55),m['rock'],hero,12+i,4);c.fibers('R04_%s_heather_outline'%name,ob,m['rock'],hero,1800,.013,.001,510480+i)
# Authored banks, clustered without placing vegetation into the actor corridor.
route=[(-2.4,-1.9),(-1.2,-1.8),(.15,-1.6),(.62,-1.05),(.86,-.60),(.91,-.20),(1.45,-.65)]
def reserved(x,y):
 if -1.6<x<1.45 and -.85<y<1.55:return True
 for a,b in zip(route,route[1:]):
  d=Vector((b[0]-a[0],b[1]-a[1]));q=Vector((x-a[0],y-a[1]));t=max(0,min(1,q.dot(d)/d.length_squared))
  if (q-d*t).length<.30:return True
 return False
def cushion_group(name,p,sz,seed):
 r=random.Random(seed);objects=[]
 for j in range(4):
  q=Vector(p)+Vector((r.uniform(-.35,.35)*sz,r.uniform(-.28,.28)*sz,0));objects.append(c.ell(name+'_part',q,(sz*r.uniform(.55,.85),sz*r.uniform(.5,.7),sz*r.uniform(.15,.28)),m['moss'] if j%3 else m['mosslight'],dress,j+seed,3))
 ob=c.fuse(objects,name,.028 if sz<.7 else .04);c.fibers(name+'_wool_edge',ob,m['mosslight'],dress,900,.024,.0013,seed);return ob
for i,(x,y,z,sz) in enumerate([(-3.8,-.8,.08,.85),(-3.3,1.0,.08,.7),(-4.3,3.2,.08,.8),(-2.9,4.5,.07,.7),(3.6,-1.0,.06,.7),(4.5,1.1,.09,.95),(3.4,3.4,.1,.62),(-1.2,6.6,.07,.6)]):cushion_group('R04_BANK_MOSS_%02d'%i,(x,y,z),sz,510500+i)
protos=[c.leaf_proto('R04_KIT_LEAF_%d'%i,m[['leaf','leafgold','deep'][i]],templates,i) for i in range(3)]
# Plant rosettes have thick round leaves, small stems and measured exclusion.
def plant(name,p,sz,leaves=9):
 for j in range(leaves):
  a=j*2.399+R.uniform(-.2,.2);q=Vector(p)+Vector((math.sin(a)*.025,math.cos(a)*.025,0));scale=sz*R.uniform(.7,1.15)
  c.instance(protos[j%3],name+'_leaf_%02d'%j,q,(scale*.65,scale,scale),(R.uniform(.25,.9),R.uniform(-.2,.2),a),dress)
for i,(x,y,sz) in enumerate([(-3.7,-1.1,.42),(-3.0,1.25,.32),(-4,3.2,.4),(3.6,-.9,.40),(4.5,1.0,.55),(3.4,3.2,.33),(-2.8,5.0,.35),(.35,3.5,.22),(3.2,4.0,.25),(-5.0,6.0,.35)]):plant('R04_FOREGROUND_SPRIG_%02d'%i,(x,y,.04),sz,11)
# Tufts: short curved folded blades, batched mesh; clumps authored around banks.
vs=[];fs=[];ids=[]
regions=[(-3.3,0,.9,1.8),(3.6,.5,.8,2.0),(-3.0,4.2,1.0,1.0),(1.4,4.0,1.3,.8),(-5,8,1.2,1.5),(5.4,6,1.4,1.4)]
for i in range(2100):
 x,y,wx,wy=regions[i%len(regions)];x+=R.gauss(0,wx*.55);y+=R.gauss(0,wy*.55)
 if reserved(x,y):continue
 for j in range(R.randrange(4,8)):
  a=R.random()*math.tau;ht=R.uniform(.035,.12);w=R.uniform(.006,.013);start=len(vs)
  for k in range(6):
   t=k/5;width=w*math.sin(math.pi*(.08+.92*t))**.6;bend=.05*t*t;z=ht*math.sin(t*1.3)
   for u in [-1,0,1]:vs.append((x+math.cos(a)*bend-math.sin(a)*width*u,y+math.sin(a)*bend+math.cos(a)*width*u,z+.005+(.005 if u==0 else 0)))
  for k in range(5):
   for u in range(2):q=start+k*3+u;fs.append((q,q+1,q+4,q+3));ids.append(i%3)
tufts=c.mesh('R04_SHORT_CLUSTERED_WOOL_TUFTS',vs,fs,m['moss'],dress);tufts.data.materials.append(m['leaf']);tufts.data.materials.append(m['mosslight'])
for f,i in zip(tufts.data.polygons,ids):f.material_index=i
# Canopy: continuous wool crown cushions + a restrained skirt of rounded leaves.
for i,(dx,dy,z) in enumerate(branches):
 for j in range(4):
  center=base+Vector((dx+R.uniform(-.65,.65),dy+R.uniform(-.4,.4),z+R.uniform(-.1,.5)));sc=R.uniform(.65,.95);ob=c.ell('R04_HERO_CROWN_%02d_%02d'%(i,j),center,(sc,sc*.75,sc*.55),m['leaf'] if j%2 else m['leafgold'],dress,i*10+j,4);c.fibers('R04_canopy_felt_edge_%d_%d'%(i,j),ob,m['leaf'],dress,500,.023,.0013,510600+i*10+j)
  for k in range(26):
   a=R.random()*math.tau;q=center+Vector((math.cos(a)*sc*.85,R.uniform(-.6,.3)*sc,math.sin(a)*sc*.4-.15));size=R.uniform(.20,.32);c.instance(protos[k%2],'R04_CANOPY_LEAF_%02d_%02d_%02d'%(i,j,k),q,(size*.8,size,size),(R.uniform(-.7,.7),R.uniform(-.5,.5),a),dress)
# Midground woodland: grouped branching trunks and irregular unified crowns, no rows.
for i,(x,y,size) in enumerate([(-7,12,1.5),(-4.8,14,1.7),(-2.7,16,1.4),(.1,18,1.6),(5.8,13,1.9),(8,16,1.8),(10,20,1.7),(-9,21,2.0),(-5.5,23,2.0),(4,24,2.1)]):
 height=size*1.65;wood=[c.tube('R04_MID_WOOD_%02d'%i,[(x,y,0),(x+.1,y,height*.55),(x-.1,y+.1,height)],[.18*size,.12*size,.04],m['bark'],far)]
 crowns=[]
 for j in range(4):
  a=j*math.tau/4+.4;dx=math.cos(a)*size*.5;dy=math.sin(a)*size*.4
  wood.append(c.tube('R04_MID_BRANCH_%02d_%d'%(i,j),[(x,y,height*.5),(x+dx*.6,y+dy*.6,height*.8),(x+dx,y+dy,height*1.08)],[.10*size,.06*size,.02],m['bark'],far))
  crowns.append(c.ell('R04_crown_part',(x+dx,y+dy,height+R.uniform(-.15,.3)),(size*.62,size*.55,size*.58),m['deep'] if i%3==0 else m['leaf'],far,i*3+j,3))
 crown=c.fuse(crowns,'R04_MID_UNIFIED_CROWN_%02d'%i,.075)
 # Few front-edge leafy tabs create crafted scale instead of extra ball lobes.
 for j in range(20):
  q=(x+R.uniform(-.7,.7)*size,y-size*.5,height+R.uniform(-.45,.6)*size);sc=R.uniform(.19,.30)*size;c.instance(protos[(j+i)%3],'R04_MID_LEAF_%02d_%02d'%(i,j),q,(sc*.7,sc,sc),(.6,0,R.uniform(-2,2)),far)
# Stream: retain original actual ribbon and banks; new low-gloss textile reflection.
wm=c.mat('R04_STREAM_LAVENDER_SILK_FELT','path',['686F88','B2A0A2','D8AE84']);wm.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.48
water=bpy.data.objects['WATER_STREAM_CLOTH'];water.hide_render=False;water.data.materials.clear();water.data.materials.append(wm)
for o in bpy.data.objects:
 if o.name.startswith('STREAM_bank_stone_'):o.data.materials.clear();o.data.materials.append(m['rock'])
# Distance uses fixed shallow silhouettes, intentionally soft-emissive (no double lighting).
def emission(name,hx,strength=1):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*c.rgb(hx),1);em.inputs[1].default_value=strength;l.new(em.outputs[0],out.inputs[0]);return mat
for layer,(y,color,zbase) in enumerate([(65,'8B8098',2.9),(49,'696E86',2.25),(36,'536975',1.8)]):
 vs=[]
 for j in range(121):
  x=-60+j;z=zbase+1.2*math.sin(x*.12+layer*.8)+.48*math.sin(x*.31+layer);z+=.06*math.sin(x*7)
  vs.extend([(x,y,-4),(x,y,z)])
 ob=c.mesh('R04_FIXED_FAR_WOODLAND_RIDGE_%d'%layer,vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(120)],emission('R04_distance_felt_%d'%layer,color),far);ob['camera_envelope']='fixed relief, wide/medium plus +/- .25 BU; no reverse view'
# Shader sky: luminous near horizon, lavender upper dome, subtle elongated cloud wool.
skyMat=bpy.data.materials.new('R04_DUSK_CLOUD_WOOL_SKY');skyMat.use_nodes=True;n=skyMat.node_tree.nodes;l=skyMat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Generated'],sep.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(*c.rgb('F6B461'),1)
for pos,hx in [(.24,'F8A35D'),(.43,'CD8692'),(.70,'8B7CA1'),(1,'536B91')]:ramp.color_ramp.elements.new(pos).color=(*c.rgb(hx),1)
l.new(sep.outputs['Z'],ramp.inputs[0]);stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(2,1,15);l.new(tc.outputs['Generated'],stretch.inputs[0]);no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=4;no.inputs['Detail'].default_value=4;l.new(stretch.outputs[0],no.inputs[0]);mask=n.new('ShaderNodeValToRGB');mask.color_ramp.elements[0].position=.48;mask.color_ramp.elements[0].color=(0,0,0,1);mask.color_ramp.elements[1].position=.7;mask.color_ramp.elements[1].color=(.60,.60,.60,1);l.new(no.outputs['Fac'],mask.inputs[0]);mix=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],mix.inputs[0]);l.new(ramp.outputs[0],mix.inputs[1]);mix.inputs[2].default_value=(*c.rgb('998398'),1);l.new(mix.outputs[0],em.inputs[0]);em.inputs[1].default_value=1.15;l.new(em.outputs[0],out.inputs[0]);c.mesh('R04_FIXED_SKY',[(-110,99,-8),(110,99,-8),(110,99,45),(-110,99,45)],[(0,1,2,3)],skyMat,sky)
sun=emission('R04_SUNSET_WOOL_GLOW','FFDA89',1.5);o=c.ell('R04_FIXED_SUN',(-24,85,5),(2.1,.2,2.1),sun,sky,1,4)
# New views improve scale readability through framing. Actors are never rescaled.
wide=c.camera('CAM_S05_ESTABLISHING_R04',(-.6,-8.8,2.05),(.2,4.4,1.03),41,cams)
medium=c.camera('CAM_S05_MEDIUM_ACTOR_R04',(-.3,-4.8,1.55),(.15,.65,.45),49,cams)
contact=c.camera('CAM_S05_ROOT_CONTACT_R04',(-2.7,-3.8,1.1),(-.7,-.2,.16),51,cams)
for sign in [-1,1]:
 o=wide.copy();o.data=wide.data.copy();cams.objects.link(o);o.name='CAM_S05_ENVELOPE_'+('LEFT' if sign<0 else 'RIGHT')+'_R04';o.location.x+=sign*.25
c.area('R04_KEY_SUNSET',(-7,0,6),(1,4,1),2100,(1,.68,.37),4.5,lights);c.area('R04_COOL_SKY',(2,6,10),(0,3,0),850,(.58,.72,1),10,lights);c.area('R04_READABLE_FRONT',(-1,-4,5),(0,2,.4),200,(.86,.91,1),7,lights)
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.20,.25,.37,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.28
s.camera=wide;s.cycles.seed=510400;s.cycles.samples=40;s.cycles.device='CPU';s.cycles.use_denoising=True;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
s['environment_revision']='ENV_GreatTree_R04';s['design_mode']='reference_inspired';s['approval_status']='handmade-world candidate; needs visual review, not final';s['dressing_seed']=510400;s['unit_m_per_bu']=.2;s['ambient_state']='still_evening; no animation/clock reseed';s['story_prop_state']='no props'
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(E),compress=True)
(P/'build_inventory.json').write_text(json.dumps({'environment_sha256':hashlib.sha256(E.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((A/'assets/environments/great_tree/great_tree_environment_r03.blend').read_bytes()).hexdigest(),'mode':'reference_inspired','objects':len(bpy.data.objects),'faces':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),'seed':510400,'new_materials':[x.name for x in bpy.data.materials if x.name.startswith('R04_')],'old_hero_preserved':'OAK_MAIN_SOURCE_R03','library_collections':['ENV_GreatTree_R02','GT_DUSK_LIGHT_R04','GT_CAMERAS_R04']},indent=2))
# Preserve scoped proxy collection from shot, but assemble new library collections cleanly.
bpy.ops.wm.open_mainfile(filepath=str(A/'scenes/lion_and_mouse_v6/s05_environment_r03.blend'),use_scripts=False)
proxy=bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'];proxy.use_fake_user=True
for col in list(bpy.context.scene.collection.children):
 if col!=proxy:bpy.context.scene.collection.children.unlink(col)
with bpy.data.libraries.load(str(E),link=True) as (src,dst):dst.collections=['ENV_GreatTree_R02','GT_DUSK_LIGHT_R04','GT_CAMERAS_R04']
for col in dst.collections:bpy.context.scene.collection.children.link(col)
s=bpy.context.scene;s.camera=next(o for o in bpy.data.collections['GT_CAMERAS_R04'].objects if o.name.startswith('CAM_S05_ESTABLISHING_R04'))
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.20,.25,.37,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.28;s.render.resolution_x=1280;s.render.resolution_y=720;s.cycles.samples=40;s.cycles.seed=510400;s['design_mode']='reference_inspired';s['environment_library']=str(E.relative_to(ROOT));s['approval_status']='candidate only; no actor redesign';s['environment_revision']='ENV_GreatTree_R04'
# Orphaned old library datablocks can be removed safely only in this new in-memory assembly.
bpy.ops.outliner.orphans_purge(do_local_ids=False,do_linked_ids=True,do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(S),compress=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(S),compress=True)
print('R04_LIBRARY_AND_SHOT_SAVED',flush=True)
