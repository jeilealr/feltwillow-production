// Composite one owner-directed local correction patch over an unchanged PNG.
// Usage: swift compose_owner_correction_patch.swift base.png edit.png out.png x y width height feather_px
import Foundation
import CoreGraphics
import ImageIO

func readImage(_ path: String) -> CGImage {
    let url = URL(fileURLWithPath: path)
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        fatalError("Cannot read image: \(path)")
    }
    return image
}

func rgba(_ image: CGImage, width: Int, height: Int) -> [UInt8] {
    var bytes = [UInt8](repeating: 0, count: width * height * 4)
    bytes.withUnsafeMutableBytes { raw in
        guard let context = CGContext(data: raw.baseAddress, width: width, height: height,
                                      bitsPerComponent: 8, bytesPerRow: width * 4,
                                      space: CGColorSpace(name: CGColorSpace.sRGB)!,
                                      bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue |
                                                  CGBitmapInfo.byteOrder32Big.rawValue) else {
            fatalError("Cannot create bitmap context")
        }
        context.interpolationQuality = .high
        context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
    }
    return bytes
}

let args = CommandLine.arguments
guard args.count == 9,
      let x = Int(args[4]), let y = Int(args[5]),
      let patchWidth = Int(args[6]), let patchHeight = Int(args[7]),
      let featherPx = Double(args[8]), featherPx > 0 else {
    fputs("usage: compose_owner_correction_patch.swift base.png edit.png out.png x y width height feather_px\n", stderr)
    exit(2)
}

let original = readImage(args[1])
let edited = readImage(args[2])
let width = original.width
let height = original.height
guard x >= 0, y >= 0, patchWidth > 0, patchHeight > 0,
      x + patchWidth <= width, y + patchHeight <= height else {
    fatalError("Patch rectangle is outside the base canvas")
}
var base = rgba(original, width: width, height: height)
let patch = rgba(edited, width: width, height: height)

for py in y..<(y + patchHeight) {
    for px in x..<(x + patchWidth) {
        let edge = min(Double(px - x), Double(x + patchWidth - 1 - px),
                       Double(py - y), Double(y + patchHeight - 1 - py))
        let t = max(0.0, min(1.0, edge / featherPx))
        let alpha = t * t * (3.0 - 2.0 * t)
        let index = (py * width + px) * 4
        for channel in 0..<3 {
            let before = Double(base[index + channel])
            let after = Double(patch[index + channel])
            base[index + channel] = UInt8(max(0, min(255,
                (before * (1.0 - alpha) + after * alpha).rounded())))
        }
        base[index + 3] = 255
    }
}

let data = Data(base) as CFData
guard let provider = CGDataProvider(data: data),
      let output = CGImage(width: width, height: height, bitsPerComponent: 8,
                           bitsPerPixel: 32, bytesPerRow: width * 4,
                           space: CGColorSpace(name: CGColorSpace.sRGB)!,
                           bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)
                               .union(.byteOrder32Big),
                           provider: provider, decode: nil, shouldInterpolate: true,
                           intent: .defaultIntent),
      let destination = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[3]) as CFURL,
                                                        "public.png" as CFString, 1, nil) else {
    fatalError("Cannot encode output")
}
CGImageDestinationAddImage(destination, output, nil)
guard CGImageDestinationFinalize(destination) else { fatalError("PNG encode failed") }
print("\(width)x\(height) composited \(patchWidth)x\(patchHeight) local patch")
