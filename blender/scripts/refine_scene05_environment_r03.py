"""Additive, deterministic refinement of r02. No rebuild or external calls.
Run from Blender background, automatic execution disabled. See r03 task brief.
"""
import bpy, math, random, sys, json, hashlib, time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]; A=ROOT/'blender'; P=A/'renders/scene05_environment_r03'
sys.path.insert(0,str(A/'scripts')); import build as h
R=random.Random(510318)
ENV=A/'assets/environments/great_tree/great_tree_environment_r03.blend'
SHOT=A/'scenes/lion_and_mouse_v6/s05_environment_r03.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def collection(name,parent):
 c=bpy.data.collections.new(name);parent.children.link(c);return c
def mesh(name,vs,fs,mat,c):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new(name,me);c.objects.link(ob)
 if mat:me.materials.append(mat)
 for f in me.polygons:f.use_smooth=True
 return ob
def rgb(hx):
 vals=[int(hx[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in vals)
def felt(name,hx,scale=110):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Roughness'].default_value=.93;p.inputs['Specular IOR Level'].default_value=.16;p.inputs['Sheen Weight'].default_value=.32
 tc=n.new('ShaderNodeTexCoord');no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=scale;no.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],no.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.58 for x in rgb(hx)],1);ramp.color_ramp.elements[1].color=(*[x*1.12 for x in rgb(hx)],1);l.new(no.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.38;b.inputs['Distance'].default_value=.009;l.new(no.outputs['Fac'],b.inputs['Height'])
 meso=n.new('ShaderNodeTexNoise');meso.inputs['Scale'].default_value=22;meso.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],meso.inputs[0]);bb=n.new('ShaderNodeBump');bb.inputs['Strength'].default_value=.30;bb.inputs['Distance'].default_value=.018;l.new(meso.outputs['Fac'],bb.inputs['Height']);l.new(b.outputs[0],bb.inputs['Normal']);l.new(bb.outputs[0],p.inputs['Normal'])
 return m
def hide_prefix(prefix):
 for o in bpy.data.objects:
  if o.name.startswith(prefix):o.hide_render=True
def batch_blobs(name,items,mats,c):
 # Uneven rounded felt lobes; consolidated geometry rather than object scatter.
 vs=[];fs=[];ids=[];seg=10;rings=6
 for item in items:
  loc,sc,mi=item[:3];rot=Vector(item[3]).to_track_quat('Z','Y').to_matrix() if len(item)>3 else None
  start=len(vs);phase=R.random()*6.28
  for j in range(rings+1):
   th=math.pi*j/rings
   for k in range(seg):
    a=math.tau*k/seg;f=1+.12*math.sin(a*3+phase)*math.sin(th)**2+.05*math.sin(th*5+phase)
    v=Vector((sc[0]*math.sin(th)*math.cos(a)*f,sc[1]*math.sin(th)*math.sin(a)*f,sc[2]*math.cos(th)*f));v=rot@v if rot else v;vs.append(tuple(Vector(loc)+v))
  for j in range(rings):
   for k in range(seg):
    a=start+j*seg+k;b=start+j*seg+(k+1)%seg;fs.append((a,b,b+seg,a+seg));ids.append(mi)
 ob=mesh(name,vs,fs,mats[0],c)
 for m in mats[1:]:ob.data.materials.append(m)
 for f,i in zip(ob.data.polygons,ids):f.material_index=i
 return ob
bpy.ops.wm.open_mainfile(filepath=str(A/'assets/environments/great_tree/great_tree_environment_r02.blend'),use_scripts=False)
s=bpy.context.scene; original_objects=set(bpy.data.objects.keys());cam=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];s.camera=cam
parent=bpy.data.collections['ENV_GreatTree_R02'];detail=collection('GT_R03_HERO_REFINEMENT',parent);plants=collection('GT_R03_CLUSTERED_UNDERSTORY',parent);background=collection('GT_R03_DISTANCE_SKY',parent)
base=bpy.data.objects['ANCHOR_OAK_BASE'].location.copy()
def ray(u,v):return cam.rotation_euler.to_matrix()@Vector(((u-.5)*.8,(.5-v)*.45,-1))
def ground(u,v,z=0):
 d=ray(u,v);return cam.location+d*((z-cam.location.z)/d.z)
