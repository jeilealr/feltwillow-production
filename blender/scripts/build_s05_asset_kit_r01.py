"""Isolated licensed sample comparisons; never opens/saves the S05 environment."""
import bpy,sys,math,random,json,hashlib,time,resource
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'blender';P=A/'renders/s05_asset_kit_r01';W=ROOT/'work/blender/external_assets/s05_kit_r01';OUT=W/'tests/s05_external_craft_kit_r01.blend';sys.path.insert(0,str(A/'scripts'));import craft_scene05_r04 as c
assert not OUT.exists(),'Preserve existing sample revision'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=.2;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True;s.cycles.seed=510501;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
root=c.collection('S05_EXTERNAL_CRAFT_SAMPLE_R01',s.collection);prior=c.collection('01_PRIOR_NATIVE_R04_RECIPE',root);raw=c.collection('02_IMPORTED_BASELINE',root);adapt=c.collection('03_FELTWILLOW_ADAPTED',root);original=c.collection('RAW_IMPORTS_UNMODIFIED',root);original.hide_render=True;original.hide_viewport=True;lights=c.collection('SAMPLE_LIGHTS',s.collection);cams=c.collection('SAMPLE_CAMERAS',s.collection);groundcol=c.collection('SAMPLE_STAGE_SUPPORT',s.collection)
m=c.palette();r=random.Random(510501)
stageground=c.mat('SAMPLE_STUDIO_GREY_FELT','path',['777A7D','8F9293','9B9D9D']);floor=c.mesh('SAMPLE_STAGE_GROUND',[(-8,-6,-.012),(8,-6,-.012),(8,7,-.012),(-8,7,-.012)],[(0,1,2,3)],stageground,groundcol)
wide=c.camera('CAM_SAMPLE_SHOT_DISTANCE',(.4,-6.0,2.8),(.05,.25,.35),45,cams);close=c.camera('CAM_SAMPLE_CLOSE',(0,-4.0,2.3),(-.2,.25,.3),58,cams)
s.world=bpy.data.worlds.new('SAMPLE_FIXED_WORLD');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.28,.31,.36,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.24
key=c.area('SAMPLE_KEY',(-3,-2,5),(0,.3,.2),750,(1,1,1),4,lights);fill=c.area('SAMPLE_FILL',(3,2,4),(0,.3,.2),280,(1,1,1),4,lights)
# Four GLBs only; bundled material JSON inspected before import. No bundled scripts run.
imports={};audit=[]
for name in ['stump_roundDetailed','rock_largeA','grass_leafsLarge','plant_bushDetailed']:
 f=W/'selected/kenney'/(name+'.glb');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(f));obs=[o for o in bpy.data.objects if o not in before and o.type=='MESH'];assert len(obs)==1
 o=obs[0];bpy.context.view_layer.update();verts=[o.matrix_world@v.co for v in o.data.vertices];lo=Vector(tuple(min(v[i] for v in verts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in verts) for i in range(3)))
 audit.append({'asset':name,'file_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'uv_layers':[x.name for x in o.data.uv_layers],'source_world_bounds':[list(lo),list(hi)],'scale':list(o.scale),'negative_scale':any(x<0 for x in o.scale),'materials':[{'name':x.name,'alpha':x.node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value if x.use_nodes else None} for x in o.data.materials],'source_images':len(bpy.data.images),'animations':len(bpy.data.actions),'drivers':bool(o.animation_data and o.animation_data.drivers),'unit_note':'glTF meters; normalized explicitly to miniature BU, not treated as character scale','autoexec_disabled':True})
 # Convert only coordinate basis in editable imported data; raw file remains unchanged.
 me=o.data.copy()
 for v,world in zip(me.vertices,verts):v.co=world
 o.data=me;o.matrix_world.identity();o.name='RAW_KENNEY_'+name
 for col in list(o.users_collection):col.objects.unlink(o)
 original.objects.link(o);imports[name]=o
def copy_normalized(source,name,target,height,col):
 o=source.copy();o.data=source.data.copy();col.objects.link(o);o.name=name;lo=Vector(tuple(min(v.co[i] for v in o.data.vertices) for i in range(3)));hi=Vector(tuple(max(v.co[i] for v in o.data.vertices) for i in range(3)));center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));scale=height/(hi.z-lo.z)
 for v in o.data.vertices:v.co=(v.co-center)*scale
 o.location=target;o['source_asset']='Kenney Nature Kit2.1 CC0';o['normalized_height_bu']=height
 return o
