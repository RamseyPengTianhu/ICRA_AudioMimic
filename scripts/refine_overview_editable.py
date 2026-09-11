"""Reconstruct the user-selected four-panel master as native SVG objects.

Refine the exact overview-editable.png selected by the user on 2026-09-11.
Retain its palette, panel bounds and module locations, with author-requested
canvas trimming. Fix connector endpoints and crossings; robot variants come
from one common neutral master.
The official MRT-2 icon is the existing transparent project asset.
"""
from pathlib import Path
import base64
import hashlib
import html
import io
import json
import math
import shutil
import sys
import xml.etree.ElementTree as ET

import cairocffi as cairo
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures/foredance'
ASSETS = FIG / 'transparent-assets'
OUT = ROOT / 'output/overview-refined-20260911'
OUT.mkdir(parents=True, exist_ok=True)
MASTER = FIG / 'overview-imagegen-master.png'
source = Image.open(MASTER).convert('RGB')
W, H = source.size
assert (W, H) == (1536, 1024)
H = 956  # The author moved the footer legend into the header.
C = dict(blue='#0769F9', orange='#FF8A17', teal='#009EAC',
         purple='#8534DB', ink='#080F2D', gray='#717C90')
M = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
         f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         '<title>ForeDance — four-panel editable overview</title>',
         '<desc>Native editable text, shapes, arrows and symbols; transparent '
         'robot illustrations derived from one master and one human illustration. '
         'The existing transparent official Magenta application icon is embedded. '
         'Robot drawings are schematic and are not hardware evidence.</desc>', '<defs>']
