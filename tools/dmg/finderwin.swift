import CoreGraphics
let want = CommandLine.arguments[1]
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as! [[String: Any]]
for w in list where (w["kCGWindowOwnerName"] as? String) == "Finder" && (w["kCGWindowName"] as? String) == want {
  print(w["kCGWindowNumber"] as! Int); break
}
