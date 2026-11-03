import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_glass import popover, root
only = sys.argv[1:]
for src in sorted(root.glob("*/img/*.png")):
    if src.name.startswith("pop-") or "icon" in src.name or "/win/" in str(src): continue
    dst = src.parent/("pop-"+src.name)
    if not dst.exists() and not (only and src.parent.parent.name in only and ("panel" in src.name or "settings" in src.name)): continue
    if only and src.parent.parent.name not in only: continue
    popover(str(src.relative_to(root)), str(dst.relative_to(root)), "dark" in src.name); print(dst.name)
