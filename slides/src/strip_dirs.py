import sys, zipfile, shutil, os
src = sys.argv[1]; tmp = src + ".tmp"
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        if not it.filename.endswith("/"):
            zo.writestr(it, zi.read(it.filename))
os.replace(tmp, src)
