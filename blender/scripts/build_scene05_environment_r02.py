"""Persistent Great Tree r02: native felt kit, library, linked S05 study.
No provider calls. See scene05_environment_contract.md before changing sources.
"""
import bpy,math,random,json,sys,hashlib,time
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender';sys.path.insert(0,str(AREA/'scripts'))
import build as h
P=AREA/'renders/scene05_environment_r02';ENV=AREA/'assets/environments/great_tree/great_tree_environment_r02.blend';SHOT=AREA/'scenes/lion_and_mouse_v6/s05_environment_r02.blend';R=random.Random(18102651)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;h.settings();s.unit_settings.system='METRIC';s.unit_settings.scale_length=.2;s.cycles.seed=18102651;s.render.fps=24
ENVROOT=bpy.data.collections.new('ENV_GreatTree_R02');s.collection.children.link(ENVROOT)
def col(name,parent=ENVROOT):
 c=bpy.data.collections.new(name);parent.children.link(c);return c
HERO=col('GT_PERMANENT_HERO');GROUND=col('GT_GROUND_PATH');DRESS=col('GT_FELT_DRESSING');FAR=col('GT_FAR_RELIEF');SKY=col('GT_SKY_CLOUDS');ANCHORS=col('GT_SURFACES_ANCHORS');TEMPLATES=col('GT_KIT_TEMPLATES');TEMPLATES.hide_render=True;TEMPLATES.hide_viewport=True
LIGHTS=bpy.data.collections.new('GT_DUSK_LIGHT_R02');s.collection.children.link(LIGHTS)
CAMS=bpy.data.collections.new('GT_CAMERAS_R02');s.collection.children.link(CAMS)
def active(c):h.COL=c
active(CAMS);wide=h.camera('CAM_S05_GEOGRAPHY_WIDE_R02',(0,-8,1.55),(0,4,.725),45);bpy.context.view_layer.update();wide.data.sensor_width=36;wide.data.sensor_fit='HORIZONTAL'
def ground(u,v,z=0):
 direction=wide.rotation_euler.to_matrix()@Vector(((u-.5)*.8,(.5-v)*.45,-1));t=(z-wide.location.z)/direction.z;return wide.location+direction*t

def linear(v):return v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4
def rgb(hex):return tuple(linear(int(hex[i:i+2],16)/255) for i in (0,2,4))
def felt(name,color,scale=100,bump=.15,bark=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb(color),1);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb(color),1);p.inputs['Roughness'].default_value=.94;p.inputs['Sheen Weight'].default_value=.28;p.inputs['Specular IOR Level'].default_value=.2
 coord=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3;l.new(coord.outputs['Object'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.80 for x in rgb(color)],1);ramp.color_ramp.elements[1].color=(*[x*1.16 for x in rgb(color)],1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;b.inputs['Distance'].default_value=.008;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 if bark:
  mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(5,5,.55);l.new(coord.outputs['Object'],mapping.inputs[0]);groove=n.new('ShaderNodeTexNoise');groove.inputs['Scale'].default_value=3.4;groove.inputs['Detail'].default_value=3;groove.inputs['Roughness'].default_value=.72;l.new(mapping.outputs[0],groove.inputs['Vector']);bb=n.new('ShaderNodeBump');bb.inputs['Strength'].default_value=.42;bb.inputs['Distance'].default_value=.045;l.new(groove.outputs['Fac'],bb.inputs['Height']);l.new(b.outputs[0],bb.inputs['Normal']);l.new(bb.outputs[0],p.inputs['Normal'])
 return m
bark=felt('GT_wool_bark_umber','79543C',90,.20,True);ridge=felt('GT_wool_bark_ridge','94704B',180,.20);dark=felt('GT_bark_groove','513B30',90,.18)
grass=felt('GT_olive_grass_felt','737C3F',150,.27);moss=felt('GT_moss_wool','7D873D',180,.30);mosslight=felt('GT_moss_golden_tips','A09B4B',200,.25);leaf=felt('GT_leaf_olive','667842',170,.19);leaflight=felt('GT_leaf_sage','8A9255',180,.17);dirt=felt('GT_path_wool_ochre','957052',220,.24);stone=felt('GT_stone_grey_taupe','8B8478',130,.30);water=felt('GT_stream_cloth','9699AA',50,.07)
# Reuse the approved local extracted wool height, without importing its honey color.
for m in (grass,moss,stone,leaf,leaflight,ridge):
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(AREA/'assets/materials/leo_felt_patina_trial/height.png'),check_existing=True);tex.image.colorspace_settings.name='Non-Color';tex.projection='BOX';tex.projection_blend=.25;coord=next(x for x in n if x.type=='TEX_COORD');scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=4;l.new(coord.outputs['Object'],scale.inputs[0]);l.new(scale.outputs[0],tex.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.15;b.inputs['Distance'].default_value=.003;l.new(tex.outputs[0],b.inputs['Height']);old=p.inputs['Normal'].links[0].from_socket;l.new(old,b.inputs['Normal']);l.new(b.outputs[0],p.inputs['Normal'])

def mesh(name,verts,faces,material,c):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);c.objects.link(ob)
 if material:me.materials.append(material)
 for p in me.polygons:p.use_smooth=True
 return ob

