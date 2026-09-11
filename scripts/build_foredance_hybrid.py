"""Faithful hybrid redraw: original robot art; editable labels, boxes and arrows."""
from pathlib import Path
import base64,io,html
from PIL import Image
import cairosvg
import cairocffi as cairo
from build_foredance_candidate import Fig,C,PALE,R,D,OUT
C.update(blue='#176AE8',orange='#EE931A',teal='#008C99',purple='#7951C5',gray='#566477',ink='#111B35')
class Hybrid(Fig):
 def crop(self,file,box,x,y,w,h):
  im=Image.open(D/file).crop(box);buf=io.BytesIO();im.save(buf,format='PNG')
  self.s.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>')
 def save(self,name,dest=D):
  content='\n'.join(self.s+['</svg>']).replace('Native editable vector diagram.','Hybrid vector diagram with original high-resolution robot raster artwork.')
  assert not any('prefix' in t.lower() or 'd+c' in t.lower() for t in self.labels)
  (dest/(name+'.svg')).write_text(content)
  class PDF(cairosvg.surface.PDFSurface):
   def _create_surface(self,w,h):
    a,w,h=super()._create_surface(w,h);a.restrict_to_version(cairo.PDF_VERSION_1_5);return a,w,h
  PDF.convert(bytestring=content.encode(),write_to=str(dest/(name+'.pdf')))
  cairosvg.svg2png(bytestring=content.encode(),write_to=str(OUT/(name+'.png')))

def robot(f,view,x,y,w,h):
 if view=='joint':f.crop('dc-bodyparts.png',(226,104,403,423),x,y,w,h)
 elif view=='geometry':f.crop('dc-bodyparts.png',(1113,104,1296,423),x,y,w,h)
 elif view=='execution':f.crop('overview2.png',(1315,340,1500,508),x,y,w,h)
 elif view=='human':f.crop('overview2.png',(46,636,88,702),x,y,w,h)
 else:f.crop('overview2.png',(498,632,542,702),x,y,w,h)

