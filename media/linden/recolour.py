import subprocess, json, sys, urllib.request, colorsys, os
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) home-stage-assets/1.0"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
A = os.path.dirname(os.path.abspath(__file__))
FABRICS = [
  ("01", "cobalt-wool", "Cobalt wool", "caban", "#2F4B8A"),
  ("02", "moss-boucle", "Moss houndstooth", "wool_boucle", "#6A7149"),
  ("03", "ochre-velvet", "Ochre velvet", "velour_velvet", "#B8862B"),
  ("04", "oatmeal-linen", "Oatmeal linen", "rough_linen", "#CFC4AE"),
  ("05", "charcoal-herringbone", "Charcoal herringbone", "poly_wool_herringbone", "#3B3B3D"),
  ("06", "plum-corduroy", "Plum corduroy", "ribbed_corduroy", "#6E3A4A"),
]
def shade(hexc, f):
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l * f))
    return "#%02x%02x%02x" % tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))
def run(*a): subprocess.run(["magick", *a], check=True)
def out(*a): return subprocess.run(["magick", *a], check=True, capture_output=True, text=True).stdout.strip()
def mean_gray(img, mask=None):
    # Mean lightness, weighted by the mask when given (fabric pixels only).
    if mask:
        return float(out(img, "-colorspace", "gray", mask, "-alpha", "off", "-compose", "CopyOpacity", "-composite", "-scale", "1x1!", "-alpha", "off", "-format", "%[fx:p.r]", "info:"))
    return float(out(img, "-colorspace", "gray", "-format", "%[fx:mean]", "info:"))
CROP = {"charcoal-herringbone": "26%x26%", "plum-corduroy": "10%x10%"}
CONTRAST = {"charcoal-herringbone": (0.25, 1.75), "plum-corduroy": (0.4, 1.6)}


def tint(img, col, mask=None, extra=(), lo=0.62, hi=1.38):
    # Centre the texture's lightness on 0.5, then map 0..1 to a dark..light shade of the target,
    # so the average of the result lands on the target colour and the weave/shading survives.
    m = mean_gray(img, mask)
    return [img, "-colorspace", "gray", "-evaluate", "multiply", str(0.5 / m), "-sigmoidal-contrast", "1,50%",
            "+level-colors", f"{shade(col,lo)},{shade(col,hi)}", *extra]
src = f"{A}/Sofa_01/textures/Sofa_01_diff_2k.jpg"
# Upholstery is the light part of the atlas, wood the dark part: soft mask by lightness.
mask = f"{A}/build/fabric_mask.png"
run(src, "-colorspace", "gray", "-level", "30%,42%", "-blur", "0x2", mask)
manifest = []
for no, slug, name, tex, col in FABRICS:
    # Sofa texture: fabric shading kept, colour mapped between a dark and light shade of the target.
    tinted = f"{A}/build/tint_{slug}.png"
    run(*tint(src, col, mask), tinted)
    run(src, tinted, mask, "-composite", "-quality", "92", f"{A}/build/Sofa_01_diff_{slug}.jpg")
    # Swatch tile from the CC0 fabric texture, recoloured the same way.
    info = json.loads(get(f"https://api.polyhaven.com/files/{tex}"))
    url = info["Diffuse"]["1k"]["jpg"]["url"]
    raw = f"{A}/fabrics/{tex}_diff_1k.jpg"
    if not os.path.exists(raw):
        open(raw, "wb").write(get(url))
    lo, hi = CONTRAST.get(slug, (0.62, 1.38))
    run(*tint(raw, col, lo=lo, hi=hi, extra=("-gravity", "center", "-crop", CROP.get(slug, "34%x34%") + "+0+0", "+repage",
        "-resize", "800x800^", "-extent", "800x800", "-quality", "88")), f"{A}/build/swatch_{no}_{slug}.jpg")
    manifest.append(dict(no=no, slug=slug, name=name, colour=col, texture=tex, texture_url=url))
json.dump(manifest, open(f"{A}/build/fabrics.json", "w"), indent=1, ensure_ascii=False)
print("ok", len(manifest))