def anchor(name,position,role):
 ob=bpy.data.objects.new(name,None);ANCHORS.objects.link(ob);ob.location=position;ob.empty_display_type='SPHERE';ob.empty_display_size=.06;ob.hide_render=True;ob['role']=role;return ob
anchors={}
for name,u,v in [('OAK_BASE',.69,.59),('STONE_CENTER_LEFT',.26,.69),('ROCK_RIGHT',.94,.67),('MOUND_LEFT',.055,.66),('ROOT_APPROACH_START',.03,.67),('ROOT_APPROACH_TIP',.49,.86),('STREAM_GLIMPSE',.14,.53)]:anchors[name]=anchor('ANCHOR_'+name,ground(u,v),'fixed geography, inferred depth; observed plate target').location.copy()
base=anchors['OAK_BASE'];active(GROUND)
# Continuous support sheet: central acting lane stays exactly level.
verts=[];faces=[];nx=100;ny=100
for j in range(ny+1):
 y=-10+j*50/ny
 for i in range(nx+1):
  x=-24+i*48/nx;z=-.022+.018*math.sin(x*.55)*math.sin(y*.42)
  if -2.8<x<2.6 and -2.2<y<2.0:z=0
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
terrain=mesh('SURF_CLEARING',verts,faces,grass,GROUND);terrain['support']='walkable continuous ground, central reserved lane z0'
# Ribbon path from foreground to the left-stream approach.
path_rows=[(-8,3,4),(-3,1.8,2.1),(-1,1.2,1.4),(1,.55,.9),(3,-.4,.55),(5,-2.1,.40),(8,-3.7,.25),(12,-5.4,.20)]
verts=[]
for y,x,w in path_rows:verts.extend([(x-w,y,.009),(x+w,y,.009)])
path=mesh('SURF_PATH',verts,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(path_rows)-1)],dirt,GROUND);path['support']='shallow path overlay over continuous visible ground'
def path_width(y):
 for a,b in zip(path_rows,path_rows[1:]):
  if a[0]<=y<=b[0]:t=(y-a[0])/(b[0]-a[0]);return a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t
 return (-5.4,.32)
# Permanent trunk/root structure; join/remesh only the structural wood.
active(HERO);wood=[]
wood.append(h.curve('OAK_trunk_core',[base+Vector((0,0,.1)),base+Vector((-.08,.12,1)),base+Vector((.05,.05,2.3)),base+Vector((.20,.15,3.7)),base+Vector((.15,.4,5.5))],.72,bark,radii=[1.65,1.15,1,.88,.65]))
roots=[]
for i,(dx,dy,size) in enumerate([(-3.5,-1.7,.43),(-2.3,-2.2,.48),(-.6,-3,.50),(1.2,-2.8,.53),(3,-1.6,.42),(3,.9,.36),(-2.4,1.1,.38)]):
 pts=[base+Vector((dx*.03,dy*.03,.85)),base+Vector((dx*.33,dy*.33,.32)),base+Vector((dx*.72,dy*.72,.11)),base+Vector((dx,dy,.018))]
 ob=h.curve('OAK_structural_root_%02d'%i,pts,size,bark,radii=[1.25,1,.55,.06]);wood.append(ob);roots.append((pts,size))
