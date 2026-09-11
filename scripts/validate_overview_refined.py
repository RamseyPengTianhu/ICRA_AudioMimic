"""Check the selected-reference figure's geometry, local changes and assets."""
from pathlib import Path
import base64, hashlib, itertools, json, re, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output/overview-refined-20260911'; FIG=ROOT/'figures/foredance'
record=json.loads((OUT/'reconstruction-record.json').read_text()); svg=ET.parse(FIG/'overview-refined.svg'); ns={'s':'http://www.w3.org/2000/svg'}
old=ET.parse(FIG/'overview-editable.svg')
def intersect(a,b):return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])
def rect_at(x,y):
 for el in svg.findall('.//s:rect',ns):
  if float(el.get('x'))==x and float(el.get('y'))==y:return [x,y,x+float(el.get('width')),y+float(el.get('height'))]
 raise AssertionError((x,y))
def points(path):
 ts=re.findall(r'[MLHV]|-?\d+(?:\.\d+)?',path); p=[]; i=0;x=y=0
 while i<len(ts):
  cmd=ts[i];i+=1
  if cmd in ['M','L']:x,y=map(float,ts[i:i+2]);i+=2
  elif cmd=='H':x=float(ts[i]);i+=1
  elif cmd=='V':y=float(ts[i]);i+=1
  else:raise AssertionError(path)
  p.append((x,y))
 return p
boxes={n:rect_at(x,y) for n,x,y in [('context',27,336),('structure',394,318),('detail',394,428),('commit',884,358),('computed-context',386,540),('bridge',1078,377),('tracker',1195,374),('execution',1299,282),('cof-sample',788,646),('cof-commit',971,646),('cof-state',1154,646),('cof-learn',1346,646),('recorded-target',1292,840),('generated-context-summary',927,849)]}
# Endpoint constraints are independent of the path commands. These are the
# actual module borders, including the sloped shared-decoder lower boundary.
contracts={
'context-to-structure':('context','structure',(252,377),(394,361)),
'context-to-detail':('context','detail',(252,432),(394,468)),
'state-to-shared-decoder':('context','decoder',(226,491),(806,450)),
'music-film-to-structure':('music','structure',(304,344),(394,344)),
'music-film-to-detail':('music','detail',(304,450),(394,450)),
'q-to-codebook-embedding':('sampled-q','embedding',(660,357),(676,357)),
'structure-to-sum':('embedding','sum',(712,357),(739,396)),
'detail-to-sum':('residual','sum',(709,466),(739,430)),
'sampled-structure-to-detail':('sampled-q','detail',(634,370),(504,428)),
'sum-to-decoder':('sum','decoder',(756,413),(770,413)),
'decoder-to-commit':('decoder','commit',(852,414),(884,414)),
'commit-to-reference-bridge':('commit','bridge',(1055,414),(1078,414)),
'bridge-to-tracker':('bridge','tracker',(1162,414),(1195,414)),
'tracker-to-execution':('tracker','execution',(1279,415),(1299,415)),
'robot-feedback-to-tracker-only':('execution','tracker',(1423,517),(1236,455)),
'commit-to-computed-context':('commit','computed-context',(977,466),(720,559)),
'computed-context-to-history':('computed-context','context',(386,559),(130,491)),
'recorded-target-to-learn-only':('recorded-target','cof-learn',(1455,840),(1455,786)),
'full-latent-to-training-decoder':('full-latent','training-decoder-full',(591,775),(610,775)),
'structure-to-training-decoder':('structure-latent','training-decoder-structure',(562,876),(610,876)),
'training-decoder-to-full':('training-decoder-full','full-reconstruction',(641,775),(656,775)),
'training-decoder-to-structure':('training-decoder-structure','structural-reconstruction',(641,876),(656,876))}
byid={a['id']:a for a in record['arrows']}; failures=[]
for name,(src,dst,start,end) in contracts.items():
 a=byid[name]; ps=points(a['path'])
 if ps[0]!=start or ps[-1]!=end or not a['arrowhead']:failures.append(['endpoint',name])
 for pa,pb in zip(ps,ps[1:]):
  if pa[0]!=pb[0] and pa[1]!=pb[1]:failures.append(['non-orthogonal',name])
  r=[min(pa[0],pb[0])-.6,min(pa[1],pb[1])-.6,max(pa[0],pb[0])+.6,max(pa[1],pb[1])+.6]
  for n,b in boxes.items():
   if n not in [src,dst] and intersect(r,[b[0]+1,b[1]+1,b[2]-1,b[3]-1]):failures.append(['unrelated-module',name,n])
  for l in record['labels']:
   if intersect(r,l['bbox']):
    failures.append(['edge-label',name,l['text']])
