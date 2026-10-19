"""Reusable native wool kit. Import only: no scene reset, file writes or services."""
import bpy,math,random
from mathutils import Vector
R=random.Random(510400)
def rgb(h):
 v=[int(h[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in v)
def collection(name,parent):
 c=bpy.data.collections.new(name);parent.children.link(c);return c
def mesh(name,vs,fs,mat,c):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);c.objects.link(o)
 if mat:me.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 return o
def mat(name,family,colors):
 m=bpy.data.materials.new(name);m.use_nodes=True;m['craft_family']=family;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Roughness'].default_value=.92;p.inputs['Specular IOR Level'].default_value=.15;p.inputs['Sheen Weight'].default_value=.32;p.inputs['Sheen Roughness'].default_value=.8
 tc=n.new('ShaderNodeTexCoord');tc.name='REST_OBJECT_COORDINATES'
 def noise(name,scale,stretch,detail=3):
  v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=stretch;l.new(tc.outputs['Object'],v.inputs[0]);no=n.new('ShaderNodeTexNoise');no.name=name;no.inputs['Scale'].default_value=scale;no.inputs['Detail'].default_value=detail;no.inputs['Roughness'].default_value=.7;l.new(v.outputs[0],no.inputs[0]);return no
 stretch=(2.8,2.8,.32) if family=='bark' else ((1,1,2.5) if family=='path' else (1,1,1))
 meso=noise('FAMILY_MESO',8 if family=='bark' else (18 if family=='moss' else 12),stretch)
 micro=noise('SHORT_WOOL_MARLING',190 if family=='rock' else 125,(1,1.8,.65),2)
 ramp=n.new('ShaderNodeValToRGB');ramp.name='FAMILY_COLOR';ramp.color_ramp.elements[0].position=.16;ramp.color_ramp.elements[0].color=(*rgb(colors[0]),1);ramp.color_ramp.elements[1].position=.83;ramp.color_ramp.elements[1].color=(*rgb(colors[-1]),1)
 if len(colors)>2:ramp.color_ramp.elements.new(.5).color=(*rgb(colors[1]),1)
 l.new(meso.outputs['Fac'],ramp.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.name='HEATHER_COLOR';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.24 if family=='rock' else .12;l.new(ramp.outputs[0],mix.inputs[1]);l.new(micro.outputs['Fac'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.name='FINE_WOOL_NORMAL';b.inputs['Strength'].default_value=.37;b.inputs['Distance'].default_value=.006 if family=='rock' else .004;l.new(micro.outputs['Fac'],b.inputs['Height'])
 bb=n.new('ShaderNodeBump');bb.name='FAMILY_RELIEF';bb.inputs['Strength'].default_value={'bark':.35,'path':.17,'rock':.25,'moss':.32,'leaf':.16}.get(family,.2);bb.inputs['Distance'].default_value={'bark':.032,'path':.008,'rock':.012,'moss':.018,'leaf':.008}.get(family,.01);l.new(meso.outputs['Fac'],bb.inputs['Height']);l.new(b.outputs[0],bb.inputs['Normal']);l.new(bb.outputs[0],p.inputs['Normal']);m.diffuse_color=(*rgb(colors[len(colors)//2]),1)
 return m
def palette():
 return {'bark':mat('R04_WOOL_GROWTH_FOLDS','bark',['45382F','6B5140','8D7053']),
 'path':mat('R04_MATTED_EARTH_WOOL','path',['72553D','9D7751','B28B5F']),
 'moss':mat('R04_SOFT_OLIVE_CUSHION','moss',['3F4E2B','66743B','8A9150']),
 'mosslight':mat('R04_SUNLIT_MOSS_TIPS','moss',['606B36','81894A','A4A05D']),
 'rock':mat('R04_HEATHER_SLATE_WOOL','rock',['575A61','7B8084','ADB0AA']),
 'leaf':mat('R04_SAGE_FELT_LEAF','leaf',['3D523B','607449','8A955B']),
 'leafgold':mat('R04_OLIVE_FELT_LEAF','leaf',['565D2C','818541','A9A15C']),
 'deep':mat('R04_BLUEGREEN_FELT_LEAF','leaf',['2D4743','455E52','607866'])}
def ell(name,loc,scale,mat,c,seed=0,sub=3):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=name
 for col in list(o.users_collection):col.objects.unlink(o)
 c.objects.link(o)
 for v in o.data.vertices:
  q=v.co;f=1+.045*math.sin(q.x*5+seed)*math.sin(q.z*4+q.y*3)+.025*math.sin(q.y*9-seed);v.co=(q.x*scale[0]*f,q.y*scale[1]*f,q.z*scale[2]*f)
 o.data.materials.append(mat)
 for f in o.data.polygons:f.use_smooth=True
 return o
def tube(name,points,radii,mat,c,lobes=7):
 # Catmull-Rom centerline + smoothly transported ring; closed continuous volume.
 pts=[Vector(p) for p in points];vs=[];fs=[];samples=[];rr=[]
 for i in range(len(pts)-1):
  p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
  for j in range(12):
   t=j/12;t2=t*t;t3=t2*t;samples.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3));rr.append(radii[i]*(1-t)+radii[i+1]*t)
 samples.append(pts[-1]);rr.append(radii[-1]);seg=48
 for i,(p,rad) in enumerate(zip(samples,rr)):
  tangent=(samples[min(i+1,len(samples)-1)]-samples[max(0,i-1)]).normalized();u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u)
  for j in range(seg):
   a=j*math.tau/seg;r=rad*(1+.065*math.sin(a*lobes+.13*i)+.025*math.sin(a*13-.09*i));vs.append(tuple(p+r*(u*math.cos(a)+v*math.sin(a))))
 for i in range(len(samples)-1):
  for j in range(seg):a=i*seg+j;b=i*seg+(j+1)%seg;fs.append((a,b,b+seg,a+seg))
 fs.append(tuple(reversed(range(seg))));fs.append(tuple((len(samples)-1)*seg+j for j in range(seg)))
 return mesh(name,vs,fs,mat,c)
def fuse(objects,name,voxel=.04):
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
 rem=o.modifiers.new('Hand_unified_wool_mass','REMESH');rem.mode='VOXEL';rem.voxel_size=voxel;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
 sm=o.modifiers.new('Compressed_felt_softness','SMOOTH');sm.factor=.7;sm.iterations=4;bpy.ops.object.modifier_apply(modifier=sm.name)
 return o
def fibers(name,ob,mat,c,count=1500,length=.025,thickness=.0013,seed=51):
 r=random.Random(seed);data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=thickness;data.bevel_resolution=0;ob.data.calc_loop_triangles();tris=list(ob.data.loop_triangles)
 for i in range(count):
  tri=r.choice(tris);a,b,d=[ob.data.vertices[j] for j in tri.vertices];u=r.random();v=r.random()
  if u+v>1:u=1-u;v=1-v
  p=ob.matrix_world@(a.co*(1-u-v)+b.co*u+d.co*v);n=(ob.matrix_world.to_3x3()@(a.normal*(1-u-v)+b.normal*u+d.normal*v)).normalized();t=n.cross(Vector((r.random()+.1,r.random()+.1,r.random()+.1))).normalized();size=length*r.uniform(.55,1.2);sp=data.splines.new('POLY');sp.points.add(3)
  for j,pt in enumerate(sp.points):
   q=p+n*.002+t*size*(j/3)+n*size*.38*math.sin(math.pi*j/3);pt.co=(*q,1)
 o=bpy.data.objects.new(name,data);c.objects.link(o);data.materials.append(mat);o['surface_attachment']='static surface sampled; no animation qualification';return o
def leaf_proto(name,mat,c,family=0):
 vs=[];fs=[];segments=20
 for j in range(segments+1):
  t=j/segments;w=math.sin(math.pi*t)**.65*.36
  if family==1:w*=.84+.16*math.cos(t*math.pi*6)
  if family==2:w*=.64
  for k in range(7):
   u=(k-3)/3;vs.append((w*u,t,.12*math.sin(math.pi*t)+.13*u*u*math.sin(math.pi*t)+.12*t*t))
 for j in range(segments):
  for k in range(6):q=j*7+k;fs.append((q,q+1,q+8,q+7))
 o=mesh(name,vs,fs,mat,c);solid=o.modifiers.new('Dense_felt_edge_thickness','SOLIDIFY');solid.thickness=.035;bev=o.modifiers.new('Soft_cut_edge','BEVEL');bev.width=.018;bev.segments=2;return o
def instance(proto,name,loc,scale,rotation,c):
 o=proto.copy();o.data=proto.data;c.objects.link(o);o.name=name;o.location=loc;o.scale=scale;o.rotation_euler=rotation;return o
def ground_material(path,moss):
 m=path.copy();m.name='R04_CONTINUOUS_MATTED_CLEARING_EDGE';m['craft_family']='continuous_ground';n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tc=n.get('REST_OBJECT_COORDINATES');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0])
 def val(x):return x
 def op(kind,a,b=0):
  node=n.new('ShaderNodeMath');node.operation=kind
  for i,x in enumerate([a,b]):
   if isinstance(x,(int,float)):node.inputs[i].default_value=x
   else:l.new(x,node.inputs[i])
  return node.outputs[0]
 x=sep.outputs['X'];y=sep.outputs['Y'];center=op('ADD',op('MULTIPLY',op('SINE',op('MULTIPLY',y,.36)),1.1),.25)
 dist=op('SUBTRACT',op('ABSOLUTE',op('SUBTRACT',x,center)),.65)
 quiet=op('SUBTRACT',op('SQRT',op('ADD',op('MULTIPLY',op('MULTIPLY',x,.72),op('MULTIPLY',x,.72)),op('MULTIPLY',op('MULTIPLY',y,.70),op('MULTIPLY',y,.70)))),1.52)
 dist=op('MINIMUM',dist,quiet)
 no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=3.8;no.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],no.inputs[0]);dist=op('ADD',dist,op('MULTIPLY',op('SUBTRACT',no.outputs['Fac'],.5),.65))
 rem=n.new('ShaderNodeMapRange');rem.interpolation_type='SMOOTHERSTEP';rem.inputs['From Min'].default_value=-.30;rem.inputs['From Max'].default_value=.30;l.new(dist,rem.inputs['Value']);rem.name='PATH_EDGE_BLEND'
 grass=n.new('ShaderNodeValToRGB');grass.color_ramp.elements[0].color=(*rgb('465932'),1);grass.color_ramp.elements[1].color=(*rgb('82894D'),1);l.new(no.outputs['Fac'],grass.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.name='EARTH_TO_MATTED_GRASS';original=p.inputs['Base Color'].links[0].from_socket;l.new(original,mix.inputs[1]);l.new(grass.outputs[0],mix.inputs[2]);l.new(rem.outputs[0],mix.inputs[0]);l.new(mix.outputs[0],p.inputs['Base Color']);return m
def camera(name,loc,target,lens,c):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);c.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.sensor_width=36;d.clip_end=300;d.clip_start=.01;return o
def area(name,loc,target,power,color,size,c):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);c.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
