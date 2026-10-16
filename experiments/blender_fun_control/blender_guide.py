#!/usr/bin/env python3
"""Headless Cycles/CPU proof: a textured 2.5D mesh, not an animal rig."""
import hashlib
import json
import math
import os
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def main():
    if not os.environ.get('SLURM_JOB_ID'):
        raise SystemExit('CPU guide rendering requires an allocation')
    receipt=RUN/'controlled_smoke_33/receipt.json'
    if not receipt.exists() or json.loads(receipt.read_text())['status']!='complete':
        raise SystemExit('Complete the proxy-control diagnostic before Blender')
    import bpy
    import numpy as np
    start=time.time()
    out=RUN/'blender_cpu'
    out.mkdir(exist_ok=False)
    width,height,frames=416,240,33
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=1
    scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED'
    scene.render.threads=int(os.environ.get('SLURM_CPUS_PER_TASK','7'))
    scene.render.resolution_x=width; scene.render.resolution_y=height
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
    scene.view_settings.view_transform='Standard'
    scene.view_settings.look='None'
    scene.view_settings.exposure=0; scene.view_settings.gamma=1
    scene.render.film_transparent=False
    world=bpy.data.worlds.new('Black'); scene.world=world; world.color=(0,0,0)
    camera_data=bpy.data.cameras.new('OrthographicImageSpace')
    camera=bpy.data.objects.new('Camera',camera_data); scene.collection.objects.link(camera)
    camera.location=(0,0,10); camera_data.type='ORTHO'; camera_data.ortho_scale=width
    scene.camera=camera
    # Dense calibrated image-plane proxy, preserving the already-fitted canvas.
    nx,ny=104,60
    xy=np.array([(width*x/nx,height*y/ny) for y in range(ny+1) for x in range(nx+1)],dtype=float)
    verts=[(x-width/2,height/2-y,0) for x,y in xy]
    faces=[]
    for y in range(ny):
        for x in range(nx):
            a=y*(nx+1)+x; faces.append((a,a+1,a+nx+2,a+nx+1))
    mesh=bpy.data.meshes.new('ImageGrid');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('ImagePlaneProxy',mesh);scene.collection.objects.link(obj)
    uv=mesh.uv_layers.new(name='SourceImageUV')
    for polygon in mesh.polygons:
        for loop_index in polygon.loop_indices:
            idx=mesh.loops[loop_index].vertex_index; x,y=xy[idx]
            uv.data[loop_index].uv=(x/width,1-y/height)
    material=bpy.data.materials.new('UnlitSourceImage');material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear()
    tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(RUN/'story_inputs/start_fitted.png'))
    tex.interpolation='Linear'
    emission=nodes.new('ShaderNodeEmission');output=nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(tex.outputs['Color'],emission.inputs['Color'])
    material.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
    obj.data.materials.append(material)
    x,y=xy[:,0],xy[:,1]
    head=np.exp(-(((x-width*.50)/(width*.17))**4+((y-height*.38)/(height*.22))**4))*np.clip((height*.77-y)/(height*.14),0,1)
    acorn=np.exp(-(((x-width*.55)/(width*.085))**4+((y-height*.64)/(height*.13))**4))*np.clip((height*.79-y)/(height*.09),0,1)
    for i in range(frames):
        amplitude=math.sin(2*math.pi*i/(frames-1))**2
        dy=amplitude*(4*head+6*acorn)
        for idx,vertex in enumerate(mesh.vertices): vertex.co.y=height/2-y[idx]+dy[idx]
        mesh.update()
        scene.render.filepath=str(out/f'{i:06d}.png')
        bpy.ops.render.render(write_still=True)
    tex.image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'guide_scene.blend'))
    (out/'receipt.json').write_text(json.dumps(dict(status='complete',production_eligible=False,blender_version=bpy.app.version_string,
        engine='Cycles CPU',samples=1,frames=frames,width=width,height=height,total_seconds=time.time()-start,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),job_id=os.environ['SLURM_JOB_ID'],
        interpretation='Textured image-plane mesh guide; no 3D animal rig, physical-depth calibration or improved anatomy claimed.'),indent=2))

if __name__=='__main__':
    try:
        main()
    except BaseException:
        if os.environ.get('SLURM_JOB_ID'):
            import traceback
            (RUN/'blender_failure.json').write_text(json.dumps(dict(status='failed',production_eligible=False,
                job_id=os.environ['SLURM_JOB_ID'],error=traceback.format_exc()),indent=2))
        raise
