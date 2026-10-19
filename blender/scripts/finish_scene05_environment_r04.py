"""Second and final bounded correction; integrated craft and forest layers."""
import bpy,sys,math,random,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];A=R/'blender';P=A/'renders/scene05_environment_r04';E=A/'assets/environments/great_tree/great_tree_environment_r04.blend';sys.path.insert(0,str(A/'scripts'));import craft_scene05_r04 as c
bpy.ops.wm.open_mainfile(filepath=str(E),use_scripts=False);s=bpy.context.scene;assert not s.get('r04_correction_2');r=random.Random(510430);hero=bpy.data.collections['GT_R04_HERO_CRAFT'];dress=bpy.data.collections['GT_R04_AUTHORED_PLANTS'];far=bpy.data.collections['GT_R04_LAYERED_DISTANCE'];base=bpy.data.objects['ANCHOR_OAK_BASE'].location.copy();m={key:bpy.data.materials[name] for key,name in [('bark','R04_WOOL_GROWTH_FOLDS'),('moss','R04_SOFT_OLIVE_CUSHION'),('mosslight','R04_SUNLIT_MOSS_TIPS'),('leaf','R04_SAGE_FELT_LEAF'),('deep','R04_BLUEGREEN_FELT_LEAF')]};protos=[bpy.data.objects['R04_KIT_LEAF_%d'%i] for i in range(3)]
# Vertical ray samples inside trunk hit upper branch surfaces: remove those false pads.
for o in hero.objects:
 if o.name.startswith(('R04_ROOT_UNIFIED_MOSS_STRIP_','R04_root_connected_wool_')):o.hide_render=True
oak=bpy.data.objects['OAK_MAIN'];oak.data.calc_loop_triangles();bt=BVHTree.FromPolygons([oak.matrix_world@v.co for v in oak.data.vertices],[t.vertices for t in oak.data.loop_triangles],all_triangles=True)
for strip,(dx,dy) in enumerate([(-3.0,-2.0),(-.15,-2.3),(2.6,-1.7)]):
 parts=[]
 for j in range(14):
  t=.44+j*.035;p=base+Vector((dx*t,dy*t,0));hit,n,_,_=bt.ray_cast(p+Vector((0,0,3)),Vector((0,0,-1)))
  if hit is None or hit.z>1.15:continue
  sz=r.uniform(.15,.24);o=c.ell('R04_moss_embedded_part',hit-n*.015,(sz,sz*.75,sz*.48),m['moss'],hero,strip*30+j,3);o.rotation_euler=n.to_track_quat('Z','Y').to_euler();parts.append(o)
 if parts:
  ob=c.fuse(parts,'R04_EMBEDDED_ROOT_MOSS_%d'%strip,.023);c.fibers('R04_embedded_moss_short_wool_%d'%strip,ob,m['mosslight'],hero,2200,.021,.0013,510440+strip)
# Keep just a few irregular woodland trunks as framing, not an orchard boundary.
for o in far.objects:
 if o.name.startswith(('R04_MID_WOOD_','R04_MID_BRANCH_','R04_MID_UNIFIED_CROWN_','R04_MID_LEAF_')):
  # last/first groups: left/right framing; middle row retired in this candidate.
  if not any(o.name.startswith(prefix+idx) for prefix in ['R04_MID_WOOD_','R04_MID_BRANCH_','R04_MID_UNIFIED_CROWN_','R04_MID_LEAF_'] for idx in ['00','04','06','07']):o.hide_render=True
# Authored thickets form a continuous midground with asymmetry and small clear gaps.
regions=[(-6.5,7.5,1.0),(-4.3,8.4,.8),(-2.8,9.8,.85),(-.8,11.3,1.0),(1.3,12.2,.9),(5.5,8.8,1.15),(7.2,11.8,1.2),(3.4,13,1.0),(-6,14,1.4),(-1,17,1.3),(6,18,1.5),(-4.1,4.8,.55)]
for i,(x,y,sz) in enumerate(regions):
 parts=[]
 for j in range(5):
  a=j*2.399;q=Vector((x+math.cos(a)*sz*.38,y+math.sin(a)*sz*.3,sz*.34+r.uniform(-.06,.08)));parts.append(c.ell('R04_thicket_mass',q,(sz*.52,sz*.45,sz*.40),m['deep'] if i%4==0 else m['leaf'],dress,i*10+j,3))
 ob=c.fuse(parts,'R04_AUTHORED_THICKET_%02d'%i,.045)
 for j in range(55 if y<13 else 25):
  a=r.random()*math.tau;rr=r.uniform(.35,.85)*sz;q=(x+math.cos(a)*rr,y+math.sin(a)*sz*.5,sz*.45+r.uniform(-.20,.22)*sz);length=r.uniform(.15,.26)*sz
  c.instance(protos[(j+i)%3],'R04_THICKET_LEAF_%02d_%03d'%(i,j),q,(length*.75,length,length),(.4+r.uniform(0,.6),r.uniform(-.3,.3),a),dress)
