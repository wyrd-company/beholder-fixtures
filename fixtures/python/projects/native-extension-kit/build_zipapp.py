import pathlib
import zipfile
import os

dist = pathlib.Path("dist")
dist.mkdir(parents=True, exist_ok=True)
src = pathlib.Path("zip_src/native_app")
out = dist / "native_app.pyz"
fixed_date = (1980, 1, 1, 0, 0, 0)
with zipfile.ZipFile(str(out), "w", compression=zipfile.ZIP_DEFLATED) as zf:
    main_src = src / "__main__.py"
    zi = zipfile.ZipInfo("__main__.py", date_time=fixed_date)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(zi, main_src.read_text(encoding="utf-8"))
    for p in sorted(src.rglob("*")):
        if p.is_file() and p.name != "__main__.py" and "__pycache__" not in p.parts:
            rel = "native_app/" + str(p.relative_to(src))
            zi2 = zipfile.ZipInfo(rel, date_time=fixed_date)
            zi2.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zi2, p.read_bytes())
data = out.read_bytes()
if not data.startswith(b"#!"):
    out.write_bytes(b"#!/usr/bin/env python3\n" + data)
    try:
        os.chmod(out, 0o755)
    except Exception:
        pass
print(f"built {out}")
print(zipfile.ZipFile(str(out)).namelist())
