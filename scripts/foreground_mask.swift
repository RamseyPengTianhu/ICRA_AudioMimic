// Local foreground masks only. The companion PNG operation preserves original
// robot RGB samples and changes only alpha, as explicitly authorized by user.
import Foundation
import Vision
import ImageIO
import CoreImage

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("Usage: foreground_mask INPUT OUTPUT_MASK.png") }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])
let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(url: input, options: [:])
try handler.perform([request])
guard let observation = request.results?.first else { fatalError("No foreground detected") }
let buffer = try observation.generateScaledMaskForImage(forInstances: observation.allInstances, from: handler)
let mask = CIImage(cvPixelBuffer: buffer)
let context = CIContext()
try context.writePNGRepresentation(of: mask, to: output, format: .RGBA8,
                                  colorSpace: CGColorSpaceCreateDeviceRGB())
print("Foreground instances: \(observation.allInstances.count); wrote \(output.lastPathComponent)")