branches=[(-4.1,-.1,3.65),(-2.2,.7,4.5),(2.6,.25,4.2),(4.5,.8,3.8)]
for i,(dx,dy,z) in enumerate(branches):
 pts=[base+Vector((.02,0,3.05)),base+Vector((dx*.45,dy*.4,z-.18)),base+Vector((dx,dy,z))];wood.append(h.curve('OAK_structural_branch_%02d'%i,pts,.36,bark,radii=[1.7,.85,.22]))
# Continuous organic wood silhouette, unlike the disconnected earlier blockout.
bpy.ops.object.select_all(action='DESELECT')
for ob in wood:ob.data.use_fill_caps=True;ob.select_set(True)
bpy.context.view_layer.objects.active=wood[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();oak=bpy.context.object;oak.name='OAK_MAIN'
rem=oak.modifiers.new('Fused structural felt wood','REMESH');rem.mode='VOXEL';rem.voxel_size=.045;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
sm=oak.modifiers.new('Compressed hand-felt smoothing','SMOOTH');sm.factor=.75;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
# Closed structural wood must intersect horizontal center rays at every height.
oak.data.calc_loop_triangles();woodtree=BVHTree.FromPolygons([v.co for v in oak.data.vertices],[t.vertices for t in oak.data.loop_triangles],all_triangles=True)
trunk_sections=[]
for j in range(1,21):
 z=j*.23;p,n,idx,d=woodtree.ray_cast(Vector((base.x+.025*z,-12,z)),Vector((0,1,0)))
 trunk_sections.append({'height':z,'hit':p is not None})
assert all(x['hit'] for x in trunk_sections),'Fused trunk has an unsupported opening'
# Staggered low sculpted ridges: handmade bark masses, no photoreal image bark.
tex=bpy.data.textures.new('GT_compressed_wood_irregularity',type='CLOUDS');tex.noise_scale=.19;tex.noise_depth=2
dis=oak.modifiers.new('Hand-felt wood relief','DISPLACE');dis.texture=tex;dis.strength=.055;dis.mid_level=.5;bpy.ops.object.modifier_apply(modifier=dis.name)
for i in range(220):
 a=R.uniform(0,math.tau);z0=R.uniform(.15,4.2);length=R.uniform(.20,.70);pts=[]
 for k in range(5):
  z=z0+length*k/4;rad=1.17-(min(z,1.0)/1.0)*.34-max(0,z-1)*.065;theta=a+.025*math.sin(k*1.8+i)
  pts.append((base.x+.04*z+math.cos(theta)*rad,base.y+.06*z+math.sin(theta)*rad,z))
 h.curve('OAK_short_felt_fold_%03d'%i,pts,R.uniform(.008,.016),ridge if i%3 else dark,radii=[.05,.8,1,.75,.05])
for i,(pts,size) in enumerate(roots):
 for k in range(5):
  off=(k-2)*size*.17;q=[tuple(p+Vector((off,0,size*.50*(1-j/len(pts))))) for j,p in enumerate(pts)];h.curve('ROOT_fold_%02d_%02d'%(i,k),q,.012,ridge,radii=[1,.9,.55,.05])
# The required low diagonal approach root is its own stable interaction object.
a=anchors['ROOT_APPROACH_START'];b=anchors['ROOT_APPROACH_TIP'];rpts=[a+Vector((0,0,.12)),a.lerp(b,.30)+Vector((0,0,.12)),a.lerp(b,.68)+Vector((0,0,.075)),b+Vector((0,0,.018))]
root=h.curve('ROOT_APPROACH_A',rpts,.12,bark,radii=[1.3,1,.65,.12]);root.data.use_fill_caps=True;root['role']='low fixed contactable approach root; forepaw is separate actor story contact'
for j in range(4):h.curve('ROOT_APPROACH_felt_fold_%02d'%j,[p+Vector(((j-1.5)*.025,0,.045)) for p in rpts],.009,ridge,radii=[1,.9,.6,.05])
# Hero rock/mound silhouettes placed by registered observed contact anchors.
active(HERO)
for name,sc,mat in [('MOUND_LEFT',(1.25,.85,.34),moss),('STONE_CENTER_LEFT',(.40,.30,.28),stone),('ROCK_RIGHT',(.95,.60,.63),stone)]:
 p=anchors[name];ob=h.ell(name,p+Vector((0,0,sc[2]*.55)),sc,mat,irregular=.10,segments=40,rings=24);ob['landmark_id']=name
# A distant cloth-water ribbon and stable bank pebbles.
active(GROUND);stream=anchors['STREAM_GLIMPSE'];verts=[]
for j in range(12):
 y=stream.y+j*1.3;x=stream.x-1.5*math.sin(j*.35)-j*.22;width=.58+.04*j;verts.extend([(x-width,y,-.004),(x+width,y,-.004)])
mesh('WATER_STREAM_CLOTH',verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(11)],water,GROUND)
for j in range(18):
 y=stream.y+R.uniform(0,7);x=stream.x+R.choice([-1,1])*R.uniform(.5,1.0)-.15*(y-stream.y);h.ell('STREAM_bank_stone_%02d'%j,(x,y,.1),(R.uniform(.15,.35),.22,.18),stone,irregular=.12,segments=16,rings=10)