def plane(u,v,y):
 d=ray(u,v);return cam.location+d*((y-cam.location.y)/d.y)
olive=felt('R03_deep_olive_wool','697039');sage=felt('R03_sage_wool','737E47');gold=felt('R03_moss_lit_tips','939044');deep=felt('R03_shaded_leaf','44583A');bark=felt('R03_bark_compressed_wool','72503D');barklit=felt('R03_bark_fold_light','8B6246');soil=felt('R03_path_matted_earth','926747',180);rockmat=felt('R03_stone_heather_felt','85817B',150)
bpy.data.objects['SURF_CLEARING'].data.materials.clear();bpy.data.objects['SURF_CLEARING'].data.materials.append(olive)
# Preserve camera optical center and lens: framing is refined through measured forms.
# Source tree base is already registered; moving the camera would worsen it.
cam['r03_fit']='45 mm retained after anchor comparison; shape/ground residuals refined in world space; not a solved camera'
cam.data.dof.use_dof=False
# Existing root/trunk mesh is retained and shaped, with continuous broad bark flow.
oak=bpy.data.objects['OAK_MAIN'];oak.data.materials.clear();oak.data.materials.append(bark)
for vert in oak.data.vertices:
 w=oak.matrix_world@vert.co;d=w-base;ang=math.atan2(d.y,d.x);z=w.z
 weight=min(1,max(0,(z-.15)/.7))*min(1,max(0,(3.5-z)/.7))
 off=(.050*math.sin(ang*13+.55*math.sin(z*1.7))+.027*math.sin(ang*23-z*.8))*weight
 normal=vert.normal;vert.co+=normal*off
 if z<1.3:
  w=oak.matrix_world@vert.co;w.x=base.x+(w.x-base.x)*(1+.35*min(1,max(0,z)/.8));vert.co=oak.matrix_world.inverted()@w
 elif z<3.1:
  w=oak.matrix_world@vert.co;w.x=base.x+(w.x-base.x)*1.40;vert.co=oak.matrix_world.inverted()@w
 elif z<3.8:
  t=(z-3.1)/.7;t=t*t*(3-2*t);w=oak.matrix_world@vert.co;w.x=base.x+(w.x-base.x)*(1+.4*(1-t));vert.co=oak.matrix_world.inverted()@w
tex=bpy.data.textures.new('R03_medium_bark_felt_relief',type='CLOUDS');tex.noise_scale=.065;tex.noise_depth=2
mod=oak.modifiers.new('R03_compressed_bark_relief','DISPLACE');mod.texture=tex;mod.strength=.025;mod.mid_level=.5
hide_prefix(('OAK_short_felt_fold_','ROOT_fold_','MOSS_trunk_seam_','MOSS_root_'))
bpy.context.view_layer.update();ev=oak.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();tree=BVHTree.FromPolygons([oak.matrix_world@v.co for v in me.vertices],[t.vertices for t in me.loop_triangles],all_triangles=True);ev.to_mesh_clear()
# Tapered bark ribbons sit on the actual surface, avoiding floating short cords.
vs=[];fs=[]
for i in range(125):
 a=R.uniform(-math.pi,math.pi);z0=R.uniform(.10,3.9);length=R.uniform(.22,1.15);width=R.uniform(.015,.055);start=len(vs);valid=True
 for j in range(15):
  t=j/14;z=z0+t*length;angle=a+.055*math.sin(z*2+i);di=Vector((math.cos(angle),math.sin(angle),0));hit,n,_,_=tree.ray_cast(base+Vector((0,0,z))+di*4,-di)
  if hit is None:valid=False;break
  tangent=Vector((-di.y,di.x,0));w=width*math.sin(math.pi*t)**.6
  for k in [-1,0,1]:vs.append(tuple(hit+tangent*w*k+n*(.003+(.014 if k==0 else 0)*math.sin(math.pi*t))))
 if valid:
  for j in range(14):
   for k in range(2):q=start+j*3+k;fs.append((q,q+1,q+4,q+3))