# Preserve the prior native craft recipe as actual comparison objects.
rod=c.tube('PRIOR_isolated_approach_root',[(-2.0,.20,.10),(-1.65,.2,.09),(-1.05,.15,.045),(-.75,.10,.01)],[.11,.09,.055,.008],m['bark'],prior)
mos=c.fuse([c.ell('prior_moss_part',(-.25,.45,.08),(.48,.28,.13),m['moss'],prior,5,3),c.ell('prior_moss_part',(-.04,.47,.08),(.32,.25,.12),m['moss'],prior,7,3)],'PRIOR_moss_cushion',.024);c.fibers('PRIOR_moss_short_wool',mos,m['mosslight'],prior,1800,.020,.0013,51)
rock=c.ell('PRIOR_heather_rock',(.90,.45,.26),(.45,.34,.31),m['rock'],prior,3,4);c.fibers('PRIOR_rock_edge',rock,m['rock'],prior,1200,.013,.001,52)
leaf=c.leaf_proto('PRIOR_leaf',m['leaf'],prior,1);leaf.location=(1.65,.22,.02);leaf.scale=(.45,.55,.55);leaf.rotation_euler=(.6,0,-.6)
pathprior=c.mesh('PRIOR_path_edge',[(-.70,-.50,.001),(.50,-.50,.001),(.50,.05,.001),(-.70,.05,.001)],[(0,1,2,3)],c.ground_material(m['path'],m['moss']),prior)
# Import baseline: selected geometry + unadapted plush maps on unchanged curved samples.
stump=copy_normalized(imports['stump_roundDetailed'],'IMPORT_stump',(-1.55,.4,.005),.72,raw)
rawrock=copy_normalized(imports['rock_largeA'],'IMPORT_rock',(.9,.45,.005),.55,raw);rawleaf=copy_normalized(imports['grass_leafsLarge'],'IMPORT_leaf_cluster',(1.65,.3,.005),.5,raw)
rawbush=copy_normalized(imports['plant_bushDetailed'],'IMPORT_bush_example',(1.5,1.25,.005),.45,raw)
maps={}
for role,suffix in [('diff','diff_1k.jpg'),('height','disp_1k.png'),('normal','nor_gl_1k.png'),('rough','rough_1k.png')]:
 im=bpy.data.images.load(str(W/'originals/polyhaven_curly_teddy_natural_1k'/('curly_teddy_natural_'+suffix)),check_existing=True)
 if role!='diff':im.colorspace_settings.name='Non-Color'
 maps[role]=im
