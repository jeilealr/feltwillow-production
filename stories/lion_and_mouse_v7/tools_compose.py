#!/usr/bin/env python3
"""Deterministically place transparent v7 character cutouts on registered 16:9 plates.
Supports 8-bit RGB/RGBA non-interlaced PNG. Background pixels are copied unchanged.
"""
from __future__ import annotations
import argparse, binascii, math, struct, zlib
from pathlib import Path
SIG=b'\x89PNG\r\n\x1a\n'
def read_png(path):
    data=Path(path).read_bytes(); assert data[:8]==SIG, 'not PNG'
    i=8; chunks=[]
    while i<len(data):
        n=struct.unpack('>I',data[i:i+4])[0]; typ=data[i+4:i+8]; payload=data[i+8:i+8+n]; i+=12+n
        chunks.append((typ,payload))
        if typ==b'IEND': break
    ihdr=next(v for t,v in chunks if t==b'IHDR')
    w,h,depth,ct,comp,filt,inter=struct.unpack('>IIBBBBB',ihdr)
    if depth!=8 or ct not in (2,6) or inter!=0: raise ValueError(f'unsupported PNG layout {depth=} {ct=} {inter=}')
    bpp=3 if ct==2 else 4; raw=zlib.decompress(b''.join(v for t,v in chunks if t==b'IDAT'))
    stride=w*bpp; out=bytearray(h*stride); pos=0
    for y in range(h):
        ft=raw[pos]; pos+=1; row=bytearray(raw[pos:pos+stride]); pos+=stride
        prev=out[(y-1)*stride:y*stride] if y else None
        for x in range(stride):
            a=row[x-bpp] if x>=bpp else 0; b=prev[x] if prev is not None else 0; c=prev[x-bpp] if prev is not None and x>=bpp else 0
            if ft==1: row[x]=(row[x]+a)&255
            elif ft==2: row[x]=(row[x]+b)&255
            elif ft==3: row[x]=(row[x]+((a+b)//2))&255
            elif ft==4:
                p=a+b-c; pa=abs(p-a); pb=abs(p-b); pc=abs(p-c); pr=a if pa<=pb and pa<=pc else b if pb<=pc else c; row[x]=(row[x]+pr)&255
            elif ft!=0: raise ValueError(f'PNG filter {ft}')
        out[y*stride:(y+1)*stride]=row
    if ct==2:
        rgba=bytearray(w*h*4)
        for j in range(w*h): rgba[4*j:4*j+3]=out[3*j:3*j+3]; rgba[4*j+3]=255
        out=rgba
    return w,h,out

def png_chunk(t,b): return struct.pack('>I',len(b))+t+b+struct.pack('>I',binascii.crc32(t+b)&0xffffffff)
def write_rgb(path,w,h,pix):
    raw=b''.join(b'\0'+bytes(pix[y*w*3:(y+1)*w*3]) for y in range(h))
    data=SIG+png_chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+png_chunk(b'IDAT',zlib.compress(raw,6))+png_chunk(b'IEND',b'')
    Path(path).write_bytes(data)
def bbox_alpha(w,h,p,threshold=12):
    xs=[];ys=[]
    for y in range(h):
        for x in range(w):
            if p[(y*w+x)*4+3]>threshold: xs.append(x);ys.append(y)
    if not xs: raise ValueError('empty character alpha')
    pad=max(2,int(max(max(xs)-min(xs),max(ys)-min(ys))*.012))
    return max(0,min(xs)-pad),max(0,min(ys)-pad),min(w,max(xs)+pad+1),min(h,max(ys)+pad+1)
def resize_rgba(src,sw,sh,dw,dh):
    out=bytearray(dw*dh*4)
    for y in range(dh):
        sy=(y+.5)*sh/dh-.5; y0=max(0,min(sh-1,int(math.floor(sy)))); y1=min(sh-1,y0+1); fy=max(0,min(1,sy-y0))
        for x in range(dw):
            sx=(x+.5)*sw/dw-.5; x0=max(0,min(sw-1,int(math.floor(sx)))); x1=min(sw-1,x0+1); fx=max(0,min(1,sx-x0))
            oi=(y*dw+x)*4
            for c in range(4):
                a=src[(y0*sw+x0)*4+c]*(1-fx)+src[(y0*sw+x1)*4+c]*fx
                b=src[(y1*sw+x0)*4+c]*(1-fx)+src[(y1*sw+x1)*4+c]*fx
                out[oi+c]=int(a*(1-fy)+b*fy+.5)
    return out
def composite(background,layer,outfile,height_frac=.25,center_x=.5,ground_y=.84,zoom=1.0,crop_center_x=.5,crop_center_y=.5):
    bw,bh,bg=read_png(background); lw,lh,lp=read_png(layer)
    if zoom>1.0001:
        cw=max(1,int(bw/zoom)); ch=max(1,int(bh/zoom)); x0=max(0,min(bw-cw,int(bw*crop_center_x-cw/2))); y0=max(0,min(bh-ch,int(bh*crop_center_y-ch/2)))
        cropped=bytearray(cw*ch*4)
        for yy in range(ch):
            cropped[yy*cw*4:(yy+1)*cw*4]=bg[((yy+y0)*bw+x0)*4:((yy+y0)*bw+x0+cw)*4]
        bg=resize_rgba(cropped,cw,ch,bw,bh)
    x0,y0,x1,y1=bbox_alpha(lw,lh,lp); cw,ch=x1-x0,y1-y0
    crop=bytearray(cw*ch*4)
    for y in range(ch): crop[y*cw*4:(y+1)*cw*4]=lp[((y+y0)*lw+x0)*4:((y+y0)*lw+x1)*4]
    dh=max(1,int(bh*height_frac)); dw=max(1,int(cw*dh/ch)); fg=resize_rgba(crop,cw,ch,dw,dh)
    left=int(bw*center_x-dw/2); top=int(bh*ground_y-dh)
    # Small radial contact shadow below the feet; keep the background outside this ellipse unchanged.
    shadow_cx=int(bw*center_x); shadow_y=int(bh*ground_y); rx=max(2,int(dw*.34)); ry=max(2,int(dh*.025))
    rgb=bytearray(bw*bh*3)
    for i in range(bw*bh): rgb[i*3:i*3+3]=bg[i*4:i*4+3]
    for y in range(max(0,shadow_y-ry),min(bh,shadow_y+ry+1)):
        for x in range(max(0,shadow_cx-rx),min(bw,shadow_cx+rx+1)):
            r=((x-shadow_cx)/rx)**2+((y-shadow_y)/ry)**2
            if r<1:
                a=int(35*(1-r)**2); i=(y*bw+x)*3
                for c in range(3): rgb[i+c]=(rgb[i+c]*(255-a))//255
    for y in range(dh):
        yy=top+y
        if yy<0 or yy>=bh: continue
        for x in range(dw):
            xx=left+x
            if xx<0 or xx>=bw: continue
            fi=(y*dw+x)*4; a=fg[fi+3]
            if a==0: continue
            bi=(yy*bw+xx)*3; inv=255-a
            for c in range(3): rgb[bi+c]=(fg[fi+c]*a+rgb[bi+c]*inv)//255
    write_rgb(outfile,bw,bh,rgb)
    return {'background_size':[bw,bh],'layer_alpha_bbox':[x0,y0,x1,y1],'placed_size':[dw,dh],'placement_px':[left,top],'height_fraction':height_frac,'center_x':center_x,'ground_y':ground_y}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--background',required=True);p.add_argument('--layer',required=True);p.add_argument('--out',required=True);p.add_argument('--height-frac',type=float,default=.25);p.add_argument('--center-x',type=float,default=.5);p.add_argument('--ground-y',type=float,default=.84);p.add_argument('--zoom',type=float,default=1.0);p.add_argument('--crop-center-x',type=float,default=.5);p.add_argument('--crop-center-y',type=float,default=.5);a=p.parse_args()
    print(composite(a.background,a.layer,a.out,a.height_frac,a.center_x,a.ground_y,a.zoom,a.crop_center_x,a.crop_center_y))
