"""Leo r02: localized imported whisker repair, topology, rig and felt studies.
Local only. Source r01 remains unchanged. See docs/leo_tripo_r02_brief.md.
"""
import bpy,bmesh,math,sys,json,hashlib,random,time,bisect
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender';sys.path.insert(0,str(AREA/'scripts'))
import leo_tripo_canonical_pass as prior
import build as helpers
SOURCE=prior.OUT;OUT=SOURCE.with_name('leo_canonical_tripo_candidate_r02.blend')
P=AREA/'renders/leo_tripo_canonical_r02';P.mkdir(parents=True,exist_ok=True)
SEED=18102605;RNG=random.Random(SEED)
RECEIPT={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':None,'operations':[]}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(kind,**kw):
    RECEIPT['operations'].append({'operation':kind,**kw});(P/'operations.json').write_text(json.dumps(RECEIPT,indent=2)+'\n');print(kind,json.dumps(kw),flush=True)
def smoothstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def stats(me):
    bm=bmesh.new();bm.from_mesh(me);d={'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)};bm.free();return d

def cleanup(o):
    before=stats(o.data);bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table()
    unseen=set(bm.verts);small=[]
    while unseen:
        first=unseen.pop();comp={first};stack=[first]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                n=e.other_vert(v)
                if n in unseen:unseen.remove(n);comp.add(n);stack.append(n)
        if len(comp)<40:small.extend(comp)
    small_count=len(small)
    bmesh.ops.delete(bm,geom=small,context='VERTS')
    # Identified from the clay inspection: three source branches on +X cheek.
    lines=[(Vector((.132,-.935,.874)),Vector((.237,-.953,.879))),
           (Vector((.137,-.919,.852)),Vector((.250,-.908,.842))),
           (Vector((.137,-.918,.834)),Vector((.251,-.911,.800)))]
    branch=[]
    for v in bm.verts:
        p=v.co
        if not(.143<p.x<.27 and p.y<-.86 and .785<p.z<.90):continue
        for a,b in lines:
            t=max(0,min(1,(p-a).dot(b-a)/(b-a).length_squared))
            if (p-(a+(b-a)*t)).length<.008:branch.append(v);break
    branch_count=len(branch);bmesh.ops.delete(bm,geom=branch,context='VERTS')
    # Preserve UVs on tiny filled root/historical holes using adjacent loop UVs.
    uv=bm.loops.layers.uv.active;uv_by_vertex={}
    for v in bm.verts:
        if v.link_loops:uv_by_vertex[v]=v.link_loops[0][uv].uv.copy()
    edges=[e for e in bm.edges if e.is_boundary]
    fill=bmesh.ops.holes_fill(bm,edges=edges,sides=24)
    for f in fill['faces']:
        for loop in f.loops:loop[uv].uv=uv_by_vertex.get(loop.vert,Vector((.5,.5)))
    # Very local root smoothing; all eyes, nose and mouth coordinates untouched.
    roots=[v for v in bm.verts if .122<v.co.x<.157 and v.co.y<-.87 and .812<v.co.z<.890]
    for i in range(18):bmesh.ops.smooth_vert(bm,verts=roots,factor=.40,use_axis_x=True,use_axis_y=True,use_axis_z=True)
    # Tiny original isolated face/loose edges are not useful surface anatomy.
    isolated=[f for f in bm.faces if all(e.is_boundary for e in f.edges)]
    if isolated:bmesh.ops.delete(bm,geom=isolated,context='FACES_ONLY')
    wires=[e for e in bm.edges if not e.link_faces]
    if wires:bmesh.ops.delete(bm,geom=wires,context='EDGES')
    loose=[v for v in bm.verts if not v.link_faces]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    bm.normal_update();bm.to_mesh(o.data);bm.free();o.data.update()
    log('remove_identified_imported_whisker_branches',deleted_branch_vertices=branch_count,deleted_microscopic_island_vertices=small_count,filled_faces=len(fill['faces']),smoothed_root_vertices=len(roots),before=before,after=stats(o.data))

def feet(o):
    me=o.data;eligible={v.index for v in me.vertices if v.co.z<.155};adj={i:[] for i in eligible}
    for e in me.edges:
        a,b=e.vertices
        if a in eligible and b in eligible:adj[a].append(b);adj[b].append(a)
    unseen=set(eligible);comps=[]
    while unseen:
        first=unseen.pop();ids=[first];stack=[first]
        while stack:
            for n in adj[stack.pop()]:
                if n in unseen:unseen.remove(n);ids.append(n);stack.append(n)
        if len(ids)>80:comps.append(ids)
    result={}
    for ids in comps:
        center=sum((me.vertices[i].co for i in ids),Vector())/len(ids)
        name=('front' if center.y<0 else 'hind')+'.'+('L' if center.x<0 else 'R')
        result[name]={'ids':ids,'center':list(center),'min':[min(me.vertices[i].co[j] for i in ids) for j in range(3)],'max':[max(me.vertices[i].co[j] for i in ids) for j in range(3)]}
    if len(result)!=4:raise RuntimeError('Cannot resolve four plantar regions: '+str(result.keys()))
    return result

def refine_paws(o,paws):
    changed=set();me=o.data
    # Refine the existing pads without adding overlapping toe objects. Three
    # shallow grooves divide four softly raised toe lobes within each footprint.
    for name,data in paws.items():
        cx,cy,cz=data['center'];xmin,ymin,zmin=data['min'];xmax,ymax,zmax=data['max'];width=xmax-xmin
        separators=[xmin+width*t for t in (.26,.50,.74)]
        for v in me.vertices:
            p=v.co
            if not(xmin-.015<p.x<xmax+.015 and ymin-.015<p.y<ymax and p.z<.20):continue
            front=1-smoothstep(ymin+.04,ymin+.13,p.y);top=smoothstep(.028,.065,p.z)*(1-smoothstep(.12,.19,p.z))
            if front*top<.001:continue
            groove=max(math.exp(-((p.x-s)/.009)**2) for s in separators)
            p.z-=.0055*groove*front*top
            # Round pad front slightly, keeping support level untouched.
            p.y+=.003*groove*front*top;changed.add(v.index)
        # Bring the original small supporting gaps to the same plane smoothly.
        for v in me.vertices:
            p=v.co
            if xmin-.01<p.x<xmax+.01 and ymin-.01<p.y<ymax+.015 and p.z<.14:
                p.z-=zmin*(1-smoothstep(.04,.14,p.z));changed.add(v.index)
    me.update();log('restrained_paw_grooves_and_support_refinement',changed_vertices=len(changed),paw_regions={n:{k:v for k,v in d.items() if k!='ids'} for n,d in paws.items()})

class Surface:
    def __init__(self,o):
        self.o=o;self.me=o.data;self.me.calc_loop_triangles();self.tris=list(self.me.loop_triangles)
        self.tree=BVHTree.FromPolygons([v.co for v in self.me.vertices],[t.vertices for t in self.tris],all_triangles=True)
        self.uv=self.me.uv_layers.active.data
    def uv_at(self,p,idx=None):
        if idx is None:p,n,idx,d=self.tree.find_nearest(p)
        t=self.tris[idx];a,b,c=[self.me.vertices[i].co for i in t.vertices];ua,ub,uc=[Vector((*self.uv[i].uv,0)) for i in t.loops]
        return barycentric_transform(p,a,b,c,ua,ub,uc).xy

def mesh_from_tube(name,points,radii,sides=10):
    verts=[];faces=[]
    for i,p in enumerate(points):
        t=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=t.cross(Vector((0,1,0)))
        if u.length<.01:u=t.cross(Vector((1,0,0)))
        u.normalize();v=t.cross(u).normalized()
        for j in range(sides):
            a=math.tau*j/sides;verts.append(p+(u*math.cos(a)+v*math.sin(a))*radii[i])
    for i in range(len(points)-1):
        for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);ASSET.objects.link(o)
    for f in me.polygons:f.use_smooth=True
    return o

def map_uv(o,surface):
    uv=o.data.uv_layers.new(name='Leo_source_palette');vuv={v.index:surface.uv_at(v.co) for v in o.data.vertices}
    for loop in o.data.loops:uv.data[loop.index].uv=vuv[loop.vertex_index]

def refine_mane(surface,material):
    # Fixed individually placed rear folds stay inside the existing head outline.
    designs=[(-.27,1.23,.061,.8),(-.10,1.38,.065,1.8),(.10,1.38,.060,-.2),(.28,1.24,.055,2.5),
             (-.31,1.06,.056,-.7),(-.12,1.16,.064,2.0),(.10,1.17,.071,.5),(.29,1.04,.055,1.4),
             (-.12,.95,.054,-.1),(.10,.97,.061,2.7)]
    objects=[];changed=set()
    for k,(x,z,size,angle) in enumerate(designs):
        pts=[];rs=[]
        for i in range(40):
            t=i/39;a=angle+t*math.pi*1.7;r=size*(1-.60*t)
            xx=x+r*math.cos(a);zz=z+r*math.sin(a)
            hit,n,idx,d=surface.tree.ray_cast(Vector((xx,2,zz)),Vector((0,-1,0)))
            if hit is None or hit.y>.18:break
            width=.015*(.30+.70*math.sin(math.pi*(.05+.9*t))**.5)*(1-.45*t)
            # Ends sit within the original posterior wool mass.
            lift=.008+width*.43;pts.append(Vector((xx,hit.y+lift,zz)));rs.append(width)
        if len(pts)<40:continue
        # Carve a restrained rolled crease into the existing wool volume.
        # An earlier additive-loop test looked like separate rings and was rejected.
        for v in surface.me.vertices:
            p=v.co
            if abs(p.x-x)>size+.025 or abs(p.z-z)>size+.025 or p.y<-.40 or p.y>.18 or v.normal.y<.2:continue
            d=min(math.hypot(p.x-q.x,p.z-q.z) for q in pts)
            amount=.0075*math.exp(-(d/.009)**2)
            if amount>.00005:p.y-=amount;changed.add(v.index)
    surface.me.update()
    log('sculpt_posterior_rolled_creases',fixed_designs=len(designs),changed_vertices=len(changed),policy='subtle incised rolls in existing surface; no added decorative rings; front retained')
    return objects

def add_rest_attribute(o):
    attr=o.data.attributes.get('felt_rest') or o.data.attributes.new('felt_rest','FLOAT_VECTOR','POINT')
    for v in o.data.vertices:attr.data[v.index].vector=v.co

def felt_material(source):
    m=source.copy();m.name='Leo_Felt_r02_PaletteLocked';n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Roughness'].default_value=.94;p.inputs['Sheen Weight'].default_value=.22;p.inputs['Sheen Roughness'].default_value=.75;p.inputs['Specular IOR Level'].default_value=.20
    coord=n.new('ShaderNodeAttribute');coord.attribute_name='felt_rest';coord.label='Stable undeformed surface positions'
    meso=n.new('ShaderNodeTexNoise');meso.inputs['Scale'].default_value=200;meso.inputs['Detail'].default_value=2.4;meso.inputs['Roughness'].default_value=.72;l.new(coord.outputs['Vector'],meso.inputs['Vector'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.0017;l.new(meso.outputs['Fac'],bump.inputs['Height'])
    if p.inputs['Normal'].is_linked:l.new(p.inputs['Normal'].links[0].from_socket,bump.inputs['Normal'])
    fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=700;fine.inputs['Detail'].default_value=2;l.new(coord.outputs['Vector'],fine.inputs['Vector'])
    micro=n.new('ShaderNodeBump');micro.inputs['Strength'].default_value=.13;micro.inputs['Distance'].default_value=.00055;l.new(fine.outputs['Fac'],micro.inputs['Height']);l.new(bump.outputs['Normal'],micro.inputs['Normal']);l.new(micro.outputs['Normal'],p.inputs['Normal'])
    ramp=n.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=.88;ramp.inputs['To Max'].default_value=.98;l.new(meso.outputs['Fac'],ramp.inputs['Value']);l.new(ramp.outputs['Result'],p.inputs['Roughness'])
    return m

def build():
    global ASSET,ROOT_OBJ
    RECEIPT['source_sha256']=sha(SOURCE)
    if RECEIPT['source_sha256']!='69d4c29d2b6442eee9bb8de9cfb2289657aeec315bf99790756a2be5a67b0ac9':raise RuntimeError('r01 source changed; inspect before rebuilding')
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
    ASSET=bpy.data.collections['LEO_TRIPO_CANDIDATE_R01'];ASSET.name='LEO_TRIPO_CANDIDATE_R02';ROOT_OBJ=bpy.data.objects['Leo_ASSET_ROOT']
    o=bpy.data.objects['Leo_surface'];cleanup(o);paws=feet(o);refine_paws(o,paws)
    # The original sparse static groom is rebuilt after mesh refinement/binding.
    bpy.data.objects.remove(bpy.data.objects['Leo_attached_short_wool'],do_unlink=True)
    source_mat=o.data.materials[0];mat=felt_material(source_mat);o.data.materials[0]=mat
    surface=Surface(o);folds=refine_mane(surface,mat)
    for ob in [o]+folds:add_rest_attribute(ob)
    log('refinement_checkpoint',surface_stats=stats(o.data),paws_after={k:{key:v for key,v in d.items() if key!='ids'} for k,d in feet(o).items()})
    prior.neutral();prior.camera('front_three_quarter')
    s=bpy.context.scene;s['revision']='leo_tripo_r02';s['approval_status']='candidate_needs_visual_and_deformation_review';s['seed']=SEED
    # Store fitted plantar regions for the rig continuation.
    (P/'paw_regions.json').write_text(json.dumps(feet(o),indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
    log('saved_refined_unrigged_checkpoint',path=str(OUT.relative_to(ROOT)),sha256=sha(OUT))

if __name__=='__main__':build()