mesh('R03_surface_following_bark_folds',vs,fs,barklit,detail)
bpy.data.objects['R03_surface_following_bark_folds'].hide_render=True
# Root moss drapes: sample existing structural surface, never cover the actor lane.
items=[]
for i in range(3300):
 x=base.x+R.uniform(-3.2,3.3);y=base.y+R.uniform(-2.6,1.0)
 hit,n,_,_=tree.ray_cast(Vector((x,y,4.0)),Vector((0,0,-1)))
 if hit is None or hit.z>2.5 or n.z<.18:continue
 if math.sin(x*5+y*2)+math.sin(y*7-x*2)<-.1:continue
 size=R.uniform(.025,.105);items.append((hit+n*.004,(size*1.6,size*1.25,size*.28),R.choices([0,1,2],[.55,.3,.15])[0],tuple(n)))
for i in range(500):
 z=R.uniform(.15,1.9);a=R.choice([-1.25,-1.85])+R.uniform(-.14,.14);d=Vector((math.cos(a),math.sin(a),0));hit,n,_,_=tree.ray_cast(base+Vector((0,0,z))+d*3,-d)
 if hit is not None:items.append((hit+n*.003,(R.uniform(.04,.08),R.uniform(.07,.15),.018),R.randrange(3),tuple(n)))
batch_blobs('R03_root_moss_drapes',items,[olive,sage,gold],detail)
# Short anchored wool loops give moss a soft grazing edge without long fur.
c=bpy.data.curves.new('R03_moss_short_fibers','CURVE');c.dimensions='3D';c.bevel_depth=.0015;c.bevel_resolution=0
for item in items:
 p,sc,mi=item[:3];rot=Vector(item[3]).to_track_quat('Z','Y').to_matrix()
 for j in range(3):
  start=Vector(p)+rot@Vector((R.uniform(-sc[0],sc[0])*.7,R.uniform(-sc[1],sc[1])*.7,sc[2]*.5));a=R.uniform(0,math.tau);length=R.uniform(.014,.034);sp=c.splines.new('POLY');sp.points.add(2)
  for k,pt in enumerate(sp.points):
   t=k/2;q=start+rot@Vector((math.cos(a)*length*t,math.sin(a)*length*t,math.sin(t*math.pi)*length*.65));pt.co=(*q,1)
ob=bpy.data.objects.new('R03_surface_anchored_moss_fibers',c);detail.objects.link(ob);c.materials.append(sage)
# Lower the excessive rock profiles and soften the fluorescent left mound.
for name,scale in [('ROCK_RIGHT',(.85,.82,.72)),('STONE_CENTER_LEFT',(1.05,1,.72)),('MOUND_LEFT',(1,.95,.77))]:
 o=bpy.data.objects[name]
 for v in o.data.vertices:v.co.x*=scale[0];v.co.y*=scale[1];v.co.z*=scale[2]
 o.location.z*=scale[2]
 o.data.materials.clear();o.data.materials.append(olive if name=='MOUND_LEFT' else rockmat)
 if name!='MOUND_LEFT':
  for v in o.data.vertices:
   w=v.co;w.x+=.035*math.sin(w.y*17+w.z*5);w.z+=.025*math.sin(w.x*13+w.y*9)
