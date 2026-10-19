"""Bounded, local-only canonical candidate from the owner's preserved FBX.

blender --background --factory-startup --disable-autoexec --python-exit-code 1
  --python blender/scripts/leo_tripo_canonical_pass.py
Arguments after --: --build-only, --review-only, --audit-only.
"""
import bpy, bmesh, math, json, hashlib, sys, random, bisect, time
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender'
RAW=AREA/'assets/characters/leo/imports/tripo_owner_model'
OUT=AREA/'assets/characters/leo/leo_canonical_tripo_candidate_r01.blend'
REVIEW=AREA/'renders/leo_tripo_canonical_r01';REVIEW.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(AREA/'scripts'))
import build as h
SEED=18102603;RNG=random.Random(SEED)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
SOURCES={
 'blender/assets/characters/leo/imports/tripo_owner_model/model.fbx':'3ccead17de1785f9c0d0fa8b3d1f3d531ad8b0d433fba31091f601bda883b9b2',
 'character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png':'6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545',
 'character/characters/lion_and_mouse_v6/Leo/references/l_complete_reference_r01_candidate.png':'73aa4429cc91cd28060ca3b4fcfd42464974429a328d5ab53c3779fc1485048c'}

VIEWS={
 'front':((0,-8,.79),(0,.10,.79),2.20),
 'left':((-8,0,.79),(0,.10,.79),2.50),
 'right':((8,0,.79),(0,.10,.79),2.50),
 'rear':((0,8,.79),(0,.10,.79),2.20),
 'front_three_quarter':((-2.7,-4,1.65),(0,.05,.79),2.5),
 'rear_three_quarter':((-3,4,1.8),(0,.05,.79),2.5),
 'elevated_three_quarter':((-2.8,-4,3),(0,.05,.79),2.7),
 'portrait':((-2,-5,1.28),(0,-.52,1.13),1.43)}

def camera(view):
    loc,target,scale=VIEWS[view];c=bpy.context.scene.camera;c.location=loc
    c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale;c.data.dof.use_dof=False

def neutral():
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True;s.cycles.seed=SEED
    s.render.resolution_x=768;s.render.resolution_y=768;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.film_transparent=False
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    s.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
    for name,energy in [('Neutral_key',230),('Neutral_fill',135),('Neutral_rim',150)]:
        bpy.data.objects[name].data.energy=energy;bpy.data.objects[name].data.color=(1,1,1)

