# Visual gallery

Compare the same invented footprints across three companion views and the official RustGIS app:

| View | What it emphasizes | Main limitation |
| --- | --- | --- |
| [2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html) | Position and footprint shape | Height is an attribute rather than visible depth |
| [3D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html) | Relative extruded heights | Perspective and occlusion affect comparison |
| [3D scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html) | Oblique spatial context | Distances and areas can appear distorted |
| [RustGIS globe](https://web.rustgis.app/?blank&projection=globe&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fdemo_features.geojson) | Global orientation in the actual RustGIS app | The tiny teaching layer is difficult to see at global scale; zoom in |

The 2D and extruded 3D companion maps use MapLibre GL JS and OpenStreetMap tiles with visible attribution. The separate orbitable scene uses Three.js and no basemap. They are not RustGIS renders. The direct RustGIS link opens the upstream app with hosted GeoJSON.

![Cartographic splash](../assets/rustgis-splash.png)
