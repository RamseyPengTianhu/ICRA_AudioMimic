"""Replace only the overview wordmark; preserve every other SVG byte."""
from pathlib import Path
from html import escape
import hashlib
import json
import re
import cairosvg
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures/foredance'
OUT=ROOT/'output/method-wide-20260912'

def main():
    p=FIG/'overview.svg'
    old=p.read_text()
    match=re.search(r'<ns0:svg\b[^>]*id="foredance-wordmark".*?</ns0:svg>',old,re.S)
    if match is None and 'id="murodance-wordmark"' in old:
        print('MuRoDance wordmark already active; no content change.')
        return
    if match is None:
        raise RuntimeError('Expected the original ForeDance wordmark; refusing a broad rewrite.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'overview-before-title.svg').write_text(old)
    font=78
    first=stringWidth('MuRo','Helvetica-Bold',font)
    last=stringWidth('Dance','Helvetica-Bold',font)
    gap=17
    width=first+gap+last
    logo=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="104" viewBox="0 0 {width} 104">'
          '<title>MuRoDance</title><desc>Editable wordmark retaining the black and blue title colors.</desc>'
          f'<text x="0" y="80" font-family="Helvetica" font-size="{font}" font-weight="bold" fill="#0C0D0F">MuRo</text>'
          f'<path d="M{first+8} 9V96" stroke="#004BFF" stroke-width="3"/>'
          f'<text x="{first+gap}" y="80" font-family="Helvetica" font-size="{font}" font-weight="bold" fill="#004BFF">Dance</text></svg>')
    (FIG/'murodance-logo.svg').write_text(logo+'\n')
    embedded=logo.replace(f'width="{width}" height="104"', 'x="20" y="1" width="249" height="52" id="murodance-wordmark" preserveAspectRatio="xMidYMid meet"',1)
    new=old[:match.start()]+embedded+old[match.end():]
    assert new.replace(embedded,'WORDMARK',1)==old.replace(match.group(),'WORDMARK',1)
    p.write_text(new)
    cairosvg.svg2pdf(bytestring=new.encode(),write_to=str(FIG/'overview.pdf'))
    cairosvg.svg2png(bytestring=old.encode(),write_to=str(OUT/'overview-before-title.png'))
    cairosvg.svg2png(bytestring=new.encode(),write_to=str(OUT/'overview.png'))
    (OUT/'overview-title-change.json').write_text(json.dumps({
        'title':'MuRoDance','only_changed_svg_region':'wordmark at x=20, y=1, width=249, height=52',
        'before_svg_sha256':hashlib.sha256(old.encode()).hexdigest(),
        'after_svg_sha256':hashlib.sha256(new.encode()).hexdigest(),
        'unchanged_outside_wordmark':True},indent=2)+'\n')

if __name__=='__main__':main()
