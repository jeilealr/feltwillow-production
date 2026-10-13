import AppKit
import Foundation

let repo = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let planURL = repo.appendingPathComponent("stories/lion_and_mouse_v6/keyframe_plan.json")
let outputDir = repo.appendingPathComponent("character/characters/lion_and_mouse_v6/interactions/keyframes/.review/contact_sheets/current", isDirectory: true)
try FileManager.default.createDirectory(at: outputDir, withIntermediateDirectories: true)
let data = try Data(contentsOf: planURL)
let document = try JSONSerialization.jsonObject(with: data) as! [String: Any]
let rows = document["images"] as! [[String: Any]]
let boundaryURL = repo.appendingPathComponent("stories/lion_and_mouse_v6/video_boundary_plan.json")
let boundaryData = try Data(contentsOf: boundaryURL)
let boundaryPlan = try JSONSerialization.jsonObject(with: boundaryData) as! [String: Any]
let boundaryScenes = boundaryPlan["scenes"] as! [[String: Any]]
let orderByScene: [Int: [String: Int]] = Dictionary(uniqueKeysWithValues: boundaryScenes.map { scene in
    let ids = scene["ordered_keyframes"] as! [String]
    return (scene["scene"] as! Int, Dictionary(uniqueKeysWithValues: ids.enumerated().map { ($0.element, $0.offset) }))
})
let tileW = 480
let imageH = 270
let labelH = 34
let margin = 24
let gap = 14
let headerH = 58
let columns = 3

for scene in 1...16 {
    let sceneRows = rows.filter { ($0["scene"] as? Int) == scene }
        .sorted {
            let first = $0["id"] as! String
            let second = $1["id"] as! String
            return (orderByScene[scene]?[first] ?? Int.max, first) <
                   (orderByScene[scene]?[second] ?? Int.max, second)
        }
    let rowCount = Int(ceil(Double(sceneRows.count) / Double(columns)))
    let width = 2 * margin + columns * tileW + (columns - 1) * gap
    let height = 2 * margin + headerH + rowCount * (imageH + labelH) + max(0, rowCount - 1) * gap
    guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0),
        let context = NSGraphicsContext(bitmapImageRep: bitmap) else { fatalError("Cannot create sheet") }
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    NSColor(calibratedWhite: 0.12, alpha: 1).setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    let title = String(format: "Scene %02d — CURRENT keyframe candidates", scene)
    (title as NSString).draw(at: NSPoint(x: margin, y: height - margin - 35), withAttributes: [
        .font: NSFont.boldSystemFont(ofSize: 24), .foregroundColor: NSColor.white])
    for (index, row) in sceneRows.enumerated() {
        let id = row["id"] as! String
        let relPath = row["candidate_path"] as! String
        guard let picture = NSImage(contentsOf: repo.appendingPathComponent(relPath)) else { fatalError("Missing \(relPath)") }
        let column = index % columns
        let line = index / columns
        let x = margin + column * (tileW + gap)
        let y = height - margin - headerH - (line + 1) * (imageH + labelH) - line * gap
        picture.draw(in: NSRect(x: x, y: y + labelH, width: tileW, height: imageH),
            from: .zero, operation: .sourceOver, fraction: 1)
        let version = URL(fileURLWithPath: relPath).deletingPathExtension().lastPathComponent
        ("\(id)  •  \(version)" as NSString).draw(at: NSPoint(x: x + 2, y: y + 8), withAttributes: [
            .font: NSFont.systemFont(ofSize: 15), .foregroundColor: NSColor.white])
    }
    context.flushGraphics()
    NSGraphicsContext.restoreGraphicsState()
    let output = outputDir.appendingPathComponent(String(format: "scene%02d_keyframes.png", scene))
    try bitmap.representation(using: .png, properties: [:])!.write(to: output)
    print(output.path)
}

let manifestRows: [[String: Any]] = rows.map { row in
    ["id": row["id"]!, "scene": row["scene"]!,
     "candidate_path": row["candidate_path"]!, "sha256": row["sha256"]!]
}
let manifest: [String: Any] = ["story": "lion_and_mouse_v6", "images": manifestRows]
let manifestData = try JSONSerialization.data(withJSONObject: manifest, options: [.prettyPrinted, .sortedKeys])
try manifestData.write(to: outputDir.appendingPathComponent("manifest.json"))
