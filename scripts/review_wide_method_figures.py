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
    master=ET.parse(FIG/'boundary-state-icon.svg').getroot().find('s:g',NS)
    overview=ET.parse(FIG/'overview.svg').getroot()
    overview_glyph=overview.find('.//s:symbol[@id="boundary-state-icon"]/s:g',NS)
    assert ET.tostring(master)==ET.tostring(overview_glyph)
    glyph_counts={}
    for name in NAMES:
        svg=OUT/f'{name}.svg';root=ET.parse(svg).getroot()
        assert not root.findall('.//s:image',NS)
        icons=root.findall('.//s:g[@data-icon="boundary-state"]',NS)
        assert len(icons)==(2 if name=='structure-detail-training' else 3)
        assert all(ET.tostring(icon.find('s:g',NS))==ET.tostring(master) for icon in icons)
        for icon in icons:
            x,y,scale=map(float,re.findall(r'-?\d+(?:\.\d+)?',icon.attrib['transform']))
            assert abs(x+10.2*scale-float(icon.attrib['data-center-x']))<1e-6
            assert abs(y+14.075*scale-float(icon.attrib['data-center-y']))<1e-6
        glyph_counts[name]=len(icons)
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
    supervision={}
    for kind in ['full','structural']:
        group=rep.find(f'.//s:g[@id="{kind}-reconstruction-supervision"]',NS)
        assert group is not None
        bracket=group.find('s:path',NS)
        y=169 if kind=='full' else 407
        assert bracket.attrib['d']==f'M1554 {y}H1548V{y+112}H1554'
        # Both decoder outputs target the center of the complete coordinate pair.
        axis=y+56
        assert any(p.attrib['d']==f'M1448 {int(axis)}L1540 {int(axis)}'
                   for p in rep.findall('.//s:path',NS))
        for subset in ['structure','detail']:
            band=group.find(f's:g[@data-coordinates="{subset}"]',NS)
            assert len(band.findall('s:rect',NS))==2
            arrows=[x for x in band.findall('s:path',NS) if x.attrib.get('marker-end')]
            assert len(arrows)==int(kind=='full' or subset=='structure')
            assert band.attrib['opacity']==('1' if kind=='full' or subset=='structure' else '0.28')
        supervision[kind]=True
    assert not rep.findall('.//s:g[@id="full-coordinate-mask"]',NS)
    result['scientific_geometry']['full_and_structural_coordinate_matching']=supervision
    headings={t.text:t for t in rep.findall('.//s:text',NS)}
    for title in ['Full-motion loss','Structural loss']:
        assert float(headings[title].attrib['x'])==(1560+2028)/2
    cof=ET.parse(OUT/'cof-terminology.svg').getroot()
    result['shared_boundary_state_icon']={'identical_to_overview':True,'counts':glyph_counts}
    # Check connector alignment against the drawn context edges, including
    # enough room for an arrow shaft behind the full marker envelope.
    bands=cof.findall('.//s:g[@id="matched-generation-contexts"]/s:rect',NS)
    connectors=cof.findall('.//s:g[@id="matched-generation-contexts"]/s:path',NS)
    horizontal=[p for p in connectors if p.attrib.get('marker-end')]
    for band,arrow in zip(bands,horizontal):
        values=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',arrow.attrib['d'])))
        x,y,end=values
        assert abs(y-(float(band.attrib['y'])+float(band.attrib['height'])/2))<1e-6
        assert x>float(band.attrib['x'])+float(band.attrib['width'])
        assert end-x>5*float(arrow.attrib['stroke-width'])+20
    group=cof.find('.//s:g[@id="commit-forcing-self-rollout"]',NS)
    for tile in group.findall('s:g[@opacity]',NS):
        rects=tile.findall('s:rect',NS)
        assert len(rects)==2
        top=min(float(r.attrib['y']) for r in rects)
        bottom=max(float(r.attrib['y'])+float(r.attrib['height']) for r in rects)
        assert abs((top+bottom)/2-461)<1e-6
    assert any(p.attrib['d']=='M346 461H532' for p in group.findall('s:path',NS))
    assert all(float(i.attrib['data-center-y'])==461 for i in group.findall('s:g[@data-icon]',NS))
    headings={t.text:t for t in cof.findall('.//s:text',NS)}
    for label,axis in [('TF',204),('CoF',461)]:
        assert abs(float(headings[label].attrib['y'])-.35*float(headings[label].attrib['font-size'])-axis)<1e-6
    for label,cx in [('History',1275),('Boundary state',1530),('Commit',634),('Discard',834),('Model rollout',439)]:
        assert float(headings[label].attrib['x'])==cx
    for label in ['context','Model rollout','Commit','Discard']:
        assert float(headings[label].attrib['y'])==395
    result['label_icon_and_group_alignment']={'glyph_visible_bounds_centered':True,
        'cof_sources_plans_contexts_share_row_axis':True,'operation_labels_share_baseline':True,
        'supervision_output_brackets_centered_on_decoder_arrows':True,'group_titles_centered':True}
    result['context_arrow_alignment']=True
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