# Shared hand-cut leaf mesh; objects instance data, not thousands of unique meshes.
leafverts=[];leaffaces=[]
for j in range(13):
 t=j/12;width=math.sin(math.pi*t)**.7*.45*(.86+.14*math.sin(7*math.pi*t))
 for u in [-1,0,1]:leafverts.append((u*width,t, .10*math.sin(math.pi*t)+(.03 if u==0 else 0)))
for j in range(12):
 for k in range(2):a=j*3+k;leaffaces.append((a,a+1,a+4,a+3))
proto=mesh('KIT_FELT_LEAF',leafverts,leaffaces,leaf,TEMPLATES);proto.data.materials.append(leaflight);proto['module']='hand-cut leaf; local +Y length, origin anchored at base'
def leaf_obj(name,loc,length,width,rot,c=DRESS,matindex=0):
 ob=bpy.data.objects.new(name,proto.data);c.objects.link(ob);ob.location=loc;ob.scale=(width,length,length);ob.rotation_euler=rot;return ob
# Ferns: anchored stem and opposed folded felt leaves.
def fern(name,loc,size=1,angle=0):
 active(DRESS);origin=Vector(loc)
 for f in range(4):
  theta=angle+(f-1.5)*.47;direction=Vector((math.cos(theta),math.sin(theta),0));length=size*R.uniform(.27,.45);end=origin+direction*length+Vector((0,0,size*.22));h.curve(name+'_stem_%d'%f,[origin,origin+direction*length*.55+Vector((0,0,size*.18)),end],.005,mosslight)
  for j in range(1,7):
   t=j/7;p=origin.lerp(end,t)+Vector((0,0,math.sin(t*math.pi)*size*.035))
   for sign in [-1,1]:leaf_obj(name+'_leaf_%d_%d_%d'%(f,j,sign),p,size*.10*(1-t*.55),size*.10,(.45,sign*.35,theta+sign*1.0))
for i,(u,v,size) in enumerate([(.07,.83,1.2),(.13,.79,.9),(.22,.75,.8),(.92,.79,1.3),(.86,.77,.9),(.98,.85,1.4),(.73,.62,.8)]):fern('FERN_%02d'%i,ground(u,v,.01),size,R.uniform(0,math.tau))
# Moss clumps on hero roots and trunk: low volume, fixed seed, shared simple mesh.
active(TEMPLATES);blob=h.ell('KIT_MOSS_PILLOW',(0,0,0),(1,1,1),moss,irregular=.10,segments=12,rings=8)
def blob_obj(name,loc,scale,c=DRESS,mat=None):
 ob=bpy.data.objects.new(name,blob.data if mat is None else blob.data.copy());c.objects.link(ob);ob.location=loc;ob.scale=scale
 if mat:ob.data.materials.clear();ob.data.materials.append(mat)
 return ob
for k in range(360):
 pts,size=roots[k%len(roots)];t=R.uniform(.15,.94);seg=min(2,int(t*3));f=t*3-seg;p=pts[seg].lerp(pts[seg+1],f);p+=Vector((R.uniform(-.10,.10),R.uniform(-.10,.10),size*(1-t)*.55));blob_obj('MOSS_root_%04d'%k,p,(R.uniform(.04,.12),R.uniform(.05,.14),R.uniform(.025,.065)))
