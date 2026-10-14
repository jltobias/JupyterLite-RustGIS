"""Build a single GitHub Pages tree for JupyterLite, Jupyter Book, and maps."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"

def run(*args):
    subprocess.run([sys.executable, "-m", *args], cwd=ROOT, check=True)

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    run("jupyter", "lite", "build", "--contents", "lite", "--output-dir", str(SITE / "lab"))
    subprocess.run([shutil.which("jupyter-book") or "jupyter-book", "build", "book", "--path-output", str(SITE / "book-build")], cwd=ROOT, check=True)
    shutil.copytree(SITE / "book-build" / "_build" / "html", SITE / "book")
    shutil.rmtree(SITE / "book-build")
    shutil.copytree(ROOT / "data", SITE / "data")
    shutil.copytree(ROOT / "assets", SITE / "assets")
    maps = SITE / "maps"
    maps.mkdir()
    for name in ("2d", "3d", "scene"):
        shutil.copyfile(ROOT / "maps" / "view.html", maps / f"{name}.html")
    (SITE / "index.html").write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JupyterLite–RustGIS</title><style>body{font:1.2rem system-ui;max-width:800px;margin:7vh auto;padding:1rem;background:#102034;color:#f6f9fa}a{color:#87deee}li{margin:.7rem 0}img{width:100%;border-radius:12px}</style><h1>JupyterLite–RustGIS</h1><img src="assets/rustgis-splash.png" alt="Stylized terrain globe"><p>Browser notebooks and geospatial views inspired by RustGIS.</p><ul><li><a href="lab/index.html">JupyterLite Lab</a></li><li><a href="book/index.html">Jupyter Book</a></li><li><a href="maps/2d.html">2D map</a></li><li><a href="maps/3d.html">3D map</a></li><li><a href="maps/scene.html">3D scene</a></li><li><a href="https://web.rustgis.app/">RustGIS web app</a></li></ul></html>''', encoding="utf-8")
    (SITE / ".nojekyll").touch()

if __name__ == "__main__":
    main()
