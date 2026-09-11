"""Native-vector ForeDance candidate and terminology-aligned detail figures.
All artwork uses SVG paths/shapes/text. No bitmap tracing or embedded images.
"""
from pathlib import Path
import math, html, json
import cairosvg
import cairocffi as cairo
R=Path(__file__).resolve().parents[1]; D=R/'figures/foredance'; OUT=R/'output/figure-review-20260911'; OUT.mkdir(parents=True,exist_ok=True)
C={'blue':'#2678D8','orange':'#E79529','teal':'#008F98','purple':'#8053BE','gray':'#687586','ink':'#17243D'}
PALE={'blue':'#F0F6FE','orange':'#FFF5E7','teal':'#EFFAFA','purple':'#F6F1FC','gray':'#F5F6F8'}
class Fig:
 def __init__(self,w,h,title):
  self.w=w;self.h=h;self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{html.escape(title)}</title><desc>Native editable vector diagram. Robot poses and time ranges are schematic.</desc><defs>'];self.labels=[]
  for key,col in C.items():
   self.s.append(f'<marker id="a-{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{col}"/></marker>')
   self.s.append(f'<linearGradient id="g-{key}" x1="0" x2="1"><stop stop-color="{col}"/><stop offset=".38" stop-color="{PALE.get(key,"#DDD")}"/><stop offset=".62" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity=".75"/></linearGradient>')
  self.s.append('<linearGradient id="metal" x1="0" x2="1"><stop stop-color="#77818B"/><stop offset=".3" stop-color="#FCFEFF"/><stop offset=".55" stop-color="#D4DBE0"/><stop offset="1" stop-color="#7E8992"/></linearGradient><linearGradient id="black" x1="0" x2="1"><stop stop-color="#101A23"/><stop offset=".45" stop-color="#53616A"/><stop offset="1" stop-color="#111A24"/></linearGradient></defs>')
  self.rect(0,0,w,h,'white')
 def rect(self,x,y,w,h,fill='white',stroke='none',r=8,sw=1.3,dash=None):
  self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{C.get(stroke,stroke)}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def line(self,d,col='ink',sw=2,arr=False,dash=None):
  self.s.append(f'<path d="{d}" fill="none" stroke="{C.get(col,col)}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'+(f' marker-end="url(#a-{col})"' if arr else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def shape(self,d,fill,stroke='#34424F',sw=1):self.s.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
 def text(self,x,y,t,size=22,col='ink',bold=False,anchor='start'):
  self.labels.append(t);self.s.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{C.get(col,col)}" text-anchor="{anchor}">{html.escape(t)}</text>')
 def lines(self,x,y,ts,size=22,col='ink',bold=False,anchor='middle',gap=27):
  for i,t in enumerate(ts):self.text(x,y+i*gap,t,size,col,bold,anchor)
 def dot(self,x,y,r,fill,stroke='none',sw=1):self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" stroke-width="{sw}"/>')
 def box(self,x,y,w,h,ts,col='gray',size=22):
  self.rect(x,y,w,h,PALE[col],col);self.lines(x+w/2,y+h/2-((len(ts)-1)*26)/2+7,ts,size,col,True)
 def panel(self,x,y,w,h,letter,title,col):
  self.rect(x,y,w,h,PALE[col],f'{C[col]}',12,1);self.dot(x+28,y+30,20,'white',col);self.text(x+28,y+38,letter,27,col,True,'middle');self.text(x+61,y+39,title,27,'ink',True)
 def tokens(self,x,y,n=4,col='blue',w=19,h=26,gap=5,fade=0):
  for i in range(n):self.rect(x+i*(w+gap),y,w,h,PALE.get(col,'#eee') if fade and i>=fade else C[col],col,3,1)
 def snow(self,x,y,r=11):
  for deg in range(0,360,60):
   a=math.radians(deg);dx,dy=math.cos(a),math.sin(a)
   self.line(f'M{x} {y} l{r*dx} {r*dy}','blue',1.6)
   for side in [-1,1]:self.line(f'M{x+dx*r*.55} {y+dy*r*.55} l{r*(.35*dx-side*.25*dy)} {r*(.35*dy+side*.25*dx)}','blue',1.4)
 def wave(self,x,y,w,h,col='teal'):
  for i in range(0,int(w),3):
   env=(math.sin(i/w*math.pi)**.65)*(.25+.75*abs(math.sin(i*.041)))
   a=h*env*(.2+.8*abs(math.sin(i*.731)))
   self.line(f'M{x+i} {y-a} V{y+a}',col,1.2)
 def robot(self,x,y,scale=1,view='neutral',pose=0):
  self.s.append(f'<g transform="translate({x} {y}) scale({scale})">')
  self.s.append('<ellipse cx="0" cy="241" rx="45" ry="4" fill="#C5CDD8" opacity=".35"/>')
  fill=lambda kind: 'url(#g-'+('blue' if kind=='structure' else 'orange')+')' if view=='joint' else 'url(#metal)'
  def joint(px,py,r=8):
   self.dot(px,py,r,'url(#black)','#1D2933',.8);self.dot(px,py,r*.6,'#74808B');self.dot(px,py,r*.31,'#202B35');self.line(f'M{px-r*.32} {py} h{r*.64}','#CBD3D8',.7)
  def bone(p,q,width,kind):
   dx=q[0]-p[0];dy=q[1]-p[1];ln=math.hypot(dx,dy);ang=-math.degrees(math.atan2(dx,dy))
   self.s.append(f'<g transform="translate({p[0]} {p[1]}) rotate({ang})">')
   self.rect(-width*.35,0,width*.7,ln,'url(#black)',r=3)
   self.shape(f'M{-width*.5} 7 Q0 2 {width*.5} 7 L{width*.37} {ln-9} Q0 {ln-3} {-width*.37} {ln-9} Z',fill(kind),'#4A5967',.8)
   self.line(f'M{-width*.25} 12 L{-width*.20} {ln-14}','#FFFFFF',1.1)
   self.line(f'M{width*.28} 13 L{width*.20} {ln-15}','#3B4B5A',.7)
   self.s.append('</g>');joint(*p,max(width*.39,5));joint(*q,max(width*.33,4))
  hips=[(-17,139),(17,139)]; knees=[(-21,185),(23,185)];ankles=[(-24,226),(26,226)]
  if pose==1:knees=[(-29,182),(37,170)];ankles=[(-34,226),(24,206)]
  if pose==2:knees=[(-15,180),(44,184)];ankles=[(-25,226),(62,212)]
  for hp,kp,ap in zip(hips,knees,ankles):
   bone(hp,kp,22,'structure');bone(kp,ap,17,'structure');self.shape(f'M{ap[0]-9} {ap[1]-2} L{ap[0]+8} {ap[1]-2} L{ap[0]+13} {ap[1]+11} Q{ap[0]} {ap[1]+16} {ap[0]-13} {ap[1]+12} Z',fill('structure'));self.line(f'M{ap[0]-12} {ap[1]+12} h24','#223341',2)
  self.shape('M-24 121 Q0 114 24 121 L25 145 L11 153 L3 139 L-3 139 L-11 153 L-25 145 Z',fill('structure'))
  self.rect(-20,113,40,10,'url(#black)',r=4)
  self.shape('M-25 60 Q0 52 25 60 L29 76 L18 110 Q0 119 -18 110 L-29 76 Z',fill('structure'))
  self.shape('M-18 66 Q0 61 18 66 L14 87 Q0 94 -14 87 Z',fill('structure'),'#8595A2',.65)
  self.line('M-15 100 Q0 106 15 100','#788792',.8)
  for xx in [-19,19]:
   for yy in [69,104]:self.dot(xx,yy,1.3,'#334856')
  self.rect(-7,43,14,15,'url(#black)',r=3)
  self.shape('M-12 15 Q0 8 12 15 L15 35 Q10 48 0 50 Q-10 47 -14 36 Z','url(#metal)')
  self.shape('M-10 22 Q0 17 10 22 L10 35 Q0 43 -10 35 Z','url(#black)','#203A46')
  self.line('M-6 24 Q0 21 6 24','#33A6B7',1.5);self.dot(4,31,1.1,'#77D0D4')
  shoulders=[(-30,67),(30,67)];elbows=[(-43,99),(43,99)];wrists=[(-53,132),(53,132)]
  if pose==1:elbows=[(-49,89),(53,60)];wrists=[(-39,120),(65,29)]
  if pose==2:elbows=[(-57,77),(52,86)];wrists=[(-70,47),(81,76)]
  for sh,el,wr in zip(shoulders,elbows,wrists):
   bone(sh,el,14,'detail');bone(el,wr,11,'detail');self.rect(wr[0]-4,wr[1]+1,8,11,'url(#black)',r=2)
   for j in range(3):self.line(f'M{wr[0]-3+j*3} {wr[1]+9} v7 l2 2','#34424D',1.7)
   self.line(f'M{wr[0]-4} {wr[1]+3} l-4 5 l2 4','#34424D',2)
  if view=='geometry':
   # Exactly five structural sites; remaining markers illustrate the complementary view.
   for px,py in [(0,85),*wrists,(-24,239),(26,239)]:self.dot(px,py,5.2,'blue','white',1)
   other=[(-30,67),(30,67),(-43,99),(43,99),(-17,139),(17,139),(-21,185),(23,185),(-24,222),(26,222),(-20,116),(20,116),(-8,45),(8,45),(-23,78),(23,78),(-28,159),(28,159),(-19,170),(21,170),(-50,116),(50,116),(-53,147),(53,147),(-29,230),(31,230)]
   for px,py in other:self.dot(px,py,3.1,'orange','white',.65)
  self.s.append('</g>')
 def human(self,x,y,scale=.3):
  self.s.append(f'<g transform="translate({x} {y}) scale({scale})">');self.dot(0,17,11,'url(#metal)','#84929C')
  self.shape('M-12 32 Q0 28 12 32 L19 72 L11 91 L-11 91 L-19 72 Z','url(#metal)')
  for d in ['M-12 41 L-26 74 L-33 100','M12 41 L27 67 L36 89','M-8 89 L-15 129 L-23 168','M8 89 L20 122 L25 167']:self.line(d,'#657581',11);self.line(d,'#C9D2D9',7)
  self.s.append('</g>')
 def save(self,name,dest=D):
  content='\n'.join(self.s+['</svg>']);assert '<image' not in content and 'base64' not in content
  assert not any('prefix' in t.lower() or 'd+c' in t.lower() for t in self.labels)
  (dest/(name+'.svg')).write_text(content)
  class PDF(cairosvg.surface.PDFSurface):
   def _create_surface(self,w,h):
    a,w,h=super()._create_surface(w,h);a.restrict_to_version(cairo.PDF_VERSION_1_5);return a,w,h
  PDF.convert(bytestring=content.encode(),write_to=str(dest/(name+'.pdf')))
  cairosvg.svg2png(bytestring=content.encode(),write_to=str(OUT/(name+'.png')))
  return content

def views(f,y,x=40,w=810):
 for xx,label,view in [(x,'Joint view','joint'),(x+w/2,'Geometry view','geometry')]:
  f.rect(xx,y,w/2-12,246,'white','#CBDCED');f.text(xx+18,y+29,label,22,'blue',True);f.robot(xx+77,y+38,.81,view)
  tx=xx+146
  f.text(tx,y+79,'Structure',20,'blue',True);f.lines(tx,y+105,['root, legs, waist'] if view=='joint' else ['torso, wrists,','sole points'],19,anchor='start',gap=24)
  f.text(tx,y+165,'Detail',20,'orange',True);f.lines(tx,y+190,['arm joints'] if view=='joint' else ['remaining','body points'],19,anchor='start',gap=24)

def overview():
 f=Fig(1800,1180,'ForeDance: anticipatory music conditioning for streaming dance generation')
 f.text(22,48,'ForeDance',46,bold=True);f.line('M280 16 V51','#97A8BD',1.5);f.text(303,44,'Anticipatory music conditioning for streaming dance generation',29)
 f.panel(20,72,1760,198,'a','Anticipate from heard music','teal')
 f.text(60,145,'Heard audio',22,'teal',True);f.wave(60,195,340,35);f.line('M421 145 V245','purple',1.4,False,'5 5');f.text(421,135,'Now',20,'purple',True,'middle')
 f.line('M432 195 H487','teal',2.3,True);f.box(490,144,180,101,['MRT-2','music forecaster'],'gray',20);f.snow(651,158,9)
 f.line('M670 195 H729','teal',2.3,True)
 f.text(754,143,'Predicted music states',23,'teal',True)
 for i in range(5):
  f.rect(753+i*115,162,98,65,'white','teal',7,1,'5 3');f.tokens(765+i*115,178,4,'teal',14,29,7)
 f.line('M753 244 H1310','teal',1.3,True);f.text(1030,263,'Forecast time (schematic)',18,'teal',False,'middle')
 f.line('M1330 195 H1421','teal',2,True);f.dot(1450,194,19,'white','teal');f.text(1450,202,'b',24,'teal',True,'middle');f.lines(1600,181,['Conditions both','generation branches'],22,'teal',True)
 f.panel(20,287,1760,362,'b','Generate, commit, and execute','blue')
 # contexts
 f.box(43,418,243,106,['Committed history','+ reference state'],'purple',22)
 f.line('M286 447 H312 V401 H439','ink',1.9,True);f.line('M286 492 H312 V510 H439','ink',1.9,True)
 f.dot(361,352,15,'white','teal');f.text(361,358,'a',21,'teal',True,'middle');f.text(386,359,'Music forecast',20,'teal',True)
 f.line('M361 369 V381','teal',2,True);f.line('M328 352 H336 V490 H345','teal',2,True)
 f.line('M346 352 H328','teal',2)
 for yy in [382,491]:f.box(345,yy,76,39,['FiLM'],'teal',20);f.line(f'M421 {yy+19} H439','teal',2,True)
 f.box(440,373,194,67,['Structure planner','AR Transformer'],'blue',20)
 f.box(440,483,194,67,['Detail generator','Residual diffusion'],'orange',20)
 f.line('M634 404 H658','blue',2,True);f.tokens(667,392,4,'blue',21,27,5);f.text(715,379,'e(q)',24,'blue',True,'middle')
 f.line('M715 421 V461 H540 V482','blue',2,True);f.text(652,450,'sampled structure',17,'blue',False,'middle')
 f.line('M634 516 H658','orange',2,True);f.tokens(667,503,4,'orange',21,27,5);f.text(717,553,'r',24,'orange',True,'middle')
 f.line('M773 405 H824 V443','blue',2,True);f.line('M773 516 H824 V483','orange',2,True);f.dot(824,463,19,'white','ink');f.text(824,472,'+',31,'ink',False,'middle')
 f.line('M844 463 H866','ink',2,True);f.box(869,423,139,80,['Shared','decoder'],'purple',22)
 f.line('M286 519 H301 V568 H940 V504','purple',1.6,True);f.text(580,590,'Reference state from committed motion',19,'purple',False,'middle')
 # segment commits, represented as motion path rather than latent blocks
 f.line('M1008 463 H1034','purple',2,True);f.rect(1037,379,268,161,'white','purple');f.text(1171,408,'Commit segment',23,'purple',True,'middle')
 f.text(1171,434,'Planned reference motion',18,'purple',False,'middle')
 f.rect(1053,445,110,48,PALE['purple'],r=0);f.line('M1163 443 V496','purple',1,False,'3 3')
 f.line('M1055 476 C1075 449 1094 491 1116 467 S1144 448 1163 469','purple',2.3)
 f.line('M1163 469 C1187 497 1205 451 1221 466 S1252 492 1286 459','purple',1.6,False,'4 4')
 f.text(1107,518,'Committed',18,'purple',True,'middle');f.text(1230,518,'Revisable',18,'gray',False,'middle')
 # joint commit selection fixes both codes and decoded motion, separate updates
 f.line('M1170 540 V612 H164 V526','purple',2,True);f.rect(456,597,493,28,PALE['blue']);f.text(703,618,'Selected codes → history; decoded motion → state',18,'purple',False,'middle')
 f.text(1288,568,'time ranges schematic',16,'gray',False,'end')
 # execution quarter
 f.line('M1305 463 H1323','purple',2,True);f.box(1326,426,113,74,['Reference','bridge'],'gray',20)
 f.line('M1439 463 H1458','gray',2,True);f.box(1461,426,123,74,['SONIC','tracker'],'gray',21);f.snow(1569,436,7)
 f.line('M1584 463 H1600','gray',2,True);f.text(1680,367,'G1 execution',21,'gray',True,'middle');f.robot(1638,374,.63,'neutral',1);f.robot(1720,374,.63,'neutral',2)
 f.line('M1720 535 V581 H1521 V502','gray',1.8,True);f.text(1630,605,'Measured robot state',18,'gray',False,'middle');f.text(1685,628,'Robot poses schematic',16,'gray',False,'middle')
 # training c
 f.panel(20,667,870,442,'c','Structure–Detail Representation','blue')
 f.text(83,733,'Paired training with kinematic supervision',21,'blue')
 f.rect(40,751,245,76,'white','#D1DCEA');f.human(64,757,.34);f.text(103,779,'FineDance',21,bold=True);f.text(103,806,'Human dance data',18)
 f.line('M286 789 H306','ink',1.6,True);f.box(308,751,213,76,['Motion retargeting','Offline preprocessing'],'gray',18)
 f.line('M522 789 H546','ink',1.6,True);f.rect(549,751,321,76,'white','#D1DCEA');f.robot(577,755,.285);f.text(612,780,'G1 training motion',21,bold=True);f.text(612,806,'(Unitree G1)',18)
 # compact supervision views and paired reconstruction (same original horizontal order)
 for xx,title,view in [(40,'Joint view','joint'),(316,'Geometry view','geometry')]:
  f.rect(xx,842,263,205,'white','#D1DCEA');f.text(xx+14,870,title,22,'blue',True);f.robot(xx+52,878,.64,view)
  f.text(xx+108,902,'Structure',18,'blue',True);f.lines(xx+108,927,['root, legs,','waist'] if view=='joint' else ['torso, wrists,','soles'],17,anchor='start',gap=21)
  f.text(xx+108,982,'Detail',18,'orange',True);f.lines(xx+108,1005,['arm joints'] if view=='joint' else ['remaining','body points'],17,anchor='start',gap=20)
 f.rect(592,842,278,96,'white','blue');f.text(609,872,'e(q) + r',23,'blue',True);f.line('M711 867 H743','blue',1.5,True);f.box(747,850,105,36,['D(·, b)'],'purple',18);f.lines(610,903,['Full-motion reconstruction'],18,anchor='start')
 f.rect(592,951,278,96,'white','blue');f.text(609,981,'e(q)',23,'blue',True);f.line('M685 976 H743','blue',1.5,True);f.box(747,959,105,36,['D(·, b)'],'purple',18);f.text(610,1014,'Structural-view reconstruction',18)
 f.line('M799 938 V951','purple',1.4,False,'3 2');f.rect(41,1060,829,32,'#E6EEFA');f.text(455,1083,'One shared decoder · complementary supervision views',20,'blue',False,'middle')
 # CoF
 f.panel(908,667,872,442,'d','Commit Forcing','purple')
 widths=[189,189,222,187];xs=[927,1136,1345,1587]
 titles=[['1  Sample','structure + detail'],['2  Commit jointly','and decode'],['3  Update history','+ reconstruct state'],['4  Learn','the next plan']]
 for x,w,ls in zip(xs,widths,titles):f.box(x,754,w,177,ls,'purple',21)
 # overwrite middle area with visual elements; headings at top
 for x,w,ls in zip(xs,widths,titles):
  f.rect(x+2,757,w-4,172,'white',r=7);f.lines(x+w/2,785,ls,21,'ink',True,gap=25)
 for x in [947,1156,1607]:
  f.tokens(x,848,5,'blue',22,21,5,fade=3 if x==1156 else 0);f.tokens(x,880,5,'orange',22,21,5,fade=3 if x==1156 else 0)
 f.line('M1236 838 V909','purple',1.5,False,'4 3')
 f.text(1457,842,'History + state',20,'purple',True,'middle');f.tokens(1363,878,4,'purple',20,24,4);f.robot(1523,852,.28)
 for i in range(3):f.line(f'M{xs[i]+widths[i]} 863 H{xs[i+1]-2}','purple',2,True)
 f.line('M936 944 V963 H1566 V944','purple',1.5);f.text(1250,989,'Generated transition · stop gradient (1–3)',19,'purple',False,'middle')
 f.box(1514,1005,246,62,['Recorded next latent','target (dataset)'],'teal',19);f.line('M1682 1005 V933','teal',2,True)
 f.rect(927,1069,832,25,'#ECE5F8');f.text(1343,1089,'Continue from the generated history–state pair',20,'purple',False,'middle')
 for xx,key,label in [(160,'blue','Structure'),(421,'orange','Detail'),(637,'teal','Music'),(856,'purple','Commit / state'),(1167,'gray','External module')]:
  f.dot(xx,1145,10,key);f.text(xx+23,1153,label,21)
 f.snow(1470,1145,12);f.text(1494,1153,'Frozen',21)
 f.save('overview-candidate')
 return f

def details():
 f=Fig(1500,670,'Structure–Detail Representation and Paired Training')
 f.text(30,42,'Structure–Detail Representation and Paired Training',34,bold=True)
 views(f,62,30,1440)
 f.text(750,332,'Joint and geometry positions and velocities use their respective partitions.',21,'gray',False,'middle')
 f.box(30,421,212,105,['Native motion','+ boundary state'],'gray',23);f.line('M242 474 H282','ink',2,True);f.box(285,430,142,88,['Encoder'],'gray',23);f.line('M427 474 H468','ink',2,True)
 f.box(470,420,208,107,['Structure–detail','z = e(q) + r'],'blue',23)
 f.line('M678 448 H714 V400 H747','blue',2,True);f.line('M678 498 H714 V551 H747','blue',2,True)
 f.box(750,365,168,73,['e(q) + r'],'blue',25);f.box(750,516,168,73,['e(q)'],'blue',25)
 for yy in [365,516]:
  f.line(f'M918 {yy+36} H955','purple',2,True);f.box(958,yy,202,73,['Shared decoder','D(·, b)'],'purple',22);f.line(f'M1160 {yy+36} H1200','ink',2,True)
 f.line('M1059 438 V515','purple',1.5,False,'5 4');f.text(1070,482,'shared weights',18,'purple')
 f.box(1203,357,268,89,['Full-view supervision','All motion quantities'],'blue',22);f.box(1203,508,268,89,['Structural supervision','Blue selections above'],'blue',22)
 f.text(750,644,'Full reconstruction also receives boundary-transition supervision.',21,'gray',False,'middle');f.save('structure-detail-training')
 f=Fig(1500,650,'Teacher Forcing and Commit Forcing')
 f.text(320,49,'Teacher Forcing',35,bold=True,anchor='middle');f.text(1037,49,'Commit Forcing',35,bold=True,anchor='middle');f.line('M651 24 V552','#ABB7C7',1)
 f.box(62,192,531,139,['Recorded latent history','+ recorded reference state'],'gray',26);f.line('M327 333 V423','ink',2,True);f.box(96,426,463,100,['Learn next plan'],'blue',27)
 for y,ts,col in [(79,['Sample structure + detail'],'blue'),(201,['Commit segment + decode motion'],'purple'),(323,['Append codes + reconstruct state'],'purple')]:f.box(712,y,584,93,ts,col,24)
 f.line('M1004 174 V199','purple',2,True);f.line('M1004 296 V321','purple',2,True);f.line('M1004 418 V440','purple',2,True)
 f.box(774,443,460,83,['Learn next plan'],'blue',27)
 f.line('M1311 79 H1323 V417 H1311','purple',1.5);f.lines(1411,199,['Stop-gradient','transition','construction'],19,'purple',True,gap=27)
 f.box(75,570,1186,60,['Recorded next latent target: z* = e(q*) + r*'],'teal',25);f.line('M326 570 V528','teal',2,True, '5 4');f.line('M1004 570 V528','teal',2,True,'5 4')
 f.lines(1357,477,['Residual target','rebased onto','sampled structure'],18,'orange',False,gap=24);f.line('M1280 488 H1236','orange',2,True)
 f.save('cof-terminology')

if __name__=='__main__':
 raise SystemExit('Superseded vector-robot draft. Use build_foredance_hybrid.py for details and vectorize_imagegen_master.py for the overview.')