for k in range(100):
 t=R.random();z=.2+t*2.1;a=-math.pi/2+R.uniform(-.25,.25);rad=1.10-.35*min(z,1.5);p=base+Vector((math.cos(a)*rad,math.sin(a)*rad,z));blob_obj('MOSS_trunk_seam_%03d'%k,p,(.06,.035,.11))
# Distant broadleaf trees use clumped wool, not smooth spheres.
active(FAR);farleaf=felt('GT_far_sage','566A55',80,.15);farleaf2=felt('GT_far_cool_green','485B51',80,.12)
for k in range(74):
 y=R.uniform(15,34);x=R.uniform(-17,18)
 if -8<x<-4 and y<18:continue
 z=R.uniform(.55,1.55);h.curve('MID_tree_trunk_%03d'%k,[(x,y,0),(x+.06,y,z*.8)],.045,bark,radii=[1,.5])
 for j in range(7):
  a=j*math.tau/7;p=Vector((x+math.cos(a)*.35,y+math.sin(a)*.30,z+R.uniform(-.20,.25)));blob_obj('MID_wool_crown_%03d_%02d'%(k,j),p,(.48,.42,.48),FAR,farleaf if k%2 else farleaf2)
# Pine silhouettes: layered wool fronds rather than pure stacked cones.
for k,(u,v,y) in enumerate([(.01,.32,19),(.36,.35,22),(.52,.29,24),(.82,.25,28),(.94,.30,24)]):
 d=y-wide.location.y;ray=wide.rotation_euler.to_matrix()@Vector(((u-.5)*.8,(.5-v)*.45,-1));p=wide.location+ray*(d/ray.y);x=p.x;height=p.z
 h.curve('PINE_trunk_%d'%k,[(x,y,0),(x,y,height)],.035,bark,radii=[1,.2])
 for j in range(9):
  z=.25+j*height/10;wid=(1-z/height)*.5+.045
  for arm in range(5):
   a=arm*math.tau/5;blob_obj('PINE_felt_frond_%d_%d_%d'%(k,j,arm),(x+math.cos(a)*wid*.4,y+math.sin(a)*wid*.4,z),(wid,.18,.11),FAR,farleaf2)
# Main canopy: branch end masses, with individually instanced folded leaves.
for k in range(90):
 branch=branches[k%len(branches)];t=R.uniform(.28,1.15);p=base+Vector((branch[0]*t,branch[1]*t+R.uniform(-.3,.5),3.18+R.uniform(-.42,.42)))
 for j in range(22):
  q=p+Vector((R.uniform(-.42,.42),R.uniform(-.35,.35),R.uniform(-.2,.2)));leaf_obj('CANOPY_leaf_%03d_%02d'%(k,j),q,R.uniform(.14,.27),R.uniform(.14,.24),(R.uniform(-.5,.5),R.uniform(-.7,.7),R.uniform(0,math.tau)))
# Foreground low bushes and leaf framing; no random growth in the acting lane.
for k,(u,v) in enumerate([(.015,.69),(.075,.72),(.02,.95),(.12,.92),(.96,.74),(.97,.90),(.80,.62),(.34,.57),(.10,.57)]):
 p=ground(u,v,.015)
 for j in range(40):
  q=p+Vector((R.uniform(-.35,.35),R.uniform(-.28,.28),R.uniform(0,.28)));leaf_obj('BUSH_%02d_leaf_%03d'%(k,j),q,R.uniform(.08,.18),R.uniform(.08,.17),(R.uniform(-.4,.6),R.uniform(-.5,.5),R.uniform(0,math.tau)))
