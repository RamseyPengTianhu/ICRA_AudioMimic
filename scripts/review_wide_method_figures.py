"""Critical geometry, label clearance, and full-width manuscript inspection."""
from pathlib import Path
import json, math, re, hashlib
import xml.etree.ElementTree as ET
import pymupdf as fitz
from check_figure_line_clearance import intersects, segments

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/method-wide-20260912'
FIG=ROOT/'figures/foredance'
NS={'s':'http://www.w3.org/2000/svg'}
NAMES=['structure-detail-training','cof-terminology']

def review():
    result={'figures':{},'scientific_geometry':{}}
    for name in NAMES:
        svg=OUT/f'{name}.svg';root=ET.parse(svg).getroot()
        assert not root.findall('.//s:image',NS)
        page=fitz.open(OUT/f'{name}.pdf')[0]
        assert not page.get_images()
        spans=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
        collisions=[]
        for s in spans:
            assert page.rect.contains(fitz.Rect(s['bbox'])),(name,s['text'])
            r=fitz.Rect(s['bbox'])+(-1,-1,1,1)
            for d in page.get_drawings():
                if d['color'] is not None and r.intersects(fitz.Rect(d['rect'])+(-2,-2,2,2)):
                    if any(intersects(a,b,r) for a,b in segments(d['items'])):
                        collisions.append(['stroke',s['text'],list(d['rect'])])
                if d['fill'] is not None and fitz.Rect(d['rect']).get_area()<800:
                    if fitz.Rect(s['bbox']).intersects(fitz.Rect(d['rect'])):
                        collisions.append(['filled glyph',s['text'],list(d['rect'])])
        for i,a in enumerate(spans):
            for b in spans[i+1:]:
                if fitz.Rect(a['bbox']).intersects(fitz.Rect(b['bbox'])):collisions.append(['text',a['text'],b['text']])
        result['figures'][name]={'canvas':list(map(float,root.attrib['viewBox'].split()[2:])),
            'sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'embedded_images':0,
            'collisions':collisions,'smallest_print_font_pt':min(s['size'] for s in spans)/page.rect.width*504}
    point=lambda n:(float(n.attrib['cx']),float(n.attrib['cy']))
    rep=ET.parse(OUT/'structure-detail-training.svg').getroot()
    q,z=point(rep.find('.//*[@id="selected-prototype"]')),point(rep.find('.//*[@id="encoded-latent"]'))
    others=[point(n) for n in rep.findall('.//*[@class="prototype"]')]
    result['scientific_geometry']['selected_is_nearest']=math.dist(q,z)<min(math.dist(p,z) for p in others)
    assert result['scientific_geometry']['selected_is_nearest']
    masks={}
    for kind in ['full','structural']:
        cells=rep.findall(f'.//s:g[@id="{kind}-coordinate-mask"]/s:rect',NS)
        assert len(cells)==32
        rows=sorted(set(x.attrib['y'] for x in cells))
        assert len(rows)==4
        for y in rows:
            row=[x for x in cells if x.attrib['y']==y]
            active=sum(x.attrib['fill']=='#0769F9' for x in row)
            assert active==8 if kind=='full' else 0<active<8
        masks[kind]=True
    result['scientific_geometry']['four_view_supervision_masks']=masks
    cof=ET.parse(OUT/'cof-terminology.svg').getroot()
    origins=[point(cof.find(f'.//*[@id="{k}-origin"]')) for k in ['sampled','recorded']]
    target=point(cof.find('.//*[@id="fixed-latent-target"]'))
    paths=cof.findall('.//s:g[@id="same-target-new-residual-origin"]/s:path',NS)
    assert len(paths)==2
    for origin,path in zip(origins,paths):
        v=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.attrib['d'])))
        start,end=v[:2],v[2:]
        dx,dy=target[0]-origin[0],target[1]-origin[1]
        assert all(abs((p[0]-origin[0])*dy-(p[1]-origin[1])*dx)<1e-6 for p in [start,end])
        assert abs(math.dist(origin,start)-20)<1e-6 and abs(math.dist(target,end)-23)<1e-6
    assert math.dist(origins[1],target)<math.dist(origins[0],target)
    result['scientific_geometry']['same_target_correct_displacements']=True
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert not any(x['collisions'] for x in result['figures'].values())
    return result

if __name__=='__main__':review()