# Approach root retains its stable name and origin; extend only its fine tip.
root=bpy.data.objects['ROOT_APPROACH_A'];root['r03_tip']='original safe contact-root endpoint retained after extended-tip clearance regression'
hide_prefix('ROOT_APPROACH_felt_fold_')
# Replace only path mesh data with a densely sampled, frayed ribbon.
rows=[(1.20,.66,.46),(.975,.73,.36),(.90,.82,.27),(.82,.80,.23),(.74,.73,.19),(.67,.61,.12),(.61,.44,.07),(.56,.22,.023),(.52,.18,.017)]
vs=[];fs=[]
for i in range(141):
 t=i/140*(len(rows)-1);k=min(len(rows)-2,int(t));f=t-k;f=f*f*(3-2*f);v,c,w=[rows[k][a]*(1-f)+rows[k+1][a]*f for a in range(3)]
 for j in range(21):
  q=j/20*2-1;u=c+w*q+(abs(q)**5)*(.004*math.sin(i*1.2)+.003*math.sin(i*2.9+j));p=ground(u,v,.006);vs.append(tuple(p))
for i in range(140):
 for j in range(20):q=i*21+j;fs.append((q,q+1,q+22,q+21))
old=bpy.data.objects['SURF_PATH'];temp=mesh('R03_path_work',vs,fs,soil,detail);old.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
def path_bounds(v):
 for a,b in zip(rows,rows[1:]):
  if b[0]<=v<=a[0]:t=(a[0]-v)/(a[0]-b[0]);t=t*t*(3-2*t);return a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t
 return (.18,.017) if v<.52 else (.67,.36)
# Remove visual repetition while retaining r02 modules for inspection/rollback.
hide_prefix(('GROUND_anchored_felt_pile','GROUND_compressed_wool_','PATH_felt_edge_','BUSH_','CANOPY_leaf_'))
def reserved(p):
 route=[(-2.4,-1.9),(-1.2,-1.8),(.15,-1.6),(.62,-1.05),(.86,-.60),(.91,-.20),(1.45,-.65)]
 if -1.5<p.x<1.4 and -.8<p.y<1.5:return True
 for a,b in zip(route,route[1:]):
  d=Vector((b[0]-a[0],b[1]-a[1]));v=Vector((p.x-a[0],p.y-a[1]));t=max(0,min(1,v.dot(d)/d.length_squared))
  if (v-d*t).length<.24:return True
 return False
# Low compressed wool islands: large distribution pattern, medium clumps, small pile.
items=[];vs=[];fs=[];ids=[]
for i in range(22000):
 u=R.uniform(-.04,1.04);v=R.uniform(.52,1.05);p=ground(u,v,.007);c,w=path_bounds(v);edge=abs(u-c)-w
 density=.55+.28*math.sin(p.x*4+p.y*1.3)*math.sin(p.y*3.2)+.2*math.sin(p.x*9-p.y*2)
 if edge<-.015 and R.random()>.025:continue
 if R.random()>density:continue
 reserve=reserved(p);sz=R.uniform(.022,.073)*(1 if v>.7 else .75)
 items.append((p,(sz*1.2,sz,sz*(.16 if reserve else .40)),R.choices([0,1,2,3],[.45,.25,.12,.18])[0]))
 if reserve or (edge<-.01 and R.random()>.12):continue
 for b in range(R.randrange(3,7)):
  a=R.uniform(0,math.tau);ht=R.uniform(.025,.095);wd=R.uniform(.004,.009);dx=math.cos(a);dy=math.sin(a);q=len(vs)
  vs.extend([(p.x-dy*wd,p.y+dx*wd,p.z),(p.x+dy*wd,p.y-dx*wd,p.z),(p.x+dx*ht*.3+dy*wd*.6,p.y+dy*ht*.3-dx*wd*.6,p.z+ht*.65),(p.x+dx*ht*.3-dy*wd*.6,p.y+dy*ht*.3+dx*wd*.6,p.z+ht*.65),(p.x+dx*ht*.8,p.y+dy*ht*.8,p.z+ht*.8)])
  fs.extend([(q,q+1,q+2,q+3),(q+3,q+2,q+4)]);ids.extend([i%3,i%3])