def build():
    for path,expected in SOURCES.items():
        if sha(ROOT/path)!=expected:raise RuntimeError('Source changed: '+path)
    bpy.ops.wm.open_mainfile(filepath=str(RAW/'leo_import_untouched.blend'),use_scripts=False)
    s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=.2
    asset=bpy.data.collections.new('LEO_TRIPO_CANDIDATE_R01');s.collection.children.link(asset)
    mesh=next(o for o in s.objects if o.type=='MESH');mesh.name='Leo_surface'
    for c in list(mesh.users_collection):c.objects.unlink(mesh)
    asset.objects.link(mesh)
    # Recorded uniform normalization, not anatomical reshaping. +X import -> -Y.
    world=mesh.matrix_world.copy();rot=Matrix.Rotation(-math.pi/2,4,'Z')
    points=[rot@world@v.co for v in mesh.data.vertices]
    zmin=min(p.z for p in points);zmax=max(p.z for p in points);scale=1.5/(zmax-zmin)
    for v,p in zip(mesh.data.vertices,points):v.co=Vector((p.x*scale,p.y*scale,(p.z-zmin)*scale))
    mesh.matrix_world=Matrix.Identity(4)
    mesh.data.update()
    for f in mesh.data.polygons:f.use_smooth=True
    root=bpy.data.objects.new('Leo_ASSET_ROOT',None);asset.objects.link(root);mesh.parent=root
    root['approval']='unapproved canonical candidate';root['forward']='-Y';root['unit_m']=.2
    root['normalization_uniform_scale']=scale;root['import_zmin']=zmin;root['import_rotation_z_deg']=-90
    root['raw_fbx_sha256']=SOURCES[str((RAW/'model.fbx').relative_to(ROOT))]
    # Material structure: preserve color/normal maps, clamp wool to matte nonmetal.
    m=mesh.data.materials[0];m.name='Leo_import_palette_felt_r01';p=m.node_tree.nodes.get('Principled BSDF');links=m.node_tree.links
    for socket in ('Metallic','Roughness'):
        for link in list(p.inputs[socket].links):links.remove(link)
    p.inputs['Metallic'].default_value=0;p.inputs['Roughness'].default_value=.92
    p.inputs['Specular IOR Level'].default_value=.22;p.inputs['Sheen Weight'].default_value=.12;p.inputs['Sheen Roughness'].default_value=.8
    for n in m.node_tree.nodes:
        if n.type=='NORMAL_MAP':n.inputs['Strength'].default_value=.55
    for im in bpy.data.images:
        if not im.packed_file:im.pack()
        # Point the packed image at a portable repository-local original map.
        name={ '_0':'Color.jpg','_1':'Roughness.jpg','_2':'Metallic.jpg','_3':'Normal.png' }
        for suffix,filename in name.items():
            if im.name.endswith(suffix):im.filepath=str(RAW/filename)
    # Attach subtle wool in UV/material regions, retaining stable albedo colors.
    h.COL=asset;h.PARTS=[]
    mesh.data.calc_loop_triangles();tris=list(mesh.data.loop_triangles);acc=[];total=0
    for tr in tris:total+=tr.area;acc.append(total)
    c=bpy.data.curves.new('Leo_short_wool_stable_UV','CURVE');c.dimensions='3D';c.bevel_depth=.00023;c.bevel_resolution=0
    uv=mesh.data.uv_layers.active.data
    # Shared packed color atlas; curve UVs use per-corner interpolated source UV.
    uv_coords=[]
    for k in range(36000):
        tr=tris[bisect.bisect_left(acc,RNG.random()*total)]
        u=RNG.random();v=RNG.random()
        if u+v>1:u=1-u;v=1-v
        a,b,d=[mesh.data.vertices[i] for i in tr.vertices];pos=a.co*(1-u-v)+b.co*u+d.co*v
        normal=(a.normal*(1-u-v)+b.normal*u+d.normal*v).normalized()
        # Avoid facial features: eye/nose/muzzle region needs clean readable edges.
        if pos.y<-.58 and abs(pos.x)<.33 and .76<pos.z<1.38:continue
        tangent=normal.cross(Vector((RNG.random(),RNG.random(),RNG.random()))).normalized()
        length=RNG.uniform(.003,.007);sp=c.splines.new('POLY');sp.points.add(4)
        for j,pt in enumerate(sp.points):
            t=j/4;q=pos+normal*(.0006+math.sin(t*math.pi)*length*.32)+tangent*(length*t)
            pt.co=(*q,1)
        uv_coords.append(uv[tr.loops[0]].uv*(1-u-v)+uv[tr.loops[1]].uv*u+uv[tr.loops[2]].uv*v)
    wool=bpy.data.objects.new('Leo_attached_short_wool',c);asset.objects.link(wool);wool.parent=root
    # Convert static candidate fibers to a lightweight mesh to carry true source UV.
    bpy.ops.object.select_all(action='DESELECT');wool.select_set(True);bpy.context.view_layer.objects.active=wool
    bpy.ops.object.convert(target='MESH');wool=bpy.context.object
    # Each poly strand produces (5*4)=20 vertices with bevel_resolution 0.
    # Derive connected strands from geometry instead of assuming a tessellation count.
    parent=list(range(len(wool.data.vertices)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for e in wool.data.edges:
        a,b=e.vertices;parent[find(b)]=find(a)
    groups={}
    for i in range(len(parent)):groups.setdefault(find(i),[]).append(i)
    strands=sorted(groups.values(),key=lambda g:min(g));assert len(strands)==len(uv_coords)
    # Associate converted strand geometry by spatial proximity, not spline order:
    # conversion can reorder disconnected strands and swap their palette regions.
    from mathutils.bvhtree import BVHTree
    from mathutils.geometry import barycentric_transform
    tree=BVHTree.FromPolygons([v.co for v in mesh.data.vertices],[tr.vertices for tr in tris],all_triangles=True)
    per_vertex={}
    for ids in strands:
        center=sum((wool.data.vertices[i].co for i in ids),Vector())/len(ids)
        point,normal,idx,distance=tree.find_nearest(center);tr=tris[idx]
        a,b,d=[mesh.data.vertices[i].co for i in tr.vertices]
        ua,ub,ud=[Vector((*uv[i].uv,0)) for i in tr.loops]
        mapped=barycentric_transform(point,a,b,d,ua,ub,ud)
        for i in ids:per_vertex[i]=mapped.xy
    layer=wool.data.uv_layers.new(name='Source_palette_UV')
    for loop in wool.data.loops:layer.data[loop.index].uv=per_vertex[loop.vertex_index]
    fm=m.copy();fm.name='Leo_short_wool_palette';pp=fm.node_tree.nodes.get('Principled BSDF')
    for link in list(pp.inputs['Normal'].links):fm.node_tree.links.remove(link)
    pp.inputs['Roughness'].default_value=.97;pp.inputs['Sheen Weight'].default_value=.06
    wool.data.materials.append(fm)
    # Pale fine whiskers, source omitted them. Roots/length explicitly reviewable.
    whisker=h.felt('Leo_cream_whisker',(.86,.72,.48),200,.04)
    for side,sign in [('L',-1),('R',1)]:
        for i in range(3):
            root_x=sign*.12;root_z=.925-i*.014
            hit,_,_,_=tree.ray_cast(Vector((root_x,-2,root_z)),Vector((0,1,0)))
            y=hit.y-.001 if hit else -.96
            o=h.curve('Leo_whisker_'+side+'_'+str(i),[(root_x,y,root_z),(sign*.25,y+.012,root_z+.015-i*.012),(sign*.37,y+.05,root_z+.030-i*.024)],.00065,whisker)
            o.parent=root
    # A simple non-rendering landmark guide, explicitly not an animation rig.
    guides=bpy.data.collections.new('LEO_RIG_PLAN_GUIDES');s.collection.children.link(guides)
    landmarks={'pelvis':(0,.47,.56),'chest':(0,-.20,.66),'neck':(0,-.38,.89),'head':(0,-.46,1.13),
      'paw.front.L':(-.20,-.46,.06),'paw.front.R':(.20,-.46,.06),
      'paw.hind.L':(-.21,.57,.06),'paw.hind.R':(.21,.57,.06),'tail.root':(0,.74,.67)}
    for name,pos in landmarks.items():
        o=bpy.data.objects.new('GUIDE_'+name,None);guides.objects.link(o);o.location=pos;o.empty_display_size=.035;o.hide_render=True;o.parent=root
        o['status']='provisional landmark: fit before binding'
    studio=bpy.data.collections.new('LEO_REVIEW_STUDIO');s.collection.children.link(studio);h.COL=studio
    h.settings();floor=h.felt('Leo_review_floor',(.77,.77,.77),60,.015)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));h.register(bpy.context.object,'Review_floor',floor)
    h.area('Neutral_key',(-3,-4,5),(0,0,.75),230,(1,1,1),4)
    h.area('Neutral_fill',(3,-2,3),(0,0,.75),135,(1,1,1),3)
    h.area('Neutral_rim',(0,3,4),(0,0,.75),150,(1,1,1),3)
    h.camera('Leo_review_camera',(2.7,-4,1.65),(0,.05,.79),ortho=2.5)
    neutral();camera('front_three_quarter')
    s['approval_status']='promising_imported_prototype_needs_owner_review';s['seed']=SEED
    s['geometry_policy']='Imported surface topology preserved; uniform normalization only; added separate wool/whiskers'
    s['mouth_policy']='neutral closed; no added teeth';s['rig_status']='landmark guide and written plan only; not bound'
    s['source_bindings']=json.dumps(SOURCES,sort_keys=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
    # save_as_mainfile remaps packed image labels; use actual relative paths.
    print('LEO_TRIPO_CANDIDATE_SAVED',OUT,flush=True)

def audit():
    bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False)
    o=bpy.data.objects['Leo_surface'];me=o.data
    bm=bmesh.new();bm.from_mesh(me)
    nonmanifold=sum(not e.is_manifold for e in bm.edges);boundary=sum(e.is_boundary for e in bm.edges);bm.free()
    parent=list(range(len(me.vertices)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for e in me.edges:
        a,b=e.vertices;parent[find(b)]=find(a)
    comp={}
    for v in me.vertices:comp.setdefault(find(v.index),[]).append(v.index)
    components=[]
    for ids in sorted(comp.values(),key=len,reverse=True):
        components.append({'vertices':len(ids),'min':[min(me.vertices[i].co[j] for i in ids) for j in range(3)],
          'max':[max(me.vertices[i].co[j] for i in ids) for j in range(3)]})
    # Compare normalized mesh with raw imported data, index by index.
    candidate_images=list(bpy.data.images)
    original_library_count=len(bpy.data.libraries)
    with bpy.data.libraries.load(str(RAW/'leo_import_untouched.blend'),link=False) as (src,dst):dst.meshes=list(src.meshes)
    raw=dst.meshes[0];root=bpy.data.objects['Leo_ASSET_ROOT'];scale=root['normalization_uniform_scale'];zmin=root['import_zmin']
    rot=Matrix.Rotation(-math.pi/2,4,'Z')
    max_error=max((me.vertices[i].co-Vector(((rot@v.co).x*scale,(rot@v.co).y*scale,((rot@v.co).z-zmin)*scale))).length for i,v in enumerate(raw.vertices))
    bpy.data.meshes.remove(raw)
    p=o.data.materials[0].node_tree.nodes.get('Principled BSDF')
    checks={'source_hashes_unchanged':all(sha(ROOT/path)==expected for path,expected in SOURCES.items()),
      'source_mesh_vertex_and_face_counts_preserved':len(me.vertices)==48753 and len(me.polygons)==48742,
      'uniform_normalization_coordinate_error_below_1e-6':max_error<1e-6,
      'uv_layer_present':len(me.uv_layers)>0,'all_four_images_packed':len(candidate_images)==4 and all(im.packed_file for im in candidate_images),
      'no_external_linked_libraries':original_library_count==0,
      'no_embedded_scripts':len(bpy.data.texts)==0,'non_metal_felt':p.inputs['Metallic'].default_value==0,
      'six_whisker_curves':len([ob for ob in bpy.data.objects if ob.name.startswith('Leo_whisker_')])==6,
      'neutral_height_1_5':abs(max(v.co.z for v in me.vertices)-1.5)<1e-5,
      'lowest_vertex_at_ground':abs(min(v.co.z for v in me.vertices))<1e-5,
      'unbound_mesh_not_misrepresented_as_rigged':not any(mod.type=='ARMATURE' for mod in o.modifiers)}
    # Paw-region heights are diagnostics, not semantic counts inferred from names.
    paw_regions={}
    for end,(lo,hi) in {'front':(-.8,-.1),'hind':(.20,.85)}.items():
        for side,(xmin,xmax) in {'L':(-.5,-.055),'R':(.055,.5)}.items():
            vs=[v.co for v in me.vertices if lo<v.co.y<hi and xmin<v.co.x<xmax and v.co.z<.2]
            paw_regions[end+'.'+side]={'sample_vertices':len(vs),'min_z':min((v.z for v in vs),default=None)}
    report={'candidate':str(OUT.relative_to(ROOT)),'sha256':sha(OUT),'source_hashes':SOURCES,
      'blender':bpy.app.version_string,'counts':{'vertices':len(me.vertices),'faces':len(me.polygons),
      'quads':sum(len(f.vertices)==4 for f in me.polygons),'triangles':sum(len(f.vertices)==3 for f in me.polygons),
      'ngons':sum(len(f.vertices)>4 for f in me.polygons),'nonmanifold_edges':nonmanifold,'boundary_edges':boundary,'connected_components':len(components)},
      'components':components,'normalization_max_coordinate_error':max_error,'paw_region_ground_diagnostics':paw_regions,
      'checks':checks,'check_failures':[k for k,v in checks.items() if not v],
      'rig_suitability':'No weights/rig; quad count does not establish joint edge flow; inspect shoulders/hips/neck before binding.',
      'not_tested':['UV overlap','geometric self-intersection','animation deformation','temporal fiber stability','physical wall thickness'],
      'approval':'No owner canonical selection inferred from checks'}
    (REVIEW/'technical_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print('AUDIT',json.dumps({'checks':checks,'counts':report['counts'],'max_error':max_error}),flush=True)
    if not all(checks.values()):raise RuntimeError('Structural checks failed')

def review():
    bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);neutral();records=[]
    def render(name,state='candidate'):
        s=bpy.context.scene;dest=REVIEW/(name+'.png');s.render.filepath=str(dest);t=time.perf_counter();bpy.ops.render.render(write_still=True)
        records.append({'path':str(dest.relative_to(ROOT)),'sha256':sha(dest),'candidate_sha256':sha(OUT),'state':state,
          'seconds':round(time.perf_counter()-t,3),'engine':'CYCLES','device':'CPU','samples':40,'resolution':[768,768],
          'camera_matrix':[list(r) for r in s.camera.matrix_world],'ortho_scale':s.camera.data.ortho_scale,
          'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'output':'RGB PNG / sRGB','blender':bpy.app.version_string})
        (REVIEW/'render_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    # Baseline uses the same geometry/normalization/studio; original imported shader.
    surface=bpy.data.objects['Leo_surface'];wool=bpy.data.objects['Leo_attached_short_wool'];wool.hide_render=True
    whiskers=[o for o in bpy.data.objects if o.name.startswith('Leo_whisker_')]
    for o in whiskers:o.hide_render=True
    current=surface.data.materials[0]
    with bpy.data.libraries.load(str(RAW/'leo_import_untouched.blend'),link=False) as (src,dst):dst.materials=list(src.materials)
    original=dst.materials[0];surface.data.materials[0]=original
    for view in ('front_three_quarter','portrait','rear'):
        camera(view);render('import_before_'+view,'normalized import; original shader; no added wool/whiskers')
    surface.data.materials[0]=current;wool.hide_render=False
    for o in whiskers:o.hide_render=False
    for view in VIEWS:camera(view);render(view)
    # Clay, wire and silhouette expose geometry rather than hiding it in texture.
    wool.hide_render=True
    for o in whiskers:o.hide_render=True
    clay=bpy.data.materials.new('Review_clay');clay.use_nodes=True
    clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.42,.42,.42,1)
    clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.95
    surface.data.materials[0]=clay;camera('front_three_quarter');render('clay_three_quarter','clay; no wool/whiskers')
    camera('rear');render('clay_rear','clay; no wool/whiskers')
    wire=clay.copy();wire.name='Review_wire';nodes=wire.node_tree.nodes;links=wire.node_tree.links
    w=nodes.new('ShaderNodeWireframe');w.inputs['Size'].default_value=.00055
    ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.65,.65,.65,1);ramp.color_ramp.elements[1].color=(.015,.015,.015,1)
    links.new(w.outputs[0],ramp.inputs[0]);links.new(ramp.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])
    surface.data.materials[0]=wire;camera('right');render('wire_right','wire material; no wool/whiskers')
    black=clay.copy();p=black.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(0,0,0,1);p.inputs['Specular IOR Level'].default_value=0
    surface.data.materials[0]=black;camera('front_three_quarter');render('silhouette_three_quarter','black surface; no wool/whiskers')
    surface.data.materials[0]=current;wool.hide_render=False
    for o in whiskers:o.hide_render=False
    camera('front_three_quarter');bpy.data.objects['Neutral_key'].data.color=(1,.79,.57)
    bpy.data.objects['Neutral_rim'].data.color=(.62,.74,1);render('story_light_study','illustrative warm key/cool rim; same intrinsic materials')
    print('REVIEW_COMPLETE',len(records),flush=True)

if __name__=='__main__':
    if '--review-only' not in sys.argv and '--audit-only' not in sys.argv:build()
    if '--build-only' not in sys.argv and '--review-only' not in sys.argv:audit()
    if '--build-only' not in sys.argv and '--audit-only' not in sys.argv:review()
