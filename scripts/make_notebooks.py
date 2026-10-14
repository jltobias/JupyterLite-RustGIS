"""Generate the browser course and the separate native RustGIS notebook."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://jltobias.github.io/JupyterLite-RustGIS"
STAC = "https://jltobias.github.io/JupyterLite-STAC-Browser"

def M(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip().splitlines(True)}

def C(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.strip().splitlines(True)}

def save(name, cells, browser=True):
    nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3 (Pyodide)" if browser else "Python 3", "language": "python", "name": "python"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    for folder in ([ROOT / "lite", ROOT / "notebooks"] if browser else [ROOT / "notebooks"]):
        folder.mkdir(exist_ok=True)
        (folder / name).write_text(json.dumps(nb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def media():
    return f'''![STAC to RustGIS workflow]({BASE}/assets/stac-rustgis-flow.svg)

<video controls preload="metadata" width="760" src="{BASE}/assets/stac-rustgis-tour.mp4">A captioned five-step STAC to RustGIS explainer.</video>

[Open or download the captioned explainer video]({BASE}/assets/stac-rustgis-tour.mp4).

**Video transcript:** Discover a public STAC collection; bound a search by area, date, and page size; inspect license and assets; export GeoJSON plus query provenance; open the result in RustGIS. Metadata footprints do not show raster pixel values.'''

def source_note():
    return f'''**Sources:** [RustGIS](https://github.com/opengeos/RustGIS), [RustGIS web URL parameters](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app), [your STAC Browser]({STAC}/explorer/), [STAC specification](https://stacspec.org/). All hosted data here is public teaching material. Check the provider's license before reusing STAC assets.'''

save("00_start_here.ipynb", [
    M(f'''# 0 · Start here: the RustGIS field guide

**Question:** how do catalog metadata, maps, 3D views, and AI assistance become one reproducible GIS workflow?

This course has ten browser notebooks. Run them in order or follow a branch that interests you. Every executable browser cell works without installing the native `rustgis` package. The separate `04_native_rustgis.ipynb` runs in local Jupyter with RustGIS installed.

![Where each runtime lives]({BASE}/assets/runtime-boundaries.svg)'''),
    M("## Learning route\n\n| Notebooks | Skill | Result |\n|---|---|---|\n| 01–03 | Geometry and browser maps | A validated GeoJSON handoff |\n| 04–05 | STAC discovery and provenance | WorldPop footprints and bounded searches |\n| 06 | Climate table from a sister repo | A scenario comparison chart |\n| 07 | Ollama and safe map plans | An inspectable assistant proposal |\n| 08–09 | Globe and capstone | A linked STAC → RustGIS workflow |"),
    M(media()),
    M("## Check the bundled files\n\nThe following cells use only the Python standard library. If you edit a bundled file, your browser copy takes precedence until you reset it in the JupyterLite file browser."),
    C('''from pathlib import Path
for path in sorted(Path('data').glob('*')):
    print(f'{path.name:34} {path.stat().st_size:>8,} bytes')'''),
    M("## Recognize the three runtimes\n\nJupyterLite is a Python kernel in your browser. RustGIS Web is a separate WebAssembly GIS app. Native RustGIS Python/CLI and Ollama run on a local machine. GeoJSON files and explicit URLs connect them; Python code in JupyterLite does not silently control RustGIS Web."),
    C('''import sys
print('Python:', sys.version.split()[0])
try:
    import pyodide
    print('Runtime: Pyodide in JupyterLite')
except ImportError:
    print('Runtime: local Python; browser-specific steps are optional')'''),
    M(f"## Open the real GIS\n\n[Launch RustGIS Web](https://web.rustgis.app/?blank&data={BASE}/data/demo_features.geojson) with the illustrative GeoJSON already linked. The web app accepts public data URLs when the server permits CORS. If loading fails, download the GeoJSON and use RustGIS **Add Data**."),
    C('''from IPython.display import display, HTML
display(HTML('<p><a target="_blank" rel="noopener" href="https://web.rustgis.app/?blank&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fdemo_features.geojson">Open the teaching layer in RustGIS Web ↗</a></p>'))'''),
    M("## Prediction prompt\n\nBefore continuing, write down what a STAC Item footprint can tell you, and what it cannot tell you about the underlying raster cells. Revisit this answer after notebook 04."),
    M(source_note()),
])

save("01_explore_geojson.ipynb", [
    M(f'''# 1 · Read a GeoJSON layer like an analyst

**Question:** what do geometry, properties, units, and provenance tell us before a map is drawn?

The five hand-authored features near Washington, DC are **illustrative**. The heights are invented. This is a safe sandbox for checking GIS assumptions before moving to provider data.

![Stylized cartographic splash]({BASE}/assets/rustgis-splash.png)'''),
    M("## Load and inspect\n\nA GeoJSON FeatureCollection is a list of features. Each feature has geometry and properties. Inspect the schema before choosing a map symbol or analysis tool."),
    C('''import json
from pathlib import Path
data = json.loads(Path('data/demo_features.geojson').read_text(encoding='utf-8'))
print(data['type'], data['name'], len(data['features']))
print(json.dumps(data['features'][0], indent=2)[:650])'''),
    M("## Summarize geometry types and attributes"),
    C('''from collections import Counter
features = data['features']
print('Geometry:', dict(Counter(f['geometry']['type'] for f in features)))
print('Kinds:', dict(Counter(f['properties']['kind'] for f in features)))
print('Fields:', sorted({key for f in features for key in f['properties']}))'''),
    M("## Compute the extent\n\nGeoJSON uses WGS84 longitude then latitude. An extent uses **west, south, east, north**. The code handles points and the vertices of the polygon rings."),
    C('''def vertices(feature):
    geometry = feature['geometry']
    if geometry['type'] == 'Point':
        return [geometry['coordinates']]
    if geometry['type'] == 'Polygon':
        return [point for ring in geometry['coordinates'] for point in ring]
    raise ValueError(f"Unsupported geometry: {geometry['type']}")
xy = [point for feature in features for point in vertices(feature)]
west, east = min(p[0] for p in xy), max(p[0] for p in xy)
south, north = min(p[1] for p in xy), max(p[1] for p in xy)
print('bbox:', [west, south, east, north])'''),
    M("## Visual check: schematic point view\n\nThis SVG is a quick diagnostic, not a projected basemap. Hover over a symbol to read its name."),
    C('''from IPython.display import display, HTML
from viz import points, bars
display(HTML(points(features, 'Teaching feature locations')))'''),
    M("## Compare invented heights\n\nHeight is only meaningful for polygon footprints here. Do not treat `height_m=0` on an observation point as a measured zero-height building."),
    C('''buildings = [f for f in features if f['properties']['kind'] == 'footprint']
display(HTML(bars([f['properties']['name'] for f in buildings], [f['properties']['height_m'] for f in buildings], 'Illustrative heights', ' m')))'''),
    M("## Validate before handoff"),
    C('''assert all(-180 <= x <= 180 and -90 <= y <= 90 for x, y in xy)
assert all(f['geometry']['coordinates'][0][0] == f['geometry']['coordinates'][0][-1] for f in buildings)
assert all(f['properties']['height_m'] > 0 for f in buildings)
print('Coordinate ranges, closed rings, and illustrative heights checked.')'''),
    M(f"## Compare with RustGIS\n\nOpen the [2D map]({BASE}/maps/2d.html) and the [official RustGIS app](https://web.rustgis.app/?blank&data={BASE}/data/demo_features.geojson). Can you find the same feature count and extent? Try RustGIS attribute table and layer symbology."),
    M("**Challenge:** change one illustrative height in your browser copy, rerun the chart, and describe which map view makes the change easiest to see. Reset the file after the exercise."),
    M(source_note()),
])

save("02_map_links.ipynb", [
    M(f'''# 2 · One dataset, three spatial views

**Question:** how does the visual encoding change what a reader can infer?

These are companion MapLibre maps plus a standalone Three.js scene of the same illustrative data. They are not RustGIS output. Open the same GeoJSON in RustGIS Web to compare its own map and globe.

![A diagram of browser and native runtimes]({BASE}/assets/runtime-boundaries.svg)'''),
    M(f"## Launch the interactive views\n\n- [2D map]({BASE}/maps/2d.html): footprints and locations\n- [3D extruded map]({BASE}/maps/3d.html): invented heights\n- [3D scene]({BASE}/maps/scene.html): pitched perspective\n\nDrag, tilt, and click. The map pages keep OpenStreetMap attribution visible."),
    C(f'''from IPython.display import HTML, display
base = '{BASE}/maps/'
for label, path in [('2D map','2d.html'),('3D map','3d.html'),('3D scene','scene.html')]:
    display(HTML(f'<p><a href="{{base}}{{path}}" target="_blank" rel="noopener">Open {{label}} ↗</a></p>'))'''),
    M("## A map is a set of choices\n\nInspect the shared values before discussing perspective. Extrusion is a visual encoding of `height_m`, not evidence that these are actual buildings."),
    C('''import json
from pathlib import Path
geo = json.loads(Path('data/demo_features.geojson').read_text())
rows = [(f['properties']['name'], f['geometry']['type'], f['properties']['height_m']) for f in geo['features']]
for row in rows: print(f'{row[0]:20} {row[1]:8} {row[2]:>3} m')'''),
    M("## Chart before map\n\nA bar chart makes relative heights easier to compare than a perspective scene. Compare the chart with the 3D map."),
    C('''from viz import bars, points
display(HTML(bars([r[0] for r in rows if r[1]=='Polygon'], [r[2] for r in rows if r[1]=='Polygon'], 'Compare mapped heights', ' m', '#e89a5b')))'''),
    M("## A simple coordinate view"),
    C("display(HTML(points(geo['features'], 'Plan view of the five features')))"),
    M("## Try RustGIS's own 2D and globe modes\n\nThe [RustGIS Web URL syntax](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app) supports `?data=` and `?projection=globe`. These open the actual RustGIS application, subject to browser CORS and WebGL support."),
    C(f'''from urllib.parse import quote
data_url = '{BASE}/data/demo_features.geojson'
for name, projection in [('RustGIS 2D', ''), ('RustGIS globe', '&projection=globe')]:
    url = 'https://web.rustgis.app/?blank&data=' + quote(data_url, safe='') + projection
    display(HTML(f'<p><a href="{{url}}" target="_blank" rel="noopener">{{name}} ↗</a></p>'))'''),
    M("## Reading exercise\n\n1. Which view best preserves footprint shape?\n2. Which view best communicates height?\n3. How does perspective change perceived distance?\n4. Which claim would require surveyed data instead of these fixtures?"),
    M(source_note()),
])

save("03_rustgis_bridge.ipynb", [
    M(f'''# 3 · Make a reproducible RustGIS handoff

**Question:** what should accompany a GeoJSON file when it leaves a notebook?

The handoff package will contain selected features, a source note, a bounding box, and a count. RustGIS can open the GeoJSON; the note helps a reader avoid treating invented heights as measured values.

![Handoff diagram]({BASE}/assets/stac-rustgis-flow.svg)'''),
    M("## Select a focused layer"),
    C('''import json
from pathlib import Path
source = json.loads(Path('data/demo_features.geojson').read_text())
polygons = [f for f in source['features'] if f['geometry']['type'] == 'Polygon']
print('Selected polygons:', len(polygons))'''),
    M("## Preserve the data structure\n\nA filtered GeoJSON remains a FeatureCollection. Keep the original properties, including `height_m`, so you can inspect them in RustGIS."),
    C('''selection = {'type':'FeatureCollection', 'name':'Illustrative study footprints', 'features':polygons}
Path('selected_footprints.geojson').write_text(json.dumps(selection, indent=2), encoding='utf-8')
print('Saved selected_footprints.geojson')'''),
    M("## Write a small manifest"),
    C('''manifest = {
    'source': 'JupyterLite-RustGIS/data/demo_features.geojson',
    'purpose': 'illustrative teaching fixture',
    'features': len(polygons),
    'fields': sorted({key for f in polygons for key in f['properties']}),
    'warning': 'invented heights; not surveyed data'
}
Path('selected_footprints_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))'''),
    M("## Check both files before download"),
    C('''assert json.loads(Path('selected_footprints.geojson').read_text())['features'] == polygons
assert json.loads(Path('selected_footprints_manifest.json').read_text())['features'] == len(polygons)
print('Export and manifest agree.')'''),
    M("## Open it in RustGIS\n\nDownload both files from the JupyterLite file browser. In [RustGIS Web](https://web.rustgis.app/), choose **Add Data** and select the GeoJSON. Inspect the attribute table and symbolize by `height_m`. The manifest is a human-readable provenance note, not a RustGIS project file."),
    M(f"You can also test the pre-hosted, complete [teaching layer in RustGIS](https://web.rustgis.app/?blank&data={BASE}/data/demo_features.geojson). A newly created browser file is **not automatically public at a URL**, so use the file picker for your own export."),
    M("## Native follow-through\n\nThe separate [native RustGIS notebook](https://github.com/jltobias/JupyterLite-RustGIS/blob/main/notebooks/04_native_rustgis.ipynb) uses `rustgis.Session(sample=True)`, map export, and a buffer command. It must run in local Jupyter because the native package is unavailable in Pyodide."),
    M("**Challenge:** filter the layer by a threshold such as `height_m >= 60`, update the manifest's feature count, and compare the selection with the 3D map."),
    M(source_note()),
])

save("04_stac_worldpop.ipynb", [
    M(f'''# 4 · WorldPop STAC: from discovery to RustGIS

**Question:** how can a search result become a map without confusing its footprint with raster values?

This lesson uses your [JupyterLite STAC Browser]({STAC}/explorer/) client and a frozen three-item WorldPop metadata snapshot retrieved 2026-10-14. These Items are **Degree of Urbanisation** products for Uganda, not population-count products. The snapshot is a reliability fallback; the optional live query may return different items later. No raster assets are bundled.

![STAC to RustGIS workflow]({BASE}/assets/stac-rustgis-flow.svg)'''),
    M(media()),
    M("## Inspect the query provenance\n\nThe snapshot preserves the source endpoint and exact bounded query. The Item geometries indicate coverage; asset links point to provider files and may have separate access terms."),
    C('''import json
from pathlib import Path
provenance = json.loads(Path('data/worldpop_provenance.json').read_text())
print(json.dumps(provenance, indent=2))'''),
    M("## Load the saved STAC Items"),
    C('''snapshot = json.loads(Path('data/worldpop_uga_items.geojson').read_text())
items = snapshot['features']
print('Items:', len(items))
for item in items:
    print(item['id'], 'reference year:', item['properties'].get('year'), 'assets:', len(item.get('assets', {})))'''),
    M("## Separate metadata time from reference year\n\nFor WorldPop, a STAC `datetime` may be the release time. Compare it to `properties.year`; do not present the former as the population reference year."),
    C('''for item in items:
    p=item['properties']
    print(item['id'], '| year:', p.get('year'), '| datetime:', p.get('datetime'), '| project:', p.get('project'))'''),
    M("## Compare the years visually\n\nThe chart shows metadata labels, not population estimates."),
    C('''from IPython.display import display, HTML
from viz import bars, points
display(HTML(bars([i['id'] for i in items], [i['properties'].get('year',0) for i in items], 'Reference-year metadata', '', '#e6a468')))'''),
    M("## Map a footprint schematic"),
    C("display(HTML(points(items, 'STAC Item coverage (schematic)')))"),
    M("## Inspect asset roles and links\n\nOnly print the first few names and media types. A STAC asset URL is not proof that an anonymous browser can download it."),
    C('''sample=items[0]
for key, asset in list(sample.get('assets', {}).items())[:8]:
    print(key, '|', asset.get('type'), '|', asset.get('roles'), '|', asset.get('href','')[:90])'''),
    M("## Optional live search through your STAC Browser client\n\nThe vendored client is copied from your STAC Browser repository under its MIT license. It uses browser fetch in Pyodide and a standard-library adapter locally. The query is bounded to a three-item page. Network/CORS errors leave the snapshot available."),
    C('''from stac_browser import STACBrowser, PRESETS
try:
    client = await STACBrowser(PRESETS['worldpop']).connect()
    live_items = await client.search(bbox=[29,-2,35,5], collection='UGA', limit=3)
    print('Live item IDs:', [item['id'] for item in live_items])
    print('Live provenance:', client.provenance().get('stac_root'))
except Exception as exc:
    live_items = []
    print('Live STAC search unavailable; continue with the saved snapshot:', type(exc).__name__, str(exc)[:180])'''),
    M("## Prepare a RustGIS-ready footprint export\n\nGeoJSON features retain STAC properties. Strip asset fields from the teaching export so the map layer is small; keep provenance separately."),
    C('''footprints={'type':'FeatureCollection','features':[{'type':'Feature','id':i['id'],'geometry':i['geometry'],'properties':{'id':i['id'],'year':i['properties'].get('year'),'project':i['properties'].get('project')}} for i in items]}
Path('worldpop_uga_footprints.geojson').write_text(json.dumps(footprints, indent=2))
Path('worldpop_uga_query.json').write_text(json.dumps(provenance, indent=2))
print('Saved footprints and query provenance. Download both from the file browser.')'''),
    M(f"## Open in RustGIS\n\n[Open the hosted STAC snapshot in RustGIS Web](https://web.rustgis.app/?blank&data={BASE}/data/worldpop_uga_items.geojson). For the smaller export made above, download it and use RustGIS **Add Data**. Try symbolizing by `year`, then read the Item's provider and collection license before opening any raster asset."),
    M("**Interpretation check:** the map is a coverage footprint map. It does not display Degree of Urbanisation cell values or uncertainty."),
    M(f"**Citations:** [WorldPop STAC API](https://api.stac.worldpop.org), [your STAC Browser source](https://github.com/jltobias/JupyterLite-STAC-Browser), [STAC specification](https://stacspec.org/), [RustGIS web URL guide](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app). See `data/worldpop_provenance.json` for the exact snapshot query."),
])

save("05_stac_catalogs.ipynb", [
    M(f'''# 5 · Compare STAC catalog choices

**Question:** why does a reproducible catalog search need a bounded query and a provider note?

Your [STAC Browser]({STAC}/explorer/) offers WorldPop, Copernicus, Digital Earth Africa, Earth Search, and Planetary Computer presets. Browser CORS and asset authorization vary by provider. The executable examples below keep requests optional and bounded.

![STAC workflow]({BASE}/assets/stac-rustgis-flow.svg)'''),
    M("## Inspect the exact presets from your client"),
    C('''from stac_browser import PRESETS, validate_bbox
for name, url in PRESETS.items(): print(f'{name:12} {url}')'''),
    M("## Validate a study area\n\nThe four numbers are west, south, east, north. Invalid order and values outside WGS84 are rejected before any network call."),
    C('''study_bbox = validate_bbox([-123.1, 37.2, -121.8, 38.1])
print('Study bbox:', study_bbox)
for wrong in ([35,5,29,-2], [-190,0,10,5]):
    try: validate_bbox(wrong)
    except ValueError as exc: print('Rejected',wrong,'→',str(exc)[:80])'''),
    M("## Why page limits matter\n\nSTAC searches can return many items and assets. Start with a small page, inspect metadata, then deliberately request more. No raster pixels are downloaded by the next cell."),
    C('''query = {'collection':'sentinel-2-l2a','bbox':study_bbox,'start':'2024-06-01','end':'2024-06-15','limit':3}
print(json.dumps(query, indent=2) if 'json' in globals() else query)'''),
    M("## Optional Earth Search query\n\nEarth Search is a public STAC API. An empty result or CORS/network error is a valid outcome to record, not a reason to silently expand the query."),
    C('''from stac_browser import STACBrowser
try:
    earth = await STACBrowser(PRESETS['earthsearch']).connect()
    earth_items = await earth.search(bbox=study_bbox, collection='sentinel-2-l2a', start='2024-06-01', end='2024-06-15', limit=3)
    print('Earth Search IDs:', [i['id'] for i in earth_items])
except Exception as exc:
    earth_items=[]
    print('Provider unavailable:', type(exc).__name__, str(exc)[:180])'''),
    M("## Inspect returned metadata without opening assets"),
    C('''for item in earth_items:
    print(item['id'], '| datetime', item['properties'].get('datetime'), '| cloud', item['properties'].get('eo:cloud_cover'), '| assets', len(item.get('assets',{})))
if not earth_items: print('Use the bundled WorldPop snapshot in notebook 04 for offline analysis.')'''),
    M("## Optional Copernicus connection\n\nThe same collection and bbox can be tried against the Copernicus STAC API. Its dataset files may require separate authentication; a public STAC response does not grant asset access."),
    C('''# Run only when you want another live provider request.
# cop = await STACBrowser(PRESETS['copernicus']).connect()
# cop_items = await cop.search(bbox=study_bbox, collection='sentinel-2-l2a', start='2024-06-01', end='2024-06-15', limit=3)
# print([item['id'] for item in cop_items])
print('Copernicus query is opt-in; see the commented code above.')'''),
    M(f"## Visual comparison\n\nUse the [STAC Browser Explorer]({STAC}/explorer/) to draw the same study area. Compare the browser's saved Search JSON with your Python `query` dictionary. The study rectangle is a query filter, not a measured data layer."),
    M("**Challenge:** change only the temporal window and predict how result count may change. Record provider, collection, bbox, dates, page limit, and retrieval time with any export."),
    M(f"**Citations:** [your STAC Browser](https://github.com/jltobias/JupyterLite-STAC-Browser), [Element 84 Earth Search](https://earth-search.aws.element84.com/v1), [Copernicus STAC documentation](https://documentation.dataspace.copernicus.eu/APIs/STAC.html), [STAC specification](https://stacspec.org/)."),
])

save("06_climate_scenarios.ipynb", [
    M(f'''# 6 · Climate scenario table from a sister repository

**Question:** how should a GIS analyst read a climate table before mapping it?

This CSV is copied from your [JupyterLite-zarr-sql-views](https://github.com/jltobias/JupyterLite-zarr-sql-views) repository. It originates in the [C3S Atlas user tools](https://github.com/ecmwf-projects/c3s-atlas) under Apache 2.0. It describes CMIP6 global warming level windows by model and scenario. It is **not** a geographic layer, so no map is drawn until a geographic key and spatial data are supplied.

![Runtime boundaries]({BASE}/assets/runtime-boundaries.svg)'''),
    M("## Parse the unusual two-row header\n\nThe first header row holds warming levels; the second holds scenarios. `9999` and `NA` are missing or unavailable markers, not years."),
    C('''import csv
from pathlib import Path
with Path('data/CMIP6_WarmingLevels.csv').open(newline='', encoding='utf-8') as handle:
    rows=list(csv.reader(handle))
levels, scenarios = rows[:2]
print('Models:', len(rows)-2, '| pairs:', len(levels)-1)
print([(scenarios[i], levels[i]) for i in range(1,6)])'''),
    M("## Make tidy records"),
    C('''records=[]
for row in rows[2:]:
    for i in range(1,min(len(row),len(levels))):
        if row[i] not in ('9999','NA',''):
            records.append({'model':row[0],'scenario':scenarios[i],'level':levels[i],'window':row[i]})
print('Usable model–scenario–level windows:',len(records))
print(records[:3])'''),
    M("## Count availability, not climate impact\n\nThis chart counts table entries with a reported time window. It does not show probability, temperature magnitude, or regional exposure."),
    C('''from collections import Counter
from IPython.display import display, HTML
from viz import bars
counts=Counter(r['scenario'] for r in records)
display(HTML(bars(sorted(counts),[counts[k] for k in sorted(counts)],'Available model windows by scenario',' records')))'''),
    M("## Inspect one warming level"),
    C('''level='2'
subset=[r for r in records if r['level']==level]
print(f'{len(subset)} records for {level}°C')
for r in subset[:8]: print(r['scenario'],r['model'][:26],r['window'])'''),
    M("## A timeline view\n\nUse the start of each reported window as a small comparative graphic. It is not a forecast interval plot."),
    C('''starts=[int(r['window'][:4]) for r in subset if r['window'][:4].isdigit()]
decades=Counter((year//10)*10 for year in starts)
display(HTML(bars([str(d) for d in sorted(decades)],[decades[d] for d in sorted(decades)],'Start decade of reported 2°C windows',' models','#e79c61')))'''),
    M("## GIS decision: can this be mapped?\n\nNo. A table of global model windows lacks coordinates, polygons, or a geographic join key. A responsible RustGIS workflow would obtain a regional raster/vector product with its own provenance, then join or compare using a defensible spatial and temporal method."),
    C('''has_geometry = any(key in records[0] for key in ('geometry','lon','lat','region_id'))
print('Has geographic key?', has_geometry)
assert not has_geometry'''),
    M("**Challenge:** compare counts for 1.5°C and 3°C, then explain why missingness can bias a visual summary. Do not substitute this count for a climate risk estimate."),
    M("**Citations:** [source repository and notices](https://github.com/jltobias/JupyterLite-zarr-sql-views/blob/main/THIRD_PARTY_NOTICES.md), [C3S Atlas user tools](https://github.com/ecmwf-projects/c3s-atlas), [Apache 2.0 license in this repo](https://github.com/jltobias/JupyterLite-RustGIS/blob/main/licenses/c3s-atlas-Apache-2.0.txt)."),
])

save("07_ollama_assistance.ipynb", [
    M(f'''# 7 · AI assistance with Ollama and RustGIS

**Question:** how can an assistant propose map operations while the analyst keeps control of the data and commands?

RustGIS has its **own AI Assistant**. Its [assistant guide](https://github.com/opengeos/RustGIS/blob/main/docs/user-guide/assistant.md) documents Ollama as a local provider, usually at `http://localhost:11434`. This notebook teaches an inspectable plan; it does not pretend to invoke RustGIS from Pyodide or send data to a model.

![Where RustGIS and Ollama run]({BASE}/assets/runtime-boundaries.svg)'''),
    M("## Local setup, outside JupyterLite\n\n1. Install and start [Ollama](https://ollama.com/). Pull a tool-capable model, such as the RustGIS guide's `qwen3` example.\n2. In **native RustGIS**, open **Analyze → AI Assistant**, choose **Ollama**, and select the model.\n3. In RustGIS Web, browser access to your local server needs an allowed origin. The RustGIS guide gives `OLLAMA_ORIGINS=https://web.rustgis.app ollama serve`. Browser/network policies may still block it.\n4. Inspect every command and its result in the RustGIS conversation. Commands with file, network, plugin, script, or project replacement effects require explicit RustGIS approval."),
    M("## Other assistant providers\n\nThe [RustGIS guide](https://github.com/opengeos/RustGIS/blob/main/docs/user-guide/assistant.md) also documents Anthropic, OpenAI, Gemini, OpenRouter, and OpenAI-compatible local servers such as LM Studio. Provider choice changes where prompts and any read map data are sent. For this lesson, Ollama is the local example; no provider is contacted by the notebook."),
    M("## Author a bounded question\n\nThe prompt names the dataset and asks for a plan first. It avoids passing fabricated heights as real evidence."),
    C('''question = (
    'Using the illustrative study footprints layer, propose a way to symbolize height_m. '
    'State that heights are invented teaching values. List the fields you would inspect '
    'and the RustGIS commands you would use, but do not run anything yet.'
)
print(question)'''),
    M("## A typed, authored example response\n\nThis fixture is **not** model output. It lets us practice validation even when Ollama is absent."),
    C('''proposal = {
    'layer':'Illustrative study footprints',
    'field':'height_m',
    'symbol':'graduated',
    'classes':3,
    'minimum':0,
    'maximum':100,
    'note':'Illustrative heights only; do not infer real building height.'
}
print(proposal)'''),
    M("## Validate before acting\n\nThe notebook accepts only a small set of values. It does not execute generated Python, SQL, shell, URLs, or RustGIS commands."),
    C('''def validate_plan(plan, fields):
    if plan.get('field') not in fields: raise ValueError('Unknown field')
    if plan.get('symbol') not in {'graduated','single'}: raise ValueError('Unsupported symbol')
    if type(plan.get('classes')) is not int or not 2 <= plan['classes'] <= 7: raise ValueError('Invalid class count')
    if not 0 <= plan.get('minimum',-1) < plan.get('maximum',-1) <= 500: raise ValueError('Invalid range')
    return True
assert validate_plan(proposal, {'name','kind','height_m'})
print('Plan passes the teaching checks; a person still reviews it.')'''),
    M("## Visualize the proposal without changing a GIS project"),
    C('''from IPython.display import display, HTML
from viz import bars
display(HTML(bars(['Low','Medium','High'], [33,67,100], 'Illustrative graduated class ceilings', ' m', '#e9a461')))'''),
    M("## Reject an unsafe or unsupported proposal"),
    C('''bad = dict(proposal, field='download_and_run', classes=100)
try: validate_plan(bad, {'name','kind','height_m'})
except ValueError as exc: print('Rejected:',exc)'''),
    M("## Try the actual RustGIS assistant\n\nOpen [RustGIS Web with this layer](https://web.rustgis.app/?blank&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fdemo_features.geojson) or use desktop RustGIS. Open the AI Assistant pane. Ask the question above. Review its proposed command parameters and output, and use undo if a map change is wrong. The upstream guide says provider requests can include layer names, fields, extent, and rows the assistant reads, so choose an appropriate model/provider for your data."),
    M('''## Optional native CLI

`rustgis-cli ask --sample "Which 5 countries have the largest GDP?"` is the upstream quick-start example. Run it in a local terminal with a configured assistant provider; it is not a JupyterLite command.'''),
    M("**Reflection:** Which parts of the assistant response are observations about the data, which are proposed operations, and which require your approval or independent verification?"),
    M("**Citations:** [RustGIS AI Assistant guide](https://github.com/opengeos/RustGIS/blob/main/docs/user-guide/assistant.md), [RustGIS CLI guide](https://github.com/opengeos/RustGIS/blob/main/docs/cli.md), [Ollama](https://ollama.com/), [your GeoLibre–Ollama teaching notebooks](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/tree/main/book/notebooks)."),
])

save("08_globe_and_scene.ipynb", [
    M(f'''# 8 · Globe, 3D map, and 3D scene

**Question:** what changes when we move from plan view to a globe or an oblique scene?

RustGIS supports a globe projection and 3D views. The companion map pages render our invented footprints with MapLibre and the orbitable scene with Three.js; RustGIS links open the real application. Do not read the invented extrusion heights as observed terrain or building data.

![Stylized globe]({BASE}/assets/rustgis-splash.png)'''),
    M("## Open four views\n\n- [Companion 2D map](https://jltobias.github.io/JupyterLite-RustGIS/maps/2d.html)\n- [Companion 3D extrusions](https://jltobias.github.io/JupyterLite-RustGIS/maps/3d.html)\n- [Companion pitched scene](https://jltobias.github.io/JupyterLite-RustGIS/maps/scene.html)\n- [RustGIS globe with the teaching layer](https://web.rustgis.app/?blank&projection=globe&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fdemo_features.geojson)"),
    M("## Inspect values before perspective"),
    C('''import json
from pathlib import Path
data=json.loads(Path('data/demo_features.geojson').read_text())
heights={f['properties']['name']:f['properties']['height_m'] for f in data['features'] if f['geometry']['type']=='Polygon'}
heights'''),
    M("## A small multiple chart\n\nThe chart provides a precise height comparison that perspective can obscure."),
    C('''from IPython.display import display, HTML
from viz import bars
display(HTML(bars(list(heights),list(heights.values()),'Same values in every view',' m')))'''),
    M("## Compare direct RustGIS URLs\n\nRustGIS's documented web URL parameters let you request a blank project, a projection, and public data. The file still has to be fetchable by the browser."),
    C(f'''from urllib.parse import urlencode
data_url='{BASE}/data/demo_features.geojson'
for title, opts in [('Flat map',{{'blank':'','data':data_url}}),('Globe',{{'blank':'','projection':'globe','data':data_url}})]:
    url='https://web.rustgis.app/?'+urlencode(opts)
    display(HTML(f'<p><a href="{{url}}" target="_blank" rel="noopener">RustGIS {{title}} ↗</a></p>'))'''),
    M("## Scene reasoning\n\nThe standalone 3D scene lets you orbit the same invented extrusions in Three.js. It is not a surveyed 3D Tiles model. An oblique view can reveal overlap but distort apparent distance and area."),
    C('''view_notes = {
  '2D':'best for footprint shape and planimetric position',
  '3D':'helps compare relative extrusion heights',
  'scene':'adds context and depth but increases occlusion',
  'globe':'global orientation and projection context'
}
for view, note in view_notes.items(): print(f'{view:7} {note}')'''),
    M("## Investigate in RustGIS\n\nIn RustGIS, compare map projection and globe mode, then inspect the layer attributes. The source fields remain the same even when the visual perspective changes."),
    M("**Challenge:** create a two-column evidence table: what each view makes easier to see, and what it hides. Include a warning about the invented heights."),
    M("**Citations:** [RustGIS web app and projection URL guide](https://github.com/opengeos/RustGIS/blob/main/docs/installation.md#web-app), [RustGIS project](https://github.com/opengeos/RustGIS), [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js), [Three.js](https://github.com/mrdoob/three.js), [OpenStreetMap attribution](https://www.openstreetmap.org/copyright)."),
])

save("09_capstone.ipynb", [
    M(f'''# 9 · Capstone: a defensible STAC-to-RustGIS brief

**Question:** can you pass catalog results to a GIS and explain exactly what the map shows?

You will combine the WorldPop Degree of Urbanisation snapshot, a small chart, a provenance note, a RustGIS Web link, and a proposed Ollama question. The result is a metadata coverage brief—not a raster analysis.

![STAC to RustGIS flow]({BASE}/assets/stac-rustgis-flow.svg)'''),
    M("## Load the evidence package"),
    C('''import json
from pathlib import Path
items=json.loads(Path('data/worldpop_uga_items.geojson').read_text())['features']
prov=json.loads(Path('data/worldpop_provenance.json').read_text())
assert len(items)==len(prov['item_ids'])
print('Provider:',prov['provider'],'| items:',len(items),'| retrieved:',prov['retrieved_on'])'''),
    M("## Extract only claims supported by metadata"),
    C('''summary=[{'id':i['id'],'year':i['properties'].get('year'),'bbox':i.get('bbox'),'assets':len(i.get('assets',{}))} for i in items]
for row in summary: print(row)'''),
    M("## Visualize a cautious comparison"),
    C('''from IPython.display import display, HTML
from viz import bars
display(HTML(bars([r['id'] for r in summary],[r['assets'] for r in summary],'Advertised asset counts',' assets')))'''),
    M("## Export a compact GIS layer"),
    C('''layer={'type':'FeatureCollection','features':[{'type':'Feature','id':i['id'],'geometry':i['geometry'],'properties':{'id':i['id'],'year':i['properties'].get('year'),'asset_count':len(i.get('assets',{}))}} for i in items]}
Path('capstone_stac_footprints.geojson').write_text(json.dumps(layer,indent=2))
print('Saved',len(layer['features']),'footprints')'''),
    M("## Build the brief and provenance"),
    C('''brief={
 'title':'WorldPop UGA STAC metadata coverage',
 'claim':'Three catalog Item footprints are available in the saved query snapshot.',
 'not_claimed':'No raster cell values, exposure estimates, or uncertainty estimates were analyzed.',
 'source_query':prov['query_url'],
 'retrieved_on':prov['retrieved_on'],
 'item_ids':[i['id'] for i in items],
 'next_step':'Inspect collection license/provider, then open GeoJSON in RustGIS.'
}
Path('capstone_brief.json').write_text(json.dumps(brief,indent=2))
print(json.dumps(brief,indent=2))'''),
    M("## Open the real application\n\nDownload `capstone_stac_footprints.geojson` and use the file picker in [RustGIS Web](https://web.rustgis.app/). Alternatively, [open the hosted snapshot directly](https://web.rustgis.app/?blank&data=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-RustGIS%2Fdata%2Fworldpop_uga_items.geojson). Inspect the attributes and symbolize `year`. The direct URL opens the hosted snapshot, not your newly generated local export."),
    M("## Ask the assistant carefully\n\nIn native RustGIS with Ollama configured, try: *“Summarize the three STAC footprint features and propose a style by year. State explicitly that the polygons show catalog coverage rather than Degree of Urbanisation raster cell values. Show the commands before any file or network action.”* Review every action and result."),
    M("## Self-check\n\n- Can someone reproduce the query from your brief?\n- Is the provider and retrieval date present?\n- Are metadata and raster values kept separate?\n- Did you inspect license and asset access before downloading?\n- Would another reader know which steps happened in JupyterLite and which happened in RustGIS?"),
    M(f"Continue with the [STAC Browser Explorer]({STAC}/explorer/) for another bounded search, or use the [native RustGIS notebook](https://github.com/jltobias/JupyterLite-RustGIS/blob/main/notebooks/04_native_rustgis.ipynb) for Python `Session` analysis. [Read the book]({BASE}/book/index.html) for the complete route."),
    M(source_note()),
])

save("04_native_rustgis.ipynb", [
    M("# Native RustGIS: render, buffer, inspect\n\n**Run in local Jupyter, not JupyterLite.** Install `rustgis` in a compatible local Python environment. These calls follow the [upstream Python guide](https://github.com/opengeos/RustGIS/blob/main/docs/python.md). The sample data belongs to RustGIS; the teaching GeoJSON in this repository is separate."),
    M("## Runtime check\n\nThe native binding cannot be loaded by the Pyodide browser kernel. Keep native work on your computer and export files deliberately."),
    C("import platform\nprint(platform.python_version(), platform.platform())"),
    M("## Open the RustGIS sample project"),
    C("import rustgis\nsession = rustgis.Session(sample=True)\nsession"),
    M("## Render and inspect"),
    C("session.to_png('rustgis_sample.png')\nfrom IPython.display import Image, display\ndisplay(Image(filename='rustgis_sample.png'))"),
    M("## Run a documented geoprocessing command\n\nThe sample project has a `Cities` layer. The buffer distance follows the current RustGIS tool/project settings; check units before using it on another dataset."),
    C("session.run('gp.run', tool='buffer', params={'input':'Cities','distance':100})\nsession.to_png('rustgis_city_buffers.png')\ndisplay(Image(filename='rustgis_city_buffers.png'))"),
    M("## Inspect the result layer\n\nThe upstream quick start names the output `Cities_Buffer`. GeoPandas is an optional native dependency for tabular inspection."),
    C("gdf = session.layer('Cities_Buffer').to_geopandas()\nprint(gdf.shape)\ngdf.head()"),
    M("## Reproducibility note\n\nRecord the RustGIS version, tool parameters, project units, and source data before using this in a report. For AI-assisted analysis, see the [official assistant guide](https://github.com/opengeos/RustGIS/blob/main/docs/user-guide/assistant.md)."),
], browser=False)
