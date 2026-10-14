# JupyterLite–RustGIS

![Stylized terrain globe introducing JupyterLite–RustGIS](assets/rustgis-splash.png)

Explore geospatial workflows through **ten browser notebooks**, a Jupyter Book, and interactive 2D and 3D examples. The course connects an illustrative GeoJSON layer, a WorldPop STAC metadata snapshot from the user's STAC Browser workflow, and a CMIP6 table from a sister repository.

| Explore | Link |
| --- | --- |
| JupyterLite Lab | [Launch the browser lab](https://jltobias.github.io/JupyterLite-RustGIS/lab/lab/index.html) |
| Jupyter Book | [Read the guide](https://jltobias.github.io/JupyterLite-RustGIS/book/index.html) |
| 2D maps | [Open the 2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html) |
| 3D maps | [Open the extruded 3D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html) |
| 3D Scenes | [Open the 3D scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html) |
| RustGIS | [Launch the official RustGIS web app](https://web.rustgis.app/) |
| STAC Browser | [Open the sister Explorer](https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/) |

The first five links become live after the `Deploy site` workflow succeeds on `main` and GitHub Pages is set to **GitHub Actions**. The RustGIS link opens upstream now.

## What runs where

The browser Lab runs JupyterLite's Pyodide kernel. The ten notebooks include code, charts, diagrams, a captioned explainer video, STAC discovery, 2D/3D map links, and reproducible data exports. The official [RustGIS Python binding](https://github.com/opengeos/RustGIS/blob/main/docs/python.md) is native and cannot run in Pyodide. The [native RustGIS notebook](notebooks/04_native_rustgis.ipynb) shows actual `rustgis.Session` rendering and buffer analysis for local Jupyter. Companion maps use MapLibre GL JS and the standalone scene uses Three.js; they are not RustGIS renders. The notebooks also link directly into [RustGIS Web](https://web.rustgis.app/?blank&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fdemo_features.geojson) with hosted GeoJSON, using [RustGIS's documented URL parameters](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app).

## Notebook course

| Notebook | Focus |
| --- | --- |
| `00_start_here` | Runtime boundaries and learning route |
| `01_explore_geojson` | Geometry, attributes, extent, and visual checks |
| `02_map_links` | 2D, extruded 3D, scene, and RustGIS globe comparisons |
| `03_rustgis_bridge` | GeoJSON export and provenance manifest |
| `04_stac_worldpop` | WorldPop STAC Items, optional live search, and RustGIS handoff |
| `05_stac_catalogs` | Bounded searches across public STAC APIs |
| `06_climate_scenarios` | CMIP6 table parsing, charts, and map-readiness check |
| `07_ollama_assistance` | RustGIS AI Assistant setup and validated plan exercise |
| `08_globe_and_scene` | Projection and perspective reasoning |
| `09_capstone` | Reproducible STAC-to-RustGIS brief |

Start with [notebook 00 in the Lab](https://jltobias.github.io/JupyterLite-RustGIS/lab/lab/index.html?path=00_start_here.ipynb). Live STAC queries are optional and may be affected by provider availability or browser CORS; a frozen metadata snapshot keeps the lessons runnable offline. Ollama runs locally and requires separate setup and an allowed browser origin for RustGIS Web.

Sample points, polygons, and heights are hand-authored teaching fixtures, not surveyed data. The WorldPop snapshot contains Degree of Urbanisation Item footprints for Uganda, describing **metadata coverage, not raster pixel values**. See [data and code provenance](DATA_SOURCES.md).

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
- **Three.js:** Three.js contributors, [source and MIT license](https://github.com/mrdoob/three.js), used in the standalone 3D scene.
- **Related teaching repositories:** [JupyterLite-GeoLibre-GeoAI](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI) informed the Ollama exercise; [JupyterLite-zarr-sql-views](https://github.com/jltobias/JupyterLite-zarr-sql-views) supplied the attributed CMIP6 table.
- **STAC Browser:** jltobias, [JupyterLite-STAC-Browser](https://github.com/jltobias/JupyterLite-STAC-Browser). Its Pyodide client is included under its MIT license; the WorldPop snapshot records its provider query and retrieval date.
- **WorldPop:** [WorldPop STAC API](https://api.stac.worldpop.org) and [Uganda Collection](https://api.stac.worldpop.org/collections/UGA), which advertises CC BY 4.0. The bundled Degree of Urbanisation Items are metadata footprints; their provenance is in [DATA_SOURCES.md](DATA_SOURCES.md).
- **C3S Atlas user tools:** ECMWF/Copernicus Climate Change Service, [source](https://github.com/ecmwf-projects/c3s-atlas) and [Apache 2.0 notice](licenses/c3s-atlas-Apache-2.0.txt). The CMIP6 warming-level table is copied through the user's `JupyterLite-zarr-sql-views` repository.
- **Ollama:** [official project](https://ollama.com/); see the [RustGIS AI Assistant guide](https://github.com/opengeos/RustGIS/blob/main/docs/user-guide/assistant.md) for local provider configuration.

See [CITATION.cff](CITATION.cff) for citing this repository and [book/references.md](book/references.md) for the book's references.
