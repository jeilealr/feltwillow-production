#!/usr/bin/env python3
"""Read-only material/image graph report. Run inside Blender with --disable-autoexec.

No rendering, shader mutation, provider calls or scene saves. Graph reachability
is only potential contribution: shader weights, groups and visibility still need
inspection and render A/B. Native Blender execution must be validated locally.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

def upstream_nodes(nodes, links):
    """Conservative node-level upstream set for active material outputs."""
    lookup = {n['id']: n for n in nodes}
    todo = [n['id'] for n in nodes if n.get('type') == 'ShaderNodeOutputMaterial' and n.get('active_output') is True]
    parents = {}
    for edge in links:
        if edge['from'] in lookup and edge['to'] in lookup:
            parents.setdefault(edge['to'], set()).add(edge['from'])
    seen = set()
    while todo:
        key = todo.pop()
        if key in seen:
            continue
        seen.add(key)
        todo.extend(parents.get(key, ()))
    return seen

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def label(path, base):
    try:
        return Path(path).resolve().relative_to(base).as_posix()
    except ValueError:
        return '[external]/' + Path(path).name

def inspect(bpy):
    file = Path(bpy.data.filepath) if bpy.data.filepath else None
    base = file.resolve().parent if file else Path.cwd()
    material_users = {}
    for obj in bpy.data.objects:
        for slot in getattr(obj, 'material_slots', []):
            if slot.material:
                material_users.setdefault(slot.material.name, set()).add(obj.name)
    materials = []
    for material in bpy.data.materials:
        graphs, seen = [], set()
        queue = [material.node_tree] if material.node_tree else []
        while queue:
            tree = queue.pop()
            key = tree.as_pointer()
            if key in seen:
                continue
            seen.add(key)
            nodes = []
            for node in tree.nodes:
                row = {'id': node.name, 'type': node.bl_idname, 'muted': bool(node.mute),
                       'active_output': bool(getattr(node, 'is_active_output', False))}
                image = getattr(node, 'image', None)
                if image:
                    row['image'] = image.name
                child = getattr(node, 'node_tree', None)
                if child:
                    row['group_tree'] = child.name
                    queue.append(child)
                nodes.append(row)
            links = [{'from': l.from_node.name, 'from_socket': l.from_socket.name,
                      'to': l.to_node.name, 'to_socket': l.to_socket.name}
                     for l in tree.links if l.is_valid]
            reachable = upstream_nodes(nodes, links)
            for row in nodes:
                row['on_node_path_to_active_material_output'] = row['id'] in reachable
            graphs.append({'tree': tree.name, 'is_material_root': tree == material.node_tree,
                           'nodes': nodes, 'links': links})
        materials.append({'name': material.name, 'uses_nodes': bool(material.use_nodes),
                          'object_material_slot_users': sorted(material_users.get(material.name, ())),
                          'graphs': graphs})
    images = []
    for image in bpy.data.images:
        row = {'name': image.name, 'size': list(image.size), 'source': image.source,
               'color_space': image.colorspace_settings.name, 'packed': []}
        packed = list(getattr(image, 'packed_files', []))
        for item in packed:
            data = bytes(item.packed_file.data)
            row['packed'].append({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        if not packed and getattr(image, 'packed_file', None):
            data = bytes(image.packed_file.data)
            row['packed'].append({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        if image.filepath:
            path = Path(bpy.path.abspath(image.filepath, library=image.library))
            row.update(path_label=label(path, base), external_file_exists=path.is_file())
            if path.is_file():
                row['external_sha256'] = digest(path)
        images.append(row)
    return {'schema': 'feltwillow.material-audit.v1', 'blend_file': file.name if file else None,
            'blend_sha256': digest(file) if file and file.is_file() else None,
            'blender_version': bpy.app.version_string, 'materials': materials, 'images': images,
            'visual_approved': False, 'provider_provenance_verified': False,
            'limitations': ['Node-level paths are potential contributions, not actual rendered weights or camera visibility.',
                           'Nested groups are inventoried separately; cross-group socket reachability is not solved.',
                           'Geometry Nodes/instance material overrides and render-layer visibility require local verification.',
                           'No provider receipt or private account history was inspected.',
                           'No rendering, scene saving, paid calls or owner approval performed.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        import bpy
    except ImportError:
        raise SystemExit('Run inside Blender; bpy is unavailable. No report created.')
    report = inspect(bpy)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(report, f, indent=2, allow_nan=False)
        f.write('\n')
    print('Wrote read-only material report:', args.out)

if __name__ == '__main__':
    main()