batch_blobs('R03_compressed_ground_islands',items,[olive,sage,gold,deep],plants)
tufts=mesh('R03_fine_clustered_grass',vs,fs,olive,plants);tufts.data.materials.append(sage);tufts.data.materials.append(gold)
for f,i in zip(tufts.data.polygons,ids):f.material_index=i
# Rounded folded oak leaves: six subtle lobes rather than flat pointed confetti.
vs=[];fs=[];ids=[]
def leaf(loc,length,width,angle,tilt,mi):
 start=len(vs)
 for j in range(13):
  t=j/12;w=width*math.sin(math.pi*t)**.65*(.78+.22*math.cos(t*math.pi*10));y=length*t
  for k in [-1,0,1]:
   x=w*k;z=length*(.18*math.sin(math.pi*t)+.70*t+tilt*t*.3)+(.024*length if k==0 else 0)
   vs.append((loc[0]+x*math.cos(angle)-y*.40*math.sin(angle),loc[1]+x*math.sin(angle)+y*.40*math.cos(angle),loc[2]+z))
 for j in range(12):
  for k in range(2):q=start+j*3+k;fs.append((q,q+1,q+4,q+3));ids.append(mi)
# Dense canopy hangs from the existing branch kit and frames left sky opening.
for u,v,sz in [(.27,.04,.13),(.29,.12,.08),(.34,.15,.10),(.40,.04,.15),(.42,.12,.09),(.48,.10,.1),(.52,.20,.075),(.59,.05,.13),(.84,.04,.12),(.94,.10,.16),(.99,.19,.10)]:
 center=plane(u,v,base.y+.4)
 for i in range(240):
  p=center+Vector((R.gauss(0,sz*3),R.gauss(0,.20),R.gauss(0,sz*1.7)));leaf(p,R.uniform(.22,.38),R.uniform(.075,.14),R.uniform(0,math.tau),R.uniform(-.7,.7),R.choices([0,1,2,3],[.45,.25,.1,.2])[0])
# Deliberate foreground and root-base plants; no random bush wall.
for u,v,sz in [(.02,.94,.65),(.09,.83,.45),(.05,.73,.45),(.90,.76,.55),(.98,.86,.65),(.80,.61,.32),(.62,.60,.28),(.35,.58,.35),(.14,.58,.3),(.97,.62,.4)]:
 p=ground(u,v,.016)
 for i in range(65):
  q=p+Vector((R.gauss(0,sz*.35),R.gauss(0,sz*.25),R.uniform(0,sz*.2)));leaf(q,R.uniform(.10,.30)*sz/.5,R.uniform(.03,.07)*sz/.5,R.uniform(0,math.tau),R.uniform(.2,1.4),R.randrange(4))
leaves=mesh('R03_lobed_felt_canopy_and_understory',vs,fs,olive,plants)
for m in [sage,gold,deep]:leaves.data.materials.append(m)
for f,i in zip(leaves.data.polygons,ids):f.material_index=i
solid=leaves.modifiers.new('R03_hand_cut_felt_thickness','SOLIDIFY');solid.thickness=.004
# Stream was below the support sheet in r02. Raise the visible cloth and shade banks.
water=bpy.data.objects['WATER_STREAM_CLOTH'];water.location.z=.028
wm=felt('R03_stream_sunset_reflection','A695A8',65);p=wm.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.36;p.inputs['Specular IOR Level'].default_value=.4;water.data.materials.clear();water.data.materials.append(wm)
# Enrich existing distant crowns with connected smaller lobes; retain their layout.
items=[]
for o in list(bpy.data.objects):
 if o.name.startswith('MID_wool_crown_'):
  o.hide_render=True
  o.location.z+=max(-.25,min(1.15,o.location.x*.07))+.18*math.sin(o.location.x*.6+o.location.y*.5)
  for i in range(14):
   p=o.location+Vector((R.uniform(-.36,.36),R.uniform(-.28,.28),R.uniform(-.30,.32)));sz=R.uniform(.15,.27);items.append((p,(sz*1.15,sz,sz*.95),R.randrange(3)))