# Ground micro-pile in a single batch, sampled with path + route exclusions.
route=[(-2.4,-1.9),(-1.2,-1.8),(.15,-1.6),(.62,-1.05),(.86,-.60),(.91,-.20),(1.45,-.65)]
def segdist(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def reserved(x,y):return (-1.5<x<1.4 and -.8<y<1.5) or min(segdist(x,y,a,b) for a,b in zip(route,route[1:]))<.24
verts=[];faces=[];matids=[]
for k in range(14000):
 x=R.uniform(-9,10);y=R.uniform(-3,14);cx,ww=path_width(y);onpath=abs(x-cx)<ww
 if reserved(x,y) or (onpath and R.random()<.97):continue
 scale=R.uniform(.035,.085)*(1 if y<5 else .75);angle=R.uniform(0,math.tau)
 for blade in range(3):
  a=angle+blade*2.1;dx=math.cos(a);dy=math.sin(a);start=len(verts);bend=scale*.35
  verts.extend([(x-dy*.012,y+dx*.012,.012),(x+dy*.012,y-dx*.012,.012),(x+dx*bend+dy*.006,y+dy*bend-dx*.006,scale*.65),(x+dx*bend-dy*.006,y+dy*bend+dx*.006,scale*.65),(x+dx*bend*1.5,y+dy*bend*1.5,scale)])
  faces.extend([(start,start+1,start+2,start+3),(start+3,start+2,start+4)]);matids.extend([k%3,k%3])
pile=mesh('GROUND_anchored_felt_pile',verts,faces,moss,DRESS);pile.data.materials.append(grass);pile.data.materials.append(mosslight)
for p,i in zip(pile.data.polygons,matids):p.material_index=i
# Dense low wool pillows, with the route kept clear and the resting area short.
for k in range(1900):
 x=R.uniform(-7,8);y=R.uniform(-2.7,10);cx,ww=path_width(y)
 if abs(x-cx)<ww*.98 or min(segdist(x,y,a,b) for a,b in zip(route,route[1:]))<.22:continue
 height=.008 if reserved(x,y) else R.uniform(.012,.027)
 blob_obj('GROUND_compressed_wool_%04d'%k,(x,y,.006),(R.uniform(.035,.095),R.uniform(.035,.10),height),DRESS)
# Small compressed wool flecks on path edges; not large loose rocks.
for k in range(220):
 y=R.uniform(-3,7);cx,ww=path_width(y);x=cx+R.choice([-1,1])*ww*R.uniform(.92,1.10)
 if reserved(x,y):continue
 blob_obj('PATH_felt_edge_%03d'%k,(x,y,.015),(R.uniform(.025,.07),R.uniform(.025,.06),.014),DRESS)
# Fixed shallow distant hill layers. These are camera-limited 2.5D assets.
for layer,(y,color,heights) in enumerate([(40,'68617B',1.3),(55,'87758B',2.1),(75,'AB8391',1.4)]):
 mat=felt('GT_mountain_layer_%d'%layer,color,8,.08);verts=[]
 for j in range(51):
  x=-55+j*2.2;z=heights+1.3*math.sin(j*.21+layer)+.35*math.sin(j*.77+layer);verts.extend([(x,y,-3),(x,y,z)])
 ob=mesh('MATTE_FAR_RIDGE_%d'%layer,verts,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(50)],mat,FAR);ob['camera_envelope']='wide/crops and tested +/- .25 BU; no reverse view'
# Emissive felt sky matte, sunset glow confined to left and low sky.
skymat=bpy.data.materials.new('GT_sky_felt_dusk');skymat.use_nodes=True;n=skymat.node_tree.nodes;l=skymat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs[1].default_value=1.15;coord=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(coord.outputs['Generated'],sep.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(*rgb('FFBC59'),1)
for pos,color in [(.30,'EE9962'),(.57,'A87991'),(1,'69678E')]:ramp.color_ramp.elements.new(pos).color=(*rgb(color),1)
l.new(sep.outputs['Z'],ramp.inputs[0]);l.new(ramp.outputs[0],em.inputs[0]);l.new(em.outputs[0],out.inputs['Surface']);mesh('MATTE_DUSK_SKY',[(-100,100,-12),(100,100,-12),(100,100,36),(-100,100,36)],[(0,1,2,3)],skymat,SKY)
# Thin irregular felt cloud ribbons: static now, separate layer IDs for later drift.
cloud=felt('GT_cloud_felt_purple','BE8792',12,.12)
cn=cloud.node_tree.nodes;cl=cloud.node_tree.links;co=cn.get('Material Output');ce=cn.new('ShaderNodeEmission');ce.inputs[0].default_value=(*rgb('BE8792'),1);ce.inputs[1].default_value=.8;cl.new(ce.outputs[0],co.inputs['Surface'])
for k,(u,v,wid) in enumerate([(.12,.12,.20),(.32,.22,.25),(.15,.28,.18),(.48,.29,.16),(.70,.10,.15)]):
 y=86;ray=wide.rotation_euler.to_matrix()@Vector(((u-.5)*.8,(.5-v)*.45,-1));p=wide.location+ray*((y-wide.location.y)/ray.y);width=wid*(y-wide.location.y)*.8;vs=[]
 for j in range(25):
  t=j/24;xx=p.x+(t-.5)*width;zz=p.z+.22*math.sin(t*13+1)+.11*math.sin(t*29+k);th=.28+math.sin(math.pi*t)*.75;vs.extend([(xx,y,zz-th),(xx,y,zz+th)])
 ob=mesh('CLOUD_FELT_BAND_%02d'%k,vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(24)],cloud,SKY);ob['future_motion']='optional world +X .015 BU/s; no in-frame wrap; no shadow modulation'
