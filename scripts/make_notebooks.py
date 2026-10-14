"""Write the teaching notebooks as standard notebook JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS = [ROOT / "notebooks", ROOT / "lite"]

def markdown(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}

def code(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.splitlines(True)}

def write(name, cells, destinations=DESTINATIONS):
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3 (Pyodide)", "language": "python", "name": "python"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    for destination in destinations:
        destination.mkdir(exist_ok=True)
        (destination / name).write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")

write("01_explore_geojson.ipynb", [
    markdown("# Explore the teaching GeoJSON\n\nThis notebook runs in JupyterLite with only the Python standard library. The features and heights are illustrative, not survey data.\n"),
    code("import json\nfrom pathlib import Path\n\ndata = json.loads(Path('data/demo_features.geojson').read_text())\nlen(data['features']), data['name']\n"),
    code("from collections import Counter\nCounter(feature['geometry']['type'] for feature in data['features'])\n"),
    code("coordinates = [point for feature in data['features'] for ring in (feature['geometry']['coordinates'] if feature['geometry']['type'] == 'Polygon' else [[feature['geometry']['coordinates']]]) for point in ring]\nxs, ys = zip(*coordinates)\nprint(f'Bounds (lon/lat): {min(xs):.4f}, {min(ys):.4f}, {max(xs):.4f}, {max(ys):.4f}')\n"),
    markdown("## Try it in RustGIS\n\nDownload `data/demo_features.geojson` from the Lab file browser, then open it in the [official RustGIS web app](https://web.rustgis.app/). Compare the layer's extent to the bounds above.\n")
])
write("02_map_links.ipynb", [
    markdown("# Compare 2D and 3D views\n\nThe maps use the same illustrative GeoJSON as notebook 01. They are companion MapLibre visualizations; RustGIS itself runs in its [official browser app](https://web.rustgis.app/).\n"),
    code('''from IPython.display import display, HTML
base = '../maps/'
for label, page in [('2D map', '2d.html'), ('3D extruded map', '3d.html'), ('3D scene', 'scene.html')]:
    display(HTML(f'<p><a href="{base}{page}" target="_blank" rel="noopener">Open {label}</a></p>'))
'''),
    markdown("**Compare:** Which view makes the polygon footprint easiest to judge? Which makes the invented `height_m` differences easiest to see? Open the GeoJSON in RustGIS and compare its native map or globe view.\n")
])
write("03_rustgis_bridge.ipynb", [
    markdown("# From teaching data to RustGIS\n\nRustGIS can open GeoJSON in its browser app. Its native Python package works in a local Python notebook, but is unavailable in JupyterLite's Pyodide kernel. This notebook prepares a small selection you can open in the RustGIS web app.\n"),
    code("import json\nfrom pathlib import Path\nfeatures = json.loads(Path('data/demo_features.geojson').read_text())['features']\nselected = {'type': 'FeatureCollection', 'features': [f for f in features if f['geometry']['type'] == 'Polygon']}\nPath('selected_footprints.geojson').write_text(json.dumps(selected, indent=2))\nprint('Saved', len(selected['features']), 'illustrative footprints.')\n"),
    markdown("Download `selected_footprints.geojson` from the Lab file browser. In [RustGIS Web](https://web.rustgis.app/), open the file, symbolize the polygon layer, and inspect its attributes. For `rustgis.Session`, continue with the [native notebook](https://github.com/jltobias/JupyterLite-RustGIS/blob/main/notebooks/04_native_rustgis.ipynb).\n")
])
write("04_native_rustgis.ipynb", [
    markdown("# Native RustGIS Python session\n\n**Run locally in Jupyter, not in JupyterLite.** Install the upstream native package with `python -m pip install rustgis`. See the [RustGIS Python guide](https://github.com/opengeos/RustGIS/blob/main/docs/python.md).\n"),
    code("import rustgis\n\nsession = rustgis.Session(sample=True)\nsession\n"),
    code("session.to_png('rustgis_sample.png')\nfrom IPython.display import Image, display\ndisplay(Image(filename='rustgis_sample.png'))\n"),
    markdown("## Buffer the sample cities\n\nThe call below follows the command form shown in the [RustGIS README](https://github.com/opengeos/RustGIS#quick-start). The distance value is interpreted by the current tool and project settings; consult the upstream tool help before applying it to your own data.\n"),
    code("session.run('gp.run', tool='buffer', params={'input': 'Cities', 'distance': 100})\nsession.to_png('rustgis_city_buffers.png')\ndisplay(Image(filename='rustgis_city_buffers.png'))\n"),
    markdown("The upstream sample project is used here because the native API's file import signatures can change. Consult the [upstream documentation](https://github.com/opengeos/RustGIS/blob/main/docs/python.md) before adapting the session to your own data.\n")
], [ROOT / "notebooks"])

lite_data = ROOT / "lite" / "data"
lite_data.mkdir(exist_ok=True)
(lite_data / "demo_features.geojson").write_bytes((ROOT / "data" / "demo_features.geojson").read_bytes())
