// Crop an approved plate in native pixel space for a registered camera view.
// Usage: swift production/crop_plate.swift input.png output.png x y w h
// x, y, w, h are normalized against the full input image.
import AppKit
import Foundation

guard CommandLine.arguments.count == 7 else {
    fputs("usage: crop_plate.swift input output x y w h\n", stderr)
    exit(2)
}
let args = CommandLine.arguments
guard let image = NSImage(contentsOfFile: args[1]),
      let source = image.cgImage(forProposedRect: nil, context: nil, hints: nil),
      let x = Double(args[3]), let y = Double(args[4]),
      let w = Double(args[5]), let h = Double(args[6]) else {
    fputs("invalid image or crop arguments\n", stderr)
    exit(2)
}
let width = source.width, height = source.height
let rect = CGRect(x: Int((x * Double(width)).rounded()),
                  y: Int((y * Double(height)).rounded()),
                  width: max(1, Int((w * Double(width)).rounded())),
                  height: max(1, Int((h * Double(height)).rounded())))
guard let cropped = source.cropping(to: rect),
      let data = NSBitmapImageRep(cgImage: cropped).representation(using: .png, properties: [:]) else {
    fputs("crop falls outside plate\n", stderr)
    exit(2)
}
try FileManager.default.createDirectory(at: URL(fileURLWithPath: args[2]).deletingLastPathComponent(),
                                        withIntermediateDirectories: true)
try data.write(to: URL(fileURLWithPath: args[2]), options: .atomic)
