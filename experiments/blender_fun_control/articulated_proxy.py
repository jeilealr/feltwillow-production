#!/usr/bin/env python3
"""First true 3D articulated proxy; CPU Blender; experimental geometry only."""
import json
import math
import os
from pathlib import Path
import time

from hashlib import sha256
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/articulated_20261016_v2'


def main():
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    import bpy
    import numpy as np
    from mathutils import Vector
    RUN.mkdir(exist_ok=False)
    (RUN/'executed_proxy.py').write_bytes(Path(__file__).read_bytes())
    started=time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1
    scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=7
    scene.render.resolution_x=416;scene.render.resolution_y=240;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    world=bpy.data.worlds.new('World');scene.world=world;world.color=(0,0,0)
    # Depth is encoded in emission: camera-space distance, fixed near/far per clip.
    depth=bpy.data.materials.new('FixedRangeInverseCameraDepth');depth.use_nodes=True
    nodes=depth.node_tree.nodes;nodes.clear();links=depth.node_tree.links
    geometry=nodes.new('ShaderNodeTexCoord')
    camera_data=nodes.new('ShaderNodeCameraData')
    mapping=nodes.new('ShaderNodeMapRange');mapping.clamp=True
    mapping.inputs['From Min'].default_value=5.0;mapping.inputs['From Max'].default_value=12.0
    mapping.inputs['To Min'].default_value=1;mapping.inputs['To Max'].default_value=0
    # Emission image is sRGB encoded by Blender; the encoder linearizes it later.
    emission=nodes.new('ShaderNodeEmission');output=nodes.new('ShaderNodeOutputMaterial')
    links.new(camera_data.outputs['View Z Depth'],mapping.inputs['Value'])
    links.new(mapping.outputs['Result'],emission.inputs['Color']);links.new(emission.outputs[0],output.inputs['Surface'])
    def ellipsoid(name,location,scale):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=location)
        obj=bpy.context.object;obj.name=name;obj.scale=scale;obj.data.materials.append(depth)
        for polygon in obj.data.polygons:polygon.use_smooth=True
        return obj
    def rod(name,a,b,r):
        a,b=Vector(a),Vector(b);delta=b-a
        obj=ellipsoid(name,(a+b)/2,(r,r,delta.length/2+r*.5))
        obj.rotation_quaternion=delta.to_track_quat('Z','Y');obj.rotation_mode='QUATERNION'
        return obj
    def limb(name,root,target,length1,length2,bend):
        # Two-segment analytic IK; root and target are explicit contact constraints.
        root,target=Vector(root),Vector(target);delta=target-root;distance=delta.length
        if not abs(length1-length2)<distance<length1+length2:
            raise RuntimeError(f'Unreachable joint target {name}: {distance}')
        direction=delta.normalized();normal=Vector(bend)
        normal=(normal-direction*normal.dot(direction)).normalized()
        along=(length1**2-length2**2+distance**2)/(2*distance)
        joint=root+along*direction+math.sqrt(max(0,length1**2-along**2))*normal
        rod(name+'_upper',root,joint,.055);rod(name+'_lower',joint,target,.045)
        return list(joint)
    camera_data=bpy.data.cameras.new('ProxyCamera');camera=bpy.data.objects.new('Camera',camera_data)
    scene.collection.objects.link(camera);scene.camera=camera
    camera_data.type='ORTHO';camera_data.ortho_scale=4.6
    def aim(location):
        camera.location=location
        camera.rotation_euler=(Vector((0,0,.85))-camera.location).to_track_quat('-Z','Y').to_euler()
    aim((0,-8,4.1))
    # Flat ground and distant scene markers provide true relative-depth/parallax cues.
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0));bpy.context.object.name='Ground';bpy.context.object.data.materials.append(depth)
    for x,y,r in [(-2,2,.5),(1.6,2.3,.55),(-2.2,-.5,.35)]:ellipsoid('BackgroundRock',(x,y,r*.5),(r,r,r*.6))
    static=set(bpy.data.objects)
    specs={
        'reach':dict(prompt='A single small grey needle-felt mouse Milo sits beside the stream holding one acorn in both paws. He raises the acorn to his mouth, takes a small nibble, then lowers it. Both paws remain in contact with the same acorn. Feet planted, fixed camera, warm felt storybook animation.',representation='canny'),
        'walk':dict(prompt='A single small grey needle-felt mouse Milo holds one acorn against his chest with both front paws and takes two short upright steps to the right on his hind feet, then stops. Alternating feet lift and plant without sliding. Fixed camera, stream background, warm felt storybook animation.',representation='canny'),
        'camera':dict(prompt='A single small grey needle-felt mouse Milo remains seated holding one acorn beside the stream. The camera slowly tracks to the right past a low foreground mossy rock. The rock briefly hides part of his lower body and moves faster across the view than the distant stream. Preserve the same mouse and acorn, warm felt storybook animation.',representation='depth')}
    records={}
    for case,spec in specs.items():
        folder=RUN/case;folder.mkdir();records[case]=[]
        for index in range(49):
            t=index/48
            for obj in list(bpy.data.objects):
                if obj not in static:bpy.data.objects.remove(obj,do_unlink=True)
            camera_data.ortho_scale=4.6
            aim((.70*t if case=='camera' else 0,-8,4.1))
            shift=.60*t if case=='walk' else 0
            # Ground feet are locked in world-space during stance; smooth swing uses lift.
            feet=[]
            for side in (-1,1):
                initial=-.20 if side==-1 else .20
                if case=='walk':
                    start,end=(0,.5) if side==-1 else (.5,1)
                    u=min(1,max(0,(t-start)/(end-start)))
                    smooth=u*u*(3-2*u)
                    fx=initial+.60*smooth;fz=.06+.17*math.sin(math.pi*u)
                else:fx=initial;fz=.06
                feet.append((fx,-.04,fz))
            root=(shift,0,.57)
            ellipsoid('Torso',(shift,0,.64),(.36,.22,.43))
            head=(shift,-.04,1.25)
            ellipsoid('Head',head,(.43,.28,.33))
            ellipsoid('Muzzle',(shift,-.29,1.16),(.19,.11,.12))
            ellipsoid('Nose',(shift,-.40,1.18),(.055,.035,.04))
            for side in (-1,1):
                ellipsoid('Ear',(shift+side*.40,.01,1.61),(.32,.09,.33))
                ellipsoid('Eye',(shift+side*.15,-.285,1.33),(.065,.035,.075))
            rod('Tail',(shift-.22,.08,.33),(shift-.65,.09,.20),.025)
            for side,foot in zip((-1,1),feet):
                hip=(shift+side*.16,.01,.55)
                knee=limb('Leg',hip,foot,.36,.36,(side,-.2,0))
                ellipsoid('Foot',(foot[0],foot[1]-.035,foot[2]),(.13,.17,.065))
            lift=.24*math.sin(math.pi*t)**2 if case=='reach' else 0
            acorn=(shift,-.32,.80+lift)
            ellipsoid('Acorn',acorn,(.15,.13,.19))
            ellipsoid('AcornCap',(shift,-.32,.91+lift),(.17,.14,.07))
            rod('Stem',(shift,-.32,.96+lift),(shift+.03,-.32,1.04+lift),.022)
            paws=[]
            for side in (-1,1):
                shoulder=(shift+side*.22,-.02,.96)
                paw=(shift+side*.15,-.32,.81+lift)
                elbow=limb('Arm',shoulder,paw,.25,.25,(side,-.1,0))
                ellipsoid('Paw',paw,(.07,.07,.08));paws.append(paw)
            if case=='camera':ellipsoid('ForegroundOccluder',(-.18,-1,.27),(.45,.27,.27))
            scene.render.filepath=str(folder/f'{index:06d}.png')
            bpy.ops.render.render(write_still=True)
            records[case].append(dict(frame=index,feet=feet,paws=paws,acorn=acorn,camera=list(camera.location),root=root))
        bpy.ops.wm.save_as_mainfile(filepath=str(folder/'proxy_scene.blend'))
    # Each foot swings once. During its stance interval, displacement must be zero.
    checks={}
    for side,indices in [(0,range(24,49)),(1,range(0,25))]:
        positions=np.array([records['walk'][i]['feet'][side] for i in indices])
        checks[str(side)]=float(np.linalg.norm(positions-positions[0],axis=1).max())
    if max(checks.values())>1e-6:raise RuntimeError('Foot stance slides in authored proxy')
    manifest=dict(status='complete',production_eligible=False,approval='isolated_experiment_not_for_production',
        job_id=os.environ['SLURM_JOB_ID'],blender_version=bpy.app.version_string,frames=49,fps=16,width=416,height=240,
        total_seconds=time.time()-started,script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        representation='Linear inverse camera-Z, fixed [5,12] proxy units, nearer brighter; rendered sRGB must be linearized before guide encoding.',
        cases=specs,trajectory=records,stance_max_displacement=checks,
        limitations=['Analytic linked primitive proxy, not a skinned production mouse or collision solver.',
        'Geometry is approximate, not calibrated to approved plate or starting illustration.',
        'Two upright steps suit the anthropomorphic starting illustration; not quadruped gait validation.',
        'Perspective/occlusion guide via generic depth control, not explicit Camera model or camera-pose inputs.',
        'Guide quality and start alignment must be inspected before GPU inference.'])
    (RUN/'proxy_receipt.json').write_text(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
