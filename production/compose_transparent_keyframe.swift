// Compose RGBA character layers over an already-materialized registered plate crop.
// This path preserves ImageGen transparency and never redraws the approved plate.
// Usage: swift production/compose_transparent_keyframe.swift plate.png out.png blur_px \
//        layer.png height_fraction center_x_fraction bottom_y_fraction [...]
// Character height and bottom position are normalized to the 1920x1080 output.
import AppKit
import Foundation
func makeRep(_ w:Int,_ h:Int)->NSBitmapImageRep {
 NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:w,pixelsHigh:h,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
}
func load(_ p:String)->NSImage { guard let i=NSImage(contentsOfFile:p) else {fatalError("cannot load \(p)")}; return i }
func bounds(_ image:NSImage)->NSRect {
 guard let t=image.tiffRepresentation,let rep=NSBitmapImageRep(data:t) else {fatalError("cannot decode layer")}
 var x0=rep.pixelsWide,y0=rep.pixelsHigh,x1 = -1,y1 = -1
 for y in 0..<rep.pixelsHigh {for x in 0..<rep.pixelsWide {
  if let c=rep.colorAt(x:x,y:y)?.usingColorSpace(.deviceRGB),c.alphaComponent > 0.18 {x0=min(x0,x);y0=min(y0,y);x1=max(x1,x);y1=max(y1,y)}
 }}
 guard x1>=x0,y1>=y0 else {fatalError("empty layer")}
 return NSRect(x:x0,y:y0,width:x1-x0+1,height:y1-y0+1)
}
func boxPass(_ src:[UInt8],w:Int,h:Int,bpr:Int,r:Int,horizontal:Bool)->[UInt8] {
 let win=2*r+1; var dst=src; let lines=horizontal ? h : w, len=horizontal ? w : h
 for line in 0..<lines {
  var sum=[Int](repeating:0,count:4)
  func ix(_ pos:Int,_ c:Int)->Int {let p=max(0,min(len-1,pos));return horizontal ? line*bpr+p*4+c : p*bpr+line*4+c}
  for k in -r...r {for c in 0..<4 {sum[c] += Int(src[ix(k,c)])}}
  for pos in 0..<len {
   let at=horizontal ? line*bpr+pos*4 : pos*bpr+line*4
   for c in 0..<4 {dst[at+c]=UInt8(sum[c]/win)}
   if pos+1<len {for c in 0..<4 {sum[c]-=Int(src[ix(pos-r,c)]);sum[c]+=Int(src[ix(pos+r+1,c)])}}
  }
 }
 return dst
}
func blurRep(_ rep:NSBitmapImageRep,w:Int,h:Int,sigma:Double) {
 let r=max(0,Int(sigma.rounded()));if r==0{return}
 let ptr=rep.bitmapData!,bpr=rep.bytesPerRow,count=bpr*h
 var px=Array(UnsafeBufferPointer(start:ptr,count:count))
 for _ in 0..<3 {px=boxPass(px,w:w,h:h,bpr:bpr,r:r,horizontal:true);px=boxPass(px,w:w,h:h,bpr:bpr,r:r,horizontal:false)}
 px.withUnsafeBytes{memcpy(ptr,$0.baseAddress!,count)}
}
func place(_ image:NSImage,h:CGFloat,x:CGFloat,yTop:CGFloat,W:CGFloat,H:CGFloat) {
 let b=bounds(image),s=h/b.height
 let rect=NSRect(x:x*W-b.midX*s,y:(1-yTop)*H-b.minY*s,width:image.size.width*s,height:image.size.height*s)
 image.draw(in:rect,from:.zero,operation:.sourceOver,fraction:1,respectFlipped:false,hints:[.interpolation:NSImageInterpolation.high])
 print("bbox=\(b), rect=\(rect), target=\(h)")
}
guard CommandLine.arguments.count>=8,(CommandLine.arguments.count-4)%4==0 else {
 fputs("usage: compose_transparent_keyframe.swift plate.png out.png blur_px layer.png height_fraction center_x_fraction bottom_y_fraction [... ]\n",stderr)
 exit(2)
}
let plate=load(CommandLine.arguments[1]),out=CommandLine.arguments[2],sigma=Double(CommandLine.arguments[3])!,W=1920,H=1080
let bgRep=makeRep(W,H),bgCtx=NSGraphicsContext(bitmapImageRep:bgRep)!;bgCtx.imageInterpolation = .high
NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=bgCtx
plate.draw(in:NSRect(x:0,y:0,width:W,height:H),from:.zero,operation:.copy,fraction:1,respectFlipped:false,hints:[.interpolation:NSImageInterpolation.high])
bgCtx.flushGraphics();NSGraphicsContext.current=nil;NSGraphicsContext.restoreGraphicsState();blurRep(bgRep,w:W,h:H,sigma:sigma)
let bg=NSImage(size:NSSize(width:W,height:H));bg.addRepresentation(bgRep)
let final=makeRep(W,H),ctx=NSGraphicsContext(bitmapImageRep:final)!;ctx.imageInterpolation = .high
NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=ctx
bg.draw(in:NSRect(x:0,y:0,width:W,height:H),from:.zero,operation:.copy,fraction:1,respectFlipped:false,hints:[.interpolation:NSImageInterpolation.high])
var i=4
while i<CommandLine.arguments.count {
 let img=load(CommandLine.arguments[i]),h=Double(CommandLine.arguments[i+1])!,x=Double(CommandLine.arguments[i+2])!,y=Double(CommandLine.arguments[i+3])!
 place(img,h:CGFloat(h)*CGFloat(H),x:CGFloat(x),yTop:CGFloat(y),W:CGFloat(W),H:CGFloat(H));i+=4
}
NSGraphicsContext.current=nil;NSGraphicsContext.restoreGraphicsState()
try! final.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:out));print("wrote \(out) \(W)x\(H)")
