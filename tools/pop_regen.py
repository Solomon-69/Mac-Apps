import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_glass import popover, root
for f in sorted(root.glob("*/img/pop-*.png")):
    src = f.parent/f.name[4:]
    popover(str(src.relative_to(root)), str(f.relative_to(root)), "dark" in f.name); print(f.name)
