#!/usr/bin/env python3
"""Read-only Blender inventory. Writes a NEW JSON report, never saves a scene.

Run inside a trusted Blender process or with --disable-autoexec. This module was
syntax-checked but not executed with bpy in the packaging environment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

def file_hash(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def label(path:Path,base:Path):
    try:return path.resolve().relative_to(base).as_posix()
    except ValueError:return '[external]/'+path.name

def inventory(bpy):
    base=Path(bpy.data.filepath).resolve().parent if bpy.data.filepath else Path.cwd()
    objects=[]
    for obj in bpy.data.objects:
        row={'name':obj.name,'type':obj.type,'parent':obj.parent.name if obj.parent else None,
             'matrix_world':[float(v) for r in obj.matrix_world for v in r],
             'scale':[float(v) for v in obj.scale],'hide_render':bool(obj.hide_render),
             'library':label(Path(bpy.path.abspath(obj.library.filepath)),base) if obj.library else None,
             'modifiers':[{'name':m.name,'type':m.type,'show_render':m.show_render} for m in obj.modifiers]}
        if obj.type=='MESH':
            mesh=obj.data
            row['mesh']={'vertices':len(mesh.vertices),'faces':len(mesh.polygons),
                         'uv_layers':[u.name for u in mesh.uv_layers],
                         'material_slots':[s.material.name if s.material else None for s in obj.material_slots],
                         'vertex_groups':[g.name for g in obj.vertex_groups],
                         'shape_keys':[k.name for k in mesh.shape_keys.key_blocks] if mesh.shape_keys else []}
        elif obj.type=='ARMATURE':
            row['bones']=[{'name':b.name,'parent':b.parent.name if b.parent else None,'deform':bool(b.use_deform)} for b in obj.data.bones]
        elif obj.type=='CAMERA':
            row['camera']={'type':obj.data.type,'lens':obj.data.lens,'ortho_scale':obj.data.ortho_scale,
                           'shift':[obj.data.shift_x,obj.data.shift_y],
                           'dof_enabled':obj.data.dof.use_dof}
        objects.append(row)
    images=[]
    for im in bpy.data.images:
        row={'name':im.name,'source':im.source,'size':list(im.size),
             'color_space':im.colorspace_settings.name,
             'packed':bool(getattr(im,'packed_file',None) or getattr(im,'packed_files',[]))}
        if im.filepath:
            file=Path(bpy.path.abspath(im.filepath,library=im.library))
            row.update(path_label=label(file,base),file_exists=file.is_file())
        images.append(row)
    scenes=[{'name':s.name,'frame':s.frame_current,'start':s.frame_start,'end_inclusive':s.frame_end,
             'fps':s.render.fps,'fps_base':s.render.fps_base,'engine':s.render.engine,
             'resolution':[s.render.resolution_x,s.render.resolution_y],
             'resolution_percentage':s.render.resolution_percentage,
             'camera':s.camera.name if s.camera else None,
             'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,
             'exposure':s.view_settings.exposure,'display_device':s.display_settings.display_device}
            for s in bpy.data.scenes]
    path=Path(bpy.data.filepath) if bpy.data.filepath else None
    return {'schema':'feltwillow.blender.inventory.v1','blender_version':bpy.app.version_string,
            'blend_file':path.name if path else None,'blend_sha256':file_hash(path) if path and path.is_file() else None,
            'scenes':scenes,'objects':objects,'images':images,
            'libraries':[{'label':label(Path(bpy.path.abspath(l.filepath)),base),
                          'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries],
            'embedded_text_block_names':[t.name for t in bpy.data.texts],
            'limitations':['Counts are not semantic anatomy validation.','Current scene inventory only; no deformation or beauty review.',
                           'External paths are labeled, not exported. Some drivers may be disabled under safe inspection.',
                           'No image content, private custom properties or embedded script source is dumped.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    a=p.parse_args(args)
    try:import bpy
    except ImportError:raise SystemExit('Run this helper inside Blender; bpy is unavailable.')
    report=inventory(bpy)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print('Wrote inventory only:',a.out)
if __name__=='__main__':main()
