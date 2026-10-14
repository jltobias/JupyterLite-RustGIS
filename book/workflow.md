# Notebook workflow

1. Open the [Lab](https://jltobias.github.io/JupyterLite-RustGIS/lab/index.html) and run `01_explore_geojson.ipynb`. It checks geometry and computes a bounding box without extra packages.
2. Run `02_map_links.ipynb` to compare features in the [2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html), [3D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html), and [3D scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html).
3. Open bundled `data/demo_features.geojson` in the [RustGIS web app](https://web.rustgis.app/) using its file picker. Try styling features and comparing the 2D and globe views.
4. To run actual RustGIS Python commands, install `rustgis` in a local Python environment and run `04_native_rustgis.ipynb` there. Pyodide cannot load native RustGIS wheels.

The companion map pages use MapLibre GL JS and the same GeoJSON. They illustrate concepts applicable to RustGIS but do not execute RustGIS commands.

## Native RustGIS analysis

The local notebook creates `rustgis.Session(sample=True)`, exports a map with `session.to_png(...)`, and invokes RustGIS geoprocessing with `session.run('gp.run', tool='buffer', params={'input': 'Cities', 'distance': 100})`. These calls follow the [upstream RustGIS quick start](https://github.com/opengeos/RustGIS#quick-start). Check the current tool help and project units before adapting the buffer distance to real data.
