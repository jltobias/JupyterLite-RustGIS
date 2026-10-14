"""See lite/viz.py; copied for local notebook use."""
from html import escape

def bars(labels, values, title, unit="", color="#31b7c5"):
    pairs = [(str(a), float(b)) for a, b in zip(labels, values)]
    width, height = 760, max(260, 85 + 48 * len(pairs))
    max_value = max([v for _, v in pairs] + [1])
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}" viewBox="0 0 {width} {height}" style="max-width:100%;font-family:system-ui;background:#102439;border-radius:12px">',f'<text x="25" y="38" fill="white" font-size="23" font-weight="700">{escape(title)}</text>']
    for i, (label, value) in enumerate(pairs):
        y = 70 + i * 48
        bar = max(1, 440 * value / max_value)
        chunks += [f'<text x="25" y="{y+23}" fill="#d8eff0" font-size="16">{escape(label[:24])}</text>',f'<rect x="250" y="{y}" width="{bar:.1f}" height="29" rx="5" fill="{color}"/>',f'<text x="{min(710,265+bar):.1f}" y="{y+22}" fill="white" font-size="16">{value:g}{escape(unit)}</text>']
    return ''.join(chunks) + '</svg>'

def points(features, title="Feature locations"):
    pts=[]
    for feature in features:
        g=feature['geometry']; p=feature.get('properties',{})
        coords=g['coordinates'] if g['type']=='Point' else g['coordinates'][0][0]
        pts.append((float(coords[0]),float(coords[1]),g['type'],str(p.get('name',p.get('id','feature')))))
    if not pts: return '<p>No features</p>'
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    dx=max(max(xs)-min(xs),.001); dy=max(max(ys)-min(ys),.001)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}" viewBox="0 0 760 460" style="max-width:100%;font-family:system-ui;background:#102439;border-radius:12px"><text x="24" y="38" fill="white" font-size="23">{escape(title)}</text><rect x="60" y="65" width="640" height="335" fill="#1b3b51" stroke="#77b5c6"/>']
    for lon,lat,kind,name in pts:
        x=80+600*(lon-min(xs))/dx; y=380-295*(lat-min(ys))/dy
        color='#ffc46e' if kind=='Point' else '#52c9cb'
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" stroke="white" stroke-width="2"><title>{escape(name)}</title></circle>')
    out.append('<text x="60" y="430" fill="#b5d7df" font-size="15">Longitude →  •  Latitude ↑  •  Schematic coordinates; use a GIS for projected distance.</text></svg>')
    return ''.join(out)
