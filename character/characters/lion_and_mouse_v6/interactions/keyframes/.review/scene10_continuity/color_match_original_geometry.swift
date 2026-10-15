import Foundation
import CoreGraphics
import ImageIO

let args = CommandLine.arguments
guard args.count == 6,
      let red = Double(args[3]), let green = Double(args[4]), let blue = Double(args[5]),
      let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: args[1]) as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else { fatalError("input output Rgain Ggain Bgain required") }
let width = image.width, height = image.height
let space = CGColorSpace(name: CGColorSpace.sRGB)!
let flags = CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Big.rawValue
var bytes = [UInt8](repeating: 0, count: width * height * 4)
bytes.withUnsafeMutableBytes { raw in
    let context = CGContext(data: raw.baseAddress, width: width, height: height,
        bitsPerComponent: 8, bytesPerRow: width * 4, space: space, bitmapInfo: flags)!
    context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
}
let gains = [red, green, blue]
for i in stride(from: 0, to: bytes.count, by: 4) {
    for channel in 0..<3 {
        bytes[i + channel] = UInt8(max(0, min(255,
            (Double(bytes[i + channel]) * gains[channel]).rounded())))
    }
}
let provider = CGDataProvider(data: Data(bytes) as CFData)!
let output = CGImage(width: width, height: height, bitsPerComponent: 8, bitsPerPixel: 32,
    bytesPerRow: width * 4, space: space,
    bitmapInfo: CGBitmapInfo(rawValue: flags), provider: provider, decode: nil,
    shouldInterpolate: false, intent: .defaultIntent)!
let destination = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[2]) as CFURL,
    "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(destination, output, nil)
guard CGImageDestinationFinalize(destination) else { fatalError("output failed") }
print("\(width)x\(height): original geometry retained; RGB gains \(gains)")
