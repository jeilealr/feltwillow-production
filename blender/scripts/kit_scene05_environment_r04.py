"""Curved and silhouette kit gate, before scene distribution. Two local stills."""
import bpy,sys,json,time,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/scene05_environment_r04';sys.path.insert(0,str(R/'blender/scripts'));import craft_scene05_r04 as c
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True;s.cycles.seed=510400;s.unit_settings.system='METRIC';s.unit_settings.scale_length=.2
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None'
kit=c.collection('CRAFT_KIT_R04',s.collection);lights=c.collection('KIT_LIGHTS',s.collection);cams=c.collection('KIT_CAMERAS',s.collection);m=c.palette()
root=c.tube('KIT_growth_bark_root',[(-2,.4,.1),(-1.65,.5,.27),(-1.45,.6,.8),(-1.2,.65,1.7)],[.30,.34,.24,.14],m['bark'],kit);c.fibers('KIT_bark_contour_wool',root,m['bark'],kit,2000,.025)
stone=c.ell('KIT_heather_rock',(.8,.35,.32),(.60,.45,.42),m['rock'],kit,4,4);c.fibers('KIT_dense_rock_pile',stone,m['rock'],kit,3200,.016,.001)
mos=c.fuse([c.ell('cushion',(-.45,.05,.09),(.5,.34,.15),m['moss'],kit,3,3),c.ell('cushion',(-.12,.13,.08),(.32,.27,.14),m['moss'],kit,7,3)],'KIT_unified_moss_cushion',.025);c.fibers('KIT_moss_loops',mos,m['mosslight'],kit,2500,.025,.0015)
protos=[]
for i in range(3):
 proto=c.leaf_proto('KIT_felt_leaf_family_%d'%i,m[['leaf','leafgold','deep'][i]],kit,i);proto.location=(1.65+i*.25,.30,.04);proto.scale=(.55,.65,.65);proto.rotation_euler=(.45,0,-.6+i*.6);protos.append(proto)
floor=c.mesh('KIT_matted_path_edge',[(-4,-2,-.015),(4,-2,-.015),(4,3,-.015),(-4,3,-.015)],[(0,1,2,3)],c.ground_material(m['path'],m['moss']),kit)
s.camera=c.camera('CAM_KIT_actual_miniature',(.1,-5.8,3.3),(0,.35,.45),49,cams);s.world=bpy.data.worlds.new('KIT_world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.25,.32,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
c.area('KIT_soft_neutral',(-3,-2,5),(0,0,0),800,(1,1,1),4,lights);c.area('KIT_cool_fill',(3,2,4),(0,0,0),300,(1,1,1),4,lights)
s['approval_status']='craft samples for review, not beauty approval';s['unit_m_per_bu']=.2
target=R/'blender/assets/environments/great_tree/great_tree_craft_kit_r04.blend';assert not target.exists();bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
rows=[]
for name,dusk in [('kit_neutral',False),('kit_dusk',True)]:
 if dusk:
  bpy.data.objects['KIT_soft_neutral'].data.color=(1,.66,.36);bpy.data.objects['KIT_cool_fill'].data.color=(.55,.68,1)
 s.render.filepath=str(P/(name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);rows.append({'name':name,'seconds':time.perf_counter()-t,'sha256':hashlib.sha256((P/(name+'.png')).read_bytes()).hexdigest(),'resolution':[1280,720],'samples':40,'color':'Standard/None/exposure0/gamma1','purpose':'curved surface, shallow path edge and silhouette at miniature scale; no provider maps'})
(P/'kit_render_manifest.json').write_text(json.dumps(rows,indent=2))