def textile(name,adapted=False,color='6C773E',scale=.667):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF');p.inputs['Metallic'].default_value=0;p.inputs['Specular IOR Level'].default_value=.16 if adapted else .3;p.inputs['Roughness'].default_value=.92;p.inputs['Sheen Weight'].default_value=.32 if adapted else .1
 tc=n.new('ShaderNodeTexCoord');multiply=n.new('ShaderNodeVectorMath');multiply.operation='SCALE';multiply.inputs[3].default_value=scale;l.new(tc.outputs['Object'],multiply.inputs[0]);tex={}
 for role,im in maps.items():
  t=n.new('ShaderNodeTexImage');t.name='PH_CURLY_TEDDY_'+role;t.image=im;t.projection='BOX' if adapted else 'FLAT';t.projection_blend=.3;l.new(multiply.outputs[0] if adapted else tc.outputs['UV'],t.inputs[0]);tex[role]=t
 if adapted:
  grey=n.new('ShaderNodeRGBToBW');l.new(tex['diff'].outputs[0],grey.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.65 for x in c.rgb(color)],1);ramp.color_ramp.elements[1].color=(*[x*1.08 for x in c.rgb(color)],1);l.new(grey.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
 else:l.new(tex['diff'].outputs[0],p.inputs['Base Color'])
 normal=n.new('ShaderNodeNormalMap');normal.space='TANGENT';normal.inputs['Strength'].default_value=.3 if adapted else 1;l.new(tex['normal'].outputs[0],normal.inputs['Color'])
 # Tri-planar box projection has no tangent frame: use height response for adapted shaders.
 # The raw normal baseline instead uses UV tangent coordinates below, not Object normals.
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.22 if adapted else .6;b.inputs['Distance'].default_value=.008 if adapted else .025;l.new(tex['height'].outputs[0],b.inputs['Height'])
 if not adapted:l.new(normal.outputs[0],b.inputs['Normal'])
 l.new(b.outputs[0],p.inputs['Normal'])
 if adapted:p.inputs['Roughness'].default_value=.95
 else:l.new(tex['rough'].outputs[0],p.inputs['Roughness'])
 mat.diffuse_color=(*c.rgb(color if adapted else 'BAAD96'),1);mat['provenance']='Poly Haven Curly Teddy Natural; Rico Cilliers/colormass; CC0';mat['map_role']='Adapted: color marling + height-to-bump; normal/rough loaded but inactive. Raw: diffuse/normalGL/rough/height.';return mat
rawtextile=textile('IMPORT_PH_PLUSH_BASELINE',False)
rawmos=mos.copy();rawmos.data=mos.data.copy();raw.objects.link(rawmos);rawmos.name='IMPORT_same_cushion_raw_plush';rawmos.data.materials.clear();rawmos.data.materials.append(rawtextile)
rawpath=pathprior.copy();rawpath.data=pathprior.data.copy();raw.objects.link(rawpath);rawpath.name='IMPORT_same_path_raw_plush';rawpath.data.materials.clear();rawpath.data.materials.append(rawtextile)
for o in [rawmos,rawpath]:
 uv=o.data.uv_layers.new(name='SAMPLE_PLANAR_UV_0p3m')
 for loop in o.data.loops:
  p=o.matrix_world@o.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(p.x*.667,p.y*.667)
# Felt adaptation: rooted chopped stump; different scale-dependent use of same map.
astump=copy_normalized(imports['stump_roundDetailed'],'ADAPT_stump_volume',(-1.55,.4,.005),.72,adapt)
for f in astump.data.polygons:f.use_smooth=True
bev=astump.modifiers.new('Soft_cut_stump_edges','BEVEL');bev.width=.035;bev.segments=3;bpy.context.view_layer.objects.active=astump;astump.select_set(True);bpy.ops.object.modifier_apply(modifier=bev.name)
astump.data.materials.clear();astump.data.materials.append(m['bark'])
rootparts=[astump]
for i,(points,radii) in enumerate([([(-1.55,.4,.25),(-1.2,.15,.10),(-.85,-.10,.04),(-.62,-.25,-.015)],[.20,.13,.07,.008]),([(-1.65,.5,.2),(-1.95,.35,.10),(-2.2,.17,.015)],[.17,.11,.006]),([(-1.65,.55,.22),(-1.7,.85,.09),(-1.8,1.0,.015)],[.16,.09,.006])]):rootparts.append(c.tube('ADAPT_stump_root_%d'%i,points,radii,m['bark'],adapt,5))
astump=c.fuse(rootparts,'ADAPT_ROOTED_CHOPPED_STUMP',.018);top=c.mat('ADAPT_cut_end_compressed_wool','bark',['8A7053','AB926D','C5AC81']);astump.data.materials.append(top)
for f in astump.data.polygons:
 if f.center.z>.55 and f.normal.z>.70:f.material_index=1
c.fibers('ADAPT_stump_sparse_felt_edge',astump,m['bark'],adapt,1500,.012,.0011,58)
# Endgrain is modeled as restrained felt seams, not a photograph painted on a cap.
for i,rad in enumerate([.15,.23]):
 data=bpy.data.curves.new('ADAPT_cut_felt_ring_data','CURVE');data.dimensions='3D';data.bevel_depth=.004;sp=data.splines.new('POLY');sp.points.add(63)
 for j,pt in enumerate(sp.points):
  a=math.tau*j/64;rr=rad*(1+.035*math.sin(a*5+i));pt.co=(-1.55+rr*math.cos(a),.4+rr*.8*math.sin(a),.71+.005*math.sin(a*3),1)
 sp.use_cyclic_u=True;o=bpy.data.objects.new('ADAPT_CUT_FELT_SEAM_%d'%i,data);adapt.objects.link(o);data.materials.append(m['bark'])
adaptmos=mos.copy();adaptmos.data=mos.data.copy();adapt.objects.link(adaptmos);adaptmos.name='ADAPT_compressed_moss_cushion';adaptmos.data.materials.clear();adaptmos.data.materials.append(textile('ADAPT_PH_COMPRESSED_MOSS',True,'66783E',1.5));c.fibers('ADAPT_moss_short_pile',adaptmos,m['mosslight'],adapt,2200,.015,.0011,59)
adaptpath=pathprior.copy();adaptpath.data=pathprior.data.copy();adapt.objects.link(adaptpath);adaptpath.name='ADAPT_matted_path_edge';adaptpath.data.materials.clear();groundmat=c.ground_material(m['path'],m['moss']);adaptpath.data.materials.append(groundmat)
# Existing approved PATINA roughness is reused as a bounded variation, not metal.
pat=bpy.data.images.load(str(A/'assets/materials/leo_felt_patina_trial/roughness.png'),check_existing=True);pat.colorspace_settings.name='Non-Color';n=groundmat.node_tree.nodes;l=groundmat.node_tree.links;p=n.get('Principled BSDF');t=n.new('ShaderNodeTexImage');t.name='EXISTING_PATINA_ROUGHNESS_TRIAL';t.image=pat;t.projection='BOX';t.projection_blend=.3;tc=n.get('REST_OBJECT_COORDINATES');l.new(tc.outputs['Object'],t.inputs[0]);rem=n.new('ShaderNodeMapRange');rem.inputs['To Min'].default_value=.82;rem.inputs['To Max'].default_value=.98;l.new(t.outputs[0],rem.inputs['Value']);l.new(rem.outputs[0],p.inputs['Roughness'])
arock=copy_normalized(imports['rock_largeA'],'ADAPT_HEATHER_ROCK',(.9,.45,.005),.55,adapt);arock.data.materials.clear();arock.data.materials.append(m['rock']);arock.data.materials.append(m['rock'])
bev=arock.modifiers.new('Soft_rock_edges','BEVEL');bev.width=.045;bev.segments=3;sub=arock.modifiers.new('Dense_rounded_wool_form','SUBSURF');sub.levels=2
for f in arock.data.polygons:f.use_smooth=True
# Imported broad-leaf mesh has source volume; round, thicken and give cupped felt material.
aleaf=copy_normalized(imports['grass_leafsLarge'],'ADAPT_FELT_LEAF_CLUSTER',(1.65,.3,.005),.5,adapt);aleaf.data.materials.clear();aleaf.data.materials.append(m['leaf']);aleaf.data.materials.append(m['leaf'])
bev=aleaf.modifiers.new('Rounded_felt_leaf_edges','BEVEL');bev.width=.014;bev.segments=3;sub=aleaf.modifiers.new('Smooth_felt_tabs','SUBSURF');sub.levels=2
for f in aleaf.data.polygons:f.use_smooth=True
abush=copy_normalized(imports['plant_bushDetailed'],'ADAPT_BUSH_SHAPE_TEST',(1.5,1.25,.005),.45,adapt);abush.data.materials.clear();abush.data.materials.append(m['leaf']);sub=abush.modifiers.new('Soft_bush_form','SUBSURF');sub.levels=2
for f in abush.data.polygons:f.use_smooth=True
for im in bpy.data.images:
 if im.source=='FILE':im.pack();im.filepath=bpy.path.relpath(im.filepath,start=str(OUT.parent))
s.camera=wide;s['mode']='reference_inspired';s['status']='isolated sample kit; owner review pending; no S05 integration';s['source_credit']='Selected material maps: Poly Haven (CC0), mesh bases: Kenney NatureKit2.1 (CC0).';s['scope']='No character or production changes. Stump is owner-directed sample, not integrated story prop.';s['external_code']='GLB data only, autoexec disabled; no scripts/drivers imported'
prior.hide_render=True;raw.hide_render=True;adapt.hide_render=False;bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
(P/'import_inspection.json').write_text(json.dumps({'assets':audit,'auto_execution_disabled':True,'no_external_scripts_run':True,'source_formats':'GLB2 embedded data; PNG/JPG images','packed_images':[{'name':im.name,'size':list(im.size),'color_space':im.colorspace_settings.name,'packed':bool(im.packed_file)} for im in bpy.data.images if im.source=='FILE'],'raw_source_unchanged':True,'warnings':['No source unit metadata beyond glTF meter convention; explicit miniature normalization.','Source UVs may only supply flat-color layout; adapted object-space height uses stable scale.','Raw imported normal interpretation must be judged; photographic plush is not needle felt.','Bush geometry may remain unsuitable despite smoothing; no mass distribution.','No temporal stability proof from stills.']},indent=2))
records=[]
for lightname,dusk in [('neutral',False),('dusk',True)]:
 key.data.color=(1,.66,.36) if dusk else (1,1,1);fill.data.color=(.56,.70,1) if dusk else (1,1,1)
 for stage,col in [('prior',prior),('imported',raw),('adapted',adapt)]:
  for other in [prior,raw,adapt]:other.hide_render=other!=col
  for camera,width in [(wide,1280),(close,1280)]:
   s.camera=camera;s.render.resolution_x=width;s.render.resolution_y=720;s.cycles.samples=40;name=stage+'_'+lightname+('_shot' if camera==wide else '_close');s.render.filepath=str(P/(name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
   records.append({'name':name,'sha256':hashlib.sha256((P/(name+'.png')).read_bytes()).hexdigest(),'sample_blend_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'stage':stage,'light':lightname,'camera':camera.name,'matrix':[list(x) for x in camera.matrix_world],'lens':camera.data.lens,'resolution':[1280,720],'samples':40,'seed':510501,'denoising':True,'color':['Standard','None',0,1],'seconds':round(elapsed,3),'process_maxrss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'memory_note':'Measured cumulative peak resident set for this process, not per-asset allocation or benchmark.'});(P/'render_manifest.json').write_text(json.dumps(records,indent=2));print('SAMPLE_RENDER',name,flush=True)
print('ISOLATED_KIT_COMPLETE',flush=True)