# Sunset disk placed in the approved far-left opening; no clouds cast light changes.
sunmat=bpy.data.materials.new('GT_sunset_disk_glow');sunmat.use_nodes=True;ns=sunmat.node_tree.nodes;ls=sunmat.node_tree.links;ns.clear();oo=ns.new('ShaderNodeOutputMaterial');ee=ns.new('ShaderNodeEmission');ee.inputs[0].default_value=(*rgb('FFD880'),1);ee.inputs[1].default_value=2;ls.new(ee.outputs[0],oo.inputs[0])
y=90;ray=wide.rotation_euler.to_matrix()@Vector(((.075-.5)*.8,(.5-.35)*.45,-1));p=wide.location+ray*((y-wide.location.y)/ray.y);vs=[tuple(p)]+[(p.x+math.cos(j*math.tau/64)*1.8,y,p.z+math.sin(j*math.tau/64)*1.8) for j in range(64)];mesh('SUNSET_FIXED_DISK',vs,[(0,j+1,(j+1)%64+1) for j in range(64)],sunmat,SKY)
# Stable interaction anchors and route, hidden in beauty.
for name,pos,role in [('LEO_REST_CENTER',(-.2,.40,.01),'reserved lying envelope, not a posed Leo'),('LEO_PAW_CONTACT',(.60,-.30,.01),'future actor paw landmark'),('LEO_NOSE_CONTACT',(.88,.22,.12),'future actor nose landmark'),('MILO_ROOT_BYPASS',(.15,-1.6,.01),'route around low root tip'),('MILO_EXIT',(1.45,-.65,.01),'clear ground exit')]:anchor('ANCHOR_'+name,pos,role)
for i,(x,y) in enumerate(route):anchor('ROUTE_MILO_%02d'%i,(x,y,.012),'ordered approach/interaction/exit route')
# Scene-appropriate light rig separate from persistent geometry.
active(LIGHTS);h.area('LIGHT_Dusk_soft_sky',(1,6,9),(0,3,0),500,(.66,.72,1),9);h.area('LIGHT_Neutral_readable_fill',(0,-5,5),(0,3,.6),180,(.91,.92,1),7);h.area('LIGHT_Sunset_far_left',(-8,1,4),(1,3,.8),3000,(1,.63,.30),4)
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.23,.34,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
# Crop study: same optical center, newer proposed p02 crop, explicitly unapproved.
active(CAMS);crop=wide.copy();crop.data=wide.data.copy();CAMS.objects.link(crop);crop.name='CAM_S05_P02_PROPOSED_CROP_STUDY_R02';rect=(.08667,.25667,.66667,.66667);x,y,w,hh=rect;crop.data.lens=45/w;crop.data.shift_x=((x+w/2)-.5)/w;crop.data.shift_y=(.5-(y+hh/2))*(9/16)/w;crop['status']='proposed current-plan crop, not approved image replacement';crop['crop_rect_on_plate']=rect
h.camera('CAM_GT_ROOT_CONTACT_DETAIL_R02',(-1.3,-3.2,1.05),(-1.1,.0,.12),52)
h.camera('CAM_GT_OVERVIEW_DIAGNOSTIC_R02',(-8,-7,8),(0,3,.7),42)
for sign in [-1,1]:
 c=wide.copy();c.data=wide.data.copy();CAMS.objects.link(c);c.name='CAM_GT_ENVELOPE_'+('LEFT' if sign<0 else 'RIGHT');c.location.x+=sign*.25;c.rotation_euler=(Vector((0,4,.725))-c.location).to_track_quat('-Z','Y').to_euler()
