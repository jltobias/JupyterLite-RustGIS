# Data and code provenance

## WorldPop STAC Item snapshot

`data/worldpop_uga_items.geojson` is a three-item STAC metadata response from the [WorldPop STAC API](https://api.stac.worldpop.org), retrieved 2026-10-14. The returned Items are **Degree of Urbanisation** products for Uganda (2028–2030), not population-count products. The exact bounded query, IDs, and retrieval date are recorded in `data/worldpop_provenance.json`. The [UGA Collection](https://api.stac.worldpop.org/collections/UGA) advertised `CC-BY-4.0` on that date. This file contains Item footprints, properties, and asset references, **not raster pixel values**. Asset access and any item-specific terms still need checking before downloading or publishing underlying data.

The companion `stac_browser.py` client in `lite/` and `notebooks/` is copied from [jltobias/JupyterLite-STAC-Browser](https://github.com/jltobias/JupyterLite-STAC-Browser), commit `13034913fc27b9dfff637c02ad799d6ebbd69538`, under the MIT license reproduced in `lite/STAC_BROWSER_LICENSE.txt`. The browser course uses its bounded search and provenance API.

## CMIP6 warming-level table

`data/CMIP6_WarmingLevels.csv` is copied unchanged from [jltobias/JupyterLite-zarr-sql-views](https://github.com/jltobias/JupyterLite-zarr-sql-views), commit `c0a4870ebfb6a099877d67ac8d6d8e4ae6b1112c`. That repository attributes the file to the [C3S Atlas user tools](https://github.com/ecmwf-projects/c3s-atlas), `auxiliar/GWLs/CMIP6_WarmingLevels.csv`, under Apache 2.0; the license text is in `licenses/c3s-atlas-Apache-2.0.txt`. The table gives model/scenario warming-level windows; it has no geometry and is not a regional map layer.

## Illustrative teaching data

`data/demo_features.geojson` was authored for this repository. Its heights and observation locations are invented teaching fixtures and must not be presented as surveyed geographic facts.

The generated splash image, diagrams, and silent captioned explainer video were created for this repository. The video transcript is included in notebook 00 and notebook 04.
