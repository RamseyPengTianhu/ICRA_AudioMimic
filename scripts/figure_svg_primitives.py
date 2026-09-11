"""Small native-SVG primitives used to reconstruct accepted paper artwork."""
from html import escape
from pathlib import Path
import json
import cairosvg

C = dict(blue='#0769F9', orange='#FF8A17', teal='#009EAC',
         purple='#8534DB', ink='#080F2D', gray='#8D96A8',
         pale_blue='#EDF4FF', pale_orange='#FFF2E4', pale_teal='#E5F7F7',
         pale_purple='#F3ECFC')

def color(c):
    return C.get(c, c)

class Figure:
    def __init__(self, width, height, title, reference):
        self.width, self.height = width, height
        self.labels = []
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
                      f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                      f'<title>{escape(title)}</title>',
                      '<desc>Editable native SVG. Flat two-dimensional scientific schematic. '
                      'Reconstructed from the selected imagegen composition with author-requested '
                      'semantic and connection corrections.</desc>', '<defs>']
        for name in ('blue', 'orange', 'teal', 'purple', 'ink', 'gray'):
            self.parts.append(f'<marker id="arrow-{name}" viewBox="0 0 10 10" '
                              f'refX="9" refY="5" markerWidth="5" markerHeight="5" '
                              f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" '
                              f'fill="{color(name)}"/></marker>')
        self.parts += ['</defs>', f'<metadata>{escape(json.dumps({"reference":str(reference)}))}</metadata>',
                       f'<rect width="{width}" height="{height}" fill="white"/>']

    def raw(self, s):
        self.parts.append(s)

    def group(self, name):
        self.parts.append(f'<g id="{escape(name)}">')

    def end(self):
        self.parts.append('</g>')

    def path(self, d, stroke='ink', sw=2.4, fill='none', arrow=False, dash=None, opacity=1):
        a = f' marker-end="url(#arrow-{stroke})"' if arrow else ''
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.parts.append(f'<path d="{d}" fill="{color(fill)}" stroke="{color(stroke)}" '
                          f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
                          f'opacity="{opacity}"{a}/>')

    def line(self, x1, y1, x2, y2, **kwargs):
        self.path(f'M{x1} {y1}L{x2} {y2}', **kwargs)

    def rect(self, x, y, w, h, fill='white', stroke='none', sw=1.8, r=0, opacity=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
                          f'fill="{color(fill)}" stroke="{color(stroke)}" stroke-width="{sw}" '
                          f'opacity="{opacity}"/>')

    def circle(self, x, y, r, fill='white', stroke='ink', sw=2.2, opacity=1):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color(fill)}" '
                          f'stroke="{color(stroke)}" stroke-width="{sw}" opacity="{opacity}"/>')

    def text(self, x, y, s, size=28, fill='ink', anchor='start', weight='normal', math=False):
        family = 'Times New Roman' if math else 'Helvetica'
        style = 'italic' if math else 'normal'
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
                          f'font-style="{style}" font-weight="{weight}" text-anchor="{anchor}" '
                          f'fill="{color(fill)}">{escape(s)}</text>')
        self.labels.append(dict(x=x,y=y,text=s,size=size,family=family))

    def rich(self, x, y, runs, size=30, fill='ink', anchor='start', math=True):
        family = 'Times New Roman' if math else 'Helvetica'
        style = 'italic' if math else 'normal'
        a = [f'<text x="{x}" y="{y}" font-family="{family}" font-style="{style}" '
             f'font-size="{size}" text-anchor="{anchor}" fill="{color(fill)}">']
        plain = ''
        for run in runs:
            if isinstance(run, str):
                a.append(escape(run)); plain += run
            else:
                value, shift = run
                dy = size*.25 if shift == 'sub' else -size*.4
                a.append(f'<tspan dy="{dy}" font-size="{size*.68}">{escape(value)}</tspan>'
                         f'<tspan dy="{-dy}" font-size="{size}">​</tspan>')
                plain += value
        a.append('</text>')
        self.parts.append(''.join(a))
        self.labels.append(dict(x=x,y=y,text=plain,size=size,family=family))

    def flame(self, x, y, h=32):
        self.parts.append(f'<g transform="translate({x} {y}) scale({h/32})">'
          '<path d="M12.3 1C14.2 8.2 20.8 10.5 21.1 17.4C21.4 24.8 17.4 30.4 11.6 30.4'
          'C5.8 30.4 2.2 26.1 2.6 20.3C2.8 16.8 4.6 14.5 7.1 11.7'
          'C6.7 16.1 8.3 18.1 10.1 18.5C8.7 11.6 14 8.1 12.3 1Z" fill="#F27822"/>'
          '<path d="M12 17C13 21.1 17.4 22.7 15.6 26.3C14.1 29.4 9.2 29 8.2 26.1'
          'C7.1 23 10.5 20.6 12 17Z" fill="#FFD17D"/></g>')

    def pose(self, x, y, scale=1.5, velocity=True):
        self.parts.append(f'<g transform="translate({x} {y}) scale({scale})" '
                          f'stroke="{C["purple"]}" fill="none" stroke-width="2.1" '
                          'stroke-linecap="round" stroke-linejoin="round">'
                          '<circle cx="10.5" cy="3.9" r="2.8" fill="#8534DB" stroke="none"/>'
                          '<path d="M10.5 8L9 17M10 10L5.5 13L3.2 17'
                          'M10 10L14.4 13L17.2 10M9 17L5 22L4 26M9 17L13 21L16 25.8"/>')
        if velocity:
            self.parts.append('<path d="M23 21L27 17L31 20L35 12L39 15" stroke-width="1.6"/>')
        self.parts.append('</g>')

    def save(self, stem):
        stem = Path(stem)
        stem.parent.mkdir(parents=True, exist_ok=True)
        svg = '\n'.join(self.parts+['</svg>'])
        stem.with_suffix('.svg').write_text(svg)
        cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(stem.with_suffix('.pdf')))
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(stem.with_suffix('.png')))
        stem.with_suffix('.labels.json').write_text(json.dumps(self.labels,indent=2)+'\n')
        return svg