def overview():
 f=Hybrid(1536,1024,'ForeDance overview: faithful hybrid candidate')
 f.text(17,42,'ForeDance',41,bold=True);f.line('M236 10 V42','#6E82AC',1);f.text(255,35,'Anticipatory music conditioning for streaming dance generation',25)
 f.panel(13,57,1510,163,'a','Anticipate from heard music','teal')
 f.text(79,122,'Heard audio (causal)',18,'teal');f.wave(79,161,294,29);f.text(383,121,'Now',18,'ink',True,'middle');f.line('M383 128 V204','purple',1.4,False,'5 5');f.line('M79 204 H361','gray',1,True);f.text(367,211,'t',18,'teal')
 f.line('M403 158 H484','ink',1.8,True);f.shape('M487 103 L598 129 L598 181 L487 204 Z','#EFF2F7','#6B82AA',1);f.crop('mrt2-official-app-icon.png',(0,0,1024,1024),497,134,38,38);f.text(563,151,'MRT-2',19,'ink',True,'middle');f.snow(556,175,9)
 f.line('M600 155 H660','teal',2,True);f.rect(666,98,331,104,'#EAF8FE');f.text(680,123,'Predicted music states',21,'ink',True)
 for i,heights in enumerate([[16,26,21,30],[28,18,31,22],[21,32,15,26]]):
  for j,h in enumerate(heights):
   colors=[['#69BAC1','#1C8D9A','#4EB1B7','#85CBD1'],['#328EA6','#6BB8C1','#0A8D97','#95CFD3'],['#86C8CC','#27889E','#64B5BD','#18999D']]
   f.rect(695+i*102+j*18,177-h,15,h,colors[i][j],r=2)
  f.text(771+i*102,173,'···',21,'teal')
 f.text(824,194,'Future time (schematic)',16,'teal',False,'middle')
 f.text(1110,130,'Music conditioning',19,'teal',True);f.text(1110,155,'Shared by both branches',18,'teal')
 f.panel(13,235,1510,341,'b','Generate, commit, and execute','blue')
 f.rect(332,280,600,230,'#FFFFFF','#FFB4C1',8,1);f.text(355,310,'Structure–detail generator',24,'ink',True);f.rect(703,287,212,30,'#ECF3FF','#8EACEA',4);f.text(809,308,'Trained with Commit Forcing',15,'blue',False,'middle')
 f.rect(29,338,220,123,PALE['purple'],'purple');f.text(139,370,'Reference context',20,'purple',True,'middle');f.lines(139,402,['Committed history','+ reference state'],18,'ink',False,gap=24)
 f.line('M249 370 H282 V371 H414','ink',1.7,True);f.line('M249 432 H283 V477 H414','ink',1.7,True)
 # One forecast bus explicitly terminates at both FiLM modules.
 f.line('M998 155 H1060 V281 H315 V443 H414','teal',2,True);f.line('M315 338 H414','teal',2,True)
 for yy in [338,443]:
  f.rect(341,yy-13,60,24,'white',r=3);f.text(371,yy+5,'FiLM',17,'teal',True,'middle')
 f.box(416,320,159,68,['Structure planner','AR Transformer'],'blue',17)
 f.box(416,425,159,64,['Residual diffusion','Detail generator'],'orange',17)
 f.line('M575 357 H589','blue',1.6,True);f.tokens(593,345,3,'blue',16,26,4);f.text(622,334,'q',21,'blue',True,'middle');f.line('M650 357 H664','blue',1.5,True);f.tokens(669,345,3,'blue',16,26,4);f.text(699,334,'e(q)',22,'blue',True,'middle')
 f.line('M699 373 V405 H490 V424','blue',1.7,True);f.text(594,399,'sampled structure',15,'blue',False,'middle')
 f.line('M575 460 H602','orange',1.5,True);f.tokens(613,447,5,'orange',18,26,5);f.text(670,491,'r',24,'orange',True,'middle')
 f.line('M729 358 H750 V394','blue',1.8,True);f.line('M729 460 H750 V433','orange',1.8,True);f.dot(750,414,18,'white','ink');f.text(750,423,'+',30,'ink',False,'middle')
 f.line('M769 414 H778','ink',1.7,True);f.shape('M779 359 L854 386 L854 442 L779 467 Z','#F2EFF8','#61719C',1);f.lines(813,407,['Shared','decoder'],17,'ink',True,gap=24)
 f.line('M283 432 V522 H813 V469','purple',1.5,True);f.text(753,518,'Reference state',16,'purple',False,'middle')
 f.line('M854 414 H880','ink',1.7,True);f.rect(883,358,166,116,'#F4EFFB','purple',5);f.text(966,384,'Commit segment',19,'purple',True,'middle')
 f.line('M896 417 C908 395 924 435 940 413 S960 404 966 413','purple',2.2);f.line('M966 413 C983 434 997 399 1009 414 S1030 430 1039 410','purple',1.5,False,'4 3');f.line('M966 394 V429','purple',1,False,'3 2')
 f.text(927,449,'Committed',14,'purple',True,'middle');f.text(1009,449,'Revisable',14,'gray',False,'middle');f.text(966,468,'Reference motion · schematic',12,'purple',False,'middle')
 f.line('M1049 414 H1071','purple',1.8,True);f.box(1074,375,97,74,['Reference','bridge'],'gray',18);f.line('M1171 414 H1194','gray',1.7,True);f.rect(1197,375,94,74,PALE['gray'],'gray');f.text(1244,397,'SONIC',19,'gray',True,'middle');f.text(1244,421,'tracker',18,'gray',True,'middle');f.snow(1244,439,7)
 f.line('M1291 414 H1312','gray',1.7,True);f.text(1414,308,'Humanoid execution',20,'ink',True,'middle');f.text(1320,333,'(schematic)',17);robot(f,'execution',1315,340,187,169)
 f.line('M1427 510 V532 H1244 V451','gray',1.7,True);f.text(1325,552,'Measured robot state',17,'gray',False,'middle')
 f.line('M984 475 V555 H131 V464','purple',1.7,True);f.rect(312,540,643,29,PALE['blue']);f.text(634,560,'Selected codes → history; decoded motion → reference state',18,'purple',False,'middle')
 f.panel(15,592,770,352,'c','Structure–Detail Representation','blue');f.text(78,650,'Paired training with kinematic supervision',16,'blue')
 # Source strip retains its original three nodes, labels, silhouettes and order.
 f.rect(30,658,202,65,'#EDF6FF');robot(f,'human',43,660,41,60);f.text(108,681,'FineDance',20,bold=True);f.text(95,709,'Human dance data',16)
 f.line('M234 691 H256','ink',1.5,True);f.box(258,658,190,65,['Motion retargeting','Offline preprocessing'],'gray',18)
 f.line('M450 691 H473','ink',1.5,True);f.rect(476,658,292,65,'#EDF6FF');robot(f,'g1',492,658,43,65);f.text(556,681,'G1 training motion',20,bold=True);f.text(556,709,'(Unitree G1)',16)
 for xx,title,view in [(30,'Joint view','joint'),(259,'Geometry view','geometry')]:
  f.rect(xx,736,224,158,'#EDF6FF');f.text(xx+14,761,title,20,'blue',True);robot(f,view,xx+10,767,66,122)
  f.text(xx+90,788,'Structure',15,'blue',True);f.lines(xx+90,810,['root, legs, waist'] if view=='joint' else ['torso, wrists, soles'],14,anchor='start',gap=17)
  f.text(xx+90,849,'Detail',15,'orange',True);f.lines(xx+90,870,['arm joints'] if view=='joint' else ['remaining body points'],14,anchor='start',gap=17)
 for yy,formula,ts in [(744,'e(q) + r',['Full-motion','reconstruction']),(824,'e(q)',['Structural-view','reconstruction'])]:
  f.rect(513,yy,255,64,'white','blue',5);f.text(527,yy+36,formula,23,'blue',True);f.line(f'M613 {yy+31} H639','blue',1.5,True);f.lines(651,yy+25,ts,17,anchor='start',gap=21)
 f.rect(30,904,738,27,'#E4EFFD');f.text(399,924,'Shared decoder · complementary kinematic supervision',18,'blue',False,'middle')
 f.panel(800,592,723,352,'d','Commit Forcing','purple')
 xs=[813,995,1176,1358];w=168
 for x,ts in zip(xs,[['1. Sample','structure + detail'],['2. Commit jointly','+ decode'],['3. Update history','+ reconstruct state'],['4. Learn','continuation']]):
  width=151 if x==1358 else 168;f.rect(x,655,width,148,'white','purple',4);f.lines(x+width/2,682,ts,17,'ink',True,gap=22)
 for x in [830,1011,1374]:
  f.tokens(x,733,5,'blue',18,22,4,3 if x==1011 else 0);f.tokens(x,766,5,'orange',18,22,4,3 if x==1011 else 0)
 f.line('M1075 726 V794','purple',1,False,'3 3');f.text(1258,735,'History + state',17,'purple',True,'middle');f.tokens(1192,761,3,'purple',18,22,4);robot(f,'g1',1280,744,30,51)
 for start,end in [(981,994),(1163,1175),(1344,1357)]:f.line(f'M{start} 751 H{end}','purple',1.7,True)
 f.line('M821 817 V829 H1344 V817','purple',1.2);f.text(1079,851,'Generated transition · stop gradient',17,'purple',False,'middle')
 f.box(1291,862,217,58,['Recorded next latent target','(from dataset)'],'teal',16);f.line('M1432 862 V805','teal',1.6,True)
 f.rect(813,918,463,19,'#EBE3F9');f.text(1044,933,'Continue from generated history and state',16,'purple',False,'middle')
 for x,key,label in [(178,'blue','Structure (discrete)'),(407,'orange','Detail (continuous)'),(642,'teal','Music condition'),(839,'purple','Commit / state'),(1055,'gray','External module')]:
  f.rect(x,971,34,28,C[key],r=3);f.text(x+45,992,label,16)
 f.snow(1266,985,12);f.text(1290,992,'Frozen',17)
 f.save('overview-candidate')

