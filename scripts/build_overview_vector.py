"""Rebuild overview diagram as editable SVG and print PDF; retain original robot artwork.
Requires Pillow and CairoSVG. The source PNG is immutable.
"""
from pathlib import Path
import base64, io, html, math
from PIL import Image
import cairosvg
import cairocffi as cairo
measure=cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32,1,1))
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'figures/foredance'
source=Image.open(DEST/'overview.png').convert('RGB')
W,H=source.size
assert (W,H)==(1685,934)
blue='#0863ff'; orange='#ff8907'; teal='#008c99'; purple='#8514ed'; navy='#080e48'; ink='#0a0c20'
s=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1685" height="934" viewBox="0 0 1685 934">', '<title>ForeDance overview</title>', '<desc>Editable vector reconstruction of the original overview. Three embedded crops retain original schematic robot artwork, with an official Magenta RealTime 2 application icon; all diagram labels, connections, and blocks are vector elements.</desc>', '<defs>']
for name,color in [('blue',blue),('orange',orange),('teal',teal),('purple',purple),('black','#333333')]:
 s.append(f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="{color}"/></marker>')
 pale='#'+''.join(f'{round(255*.94+int(color[i:i+2],16)*.06):02x}' for i in (1,3,5))
 s.append(f'<linearGradient id="{name}-fade" x2="0%" y2="100%"><stop stop-color="white"/><stop offset="1" stop-color="{pale}"/></linearGradient>')
 s.append(f'<linearGradient id="{name}-token" x2="1" y2="1"><stop stop-color="{color}" stop-opacity="0.38"/><stop offset="0.55" stop-color="{color}" stop-opacity="0.76"/><stop offset="1" stop-color="{color}" stop-opacity="0.4"/></linearGradient>')
s+=['</defs>','<rect width="1685" height="934" fill="white"/>']
def rect(x,y,w,h,fill='white',stroke='none',r=6,sw=1.3,dash=None):
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def path(d,color='#333333',sw=2,arrow=None,dash=None):
 s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"'+(f' marker-end="url(#arrow-{arrow})"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def text(x,y,value,size=20,color=ink,weight='normal',anchor='start',width=None,italic=False):
 attrs=f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"'
 if italic: attrs=f'font-family="Times New Roman, serif" font-style="italic" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
 measure.select_font_face('Times New Roman' if italic else 'Arial', cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if weight=='bold' else cairo.FONT_WEIGHT_NORMAL)
 measure.set_font_size(size)
 natural=measure.text_extents(value)[4]
 scale=width/natural if width and natural else (1 if italic or size>=35 else .92)
 attrs+=f' transform="translate({x} 0) scale({scale} 1) translate({-x} 0)"'
 s.append(f'<text x="{x}" y="{y}" {attrs}>{html.escape(value)}</text>')
def lines(x,y,values,size=20,color=ink,weight='normal',anchor='middle',gap=23,width=None):
 for i,v in enumerate(values): text(x,y+i*gap,v,size,color,weight,anchor,width)
def circle(x,y,r,fill,stroke='none'):
 s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
def tokens(x,y,n=6,color='blue',w=13,h=27,gap=5):
 for i in range(n): rect(x+i*(w+gap),y,w,h,f'url(#{color}-token)',r=3,sw=0)
def dots(x,y,color):
 for dx in [0,11,22]: circle(x+dx,y,1.8,color)
def crop(box):
 im=source.crop(box); b=io.BytesIO(); im.save(b,format='PNG'); x,y,x1,y1=box
 s.append(f'<image x="{x}" y="{y}" width="{x1-x}" height="{y1-y}" xlink:href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
def panel(letter,y,title):
 circle(43,y-10,21,'url(#blue-fade)','#a6bbed'); text(43,y+2,letter,35,ink,'bold','middle'); text(83,y,title,27,ink,'bold',width=350 if letter=='b' else None)
# Header and panel a.
text(23,43,'ForeDance',44,ink,'bold'); path('M261 11 V44','#6475ad',1.5)
text(280,36,'Anticipatory music conditioning for streaming dance generation',23,navy)
panel('a',92,'Anticipate from heard music')
text(83,124,'Heard audio',20,teal,'bold')
for y in [146,155,165,174,184]: path(f'M23 {y} H1664','#d6eef5',1)
# Trace the actual waveform column extents, preserving timing and envelope.
for x in range(77,541):
 ys=[y for y in range(127,199) if (lambda c:c[0]<125 and c[1]>100 and c[2]>115 and c[1]-c[0]>35)(source.getpixel((x,y)))]
 if ys: path(f'M{x} {min(ys)} V{max(ys)}',teal,0.8)
# Treble clef retained as smooth vector strokes.
path('M48 135 C30 160 28 179 45 180 C65 179 61 161 48 161 C33 161 34 185 49 187 C66 191 48 205 43 195 M48 188 L47 139 C47 120 63 139 43 158', '#8fcbd9',2.5)
dots(557,167,teal); path('M610 109 V213','#625eea',1.5,dash='7 6'); text(613,102,'Now',18,navy,anchor='middle')
path('M619 167 H691',teal,2.3,'teal')
rect(701,123,197,88,'url(#blue-fade)','#235883',7,1.5)
icon_data=base64.b64encode((DEST/'mrt2-official-app-icon.png').read_bytes()).decode()
s.append(f'<image x="710" y="136" width="42" height="42" xlink:href="data:image/png;base64,{icon_data}"/>')
lines(822,149,['Magenta','RealTime 2'],20,navy,'bold',gap=22)
# Six radial arms with outward-facing branches: a snowflake, not a star.
for angle in range(0,360,60):
 a=math.radians(angle-90); dx,dy=math.cos(a),math.sin(a)
 cx,cy=799,193
 path(f'M{cx} {cy} l{11*dx} {11*dy}',blue,1.6)
 for side in [-1,1]:
  ex,ey=cx+6*dx,cy+6*dy
  vx,vy=4*dx-side*3*dy,4*dy+side*3*dx
  path(f'M{ex} {ey} l{vx} {vy}',blue,1.4)

path('M898 167 H993',teal,2.3,'teal'); text(1000,115,'Predicted music states',21,teal,'bold')
for i,x in enumerate([1000,1113,1225,1335,1442]):
 rect(x,128,101,66,'url(#teal-fade)',teal,6,1.2,'6 4')
 # Match each source tile's distinct bar colors, retaining editable gradients.
 for j in range(4):
  bx=x+14+j*20
  stops=[]
  for offset,sy in [('0%',148),('50%',161),('100%',175)]:
   pixels=[source.getpixel((px,py)) for px in range(bx+4,bx+9) for py in range(sy-2,sy+3)]
   color='#'+''.join(f'{round(sum(p[k] for p in pixels)/len(pixels)):02x}' for k in range(3))
   stops.append(f'<stop offset="{offset}" stop-color="{color}"/>')
  gid=f'music-state-{i}-{j}'
  s.append(f'<defs><linearGradient id="{gid}" x2="0%" y2="100%">'+''.join(stops)+'</linearGradient></defs>')
  rect(bx,144,14,36,f'url(#{gid})',r=3,sw=0)
 if i<4:
  text(x+45,216,'u',23,navy,anchor='middle',italic=True)
  text(x+52,221,str(i+1),14,navy)
dots(1572,167,teal)
path('M23 232 H1664','#9aace2',1.5)
# Main streaming flow.
panel('b',270,'Generate, commit, continue')
text(578,280,'Predicted music states',20,teal,'bold',anchor='middle')
for j in range(4): rect(551+j*13,290,9,17,f'url(#music-state-0-{j})',r=2)
path('M362 350 V282 H469 V318',teal,2.2,'teal')
path('M362 357 V438 H390',teal,2.2,'teal')
rect(53,375,237,85,'url(#black-fade)','#555555',6,1.5)
lines(172,415,['Committed history','+ reference state'],20,ink,'bold')

path('M290 401 H324 V352 H391','#333333',2.2,'black')
path('M290 440 H324 V458 H391','#333333',2.2,'black')
rect(393,324,172,68,'url(#blue-fade)',blue)
rect(393,418,172,67,'url(#orange-fade)',orange)
lines(455,353,['Structure','planner'],20,blue,'bold',anchor='start')
lines(455,449,['Detail','generator'],20,ink,'bold',anchor='start')
for i,hh in enumerate([13,23,33]): rect(411+i*10,375-hh,7,hh,f'url(#blue-token)',blue,0,.5)
path('M407 455 C413 442 412 470 418 449 S422 437 425 459 S428 464 431 455 S437 461 442 453',orange,3)
path('M490 392 V416',blue,1.7,'blue');path('M566 357 H590',blue)
tokens(597,346);dots(714,357,blue);text(669,337,'e(q)',25,blue,anchor='middle',italic=True)
path('M745 354 H771 V394',blue,2,'blue')
path('M566 457 H590',orange);tokens(597,445,6,'orange');dots(714,458,orange);text(668,438,'r',25,orange,anchor='middle',italic=True)
path('M745 460 H771 V437',orange,2,'orange')
circle(771,416,20,'white','#444444');text(771,428,'+',36,'#333333',anchor='middle')
path('M791 418 H839','#333333',2.2,'black')
rect(841,375,150,84,'url(#purple-fade)','#6230a0')
lines(941,414,['Shared','decoder'],20,ink,'bold')
s.append('<path d="M862 410 L887 398 V436 L862 425 Z" fill="url(#purple-token)" stroke="#704198" stroke-width="1.2"/>');path('M871 405 V429','#ffffff',1.5)
path('M1000 287 H913 V365',purple,2.2,'purple');text(1009,294,'Reference state',19,purple,'bold',width=120)
circle(1150,287,2,purple);path('M1150 287 V276 M1150 287 L1160 292 M1150 287 L1142 296',purple,1.5)
path('M991 418 H1035','#333333',2.2,'black');rect(1038,375,165,83,'url(#purple-fade)',purple)
lines(1146,414,['Commit','prefix'],20,purple,'bold')
# A retained prefix plus a faded future suffix, replacing the storage cylinder.
for j in range(4):
 rect(1049+j*12,402,9,20,purple if j<2 else '#eee1fa',purple if j<2 else '#c3a5dd',2,1)
path('M1072 397 V426',purple,1.2,dash='3 2')
path('M1052 431 l4 4 l9 -9',purple,2.5)
path('M1203 418 H1234',purple,2,'purple')
text(1267,315,'Streaming reference motion',21,purple,'bold')
crop((1240,323,1657,518))
# Time and feedback.
path('M1267 527 H1584',purple,1.7);text(1591,533,'time t',16,purple);path('M1635 527 H1663',purple,1.6,'purple')
path('M1119 459 V528 H107 V462',purple,2.2,'purple')
# Paired history/state travels on the feedback loop.
rect(658,510,142,36,'white',purple,7)
tokens(671,519,3,'purple',9,17,4)
path('M717 528 H738',purple,1.5)
circle(749,528,2,purple)
path('M749 528 V520 M749 528 L757 531 M749 528 L743 535',purple,1.5)
path('M23 557 H1664','#9aace2',1.5)
# Training panels.
rect(23,572,922,291,'#edf7ff',r=13);rect(968,572,697,291,'#f5f1ff',r=13)
circle(43,589,21,'white','#a6bbed');text(43,602,'c',35,ink,'bold','middle')
text(94,596,'Discrete Structure + Continuous Detail',25,ink,'bold')
text(94,614,'Kinematics-guided training',16,navy)
rect(36,618,585,232,'#e2f1fd',r=10)
text(52,641,'Joint view',20,navy,'bold');text(323,641,'Geometry view',20,navy,'bold')
crop((40,646,149,843));crop((300,646,424,843));path('M291 634 V829','#8aa8cf',1)
for xx in [165,452]:
 circle(xx,681,12,'url(#blue-token)',blue);circle(xx,732,12,'url(#orange-token)',orange)
text(187,683,'Structure:',14,blue,'bold');text(187,702,'root, legs, waist',14,navy)
text(187,735,'Detail:',14,blue,'bold');text(187,754,'arm joints',14,navy)
text(475,683,'Structure:',14,blue,'bold');text(475,702,'torso, wrists, soles',14,navy)
text(475,735,'Detail:',14,blue,'bold');text(475,754,'remaining body points',14,navy)
for y in [642,729]: rect(633,y,295,72 if y==642 else 68,'url(#blue-fade)','#5e97ff')
text(652,690,'e(q)',31,blue,italic=True);text(707,690,'+',29,navy);text(733,690,'r',31,orange,italic=True);path('M758 681 H785',navy,1.8,'black')
lines(797,675,['Full-view','reconstruction'],18,navy,anchor='start',gap=21)
text(657,773,'e(q)',31,blue,italic=True);path('M735 764 H785',navy,1.8,'black');lines(797,757,['Structural-view','reconstruction'],18,navy,anchor='start',gap=21)
# Identical decoder glyphs and a shared parameter link replace the prose note.
for yy in [681,764]:
 rect(751,yy-13,39,25,'#f6f0ff',r=0)
 s.append(f'<path d="M757 {yy-7} L777 {yy-13} V{yy+13} L757 {yy+7} Z" fill="url(#purple-token)" stroke="#704198"/>')
 path(f'M764 {yy-9} V{yy+9}','white',1.3)
 path(f'M778 {yy} H792',navy,1.2,'black')
path('M768 695 V750',purple,1.2,dash='3 3')
# Commit Forcing sequence.
text(993,609,'Commit Forcing',25,ink,'bold')
for x,w,label in [(980,162,['Sample']),(1158,158,['Commit']),(1331,162,['Reconstruct','state']),(1510,143,['Train','next plan'])]:
 rect(x,627,w,106,'url(#purple-fade)','#a0aee5')
 lines(x+w/2,660 if len(label)==1 else 653,label,20,navy,'bold',gap=21)
for i in range(6): tokens(996+i*18,684,1,'orange' if i in [2,5] else 'blue',13,30)
dots(1112,700,navy);path('M1141 698 H1167',purple,2,'purple')
tokens(1192,687,4,'purple',13,25,4);path('M1187 682 Q1181 682 1181 690 V708 Q1181 715 1187 715',purple,1);path('M1259 682 Q1266 682 1266 690 V708 Q1266 715 1259 715',purple,1)
dots(1277,700,purple);path('M1309 698 H1340',purple,2,'purple')
for i in range(6): tokens(1352+i*17,687,1,'orange' if i in [2,5] else 'blue',13,27)
dots(1460,700,navy);path('M1491 698 H1516',purple,2,'purple')
for i,c in enumerate(['blue','orange','blue','orange','orange']): tokens(1531+i*18,687,1,c,13,27)
dots(1623,700,navy)
path('M989 737 V750 Q989 753 993 753 H1479 Q1483 753 1483 749 V737',purple,1.2)
# Backward gradient path stops at a double barrier before generated context.
path('M1548 738 V755 H1500',purple,1.4,'purple',dash='4 3')
path('M1490 745 V765 M1495 745 V765',purple,2)
rect(1512,778,138,51,'url(#blue-fade)','#008fbd',4)
text(1581,811,'Recorded target',16,'#005786',anchor='middle')
path('M1580 778 V735','#08799d',2,'teal')
# One enclosure carries committed history and reconstructed boundary state.
rect(1341,680,140,43,'white',purple,5)
tokens(1351,690,3,'purple',11,22,4)
path('M1400 701 H1420',purple,1.5)
circle(1440,701,2,purple)
path('M1440 701 V690 M1440 701 L1450 706 M1440 701 L1432 710',purple,1.5)
# Legend.
rect(580,878,525,44,'white','#b4bfe8',6)
for x,c,label in [(619,'blue','Structure'),(743,'orange','Detail'),(848,'teal','Music'),(955,'purple','Commit / state')]:
 circle(x,900,12,f'url(#{c}-token)',{'blue':blue,'orange':orange,'teal':teal,'purple':purple}[c]);text(x+26,906,label,14,navy)

s.append('</svg>')
svg='\n'.join(s)
(DEST/'overview.svg').write_text(svg)
class PaperPDFSurface(cairosvg.surface.PDFSurface):
 def _create_surface(self, width, height):
  surface, width, height = super()._create_surface(width, height)
  surface.restrict_to_version(cairo.PDF_VERSION_1_5)
  return surface, width, height
PaperPDFSurface.convert(bytestring=svg.encode(),write_to=str(DEST/'overview.pdf'))
preview=ROOT/'tmp/overview-vector';preview.mkdir(parents=True,exist_ok=True)
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(preview/'overview.png'))
print('Wrote overview.svg, overview.pdf and preview')
