"""Scoped layout and math-glyph repair of the September 14 accepted artwork."""
from pathlib import Path
from io import BytesIO
import subprocess
from lxml import etree as E
import cairosvg
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/figure-spacing-20260915'
NS='http://www.w3.org/2000/svg'
def el(tag,**attrs):return E.Element('{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def move(e,y):e.set('transform',f'translate(0 {y}) '+e.get('transform',''))
def export(r,name):
 p=ROOT/'figures/foredance'/name
 data=E.tostring(r,encoding='utf-8')
 p.with_suffix('.svg').write_bytes(data)
 cairosvg.svg2pdf(bytestring=data,write_to=str(p.with_suffix('.pdf')))
 cairosvg.svg2png(bytestring=data,write_to=str(p.with_suffix('.png')))
r=E.fromstring(subprocess.check_output(['git','show','9725ca2:figures/foredance/overview_framework_h8_v9.svg'],cwd=ROOT))
r.set('height','1036');r.set('viewBox','0 0 1536 1036')
r.find('{'+NS+'}rect').set('height','1036')
for id in ['a-music-anticipation','b-generate-commit-execute','predicted-states-to-time-alignment']:
 move(r.xpath('//*[@id=$id]',id=id)[0],40)
for id in ['c-representation-and-paired-training','d-commit-forcing']:
 move(r.xpath('//*[@id=$id]',id=id)[0],80)
d=r.xpath('//*[@id="d-commit-forcing"]')[0];d[0].set('height','353')
steps=r.xpath('//*[@id="cf-compact-steps"]')[0];steps.set('transform','translate(0 40)')
for e in steps:
 tag=E.QName(e).localname
 if tag=='rect' and e.get('height')=='140':e.set('height','158')
 elif tag=='text' and float(e.get('y',0))<700:pass
 else:move(e,12)
for e in d:
 if e is steps:continue
 if e.get('id')=='recorded-target-to-learn-only':e.set('d','M1455 872 V844')
 elif e.get('y') and float(e.get('y'))>=828:move(e,44)
 elif (e.get('y')=='657') or (e.get('d','').startswith(('M788 663','M1346 663'))):move(e,8)
for y,label in [(57,'Inference'),(631,'Training')]:
 g=el('g',id=label.lower()+'-section-header')
 g.append(el('rect',x=14,y=y,width=1510,height=28,rx=4,fill='#0769F9'))
 t=el('text',x=769,y=y+21,font_family='Helvetica, Arial, sans-serif',font_size=22,font_weight=700,text_anchor='middle',fill='white');t.text=label;g.append(t);r.append(g)
assert d[0].get('height')=='353'
# Apply the four PDF review annotations without changing computation routes.
for group_id,letter in [('a-music-anticipation','a'),('b-generate-commit-execute','b'),('c-representation-and-paired-training','c'),('d-commit-forcing','d')]:
    panel=r.xpath('//*[@id=$id]',id=group_id)[0]
    badge=next(e for e in panel if E.QName(e).localname=='text' and e.text==letter)
    circle=next(e for e in panel if E.QName(e).localname=='circle' and e.get('r')=='21')
    panel.remove(badge);panel.remove(circle)
    heading=next(e for e in panel if E.QName(e).localname=='text' and e.get('font-size')=='28')
    heading.set('x',str(float(panel[0].get('x'))+14))
    if letter=='c':
        next(e for e in panel if e.text=='Kinematics-Guided Supervision').set('x',heading.get('x'))
panel=r.xpath('//*[@id="b-generate-commit-execute"]')[0]
film=[e for e in panel.iter() if E.QName(e).localname=='text' and e.text=='FiLM']
film[1].getparent().remove(film[1])
for text,x,baseline,width in [(film[0],290,403,48),
    (next(e for e in panel.iter() if e.text=='Embed + Add'),568,404,104),
    (next(e for e in panel.iter() if e.text=='Latent Prefix'),595,506,90)]:
    text.getparent().remove(text)
    text.set('x',str(x));text.set('y',str(baseline));text.set('text-anchor','middle')
    group=el('g',id='inline-'+text.text.lower().replace(' + ','-').replace(' ','-'))
    group.append(text);panel.append(group)
# Leave explicit gaps in the wires; labels have no opaque background.
for id,path in {
    'music-bus':'M290 344 V384 M290 410 V450',
    'music-film-to-structure':'M290 344 H394',
    'music-film-to-detail':'M290 450 H394',
    'panel-b-music-source':'M925 312 H290 V344',
    'sampled-structure-to-detail':'M634 370 V399 H622 M514 399 H504 V428',
    'latent-prefix-history-update':'M720 499 V501 H643 M547 501 H470 V540',
}.items():
    r.xpath('//*[@id=$id]',id=id)[0].set('d',path)
# A marker on a multi-subpath SVG path creates an arrow at every gap.
# Keep the arrowhead only on the segment that reaches the destination.
for id in ['sampled-structure-to-detail','latent-prefix-history-update']:
    path=r.xpath('//*[@id=$id]',id=id)[0]
    first,last=path.get('d').split(' M')
    lead=E.fromstring(E.tostring(path));lead.set('id',id+'-before-label')
    lead.set('d',first);lead.attrib.pop('marker-end',None)
    path.getparent().insert(path.getparent().index(path),lead)
    path.set('d','M'+last)
r.xpath('//*[@id="latent-prefix-history-update-clearance"]')[0].set('d','M720 499 V501 H643 M547 501 H470 V540')
# Move the conditioning junction together with its shared wire.
for e in panel.iter():
    if E.QName(e).localname=='circle' and e.get('cx')=='304' and e.get('cy')=='344':e.set('cx','290')
# Second PDF review: compact module label, clearer wires, and attached headers.
heading=next(e for e in panel.iter() if e.text=='D+C Generator')
heading.set('x','856');heading.set('y','301');heading.set('font-size','19');heading.set('text-anchor','end')
for e in panel.iter():
    if E.QName(e).localname=='circle' and e.get('cx')=='739' and e.get('cy')=='413':e.set('r','12')
    if E.QName(e).localname=='text' and e.text=='+':e.set('font-size','24');e.set('y','420')
    if E.QName(e).localname=='text' and e.get('x') in ['827','839']:
        e.set('x',str(float(e.get('x'))-13))
for id,path in {
    'structure-to-sum':'M712 357 H739 V401',
    'detail-to-sum':'M709 466 H739 V425',
    'sum-to-decoder':'M751 413 H782',
    'r-prefix-tap':'M654 479 V489 H720 V499',
    'r-prefix-tap-clearance':'M654 479 V489 H720 V499',
    'latent-prefix-history-update-before-label':'M720 499 V505 H643',
    'latent-prefix-history-update':'M547 505 H470 V540',
    'latent-prefix-history-update-clearance':'M720 499 V505 H643 M547 505 H470 V540',
}.items():
    r.xpath('//*[@id=$id]',id=id)[0].set('d',path)
r.xpath('//*[@id="inline-latent-prefix"]')[0][0].set('y','510')
for id,y in [('inference-section-header',57),('training-section-header',631)]:
    g=r.xpath('//*[@id=$id]',id=id)[0]
    g[0].set('y',str(y+12));g[0].set('height','28');g[0].set('rx','0')
    g[1].set('y',str(y+33))
# Flat top edges meet the header strips without a white corner gap.
for id in ['a-music-anticipation','c-representation-and-paired-training','d-commit-forcing']:
    r.xpath('//*[@id=$id]',id=id)[0][0].set('rx','0')
# Treat each phase as one rounded card, with its own inset-free title band.
# Panel boundaries become quiet interior dividers rather than separate boxes.
for id in ['a-music-anticipation','b-generate-commit-execute','c-representation-and-paired-training','d-commit-forcing']:
    background=r.xpath('//*[@id=$id]',id=id)[0][0]
    background.set('fill','none');background.set('stroke','none')
for id,top,bottom in [('inference-section-header',69,621),('training-section-header',643,1024)]:
    card=el('rect',id=id+'-card',x=14,y=top,width=1510,height=bottom-top,rx=9,
            fill='url(#wash-blue)',stroke='#A7C5EC',stroke_width=.9)
    r.insert(4,card)
    g=r.xpath('//*[@id=$id]',id=id)[0]
    g.remove(g[0])
    band=el('path',d=f'M23 {top} H1515 Q1524 {top} 1524 {top+9} V{top+28} H14 V{top+9} Q14 {top} 23 {top} Z',fill='#0769F9')
    g.insert(0,band)
# Inference flows vertically; the two training explanations share one card.
r.append(el('path',id='inference-panel-divider',d='M30 269 H1508',fill='none',stroke='#CADCF1',stroke_width=.8))
r.append(el('path',id='training-panel-divider',d='M769 688 V1007',fill='none',stroke='#CADCF1',stroke_width=.8))
# The structure and residual meet at the same junction; only purple continues.
for id,path in {
    'q-prefix-tap':'M620 370 V381 H720 V489',
    'q-prefix-tap-clearance':'M620 370 V381 H720 V489',
    'r-prefix-tap':'M654 479 V489 H720',
    'r-prefix-tap-clearance':'M654 479 V489 H720',
    'latent-prefix-history-update-before-label':'M720 489 V505 H643',
    'latent-prefix-history-update-clearance':'M720 489 V505 H643 M547 505 H470 V540',
}.items():
    r.xpath('//*[@id=$id]',id=id)[0].set('d',path)
r.xpath('//*[@id="latent-prefix-merge"]')[0].set('cy','489')
export(r,'overview_framework_h8_v9')
r=E.fromstring(subprocess.check_output(['git','show','9725ca2:figures/foredance/cof-terminology_refined_v1.svg'],cwd=ROOT))
g=r.xpath('//*[@id="same-target-new-residual-origin"]')[0]
formulas=[(r'$z^{*}$',2250,219,38),(r'$e(\hat{q})$',1988,583,38),(r'$e(q^{*})$',2270,583,38),(r'$r^{*}_{\mathrm{rebased}} = z^{*} - e(\hat{q})$',2130,680,36)]
for i,(formula,x,y,size) in enumerate(formulas):
 old=next(e for e in g if e.get('x')==str(x) and e.get('y')==str(y))
 buf=BytesIO();math_to_image(formula,buf,prop=FontProperties(size=size,math_fontfamily='stix'),format='svg',color=old.get('fill'))
 math=E.fromstring(buf.getvalue());w=float(math.get('width')[:-2]);h=float(math.get('height')[:-2])
 # Matplotlib's glyph paths preserve accents and superscripts across PDF viewers.
 math.set('x',str(x-w/2));math.set('y',str(y-h+6));math.set('width',str(w));math.set('height',str(h));math.set('id',f'rebased-math-{i}')
 for e in math.xpath('.//*[@id="patch_1"]'):e.getparent().remove(e)
 # Namespace every generated path ID to keep independent formulas collision-free.
 ids={e.get('id'):f'math{i}-{e.get("id")}' for e in math.iter() if e.get('id')}
 for e in math.iter():
  if e.get('id'):e.set('id',ids[e.get('id')])
  for k,v in list(e.attrib.items()):
   if v.startswith('#') and v[1:] in ids:e.set(k,'#'+ids[v[1:]])
 title=el('title');title.text=formula;math.insert(0,title)
 g.replace(old,math)
export(r,'cof-terminology_refined_v1')
print('Updated both figures')