def details():
 f=Hybrid(1774,887,'Structure–Detail Representation and Paired Training')
 f.text(887,43,'Structure–Detail Representation and Paired Training',37,bold=True,anchor='middle');f.text(25,84,'(a) Body-part supervision views',28,bold=True)
 for x,title,view in [(25,'Joint view','joint'),(893,'Geometry view','geometry')]:
  f.rect(x,95,855,327,'#EAF4FC',r=12);f.text(x+31,135,title,28,'blue',True);robot(f,view,x+197,105,177,316);f.text(x+31,135,title,28,'blue',True);f.line(f'M{x+438} 148 V397','#90ABD0',1.3)
  f.dot(x+490,165,15,'blue');f.text(x+526,173,'Structure:',23,'blue',True);f.text(x+650,173,'root, legs, waist' if view=='joint' else 'torso, wrists, soles',21)
  f.dot(x+490,223,15,'orange');f.text(x+526,231,'Detail:',23,'orange',True);f.text(x+607,231,'arm joints' if view=='joint' else 'remaining body points',21)
 f.text(887,452,'Positions and their velocities use the same partition.',23,'gray',False,'middle');f.text(25,517,'(b) Two principal reconstruction paths',29,bold=True)
 f.box(33,583,279,142,['Full native motion','+ boundary state'],'gray',26);f.line('M313 653 H360','ink',2,True);f.shape('M364 551 L523 608 L523 701 L364 751 Z','#E5E8ED','#65707A',2);f.text(435,663,'Encoder',28,'ink',True,'middle');f.line('M525 653 H572','ink',2,True)
 f.box(575,581,233,144,['Structure–detail','z = e(q) + r'],'blue',25)
 for y,formula in [(541,'e(q) + r'),(664,'e(q)')]:
  f.line(f'M809 {y+42} H880','blue',2,True);f.box(883,y,178,84,[formula],'blue',30);f.line(f'M1062 {y+42} H1104','blue',2,True);f.box(1107,y-6,222,97,['Shared decoder','D(·, b)'],'purple',26)
  f.line(f'M1330 {y+42} H1370','ink',2,True)
 f.box(1373,531,375,105,['Full-view supervision','All joint and geometry quantities'],'gray',24);f.box(1373,653,375,105,['Structural-view supervision','Blue selections in (a)'],'gray',24)
 f.line('M1218 633 V656','purple',1.4,False,'4 3')
 f.text(887,819,'Supervision views guide latent roles; both paths share one decoder.',23,'gray',False,'middle');f.text(887,851,'Full reconstruction also uses boundary-transition supervision.',22,'gray',False,'middle');f.save('structure-detail-training')
 # Restore the detailed visual grammar of the original TF/CoF figure.
 f=Hybrid(1774,887,'Teacher Forcing and Commit Forcing')
 f.text(450,61,'Teacher Forcing',52,bold=True,anchor='middle');f.text(1230,61,'Commit Forcing',52,bold=True,anchor='middle');f.line('M849 22 V719','#677384',1.5)
 f.rect(180,212,570,200,'#F5F5F9','ink',13,2);f.text(465,255,'Recorded history + recorded state',29,'ink',True,'middle');f.wave(211,330,275,33,'teal');f.box(559,286,147,74,['State'],'purple',30);f.text(354,390,'Motion',24,'teal',True,'middle')
 f.line('M464 415 V533','ink',2.7,True);f.rect(211,540,509,132,PALE['blue'],'blue');f.text(465,579,'Learn next plan',31,'ink',True,'middle')
 f.rect(980,88,537,142,'#EAF2FF','ink',12,2);f.text(1248,124,'Sample structure + detail',30,'ink',True,'middle');f.tokens(1015,151,5,'blue',32,29,6);f.wave(1284,166,167,20,'orange');f.text(1100,211,'structure',23,'blue',True,'middle');f.text(1380,211,'detail',23,'orange',True,'middle');f.line('M1248 232 V251','ink',2,True)
 f.rect(980,255,537,122,'#F0EAF8','ink',12,2);f.text(1248,287,'Commit segment and decode motion',28,'ink',True,'middle');f.box(1065,307,132,55,['Codes'],'purple',27);f.line('M1209 335 H1254','ink',2,True);f.wave(1270,333,167,16,'purple');f.text(1364,366,'Motion',21,'purple',True,'middle');f.line('M1248 379 V398','ink',2,True)
 f.rect(980,400,537,120,'#F5F5F9','ink',12,2);f.text(1248,435,'Append codes + reconstruct state',28,'ink',True,'middle');f.tokens(1043,465,7,'purple',28,26,5);f.box(1365,450,122,56,['State'],'purple',25);f.line('M1248 521 V541','ink',2,True)
 f.rect(995,544,444,132,PALE['blue'],'blue');f.text(1217,581,'Learn next plan',30,'ink',True,'middle')
 f.line('M1530 90 H1548 V539 H1530','ink',2);f.lines(1661,286,['Stop-gradient','transition','construction'],26,'ink',True,gap=34)
 f.box(1493,573,267,82,['Rebase residual target','onto sampled structure'],'orange',22);f.line('M1488 611 H1443','ink',2,True)
 f.box(271,739,1236,77,['Recorded next latent target: z* = e(q*) + r*'],'gray',29)
 f.line('M623 737 V710 H464 V675','ink',2,True,'5 4');f.line('M1078 737 V710 H1244 V680','ink',2,True,'5 4')
 # small network glyphs restore original visual distinction of learning steps
 for cx,cy in [(465,625),(1217,630)]:
  f.rect(cx-74,cy-30,148,57,PALE['blue']);pts=[(-36,-16),(-36,18),(0,0),(36,-16),(36,18)]
  for a,b in [(0,2),(1,2),(2,3),(2,4),(0,3),(1,4)]:f.line(f'M{cx+pts[a][0]} {cy+pts[a][1]} L{cx+pts[b][0]} {cy+pts[b][1]}','ink',1.6)
  for px,py in pts:f.dot(cx+px,cy+py,9,'#C0DBFF','ink',1.5)
 f.text(887,861,'Rebasing preserves the target latent; decoded motion still depends on the reference state.',25,'ink',False,'middle');f.save('cof-terminology')
if __name__=='__main__':details();print('Wrote terminology-aligned detail figures; overview uses imagegen master.')
