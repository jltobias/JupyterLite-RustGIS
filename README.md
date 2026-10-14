# JupyterLite–RustGIS

![Stylized terrain globe introducing JupyterLite–RustGIS](assets/rustgis-splash.png)

Explore geospatial workflows through browser notebooks, a Jupyter Book, and interactive 2D and 3D examples. A small **illustrative** GeoJSON dataset connects every view.

| Explore | Link |
| --- | --- |
| JupyterLite Lab | [Launch the browser lab](https://jltobias.github.io/JupyterLite-RustGIS/lab/index.html) |
| Jupyter Book | [Read the guide](https://jltobias.github.io/JupyterLite-RustGIS/book/index.html) |
| 2D maps | [Open the 2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html) |
| 3D maps | [Open the extruded 3D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html) |
| 3D Scenes | [Open the 3D scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html) |
| RustGIS | [Launch the official RustGIS web app](https://web.rustgis.app/) |

The first five links become live after the `Deploy site` workflow succeeds on `main` and GitHub Pages is set to **GitHub Actions**. The RustGIS link opens upstream now.

## What runs where

The browser Lab runs JupyterLite's Pyodide kernel. Its notebooks explore bundled GeoJSON with Python's standard library and link to interactive maps. The official [RustGIS Python binding](https://github.com/opengeos/RustGIS/blob/main/docs/python.md) is native and cannot run in Pyodide. The [native RustGIS notebook](notebooks/04_native_rustgis.ipynb) shows actual `rustgis.Session` commands for local Jupyter. Companion maps use MapLibre GL JS; they are not RustGIS renders. Open the bundled data in the [RustGIS web app](https://web.rustgis.app/) to explore it with RustGIS itself.

Sample points, polygons, and heights are hand-authored teaching fixtures, not surveyed data.

## Local build

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py
python -m http.server 8000 -d _site
```

Open `http://localhost:8000/`. The build writes Lab to `_site/lab/`, the book to `_site/book/`, and map pages to `_site/maps/`.

## Sources and citation

- **RustGIS:** OpenGeos contributors, *RustGIS*, [source and Apache 2.0 license](https://github.com/opengeos/RustGIS), [documentation](https://rustgis.app/). Cite the repository with the version or commit used.
- **GeoLibre:** Wu, Q. (2026), *GeoLibre* (v3.2.0), DOI [10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400), [CITATION.cff](https://github.com/opengeos/GeoLibre/blob/main/CITATION.cff), [MIT license](https://github.com/opengeos/GeoLibre/blob/main/LICENSE). Related upstream software; not redistributed here.
- **JupyterLite:** Project Jupyter, [documentation](https://jupyterlite.readthedocs.io/) and [source](https://github.com/jupyterlite/jupyterlite).
- **Jupyter Book:** Executable Books Project, [documentation](https://jupyterbook.org/) and [source](https://github.com/executablebooks/jupyter-book).
- **MapLibre GL JS:** MapLibre contributors, [source and license](https://github.com/maplibre/maplibre-gl-js). Basemap tiles are supplied by [OpenStreetMap](https://www.openstreetmap.org/copyright), with attribution visible on each map.
- **Related teaching repositories:** [JupyterLite-GeoLibre-GeoAI](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI) and [JupyterLite-zarr-sql-views](https://github.com/jltobias/JupyterLite-zarr-sql-views) by jltobias informed the layout; no source files or data were copied.

See [CITATION.cff](CITATION.cff) for citing this repository and [book/references.md](book/references.md) for the book's references.