# Low foreground mats with organically lobed edges, not scattered coin forms.
for i,(x,y,sz) in enumerate([(-2.85,.6,.48),(2.9,1.5,.55),(-3.25,3.0,.65),(3.3,3.8,.5)]):
 parts=[]
 for j in range(4):
  a=j*2.399;parts.append(c.ell('R04_matted_bank_part',(x+math.cos(a)*sz*.25,y+math.sin(a)*sz*.3,.025),(sz*.72,sz*.55,.07),m['moss'],dress,i*10+j,3))
 ob=c.fuse(parts,'R04_INTEGRATED_CLEARING_EDGE_%d'%i,.023);c.fibers('R04_matted_edge_wool_%d'%i,ob,m['mosslight'],dress,1500,.021,.0013,510460+i)
rock=bpy.data.objects['ROCK_RIGHT'];rock.location.z-=.055;rock.rotation_euler.z=.20
# Layered distant woodland scallops and occasional pines, shallow real silhouettes.
for layer,(y,hx,zbase) in enumerate([(60,'7C7B93',2.2),(45,'5B6F80',1.5),(31,'415B61',.4)]):
 mat=bpy.data.materials.new('R04_soft_far_woodland_%d'%layer);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;out=n.get('Material Output');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*c.rgb(hx),1);em.inputs[1].default_value=.9;l.new(em.outputs[0],out.inputs[0]);vs=[];fs=[]
 for j in range(241):
  x=-40+j/3;z=zbase+.45*math.sin(x*.31+layer)+.6*math.sin(x*.13+layer)+.22*math.sin(x*2.9+.6*math.sin(x*1.7))+.12*math.sin(x*5.7)
  vs.extend([(x,y,-2),(x,y,z)])
 for j in range(240):fs.append((j*2,j*2+1,j*2+3,j*2+2))
 c.mesh('R04_LAYERED_WOODLAND_CUTOUT_%d'%layer,vs,fs,mat,far)
 for j in range(7):
  x=-20+j*6.1+layer*1.7;z=zbase+.45*math.sin(x*.31+layer)+.6*math.sin(x*.13+layer);height=r.uniform(.75,1.65);width=height*.3;vs=[(x,y-.05,z+height)]
  for k in range(1,15):
   t=k/14;xx=x+width*t*(1 if k%2 else .70);vs.append((xx,y-.05,z+height*(1-t)))
  vs.append((x-width,y-.05,z))
  for k in range(13,0,-1):
   t=k/14;vs.append((x-width*t*(1 if k%2 else .7),y-.05,z+height*(1-t)))
  c.mesh('R04_FAR_FELT_PINE_%d_%d'%(layer,j),vs,[tuple(range(len(vs)))],mat,far)
# Break long uniform cloud streaks into low-contrast banks.
mat=bpy.data.materials['R04_DUSK_CLOUD_WOOL_SKY'];n=mat.node_tree.nodes
for node in n:
 if node.type=='VECT_MATH' and node.operation=='MULTIPLY':node.inputs[1].default_value=(4,1,7)
 if node.type=='TEX_NOISE':node.inputs['Distortion'].default_value=.4;node.inputs['Detail'].default_value=5
# Slight warm rim/readable cool face, without washing all fibers in amber.
bpy.data.objects['R04_KEY_SUNSET'].data.energy=1900;bpy.data.objects['R04_COOL_SKY'].data.energy=1050
s['r04_correction_2']='removed falsely projected moss dots; layered thickets and far woodland; integrated clearing edges; retained actor lane'
bpy.ops.wm.save_as_mainfile(filepath=str(E),compress=True)
(P/'correction_2.json').write_text(json.dumps({'environment_sha256':hashlib.sha256(E.read_bytes()).hexdigest(),'changes':s['r04_correction_2'],'correction_budget_exhausted':True,'paid_requests':0},indent=2))