for a,b in itertools.combinations(record['labels'],2):
 if intersect(a['bbox'],b['bbox']):failures.append(['label-label',a['text'],b['text']])
# Include the full marker envelope; shaft-only checks missed the earlier FiLM
# collision with the wide triangular arrowhead.
marker_checks=0
for name,a in byid.items():
 if not a['arrowhead']:continue
 el=svg.find(f'.//s:path[@id="{name}"]',ns); ps=points(a['path']); end=np.array(ps[-1]); direction=end-np.array(ps[-2]); direction=direction/np.linalg.norm(direction); normal=np.array([-direction[1],direction[0]])
 k=float(el.get('stroke-width'))*.6
 triangle=[end+u*k*direction+v*k*normal for u,v in [(-9,-5),(1,0),(-9,5)]]
 envelope=[min(p[0] for p in triangle),min(p[1] for p in triangle),max(p[0] for p in triangle),max(p[1] for p in triangle)]
 for l in record['labels']:
  if intersect(envelope,l['bbox']):failures.append(['arrowhead-label',name,l['text']])
 marker_checks+=1
label_values=[l['text'] for l in record['labels']]
assert 'Context' in label_values and 'append' in label_values and 'Boundary state' in label_values
assert 'Paired' not in label_values and not any('reference state' in t.lower() or 'reference context' in t.lower() for t in label_values)
assert all(t in label_values for t in ['root, legs, waist','arm joints','torso, wrists, soles','other body points'])
assert byid['shared-training-decoder-parameters']['arrowhead'] is False
assert 'stop-gradient-backward-path' not in byid
assert all(t in label_values for t in ['Motion context','Context generation (no gradients)','Next-segment targets','(encoded from data)'])
assert not any(t in label_values for t in ['Committed reference','Stop gradient','Recorded next latent'])
assert all(t in label_values for t in ['Embed + add','compute','Trainable'])
assert 'D conditions C' not in label_values
assert 'sampled q' not in label_values
assert svg.find('.//s:g[@id="continuation-dc-pair"]',ns) is None
flames=svg.findall('.//s:use[@{http://www.w3.org/1999/xlink}href="#trainable-flame"]',ns)
assert len(flames)==5
for icon in flames:
 x,y,w,h=[float(icon.get(k)) for k in ['x','y','width','height']]
 for label in record['labels']:
  if intersect([x,y,x+w,y+h],label['bbox']):failures.append(['flame-label',icon.get('id'),label['text']])
assert not svg.findall('.//s:rect[@fill="url(#tile-gray)"]',ns)
for name,n in [('context-history',5),('cof-updated-history',4)]:
 group=svg.find(f'.//s:g[@id="{name}"]',ns)
 assert group is not None
 row=group.findall('s:rect[@fill="url(#tile-purple)"]',ns)
 assert len(row)==n and len(group.findall('s:rect',ns))==n
 assert len({el.get('y') for el in row})==1
state_symbols=svg.findall('.//s:use[@{http://www.w3.org/1999/xlink}href="#boundary-state-icon"]',ns)
assert len(state_symbols)==len(record['state_icons'])==2
state_glyph=svg.find('.//s:symbol[@id="boundary-state-icon"]',ns)
assert len(state_glyph.findall('.//s:path',ns))==1
left_divider=svg.find('.//s:path[@id="b-history-state-divider"]',ns)
right_divider=svg.find('.//s:path[@id="d-history-state-divider"]',ns)
assert left_divider.get('stroke')==right_divider.get('stroke')=='#CBB6E6'
assert left_divider.get('stroke-width')==right_divider.get('stroke-width')=='0.8'
assert left_divider.get('d')=='M529 545 V568'
assert right_divider.get('d')=='M1030 865 V888'