far1=felt('R03_far_cool_foliage','4D635B',90);far2=felt('R03_far_lit_foliage','69785B',90);far3=felt('R03_far_deep_foliage','3D5553',90)
batch_blobs('R03_distant_layered_wool_crowns',items,[far1,far2,far3],background)
# Bushes bridge bare midground and the existing forest; clumps share a low mass.
items=[]
for u,v,size in [(.02,.51,.55),(.09,.52,.45),(.32,.54,.5),(.42,.52,.45),(.52,.49,.6),(.85,.53,.45),(.97,.52,.6)]:
 center=ground(u,v,.03)
 for i in range(85):
  d=Vector((R.gauss(0,size*.4),R.gauss(0,size*.3),0));height=max(.015,size*.55-d.length*.5);sz=R.uniform(.06,.15);items.append((center+d+Vector((0,0,height)),(sz*1.2,sz,sz*.8),R.randrange(3)))
batch_blobs('R03_midground_bush_transitions',items,[olive,sage,deep],plants)
for o in bpy.data.objects:
 if o.name.startswith('MID_tree_trunk_'):o.location.z+=max(-.25,min(1.15,o.location.x*.07))+.18*math.sin(o.location.x*.6+o.location.y*.5)
# Sky is shader geometry, no pasted approved plate. Use camera-plane UV and soft noise.
hide_prefix(('CLOUD_FELT_BAND_','MATTE_DUSK_SKY'))
mat=bpy.data.materials.new('R03_stratified_dusk_sky');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['UV'],sep.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(*rgb('FFB141'),1)
for pos,hx in [(.47,'FFAE40'),(.62,'F28A53'),(.79,'A86C8D'),(1,'6D6795')]:ramp.color_ramp.elements.new(pos).color=(*rgb(hx),1)
l.new(sep.outputs['Y'],ramp.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=190;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['UV'],noise.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.10;l.new(ramp.outputs[0],mix.inputs[1]);l.new(noise.outputs['Fac'],mix.inputs[2])
mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(8,48,1);l.new(tc.outputs['UV'],mapping.inputs[0]);cloudnoise=n.new('ShaderNodeTexNoise');cloudnoise.inputs['Scale'].default_value=1;cloudnoise.inputs['Detail'].default_value=4;cloudnoise.inputs['Roughness'].default_value=.7;cloudnoise.inputs['Distortion'].default_value=.3;l.new(mapping.outputs[0],cloudnoise.inputs[0]);mask=n.new('ShaderNodeValToRGB');mask.color_ramp.elements[0].position=.51;mask.color_ramp.elements[0].color=(0,0,0,1);mask.color_ramp.elements[1].position=.67;mask.color_ramp.elements[1].color=(.6,.6,.6,1);l.new(cloudnoise.outputs['Fac'],mask.inputs[0]);cloudcolor=n.new('ShaderNodeValToRGB');cloudcolor.color_ramp.elements[0].color=(*rgb('E38D57'),1);cloudcolor.color_ramp.elements[1].color=(*rgb('76617F'),1);l.new(sep.outputs['Y'],cloudcolor.inputs[0]);skyfinal=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],skyfinal.inputs[0]);l.new(mix.outputs[0],skyfinal.inputs[1]);l.new(cloudcolor.outputs[0],skyfinal.inputs[2]);l.new(skyfinal.outputs[0],em.inputs[0]);em.inputs[1].default_value=1.25;l.new(em.outputs[0],out.inputs[0])
ob=mesh('R03_camera_limited_shader_sky',[tuple(plane(u,v,97)) for u,v in [(-.2,1.2),(1.2,1.2),(1.2,-.2),(-.2,-.2)]],[(0,1,2,3)],mat,background);uv=ob.data.uv_layers.new()
for loop,co in zip(uv.data,[(-.2,-.2),(1.2,-.2),(1.2,1.2),(-.2,1.2)]):loop.uv=co
ob['envelope']='shallow sky shader plane; original narrow camera family only'
# Feathered-looking cloud banks from many uneven overlapping low wool puffs.
def emission(name,hx):
 m=bpy.data.materials.new(name);m.use_nodes=True;nd=m.node_tree.nodes;lk=m.node_tree.links;em=nd.new('ShaderNodeEmission');em.inputs[0].default_value=(*rgb(hx),1);em.inputs[1].default_value=.95;lk.new(em.outputs[0],nd.get('Material Output').inputs[0]);return m
