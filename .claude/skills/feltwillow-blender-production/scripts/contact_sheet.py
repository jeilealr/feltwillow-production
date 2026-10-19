#!/usr/bin/env python3
"""Thumbnail existing reference renders. Not a color-managed approval tool."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import textwrap
from pathlib import Path

def make_sheet(paths:list[Path],out:Path,columns:int=3,width:int=480):
    if not paths or columns<1 or columns>12 or width<100 or width>2000:
        raise ValueError('Supply images, 1-12 columns and width 100-2000')
    if out.exists() or out.with_suffix('.json').exists():
        raise ValueError('Output or manifest already exists; choose a new filename')
    from PIL import Image, ImageOps, ImageDraw
    h=int(width*0.7);label_h=60
    sheet=Image.new('RGB',(columns*width,math.ceil(len(paths)/columns)*(h+label_h)),'white')
    draw=ImageDraw.Draw(sheet);manifest=[]
    for i,path in enumerate(paths):
        with Image.open(path) as im:
            thumb=ImageOps.contain(im.convert('RGB'),(width,h))
            x=(i%columns)*width;y=(i//columns)*(h+label_h)
            sheet.paste(thumb,(x+(width-thumb.width)//2,y+(h-thumb.height)//2))
            draw.text((x+8,y+h+5),'\n'.join(textwrap.wrap(path.name,max(16,width//7))[:3]),fill='black')
            manifest.append({'label':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                             'source_size':list(im.size)})
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('xb') as f:sheet.save(f,format='PNG')
    with out.with_suffix('.json').open('x',encoding='utf-8') as f:
        json.dump({'images':manifest,'warning':'Thumbnails resampled without managed color conversion. Inspect original renders for color/detail.'},f,indent=2)
    return sheet.size

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('images',nargs='+',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--columns',type=int,default=3);p.add_argument('--width',type=int,default=480);a=p.parse_args()
    try:print(make_sheet(a.images,a.out,a.columns,a.width))
    except (ValueError,OSError,ImportError) as e:p.error(str(e))
if __name__=='__main__':main()
