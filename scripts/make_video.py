"""Render a short silent, captioned workflow explainer (requires Pillow/imageio-ffmpeg)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT = Path(__file__).resolve().parents[1] / "assets" / "stac-rustgis-tour.mp4"
W, H, FPS = 960, 540, 12
STEPS = [
    ("DISCOVER", "Choose a public STAC collection", "WorldPop / Earth Search / Copernicus"),
    ("FILTER", "Bound the search in space and time", "bbox + collection + dates + page limit"),
    ("INSPECT", "Read license, assets, and provenance", "Footprints describe coverage, not pixels"),
    ("EXPORT", "Save GeoJSON and the exact query", "Keep the source URL with your result"),
    ("EXPLORE", "Open GeoJSON in RustGIS Web", "Then style, analyze, or move to native RustGIS"),
]

def font(size, bold=False):
    name = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()

def frame(index):
    image = Image.new("RGB", (W, H), "#0e2136")
    draw = ImageDraw.Draw(image)
    draw.text((54, 44), "STAC  →  RustGIS", font=font(43, True), fill="#f7fbfb")
    draw.text((56, 105), "A five-step metadata-to-map workflow", font=font(24), fill="#b5d9e4")
    active = min(len(STEPS)-1, index // (FPS*2))
    for i, (label, _, _) in enumerate(STEPS):
        x = 55+i*181
        color = "#e6a96f" if i == active else "#2c6075" if i < active else "#1b3b50"
        draw.rounded_rectangle((x, 175, x+160, 263), radius=15, fill=color)
        draw.text((x+15, 202), f"{i+1}. {label}", font=font(21, True), fill="#ffffff")
        if i < 4:
            draw.text((x+166, 204), "›", font=font(34, True), fill="#88dedb")
    _, headline, detail = STEPS[active]
    draw.text((56, 321), headline, font=font(32, True), fill="#ffffff")
    draw.text((57, 380), detail, font=font(24), fill="#aee5e1")
    draw.text((56, 482), "Illustrative workflow • metadata is not raster data", font=font(19), fill="#a9c1ca")
    return image.tobytes()

def main():
    writer = imageio_ffmpeg.write_frames(str(OUT), (W,H), fps=FPS, codec="libx264", quality=7, pix_fmt_in="rgb24", output_params=["-movflags", "+faststart", "-an"])
    writer.send(None)
    for i in range(FPS*10):
        writer.send(frame(i))
    writer.close()
    print(OUT)

if __name__ == "__main__":
    main()
