#import <AppKit/AppKit.h>
#import <CommonCrypto/CommonDigest.h>

// Supplementary review PNG. The 16 active sheets and their manifest stay separate.
static NSString *SHA256AtURL(NSURL *url) {
    NSData *data = [NSData dataWithContentsOfURL:url];
    if (!data) @throw [NSException exceptionWithName:@"MissingImage" reason:url.path userInfo:nil];
    unsigned char digest[CC_SHA256_DIGEST_LENGTH];
    CC_SHA256(data.bytes, (CC_LONG)data.length, digest);
    NSMutableString *result = [NSMutableString string];
    for (int i = 0; i < CC_SHA256_DIGEST_LENGTH; i++) [result appendFormat:@"%02x", digest[i]];
    return result;
}

static NSDictionary *ReadJSON(NSURL *url) {
    NSData *data = [NSData dataWithContentsOfURL:url];
    if (!data) @throw [NSException exceptionWithName:@"MissingJSON" reason:url.path userInfo:nil];
    return [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
}

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        if (argc != 2) {
            fprintf(stderr, "usage: build_keyframe_material_comparison REPO_ROOT\n");
            return 2;
        }
        NSURL *repo = [NSURL fileURLWithPath:[NSString stringWithUTF8String:argv[1]] isDirectory:YES];
        NSString *base = @"character/characters/lion_and_mouse_v6/interactions/keyframes";
        NSURL *current = [repo URLByAppendingPathComponent:
            [base stringByAppendingPathComponent:@".review/contact_sheets/current"] isDirectory:YES];
        NSDictionary *config = ReadJSON([repo URLByAppendingPathComponent:
            [base stringByAppendingPathComponent:@".review/material_calibration/comparison_manifest.json"]]);
        NSDictionary *plan = ReadJSON([repo URLByAppendingPathComponent:
            @"stories/lion_and_mouse_v6/keyframe_plan.json"]);
        NSMutableDictionary *frames = [NSMutableDictionary dictionary];
        for (NSDictionary *frame in plan[@"images"]) frames[frame[@"id"]] = frame;
        NSArray *entries = config[@"entries"];

        const NSInteger tileW = 640, imageH = 360, labelH = 34;
        const NSInteger margin = 24, gap = 18, headerH = 82, rowGap = 22;
        NSInteger width = 2 * margin + 2 * tileW + gap;
        NSInteger height = 2 * margin + headerH + entries.count * (imageH + labelH) +
            MAX(0, (NSInteger)entries.count - 1) * rowGap;
        NSBitmapImageRep *bitmap = [[NSBitmapImageRep alloc]
            initWithBitmapDataPlanes:NULL pixelsWide:width pixelsHigh:height
            bitsPerSample:8 samplesPerPixel:4 hasAlpha:YES isPlanar:NO
            colorSpaceName:NSDeviceRGBColorSpace bytesPerRow:0 bitsPerPixel:0];
        NSGraphicsContext *context = [NSGraphicsContext graphicsContextWithBitmapImageRep:bitmap];
        [NSGraphicsContext saveGraphicsState];
        [NSGraphicsContext setCurrentContext:context];
        [[NSColor colorWithCalibratedWhite:0.12 alpha:1] setFill];
        NSRectFill(NSMakeRect(0, 0, width, height));
        [@"Leo material trials — NOT ACTIVE KEYFRAMES" drawAtPoint:
            NSMakePoint(margin, height - margin - 32) withAttributes:@{
            NSFontAttributeName: [NSFont boldSystemFontOfSize:25],
            NSForegroundColorAttributeName: NSColor.whiteColor}];
        [@"Compare color and texture; trial framing/geometry failed review" drawAtPoint:
            NSMakePoint(margin, height - margin - 58) withAttributes:@{
            NSFontAttributeName: [NSFont systemFontOfSize:16],
            NSForegroundColorAttributeName: [NSColor colorWithCalibratedRed:1 green:0.73 blue:0.54 alpha:1]}];

        NSMutableArray *outputEntries = [NSMutableArray array];
        NSInteger index = 0;
        for (NSDictionary *entry in entries) {
            NSString *frameID = entry[@"frame_id"];
            NSDictionary *frame = frames[frameID];
            NSString *sourcePath = frame[@"candidate_path"];
            NSString *sourceHash = frame[@"sha256"];
            NSString *trialPath = entry[@"trial_path"];
            NSString *trialHash = entry[@"trial_sha256"];
            if (!sourcePath || ![sourceHash isEqualToString:entry[@"source_sha256"]]) {
                @throw [NSException exceptionWithName:@"StaleComparison"
                    reason:[NSString stringWithFormat:@"%@ active source changed", frameID] userInfo:nil];
            }
            NSURL *sourceURL = [repo URLByAppendingPathComponent:sourcePath];
            NSURL *trialURL = [repo URLByAppendingPathComponent:trialPath];
            if (![SHA256AtURL(sourceURL) isEqualToString:sourceHash] ||
                ![SHA256AtURL(trialURL) isEqualToString:trialHash]) {
                @throw [NSException exceptionWithName:@"StaleComparison"
                    reason:[NSString stringWithFormat:@"%@ image hash differs", frameID] userInfo:nil];
            }
            CGFloat y = height - margin - headerH - (index + 1) * (imageH + labelH) - index * rowGap;
            NSArray *urls = @[sourceURL, trialURL];
            NSArray *labels = @[
                [NSString stringWithFormat:@"CURRENT %@ • %@", frameID, sourceURL.lastPathComponent],
                [NSString stringWithFormat:@"TRIAL %@ • material r01 • REJECTED geometry", frameID]
            ];
            for (NSInteger column = 0; column < 2; column++) {
                NSImage *picture = [[NSImage alloc] initWithContentsOfURL:urls[column]];
                if (!picture) @throw [NSException exceptionWithName:@"MissingImage" reason:urls[column] userInfo:nil];
                CGFloat x = margin + column * (tileW + gap);
                [picture drawInRect:NSMakeRect(x, y + labelH, tileW, imageH)
                    fromRect:NSZeroRect operation:NSCompositingOperationSourceOver fraction:1];
                [labels[column] drawAtPoint:NSMakePoint(x + 2, y + 8) withAttributes:@{
                    NSFontAttributeName: [NSFont systemFontOfSize:15],
                    NSForegroundColorAttributeName: NSColor.whiteColor}];
            }
            [outputEntries addObject:@{@"frame_id": frameID, @"source_path": sourcePath,
                @"source_sha256": sourceHash, @"trial_path": trialPath,
                @"trial_sha256": trialHash, @"disposition": entry[@"disposition"]}];
            index++;
        }
        [context flushGraphics];
        [NSGraphicsContext restoreGraphicsState];
        [[NSFileManager defaultManager] createDirectoryAtURL:current withIntermediateDirectories:YES
            attributes:nil error:nil];
        NSURL *sheet = [current URLByAppendingPathComponent:@"material_color_comparison.png"];
        [[bitmap representationUsingType:NSBitmapImageFileTypePNG properties:@{}]
            writeToURL:sheet atomically:YES];
        NSDictionary *output = @{@"story": @"lion_and_mouse_v6",
            @"status": @"material_calibration_only_not_active", @"entries": outputEntries};
        NSData *manifest = [NSJSONSerialization dataWithJSONObject:output
            options:NSJSONWritingPrettyPrinted | NSJSONWritingSortedKeys error:nil];
        [manifest writeToURL:[current URLByAppendingPathComponent:@"material_color_comparison.json"]
            atomically:YES];
        puts(sheet.path.UTF8String);
        return 0;
    }
}