for name, color in C.items():
    parts.append(f'<marker id="arrow-{name}" viewBox="0 0 10 10" '
                 f'refX="9" refY="5" markerWidth="6" markerHeight="6" '
                 f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>')
    pale = '#' + ''.join(f'{round(255*.94+int(color[i:i+2],16)*.06):02x}' for i in (1, 3, 5))
    parts.append(f'<linearGradient id="wash-{name}" x1="0" y1="0" x2="1" y2="1">'
                 f'<stop stop-color="white"/><stop offset="1" stop-color="{pale}"/></linearGradient>')
    parts.append(f'<linearGradient id="tile-{name}" x1="0" y1="0" x2="1" y2=".3">'
                 f'<stop stop-color="{color}" stop-opacity=".60"/>'
                 f'<stop offset=".38" stop-color="{color}" stop-opacity=".94"/>'
                 f'<stop offset="1" stop-color="{color}" stop-opacity=".70"/></linearGradient>')
parts += ['<linearGradient id="decoder" x1="0" y1="0" x2="1" y2="0">'
          '<stop stop-color="#F4F5F9"/><stop offset="1" stop-color="#DBDFE9"/>'
          '</linearGradient>',
          '<symbol id="boundary-state-icon" viewBox="0 0 36 28">'
          '<title>Boundary pose</title>'
          '<g fill="none" stroke="#8534DB" stroke-width="2.1" '
          'stroke-linecap="round" stroke-linejoin="round">'
          '<circle cx="10.5" cy="3.9" r="2.8" fill="#8534DB" stroke="none"/>'
          '<path d="M10.5 8 L9 17 M10 10 L5.5 13 L3.2 17 '
          'M10 10 L14.4 13 L17.2 10 M9 17 L5 22 L4 26 '
          'M9 17 L13 21 L16 25.8"/>'
          '</g>'
          '</symbol>',
          '<symbol id="trainable-flame" viewBox="0 0 24 32">'
          '<title>Trainable</title>'
          '<path d="M12.3 1 C14.2 8.2 20.8 10.5 21.1 17.4 '
          'C21.4 24.8 17.4 30.4 11.6 30.4 C5.8 30.4 2.2 26.1 2.6 20.3 '
          'C2.8 16.8 4.6 14.5 7.1 11.7 C6.7 16.1 8.3 18.1 10.1 18.5 '
          'C8.7 11.6 14 8.1 12.3 1 Z" fill="#F27822"/>'
          '<path d="M12 17 C13 21.1 17.4 22.7 15.6 26.3 '
          'C14.1 29.4 9.2 29 8.2 26.1 C7.1 23 10.5 20.6 12 17 Z" fill="#FFD17D"/>'
          '</symbol>', '</defs>']
labels, images, arrows, groups, state_icons, logos = [], [], [], [], [], []
embedded_assets = {}


def color(c):
    return C.get(c, c)


def group(name):
    parts.append(f'<g id="{name}">')
    groups.append(name)


def end():
    parts.append('</g>')


def rect(x, y, w, h, fill='white', stroke='none', r=5, sw=1, dash=None):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
                 f'fill="{color(fill)}" stroke="{color(stroke)}" stroke-width="{sw}"'
                 + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')


def line(d, c='ink', sw=2, arrow=False, dash=None, id=None):
    parts.append('<path ' + (f'id="{id}" ' if id else '') +
                 f'd="{d}" fill="none" stroke="{color(c)}" stroke-width="{sw}" '
                 'stroke-linecap="round" stroke-linejoin="round"' +
                 (f' marker-end="url(#arrow-{c})"' if arrow else '') +
                 (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    if id:
        arrows.append(dict(id=id, path=d, color=c, arrowhead=arrow))


def shape(d, fill, stroke='ink', sw=1):
    parts.append(f'<path d="{d}" fill="{color(fill)}" stroke="{color(stroke)}" '
                 f'stroke-width="{sw}" stroke-linejoin="round"/>')


def circle(x, y, r, fill='white', stroke='none', sw=1):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color(fill)}" '
                 f'stroke="{color(stroke)}" stroke-width="{sw}"/>')


def text(x, y, value, size=18, c='ink', bold=False, anchor='start', maxw=None, mathfont=False):
    family = 'Times New Roman' if mathfont else 'Helvetica'
    M.select_font_face(family, cairo.FONT_SLANT_ITALIC if mathfont else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    requested_size = size
    M.set_font_size(size)
    advance = M.text_extents(value)[4]
    if maxw and advance > maxw:
        size = round(size * maxw / advance, 2)
        M.set_font_size(size)
        advance = M.text_extents(value)[4]
    # Preserve the actual letter proportions; fit using font size, never scale-x.
    attrs = f'font-family="{family}, {"serif" if mathfont else "Arial, sans-serif"}" '
    attrs += f'font-size="{size}" font-weight="{700 if bold else 400}" fill="{color(c)}" text-anchor="{anchor}"'
    if mathfont:
        attrs += ' font-style="italic"'
    parts.append(f'<text x="{x}" y="{y}" {attrs}>{html.escape(value)}</text>')
    xb,yb,tw,th,_,_=M.text_extents(value)
    shift=0 if anchor=='start' else advance/2 if anchor=='middle' else advance
    labels.append(dict(text=value,x=x,y=y,font_size=size,requested_font_size=requested_size,
                       font_family=family,font_weight=700 if bold else 400,horizontal_scale=1,
                       bbox=[x+xb-shift,y+yb,x+xb+tw-shift,y+yb+th]))


def lines(x, y, values, size=18, c='ink', bold=False, anchor='middle', gap=22, maxw=None):
    for i, value in enumerate(values):
        text(x, y+i*gap, value, size, c, bold, anchor, maxw)


def state_pair(x, y, next_step=False):
    # Explicit baseline positions keep subscripts editable and avoid missing
    # Unicode subscript glyphs in PDF backends and font substitutions.
    text(x,y,'h',25,mathfont=True)
    text(x+12,y+6,'t+1' if next_step else 't',13,mathfont=True)
    offset = 36 if next_step else 23
    text(x+offset,y,',',23,mathfont=True)
    text(x+offset+12,y,'b',25,mathfont=True)
    text(x+offset+24,y+6,'ref',13,mathfont=True)


def boundary_state_icon(name, x, y):
    """A posed body represents the boundary state."""
    group(name)
    parts.append(f'<use xlink:href="#boundary-state-icon" x="{x}" y="{y}" width="36" height="28"/>')
    state_icons.append(dict(id=name,bbox=[x,y,x+36,y+28],meaning='boundary pose'))
    end()


def flame(name, x, y, w=24, h=32):
    parts.append(f'<use id="{name}" xlink:href="#trainable-flame" '
                 f'x="{x}" y="{y}" width="{w}" height="{h}"/>')


def tiles(x, y, n=4, c='blue', w=16, h=26, gap=4, keep=None):
    for i in range(n):
        faded = keep is not None and i >= keep
        rect(x+i*(w+gap), y, w, h, f'url(#wash-{c})' if faded else f'url(#tile-{c})',
             '#D5DAE9' if faded else color(c), r=3, sw=.55)


def dots(x, y, c='blue', gap=8):
    for i in range(3):
        circle(x+gap*i, y, 1.7, c)


def latent_pair(name, x, y, selection=False):
    """One shared glyph for D/C rows and commit/discard in b and d."""
    group(name)
    if selection:
        text(x+28.5,y-8,'Commit',13,'purple',True,'middle')
        text(x+78.5,y-8,'Discard',13,'gray',False,'middle')
        line(f'M{x+58.5} {y-3} V{y+51}','purple',1.1,dash='4 3')
    for yy,cc,label in ((y,'blue','D'),(y+26,'orange','C')):
        text(x-17,yy+15,label,17,cc,True,'middle')
        tiles(x,yy,5,cc,17,21,3,3 if selection else None)
        dots(x+106,yy+10.5,cc,6)
    end()


def snow(x, y, r=11):
    for deg in range(0, 360, 60):
        a = math.radians(deg-90)
        dx, dy = math.cos(a), math.sin(a)
        line(f'M{x} {y} l{r*dx} {r*dy}', 'blue', 1.5)
        for side in (-1, 1):
            line(f'M{x+dx*r*.54} {y+dy*r*.54} '
                 f'l{r*(.32*dx-side*.24*dy)} {r*(.32*dy+side*.24*dx)}', 'blue', 1.3)


def raster(name, path, dest):
    path = Path(path)
    im = Image.open(path)
    assert im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] == 0
    x, y, w, h = dest
    # Each high-resolution asset is embedded once and reused with SVG <use>.
    # Original generated PNG bytes and their alpha channels are unchanged.
    if path not in embedded_assets:
        asset_id = 'asset-' + path.stem
        embedded_assets[path] = asset_id
        parts.append(f'<defs><image id="{asset_id}" width="{im.width}" height="{im.height}" '
                     f'xlink:href="data:image/png;base64,{base64.b64encode(path.read_bytes()).decode()}"/></defs>')
    scale = min(w/im.width,h/im.height)
    tx,ty = x+(w-im.width*scale)/2,y+(h-im.height*scale)/2
    parts.append(f'<use id="{name}" xlink:href="#{embedded_assets[path]}" '
                 f'transform="translate({tx} {ty}) scale({scale})"/>')
    images.append(dict(id=name,source=str(path.relative_to(ROOT)),destination=[x,y,w,h],
                       pixel_size=list(im.size),alpha_extrema=im.getchannel('A').getextrema(),
                       original_png_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return tx,ty,scale


def panel(x, y, w, h, letter, title, c='blue'):
    rect(x,y,w,h,f'url(#wash-{c})',color(c),r=8,sw=.9)
    circle(x+27,y+28,21,'white',color(c),.8)
    text(x+27,y+40,letter,35,'ink',True,'middle')
    text(x+64,y+37,title,28,'ink',True,maxw=w-90)


def decoder(x, y, w, h):
    shape(f'M{x} {y} L{x+w} {y+h*.26} V{y+h*.74} L{x} {y+h} Z', 'url(#decoder)', '#5B6582')


def vector_logo(path, dest):
    """Embed the user's outlined wordmark as editable paths, not an image."""
    node = ET.parse(path).getroot()
    x,y,w,h = dest
    node.set('x',str(x));node.set('y',str(y))
    node.set('width',str(w));node.set('height',str(h))
    node.set('id','foredance-wordmark')
    node.set('preserveAspectRatio','xMidYMid meet')
    parts.append(ET.tostring(node,encoding='unicode'))
    logos.append(dict(source=str(path.relative_to(ROOT)),destination=list(dest),
                      sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      native_paths=len(node.findall('.//{http://www.w3.org/2000/svg}path'))))


rect(0,0,W,H)
group('title')
vector_logo(FIG/'foredance-logo.svg',(20,1,249,52))
line('M286 9 V44','#8494B5',1)
end()
group('legend')
for x,c,label,maxw in [(308,'blue','Discrete structure',156),
                       (545,'orange','Continuous detail',151),
                       (782,'teal','Music conditioning',165),
                       (1027,'purple','Motion context',156)]:
    rect(x,15,28,26,f'url(#tile-{c})',r=4)
    text(x+39,35,label,18,'#203F87',maxw=maxw)
flame('legend-trainable',1241,11,23,31)
text(1276,35,'Trainable',18,'#203F87')
snow(1413,28,14)
text(1436,35,'Frozen',18,'#203F87')
end()

# a: exact master layout; restore the previously requested official full name.
group('a-music-anticipation')
panel(14,57,1509,166,'a','Anticipate from heard music','teal')
text(80,122,'Heard audio',20,'teal')
for x in range(46,371):
    ys = [y for y in range(127,199) if (lambda p: p[0]<135 and p[1]>95 and p[2]>110 and p[1]-p[0]>30)(source.getpixel((x,y)))]
    if ys:
        line(f'M{x} {min(ys)} V{max(ys)}','teal',.72)
line('M62 208 H362','ink',.8,True)
line('M62 201 V214','ink',.8)
text(373,212,'t',23,'ink',mathfont=True)
line('M383 130 V206','purple',1.3,dash='5 6')
text(383,121,'Now',20,'ink',True,'middle')
dots(402,166,'ink',8)
line('M435 160 H478','ink',1.7,True)
decoder(484,95,153,119)
raster('official-mrt2-icon',path=FIG/'mrt2-official-app-icon.png',dest=(494,135,42,42))
lines(584,148,['Magenta','RealTime 2'],18,'ink',True,gap=21,maxw=92)
snow(572,184,9)
line('M638 159 H670','teal',2,True,id='heard-to-predicted-states')
rect(676,94,822,119,'url(#wash-teal)',r=7)
text(690,122,'Predicted music states',22,'#132462',True,maxw=320)
patterns = [[25,17,32,33,32],[30,35,23,38,30],[35,34,19,29,25],
            [19,33,25,37,17],[30,22,37,27,33]]
palettes = [['#098A9B','#007A88','#54BAB5','#00A7BC','#4DADC9'],
            ['#29B2C6','#149FD1','#278C99','#006B70','#44BAD5'],
            ['#08BBB7','#009FAB','#7AC7D0','#43BEA6','#37AC9E'],
            ['#45ABB8','#028399','#2296B3','#6CC7C2','#4FA0AF'],
            ['#0B9D9D','#77BEBD','#148FBD','#39B2D1','#00798B']]
for i,x in enumerate((701,861,1021,1181,1341)):
    rect(x-1,133,108,53,'white',r=6)
    for j,hh in enumerate(patterns[i]):
        rect(x+7+j*16,180-hh,13,hh,palettes[i][j],r=2,sw=0)
    dots(x+112,164,'blue',7)
text(1087,200,'Forecast time',17,'#2D6080',anchor='middle')
end()

# b: retain original module bounds and robot poses, route both inputs distinctly.
group('b-generate-commit-execute')
panel(15,235,1508,346,'b','Generate, commit, and execute','blue')
shape('M332 279 H928 Q935 279 935 286 V333 Q935 340 928 340 H879 '
      'Q872 340 872 347 V503 Q872 510 865 510 H332 Q325 510 325 503 '
      'V286 Q325 279 332 279 Z','url(#wash-orange)','#ED8294',.85)
text(360,306,'Structure–detail generator',26,bold=True,maxw=340)
rect(728,286,197,26,'white','#18ACD1',r=4,sw=.8)
text(826,305,'Trained with Commit Forcing',16,'#077BBA',anchor='middle',maxw=180)
# The user requested an independent music-conditioning source inside panel b,
# following the earlier editable SVG, without an a-to-b connector.
text(51,303,'Music conditioning',20,'teal',bold=True,maxw=218)
for i,hh in enumerate((13,19,10,17,15)):
    rect(74+i*17,329-hh,12,hh,palettes[0][i],r=2,sw=0)
line('M163 321 H304 V344','teal',2.6,id='panel-b-music-source')
rect(27,336,225,155,'url(#wash-purple)','purple',r=5,sw=.9)
text(139,364,'Context',22,'ink',True,'middle',maxw=200)
lines(139,392,['Committed history','+ boundary state'],19,'purple',gap=23,maxw=199)
state_pair(94,439)
group('context-history')
tiles(70,453,5,'purple',17,24,4)
dots(181,466,'purple',8)
end()
# Independent black history/state edges enter at the lower input of each module.
line('M252 432 H280 V468 H394','ink',2,True,id='context-to-detail')
line('M226 491 V526 H806 V450','ink',1.8,True,id='state-to-shared-decoder')
text(827,502,'b',25,mathfont=True)
text(839,508,'ref',14,mathfont=True)
rect(394,318,185,67,'url(#wash-blue)','blue',r=6,sw=1)
rect(394,428,191,67,'url(#wash-orange)','orange',r=6,sw=1)
for i,hh in enumerate((13,22,33)):
    rect(408+i*9,371-hh,6,hh,'url(#tile-blue)',r=0)
lines(448,348,['Structure planner','AR Transformer'],18,'#064FBD',anchor='start',gap=22,maxw=122)
# Match overview2.png's denoising sketch: noise tiles -> residual tiles.
# Every noise speck is native geometry rather than an embedded raster crop.
text(489.5,450,'Residual diffusion',18,'#CF5B00',True,'middle',maxw=170)
group('residual-diffusion-noise')
for tile_index,xx in enumerate((412,433)):
    for iy in range(22):
        for ix in range(18):
            value=110+((ix*73+iy*151+ix*iy*37+tile_index*89)%115)
            shade='#'+f'{value:02x}'*3
            rect(xx+ix,461+iy,1,1,shade,r=0)
end()
line('M461 472 H496','ink',1.6,True,id='diffusion-noise-to-residual')
tiles(500,460,2,'orange',17,24,4)
dots(550,472,'ink',7)
# Keep music FiLM above the separate context arrows.
line('M304 344 V450','teal',2.8,id='music-bus')
line('M304 344 H394','teal',2.8,True,id='music-film-to-structure')
line('M304 450 H394','teal',2.8,True,id='music-film-to-detail')
circle(304,344,3.2,'teal')
text(340,329,'FiLM',18,'teal',True,maxw=40)
text(340,435,'FiLM',18,'teal',True,maxw=40)
# The black connection crosses the teal bus without joining it. A continuous
# black stroke over a narrow white under-stroke makes the crossing unambiguous.
line('M252 377 H278 V361 H394','white',6)
line('M252 377 H278 V361 H394','ink',2,True,id='context-to-structure')
line('M579 357 H595','blue',2,True)
tiles(598,345,3,'blue',12,25,3)
dots(645,357,'blue',6)
text(620,334,'q',28,'blue',anchor='middle',mathfont=True)
tiles(676,345,2,'blue',16,25,4)
text(694,334,'e(q)',28,'blue',anchor='middle',mathfont=True)
line('M660 357 H676','blue',1.8,True,id='q-to-codebook-embedding')
line('M712 357 H739 V396','blue',2.4,True,id='structure-to-sum')
# Sampled q conditions detail, independently of the codebook embedding sent
# to the shared sum. Branch from the actual q-token bottom boundary.
line('M634 370 V399 H504 V428','blue',3,True,id='sampled-structure-to-detail')
text(568,419,'Embed + add',16,'blue',anchor='middle',maxw=104)
line('M585 467 H608','orange',2.1,True)
tiles(612,453,3,'orange',17,26,4)
dots(681,467,'orange',7)
text(646,440,'r',29,'orange',anchor='middle',mathfont=True)
line('M709 466 H739 V430','orange',2.4,True,id='detail-to-sum')
circle(739,413,17,'white','ink',1)
text(739,422,'+',31,'ink',anchor='middle')
line('M756 413 H770','ink',2,True,id='sum-to-decoder')
decoder(770,353,82,109)
lines(811,411,['Shared','decoder'],18,anchor='middle',gap=21,maxw=65)
line('M852 414 H884','ink',2,True,id='decoder-to-commit')
rect(884,358,171,108,'url(#wash-purple)','purple',r=6,sw=.9)
text(969,384,'Commit segment',21,'purple',True,'middle',maxw=155)
latent_pair('commit-selection-b',919,410,selection=True)
line('M1055 414 H1078','purple',2.1,True,id='commit-to-reference-bridge')
rect(1078,377,84,78,'url(#wash-gray)','#627089',r=5)
lines(1120,408,['Reference','bridge'],18,anchor='middle',gap=23,maxw=77)
line('M1162 414 H1195','ink',2,True,id='bridge-to-tracker')
rect(1195,374,84,81,'url(#wash-gray)','#627089',r=5)
lines(1237,400,['SONIC','tracker'],18,anchor='middle',gap=22,maxw=77)
snow(1237,439,9)
line('M1279 415 H1299','ink',2,True,id='tracker-to-execution')
rect(1299,282,214,235,'url(#wash-blue)','#D8E7F3',r=5,sw=.6)
lines(1405,307,['Humanoid execution','G1 reference tracking'],20,'ink',True,gap=24,maxw=200)
raster('g1-execution-left',path=ASSETS/'g1-dance-left-consistent.png',dest=(1299,337,108,180))
raster('g1-execution-right',path=ASSETS/'g1-dance-right-consistent.png',dest=(1407,337,108,180))
line('M1423 517 V534 H1236 V455','ink',1.9,True,id='robot-feedback-to-tracker-only')
text(1340,554,'Measured robot state',16,'ink',anchor='middle',maxw=230)
# Compute the joint payload, then append it to the next input context.
rect(386,540,334,33,'white','purple',r=6,sw=.65)
text(398,554,'D',10,'blue',True,'middle')
text(398,566,'C',10,'orange',True,'middle')
tiles(410,546,3,'blue',10,10,3)
tiles(410,558,3,'orange',10,10,3)
text(452,562,'History',17,'purple')
line('M529 545 V568','#CBB6E6',.8,id='b-history-state-divider')
boundary_state_icon('boundary-state-return-icon',536,543)
text(575,562,'Boundary state',17,'purple')
line('M977 466 V559 H720','purple',2.1,True,id='commit-to-computed-context')
text(848,550,'compute',18,'purple',anchor='middle')
line('M386 559 H130 V491','purple',2.1,True,id='computed-context-to-history')
text(267,550,'append',18,'purple',anchor='middle')
end()

# c: keep original data strip, anatomy and reconstruction alignment.
group('c-representation-and-paired-training')
panel(15,591,749,353,'c','Structure–Detail Representation','blue')
text(79,649,'Paired training with kinematic supervision',19,'#0755B0',maxw=620)
rect(28,653,216,75,'url(#wash-blue)','#E2EAF5',r=5,sw=.6)
raster('human-source',path=ASSETS/'human-dance-source.png',dest=(43,654,55,74))
text(120,684,'FineDance',20,'ink',True,maxw=115)
text(105,709,'Human dance data',17,maxw=130)
line('M244 693 H262','ink',1.8,True)
rect(264,664,188,52,'url(#wash-gray)','#909CAF',r=5,sw=.8)
lines(358,685,['Motion retargeting','Offline preprocessing'],17,anchor='middle',gap=21,maxw=172)
line('M453 693 H474','ink',1.8,True)
rect(475,653,275,75,'url(#wash-blue)','#E2EAF5',r=5,sw=.6)
raster('g1-training',path=ASSETS/'g1-neutral.png',dest=(489,654,51,74))
text(558,684,'G1 training motion',20,'ink',True,maxw=180)
text(558,708,'Unitree G1',18,'#143C87')
rect(28,733,220,173,'#EDF7FE',r=5)
rect(255,733,240,173,'#EDF7FE',r=5)
text(43,754,'Joint view',20,'#063885',True)
text(269,754,'Geometry view',20,'#063885',True)
raster('joint-view',path=ASSETS/'g1-joint-view-consistent.png',dest=(28,756,97,148))
gx,gy,gs = raster('geometry-view',path=ASSETS/'g1-neutral.png',dest=(263,757,95,147))
parts.append(f'<g id="geometry-landmarks" transform="translate({gx} {gy}) scale({gs})">')
# Blue landmarks: torso center, bilateral wrists and sole points. Orange
# landmarks: remaining displayed shoulder, elbow, hip, knee and ankle points.
for px,py in [(335,334),(690,334),(277,541),(748,541),(430,703),(595,703),
              (396,1012),(627,1012),(370,1320),(649,1320)]:
    circle(px,py,29,'orange','white',7)
for px,py in [(512,437),(216,733),(799,733),(378,1450),(645,1450)]:
    circle(px,py,30,'blue','white',7)
end()
for x in (140,371):
    circle(x,786,10,'url(#tile-blue)','blue',.6)
    circle(x,843,10,'url(#tile-orange)','orange',.6)
text(160,789,'Structure',18,'blue',True,maxw=83)
text(160,810,'root, legs, waist',12,anchor='start',maxw=84)
text(160,846,'Detail',18,'orange',True)
text(160,867,'arm joints',12,maxw=80)
text(390,789,'Structure',18,'blue',True,maxw=94)
text(384,810,'torso, wrists, soles',12,maxw=107)
text(390,846,'Detail',18,'orange',True)
text(384,867,'other body points',12,maxw=107)
for y in (742,843):
    rect(504,y,247,61,'white','blue',r=5,sw=.8)
text(516,782,'e(q)',25,'blue',mathfont=True)
text(558,782,'+',22)
text(578,782,'r',25,'orange',mathfont=True)
line('M591 775 H610','blue',1.8,True,id='full-latent-to-training-decoder')
text(518,883,'e(q)',25,'blue',mathfont=True)
line('M562 876 H610','blue',1.8,True,id='structure-to-training-decoder')
for yy in (759,860):
    decoder(610,yy,31,31)
    flame(f'c-decoder-{yy}-trainable',591,yy-15,16,22)
    text(621,yy+21,'D',17,mathfont=True,anchor='middle')
    text(629,yy+24,'ψ',10,mathfont=True)
    line(f'M641 {yy+16} H656','blue',1.8,True,
         id='training-decoder-to-full' if yy==759 else 'training-decoder-to-structure')
lines(704,769,['Full-motion','reconstruction'],16,anchor='middle',gap=20,maxw=91)
lines(704,870,['Structural-view','reconstruction'],16,anchor='middle',gap=20,maxw=91)
# The two actual decoding operations share the same parameters. Link those
# operations directly, instead of placing unconnected decorative decoder icons.
line('M625.5 785.97 V860','purple',1,dash='3 3',id='shared-training-decoder-parameters')
line('M625.5 823 H636','purple',1)
text(641,827,'Shared decoder',15,'#235296',maxw=107)
end()

# d: native training steps; scope no-gradient construction to the first pass.
group('d-commit-forcing')
panel(774,591,750,353,'d','Commit Forcing','purple')
steps = [(788,172,['1. Sample','structure + detail']),
         (971,172,['2. Commit jointly','+ decode']),
         (1154,181,['3. Update history','+ reconstruct state']),
         (1346,164,['4. Learn','continuation'])]
for x,w,title in steps:
    rect(x,646,w,140,'url(#wash-purple)','purple',r=5,sw=.8)
    lines(x+w/2,673,title,19,'ink',True,gap=22,maxw=w-18)
latent_pair('sample-dc-pair',822,724)
latent_pair('commit-selection-d',999,724,selection=True)
group('learn-trainable-models')
for name,yy,cc,label in [('structure',713,'blue','Structure'),('detail',751,'orange','Detail')]:
    rect(1359,yy,138,26,f'url(#wash-{cc})',cc,r=4,sw=.8)
    flame(f'learn-{name}-trainable',1368,yy+2,17,22)
    text(1434,yy+18,label,16,cc,True,'middle',maxw=100)
end()
state_pair(1169,733,next_step=True)
group('cof-updated-history')
tiles(1170,743,4,'purple',17,24,4)
end()
raster('cof-state-g1',path=ASSETS/'g1-neutral.png',dest=(1265,705,65,80))
for start,endx in ((960,969),(1143,1152),(1335,1344)):
    line(f'M{start} 737 H{endx}','purple',1.8,True)
line('M799 793 V808 H1318 V793','purple',1.2)
# This is a scope annotation, not a reverse data-flow or feedback path.
# The lower card explains the context produced by these three operations.
line('M1059 808 V817','purple',1)
text(1059,835,'Context generation (no gradients)',16,'purple',True,'middle',maxw=420)
line('M1059 841 V849','purple',1)
rect(1292,840,218,50,'url(#wash-teal)','teal',r=5,sw=.8)
lines(1401,861,['Next-segment targets','(encoded from data)'],18,'#076C8C',gap=21,maxw=204)
line('M1455 840 V786','teal',2,True,id='recorded-target-to-learn-only')
# Shared enclosure shows generated history and its derived state as one pair.
rect(927,849,294,56,'white','purple',r=7,sw=.7)
text(938,871,'D',12,'blue',True,'middle')
text(938,889,'C',12,'orange',True,'middle')
tiles(951,859,4,'blue',13,15,4)
tiles(951,877,4,'orange',13,15,4)
line('M1030 865 V888','#CBB6E6',.8,id='d-history-state-divider')
boundary_state_icon('boundary-state-training-icon',1044,860)
lines(1083,873,['Generated history','+ boundary state'],15,'purple',anchor='start',gap=19,maxw=127)
end()

parts.append('</svg>')
svg = '\n'.join(parts)
root = ET.fromstring(svg)
ns = {'s':'http://www.w3.org/2000/svg'}
assert len(root.findall('.//s:image',ns)) == 6
assert all(i['source'] != str(MASTER.relative_to(ROOT)) for i in images)
assert len(root.findall('.//s:text',ns)) > 75
assert not any('prefix' in x['text'].lower() or 'd+c' in x['text'].lower() or 'fms14' in x['text'].lower() for x in labels)
assert not any('schematic' in x['text'].lower() for x in labels)
assert len([a for a in arrows if a['id'].startswith('music-film')]) == 2
(FIG/'overview-refined.svg').write_text(svg)


class PaperPDF(cairosvg.surface.PDFSurface):
    def _create_surface(self, width, height):
        surface, width, height = super()._create_surface(width,height)
        surface.restrict_to_version(cairo.PDF_VERSION_1_5)
        return surface,width,height


PaperPDF.convert(bytestring=svg.encode(),write_to=str(FIG/'overview-refined.pdf'))
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/'overview-refined.png'))
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/'overview-refined-2x.png'),scale=2)
report = dict(master=str(MASTER.relative_to(ROOT)),master_sha256=hashlib.sha256(MASTER.read_bytes()).hexdigest(),
              master_dimensions=list(source.size),canvas_dimensions=[W,H],text_elements=len(labels),labels=labels,images=images,arrows=arrows,
              groups=groups,state_icons=state_icons,logos=logos,svg_bytes=len(svg.encode()),
              user_authorized_changes=['Native editable text and geometry replacing traced contours',
              'Restore Magenta RealTime 2 full name and existing official icon',
              'Restore prior removal of note-like prose in favor of visual cues',
              'Place Music conditioning directly in panel b, with no connector from panel a',
              'Derive robot color and pose variants from one master, with user-authorized alpha-only background removal',
              'Use Context and Boundary state; remove b Paired and label the return arrow append',
              'Separate FiLM labels from arrowheads, use smaller one-line anatomy explanations, and show shared decoding on both reconstruction paths',
              'Explain no-gradient context generation with a scope label rather than a reverse dashed arrow',
              'Label dataset supervision Next-segment targets (encoded from data), and purple Motion context',
              'Recolor the original single-row context blocks in b and d purple to match Motion context',
              'Replace both abstract boundary-state symbols with the same humanoid-pose and velocity-arrow icon',
              'Replace the title with the author-supplied ForeDance logo, traced into ten native SVG paths',
              'Make sampled q branch separately into codebook embedding and an Embed + add input verified against the residual-generator implementation',
              'Show Structure and Detail as trainable models in Learn, with matching flame legend',
              'Add trainable flames to both shared-decoder instances in c',
              'Separate the compute and append arrows around the history and boundary-state payload',
              'Use Helvetica at natural proportions, remove horizontal text compression, and leave clear spacing for the Embed + add label',
              'Remove arrows from both boundary icons and use matching vertical history-state dividers in b and d'],
              selected_reference='output/overview-editable-20260911/overview-editable.png',
              selected_reference_sha256=hashlib.sha256((OUT/'selected-reference.png').read_bytes()).hexdigest(),
              fidelity='Selected panel bounds and palette retained; author-requested local edits, header legend and removal of the former footer area.',
              generation='One neutral robot reused directly or as imagegen variant reference. Three variants matted with original RGB unchanged; official icon retained.')
(OUT/'reconstruction-record.json').write_text(json.dumps(report,indent=2)+'\n')
if '--activate' in sys.argv:
    for ext in ('svg','pdf'):
        shutil.copy2(FIG/f'overview-refined.{ext}',FIG/f'overview.{ext}')
print(json.dumps({k:report[k] for k in ('master_dimensions','canvas_dimensions','text_elements','svg_bytes','fidelity')},indent=2))
