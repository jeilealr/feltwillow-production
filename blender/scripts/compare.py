"""Create labeled review boards. Python >=3.11 and Pillow; no source edits."""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'blender'
CFG=json.loads((A/'config/authority.json').read_text())


def board(entries,path,columns=3,cell=(480,510)):
    canvas=Image.new('RGB',(columns*cell[0],((len(entries)+columns-1)//columns)*cell[1]),'#e8e6e2')
    draw=ImageDraw.Draw(canvas)
    for i,(label,p) in enumerate(entries):
        im=Image.open(p).convert('RGB');im.thumbnail((cell[0]-16,cell[1]-55))
        x=(i%columns)*cell[0];y=(i//columns)*cell[1]
        canvas.paste(im,(x+(cell[0]-im.width)//2,y+8))
        draw.text((x+10,y+cell[1]-40),label,fill='#222222')
    path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path)


if __name__=='__main__':
    for name in ['leo','s05','rig','benchmark']:
        for rec in json.loads((A/f'renders/{name}_manifest.json').read_text()):
            for path,expected in [(ROOT/rec['image'],rec['sha256']), (ROOT/rec['input_blend'],rec['input_blend_sha256'])]:
                if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Stale review artifact; rerender before comparison: '+str(path))
            for path,expected in rec.get('linked_library_sha256',{}).items():
                lib=((ROOT/rec['input_blend']).parent/path.removeprefix('//')).resolve()
                if hashlib.sha256(lib.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed linked library; rerender: '+str(lib))
    board([('APPROVED 2D canonical',ROOT/CFG['leo']['canonical'])]+[(p.stem,p) for p in sorted((A/'renders/reference/leo').glob('*.png')) if 'comparison' not in p.name], A/'renders/reference/leo/comparison.png')
    board([('APPROVED tree_dusk r02',ROOT/CFG['location']['plate']),('Blender 3D reconstruction',A/'renders/reference/s05/environment_wide.png'),('SELECTED s05_p01',ROOT/CFG['s05_frames'][0]['candidate_path']),('Blender sleeping pose candidate',A/'renders/reference/s05/s05_p01_wide.png')],A/'renders/reference/s05/comparison.png',2,(640,410))
    views=[(p.stem,p) for p in sorted((A/'renders/diagnostic/rig').glob('*.png'))]
    if views:board(views,A/'renders/diagnostic/rig_comparison.png')
    engines=[(p.stem,p) for p in sorted((A/'renders/diagnostic/engine_comparison').glob('*.png'))]
    if engines:board(engines,A/'renders/diagnostic/engine_comparison.png',2)

    boards={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [A/'renders/reference/leo/comparison.png',A/'renders/reference/s05/comparison.png',A/'renders/diagnostic/rig_comparison.png',A/'renders/diagnostic/engine_comparison.png']}
    (A/'renders/review_boards_manifest.json').write_text(json.dumps({'status':'prototype_needs_owner_review','boards':boards},indent=2)+'\n')