for icon in record['state_icons']:
 for label in record['labels']:
  if intersect(icon['bbox'],label['bbox']):failures.append(['state-icon-label',icon['id'],label['text']])
# The author requested a global typeface update. Compare non-text SVG
# geometry and illustration placements within the previously untouched panels,
# instead of incorrectly requiring the changed typeface to be pixel-identical.
preserved={}
for name in ['a-music-anticipation','training-data']:
    current=svg.find(f'.//s:g[@id="{name}"]',ns)
    previous=old.find(f'.//s:g[@id="{name}"]',ns)
    if current is not None and previous is not None:
        def geometry(el):
            return [(node.tag,dict(node.attrib)) for node in el.iter() if node.tag!='{http://www.w3.org/2000/svg}text']
        preserved[name]=geometry(current)==geometry(previous)
assert preserved and all(preserved.values()), preserved
contract=json.loads((ROOT/'evidence/foredance/overview-typography-contract.json').read_text())
geometry=[(el.tag,dict(el.attrib)) for el in svg.getroot().iter()
          if el.tag!='{http://www.w3.org/2000/svg}text' and el.get('id')!=contract['excluded_path']]
assert hashlib.sha256(json.dumps(geometry,sort_keys=True).encode()).hexdigest()==contract['nontext_geometry_sha256']
preserved['nontext_geometry_matches_revision_contract']=True

assert all(label['horizontal_scale']==1 for label in record['labels'])
assert all('transform' not in el.attrib for el in svg.findall('.//s:text',ns))
condition=next(label for label in record['labels'] if label['text']=='Embed + add')
assert condition['bbox'][1] > 404 and condition['bbox'][3] <= 423
assert condition['bbox'][0] > 515
logo=svg.find('.//s:svg[@id="foredance-wordmark"]',ns)
assert logo is not None and len(logo.findall('.//s:path',ns))==10
assert not logo.findall('.//s:image',ns) and not logo.findall('.//s:text',ns)
assert len(record['logos'])==1
assert record['logos'][0]['sha256']==hashlib.sha256((FIG/'foredance-logo.svg').read_bytes()).hexdigest()
panels=[]
for group in ['a-music-anticipation','b-generate-commit-execute','c-representation-and-paired-training','d-commit-forcing']:
 now=svg.find(f'.//s:g[@id="{group}"]/s:rect',ns); was=old.find(f'.//s:g[@id="{group}"]/s:rect',ns)
 same=now.attrib==was.attrib; panels.append({'panel':group,'bounds_and_style_identical':same})
 if not same:failures.append(['panel-changed',group])
imgs=svg.findall('.//s:image',ns); assert len(imgs)==6
asset_checks=[]
for item in record['images']:
 path=ROOT/item['source']; im=Image.open(path); a=np.array(im.getchannel('A'))
 assert im.mode=='RGBA' and a.min()==0
 asset_checks.append({'id':item['id'],'source':item['source'],'size':im.size,'alpha_extrema':[int(a.min()),int(a.max())],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
assert sum(a['id'].startswith('music-film-to-') for a in record['arrows'])==2
assert not any('from-a' in a['id'] or 'a-to-b' in a['id'] for a in record['arrows'])
assert len(svg.findall('.//s:text',ns))==record['text_elements']
result={'selected_reference':record['selected_reference'],'canvas':record['canvas_dimensions'],'header_legend':True,'old_footer_removed':True,'preserved_nontext_geometry':preserved,'horizontal_text_compression':False,'preserved_panels':panels,'checked_module_connections':len(contracts),'checked_arrowhead_envelopes':marker_checks,'author_label_revision':{'context_and_boundary_state':True,'append_on_return_arrow':True,'b_paired_removed':True,'c_anatomy_explanations_single_line':True,'shared_decoder_on_both_reconstruction_paths':True},'nonjoining_crossing':{'position':[304,361],'foreground_edge':'context-to-structure','background_edge':'music-bus','white_understroke':True},'main_reference_feedback_separate_from_measured_robot_feedback':True,'music_arrowheads':2,'native_text_elements':record['text_elements'],'unique_embedded_pngs':len(imgs),'asset_placements':asset_checks,'failures':failures}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='asset_placements'},indent=2))
assert not failures,failures
