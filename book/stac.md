# STAC Browser to RustGIS

![Five-step STAC to RustGIS infographic](../assets/stac-rustgis-flow.svg)

The [STAC Browser Explorer](https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/) is the discovery interface. In notebook 04, its Pyodide-compatible client searches the [WorldPop STAC API](https://api.stac.worldpop.org) with a bounded Uganda query. A three-item snapshot is bundled so the lesson remains usable when a provider is offline or blocks browser requests. The query URL, retrieval date, and Item IDs are in [`worldpop_provenance.json`](https://github.com/jltobias/JupyterLite-RustGIS/blob/main/data/worldpop_provenance.json).

The resulting GeoJSON can be [opened directly in RustGIS Web](https://web.rustgis.app/?blank&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fworldpop_uga_items.geojson). RustGIS's [documented web URL syntax](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app) supports `?data=` when the host permits browser fetches. A file created inside JupyterLite must be downloaded and opened through RustGIS's file picker; it does not automatically become a public URL.

:::{important}
An Item polygon describes **catalog coverage**. These Items are Degree of Urbanisation products, and their footprints do not visualize pixel values, uncertainty, or license rights. Inspect the collection license, provider, asset roles, and access requirements before downloading data.
:::

<video controls preload="metadata" width="760" src="../assets/stac-rustgis-tour.mp4">A captioned five-step STAC to RustGIS explainer.</video>

[Open or download the captioned explainer video](../assets/stac-rustgis-tour.mp4).

**Video transcript:** Discover a public STAC collection; bound the query in space, time, and page size; inspect license and assets; export GeoJSON and query provenance; open the result in RustGIS.
