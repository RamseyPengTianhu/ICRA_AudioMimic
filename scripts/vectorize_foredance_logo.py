"""Trace the author's transparent ForeDance wordmark as editable color paths.

Requires vtracer 0.6.15, OpenCV, Pillow, NumPy and CairoSVG. The source PNG
remains byte-for-byte unchanged. Paths retain the ten original components;
nearly transparent edge noise is excluded by the alpha threshold.
"""
from pathlib import Path
import copy
import hashlib
import json
import xml.etree.ElementTree as ET

import cairosvg
import cv2
import numpy as np
from PIL import Image
import vtracer

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures/foredance'
OUT = ROOT / 'output/overview-refined-20260911'
TMP = ROOT / 'tmp/foredance-logo-vector'
TMP.mkdir(parents=True, exist_ok=True)
source = FIG / 'foredance-logo-source.png'
rgba = np.array(Image.open(source))
alpha = rgba[:, :, 3]
foreground = alpha >= 128
blue = rgba[:, :, 2] > 100
ns = {'s': 'http://www.w3.org/2000/svg'}
ET.register_namespace('', ns['s'])
tag = lambda name: '{' + ns['s'] + '}' + name
full = ET.Element(tag('svg'), width='2170', height='725', viewBox='0 0 2170 725')
ET.SubElement(full, tag('title')).text = 'ForeDance'
ET.SubElement(full, tag('desc')).text = 'Editable outlines traced from the author-provided logo; black Fore, blue divider and Dance.'
colors = {}
for name, mask in [('fore', foreground & ~blue), ('dance', foreground & blue)]:
    pixels = rgba[:, :, :3][mask]
    rgb = np.median(pixels, axis=0).astype(int)
    fill = '#' + ''.join(f'{v:02X}' for v in rgb)
    colors[name] = fill
    mask_path, trace_path = TMP / f'{name}-mask.png', TMP / f'{name}-trace.svg'
    Image.fromarray(np.where(mask, 0, 255).astype('uint8')).save(mask_path)
    vtracer.convert_image_to_svg_py(
        str(mask_path), str(trace_path), colormode='binary', mode='spline',
        filter_speckle=8, corner_threshold=60, length_threshold=3.5,
        max_iterations=10, splice_threshold=45, path_precision=3,
    )
    group = ET.SubElement(full, tag('g'), id=name, fill=fill)
    for path in ET.parse(trace_path).getroot().findall('.//s:path', ns):
        node = copy.deepcopy(path)
        node.set('fill', fill)
        group.append(node)

full_svg = ET.tostring(full, encoding='unicode')
cairosvg.svg2png(bytestring=full_svg.encode(), write_to=str(TMP/'logo-full-canvas.png'))
render = np.array(Image.open(TMP/'logo-full-canvas.png'))
render_mask = render[:, :, 3] >= 128
iou = np.sum(foreground & render_mask) / np.sum(foreground | render_mask)
source_parts = cv2.connectedComponentsWithStats(foreground.astype('uint8'), 8)[2][1:]
vector_parts = cv2.connectedComponentsWithStats(render_mask.astype('uint8'), 8)[2][1:]
assert len(source_parts) == len(vector_parts) == 10
assert iou > 0.985, iou

# Trim unused margins in the SVG viewport; the shape coordinates are unchanged.
ys, xs = np.where(foreground)
bounds = [int(xs.min())-8, int(ys.min())-8, int(xs.max())+9, int(ys.max())+9]
x0, y0, x1, y1 = bounds
full.set('viewBox', f'{x0} {y0} {x1-x0} {y1-y0}')
full.set('width', str(x1-x0)); full.set('height', str(y1-y0))
output = FIG / 'foredance-logo.svg'
output.write_text(ET.tostring(full, encoding='unicode')+'\n')
assert not full.findall('.//s:image', ns)
assert not full.findall('.//s:text', ns)
cairosvg.svg2png(url=str(output), write_to=str(OUT/'foredance-logo-vector.png'))

preview = ET.Element(tag('svg'), width='1050', height='285', viewBox='0 0 1050 285')
ET.SubElement(preview, tag('rect'), width='1050', height='285', fill='white')
logo = copy.deepcopy(full)
logo.set('x', '25'); logo.set('y', '25'); logo.set('width', '1000'); logo.set('height', '235')
preview.append(logo)
cairosvg.svg2png(bytestring=ET.tostring(preview), write_to=str(OUT/'foredance-logo-preview.png'))
report = dict(
    source=str(source.relative_to(ROOT)), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    svg=str(output.relative_to(ROOT)), svg_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
    palette=colors, source_size=[2170,725], viewbox=[x0,y0,x1-x0,y1-y0],
    alpha_threshold=128, tracing='vtracer 0.6.15, binary spline contours for two sampled colors',
    paths=len(full.findall('.//s:path',ns)), embedded_images=0, transparent_background=True,
    original_and_vector_components=10, silhouette_iou=float(iou),
    source_unchanged=True, output_bytes=output.stat().st_size,
)
(OUT/'foredance-logo-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