# Pack the sole reused texture and keep input images out of beauty entirely.
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
s.camera=wide;s['environment_revision']='ENV_GreatTree_R02';s['approval_status']='first serious reusable environment prototype; owner review pending';s['unit_m_per_bu']=.2;s['ambient_plan']='static still_evening_r02; future preset documented, no animation';s['source_plate_sha256']='3abb51cbe5ce3d52cef406ae0f753353cbce217a01e193bcc3106876982edf06'
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=str(ENV),compress=True)
inventory={'environment':str(ENV.relative_to(ROOT)),'sha256':sha(ENV),'objects':len(bpy.data.objects),'mesh_faces':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),'oak_faces':len(oak.data.polygons),'trunk_sections':trunk_sections,'landmarks':{name:list(p) for name,p in anchors.items()},'route_world_xy':route,'seed':18102651,'world_units_m':.2,'external_calls':0,'library_collections':['ENV_GreatTree_R02','GT_DUSK_LIGHT_R02','GT_CAMERAS_R02']}
(P/'build_inventory.json').write_text(json.dumps(inventory,indent=2))
# Independent scene assembly links the reusable environment and light/camera kit.
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;h.settings();s.unit_settings.system='METRIC';s.unit_settings.scale_length=.2;s.cycles.seed=18102651
with bpy.data.libraries.load(str(ENV),link=True) as (src,dst):dst.collections=['ENV_GreatTree_R02','GT_DUSK_LIGHT_R02','GT_CAMERAS_R02']
for c in dst.collections:s.collection.children.link(c)
# World belongs to the shot's light state, geometry stays linked.
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.23,.34,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
controls=bpy.data.collections.new('S05_PROXIES_DIAGNOSTIC_ONLY');s.collection.children.link(controls);controls.hide_render=True;active(controls)
proxy_mat=felt('PROXY_scale_only','59A9B1',50,.03);milo=h.ell('PROXY_MILO_025_NOT_CHARACTER',(.85,-.60,.1875),(.085,.065,.1875),proxy_mat,irregular=0);milo['neutral_height_bu']=.375;milo['milo_to_leo']=.25;milo['production_character']=False
# Neutral height ruler plus low resting envelope, not deforming the real asset.
leo=h.ell('PROXY_LEO_REST_ENVELOPE',(-.2,.4,.27),(1.05,.45,.27),proxy_mat,irregular=0);leo.display_type='WIRE';leo['standing_reference_height_bu']=1.5;leo['status']='spatial reserve only, no pose or identity claim'
active(controls);h.curve('DIAG_MILO_ROUTE',[(x,y,.027) for x,y in route],.012,proxy_mat)
for name in ['LEO_PAW_CONTACT','LEO_NOSE_CONTACT']:
 p=bpy.data.objects.get('ANCHOR_'+name).location;h.ell('PROXY_'+name,p+Vector((0,0,.06)),(.10,.10,.06),proxy_mat,irregular=0,segments=16,rings=10)
s.camera=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];s['approval_status']='S05 environment / route study; no actor performance';s['environment_library']=str(ENV.relative_to(ROOT));s['milo_proxy_height_bu']=.375;s['leo_standing_reference_height_bu']=1.5
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
(P/'scene_build.json').write_text(json.dumps({'scene':str(SHOT.relative_to(ROOT)),'sha256':sha(SHOT),'library':str(ENV.relative_to(ROOT)),'library_sha256':sha(ENV),'relative_links':[lib.filepath for lib in bpy.data.libraries],'proxy_height_ratio':.25,'no_Leo_asset_modified':True},indent=2));print('GT_ENVIRONMENT_BUILD_COMPLETE',json.dumps(inventory),flush=True)
