# Notebook workflow

1. Open [notebook 00 in the Lab](https://jltobias.github.io/JupyterLite-RustGIS/lab/lab/index.html?path=00_start_here.ipynb). Read the runtime diagram and watch the captioned workflow explainer.
2. Run notebooks 01–03 to inspect the illustrative GeoJSON, compare the [2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html), [3D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html), and [3D scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html), and export a handoff package.
3. Run notebooks 04–05 for bounded STAC discovery using the user's STAC Browser client. Open the saved Item footprints in [RustGIS Web](https://web.rustgis.app/) and keep the query provenance.
4. Use notebook 06 to decide whether a climate table is map-ready, notebook 07 to understand Ollama-assisted RustGIS, and notebooks 08–09 for perspective comparison and a reproducible capstone.
5. To run actual RustGIS Python commands, install `rustgis` in a local Python environment and run `04_native_rustgis.ipynb` there. Pyodide cannot load native RustGIS wheels.

The companion 2D and 3D maps use MapLibre GL JS; the separate orbitable scene uses Three.js. They illustrate concepts applicable to RustGIS but do not execute RustGIS commands.

## Native RustGIS analysis

The local notebook creates `rustgis.Session(sample=True)`, exports a map with `session.to_png(...)`, and invokes RustGIS geoprocessing with `session.run('gp.run', tool='buffer', params={'input': 'Cities', 'distance': 100})`. These calls follow the [upstream RustGIS quick start](https://github.com/opengeos/RustGIS#quick-start). Check the current tool help and project units before adapting the buffer distance to real data.
