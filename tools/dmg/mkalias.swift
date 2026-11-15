import AppKit
let a = CommandLine.arguments  // target aliasPath iconPng
let target = URL(fileURLWithPath: a[1]), out = URL(fileURLWithPath: a[2])
let data = try target.bookmarkData(options: .suitableForBookmarkFile, includingResourceValuesForKeys: nil, relativeTo: nil)
try? FileManager.default.removeItem(at: out)
try URL.writeBookmarkData(data, to: out)
let ok = NSWorkspace.shared.setIcon(NSImage(contentsOfFile: a[3]), forFile: out.path, options: [])
print(ok ? "icon set" : "icon failed")