cloudmats=[emission('R03_cloud_lavender','96718A'),emission('R03_cloud_warm_edge','DC896E'),emission('R03_cloud_sunlit','FFB45E')]
items=[]
for u,v,w in [(.11,.14,.27),(.22,.225,.3),(.17,.30,.30),(.42,.285,.22),(.47,.245,.25),(.14,.36,.25)]:
 for i in range(100):
  t=R.uniform(-1,1);uu=u+t*w*.5;vv=v+.006*math.sin(t*19)+R.gauss(0,.005)*(1-abs(t));p=plane(uu,vv,86);sx=R.uniform(.20,.65);items.append((p,(sx,.12,R.uniform(.07,.21)*(1-abs(t)*.7)),R.choices([0,1,2],[.55,.35,.1])[0]))
batch_blobs('R03_broken_dusk_cloud_layers',items,cloudmats,background)
bpy.data.objects['R03_broken_dusk_cloud_layers'].hide_render=True
# Restrained grazing sunset with readable cool shaded foliage.
bpy.data.objects['LIGHT_Sunset_far_left'].data.energy=2100;bpy.data.objects['LIGHT_Sunset_far_left'].data.color=(1,.57,.25);bpy.data.objects['LIGHT_Sunset_far_left'].data.size=3
bpy.data.objects['LIGHT_Dusk_soft_sky'].data.energy=650;bpy.data.objects['LIGHT_Neutral_readable_fill'].data.energy=130
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.20,.24,.37,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
s.cycles.samples=48;s.cycles.use_denoising=True;s.cycles.seed=510318;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s['environment_revision']='ENV_GreatTree_R03';s['approval_status']='refinement prototype / needs_revision / no owner approval';s['r03_source_environment_sha256']=sha(A/'assets/environments/great_tree/great_tree_environment_r02.blend')
s.render.filepath=str(P/'environment_wide.png');bpy.ops.wm.save_as_mainfile(filepath=str(ENV),compress=True)
inventory={'base_objects_retained':sorted(original_objects-set(bpy.data.objects.keys()))==[],'original_object_count':len(original_objects),'new_object_count':len(set(bpy.data.objects.keys())-original_objects),'objects':len(bpy.data.objects),'mesh_faces':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),'version':bpy.app.version_string,'environment_sha256':sha(ENV),'images':[{'name':im.name,'packed':bool(im.packed_file),'path':im.filepath} for im in bpy.data.images if im.source=='FILE'],'libraries':[x.filepath for x in bpy.data.libraries]}
(P/'build_inventory.json').write_text(json.dumps(inventory,indent=2))
# Preserve original shot assembly/proxies and migrate only its library reference.
bpy.ops.wm.open_mainfile(filepath=str(A/'scenes/lion_and_mouse_v6/s05_environment_r02.blend'),use_scripts=False)
for lib in bpy.data.libraries:
 if Path(bpy.path.abspath(lib.filepath)).name=='great_tree_environment_r02.blend':lib.filepath=str(ENV);lib.reload()
s=bpy.context.scene;s.camera=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];s['environment_library']=str(ENV.relative_to(ROOT));s['approval_status']='refinement prototype; owner review pending';s.cycles.seed=510318;s.cycles.samples=48;s.render.resolution_x=1280;s.render.resolution_y=720
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
print('REFINEMENT_R03_SAVED',flush=True)
