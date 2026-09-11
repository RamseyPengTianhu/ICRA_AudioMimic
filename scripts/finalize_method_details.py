"""Native reconstruction of the two v6 imagegen designs selected for finalization.

Conditioning is retained byte-for-byte. Coordinates use the 2048 x 683 preview
space of the 2172 x 724 source rasters. Poses are one shared vector master per
pose, so changing the supervision colors never changes the anatomy.
"""
from pathlib import Path
import math
import sys
from figure_svg_primitives import Figure, color

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/method-detail-redesign-20260911'

def limb(f, points, c, width=7.2):
    f.path('M'+'L'.join(f'{x} {y}' for x,y in points),stroke=c,sw=width)
    for x,y in points:
        f.circle(x,y,width*.46,fill=c,stroke='white',sw=.55)

def motion_pose(f,x,y,scale=1.5,phase=0,mode='full'):
    """Flat articulated body at pelvis origin; exact same paths in both views."""
    body='ink' if mode=='input' else 'blue'
    arm='ink' if mode=='input' else ('orange' if mode=='full' else '#D9C8F1')
    joints=[
      dict(la=[(-9,-32),(-23,-43),(-20,-63)],ra=[(9,-32),(23,-25),(42,-24)],
           ll=[(-5,0),(-17,29),(-27,58)],rl=[(5,0),(18,29),(23,58)]),
      dict(la=[(-9,-32),(-21,-47),(-31,-63)],ra=[(9,-32),(22,-46),(32,-63)],
           ll=[(-5,0),(-4,31),(-4,59)],rl=[(5,0),(25,15),(7,33)]),
      dict(la=[(-9,-32),(-23,-22),(-32,-7)],ra=[(9,-32),(23,-23),(43,-21)],
           ll=[(-5,0),(-18,27),(-32,48)],rl=[(5,0),(21,23),(23,58)])][phase]
    f.raw(f'<g transform="translate({x} {y}) scale({scale})">')
    # Shoulder/hip caps and tapered torso, following the flat imagegen silhouettes.
    f.path('M-9 -33Q0 -37 9 -33L7 -8Q0 -3 -7 -8Z',fill=body,stroke=body,sw=1)
    f.line(0,-37,0,-33,stroke=body,sw=7)
    f.circle(0,-46,7.5,fill=body,stroke='none')
    for key in ['ll','rl']:
        limb(f,joints[key],body,8)
        ax,ay=joints[key][-1]
        f.line(ax,ay,ax+5,ay+1,stroke=body,sw=6.3)
    f.circle(0,-1,5.6,fill=body,stroke='white',sw=.7)
    for key in ['la','ra']:
        limb(f,joints[key],arm,6.3)
        # Wrist points are among the selected geometry coordinates.
        wx,wy=joints[key][-1]
        f.circle(wx,wy,4.1,fill='blue' if mode=='structure' else arm,stroke='none')
    f.end()

def context_pose(f,x,y,scale=1,generated=False):
    """The matched purple posture glyphs in the approved TF/CoF raster."""
    f.raw(f'<g transform="translate({x} {y}) scale({scale})">')
    shift=5 if generated else 0
    f.circle(60,10+shift,11,fill='purple',stroke='none')
    f.path(f'M54 {27+shift}L33 43L34 60L42 76L55 67L65 {41+shift}Z',fill='purple',stroke='purple',sw=1)
    limb(f,[(37,43),(29,65),(17,72 if not generated else 74)],'purple',8)
    limb(f,[(62,40+shift),(65,58),(86,65 if not generated else 62)],'purple',8)
    limb(f,[(40,76),(26,102),(7,133)],'purple',10)
    limb(f,[(46,78),(71,96),(75,136)],'purple',10)
    f.line(7,133,13,137,stroke='purple',sw=8)
    f.line(75,136,86,136,stroke='purple',sw=8)
    f.end()

def representation():
    f=Figure(2048,683,'Learning structure and detail through shared reconstruction',OUT/'representation-candidate-v6.png')
    f.group('motion-input')
    for i,x in enumerate([68,186,305]): motion_pose(f,x,342,1.52,i,'input')
    f.text(183,204,'Input motion',28,anchor='middle',weight='bold')
    f.line(370,327,411,327,sw=3.6,arrow=True)
    f.path('M418 249L535 282V373L418 407Z',fill='pale_blue',stroke='ink',sw=3)
    f.text(477,327,'Encode',28,anchor='middle',weight='bold')
    f.flame(460,337,41)
    f.line(541,327,590,327,sw=3.6,arrow=True)
    f.end()
    f.group('codebook-geometry')
    f.path('M592 297C576 239 607 183 662 132C703 91 736 72 784 90'
           'C831 108 886 83 931 122C969 156 991 211 1003 272'
           'C1021 332 1027 389 1002 432C977 487 950 509 896 523'
           'C837 536 789 567 733 554C687 544 619 530 590 490'
           'C560 450 581 386 592 344C597 326 596 310 592 297Z',fill='#E1EFFF',stroke='none')
    for xx,yy in [(694,184),(788,182),(887,182),(639,240),(742,235),(834,228),
                  (693,291),(637,340),(950,311),(868,341),(911,379),(973,380),
                  (629,427),(712,434),(807,437),(669,492),(759,495),(843,496),(913,478)]:
        f.circle(xx,yy,8.6,fill='blue',stroke='none')
    f.text(801,141,'Codebook',27,anchor='middle',weight='bold')
    f.line(760,333,878,273,stroke='orange',sw=4.8,arrow=True)
    f.circle(744,343,15.4,fill='blue',stroke='none')
    f.circle(897,263,15.4,fill='ink',stroke='none')
    f.text(744,394,'Structure',28,anchor='middle',weight='bold')
    f.text(790,292,'Detail',28,anchor='middle',weight='bold',fill='orange')
    f.text(909,238,'Full code',28,anchor='middle',weight='bold')
    f.end()
    f.group('two-passes-one-decoder')
    f.path('M916 263C1020 269 1054 157 1191 200C1231 208 1251 219 1289 226',sw=4,arrow=True)
    f.text(1149,177,'Structure + detail',28,anchor='middle',weight='bold')
    f.path('M761 348C871 382 918 472 1098 475C1188 478 1241 459 1289 438',stroke='blue',sw=4,arrow=True)
    f.text(1120,505,'Structure only',28,anchor='middle',weight='bold',fill='blue')
    f.path('M1303 198L1442 154V510L1303 466Z',fill='pale_blue',stroke='ink',sw=3)
    f.circle(1303,227,9.6,fill='blue',stroke='ink',sw=1.8)
    f.circle(1303,331,9.6,fill='purple',stroke='ink',sw=1.8)
    f.circle(1303,437,9.6,fill='blue',stroke='ink',sw=1.8)
    f.text(1372,313,'Shared',28,anchor='middle',weight='bold')
    f.text(1372,345,'decoder',28,anchor='middle',weight='bold')
    f.flame(1356,357,56)
    # The state uses the same pose + velocity grammar as the paired-context figure.
    f.pose(1085,277,3.4,velocity=False)
    f.path('M1156 334L1164 325L1174 332L1182 309L1190 337L1198 322L1208 329',stroke='purple',sw=3.6)
    f.text(1124,402,'Boundary state',26,anchor='middle',weight='bold',fill='purple')
    f.line(1220,331,1289,331,stroke='purple',sw=3.7,arrow=True)
    f.line(1448,225,1540,225,sw=3.8,arrow=True)
    f.line(1448,463,1540,463,stroke='blue',sw=3.8,arrow=True)
    f.end()
    f.group('full-and-structural-supervision')
    for mode,yy in [('full',227),('structure',501)]:
        for i,xx in enumerate([1617,1774,1936]): motion_pose(f,xx,yy,1.48,i,mode)
    f.text(1765,114,'Full supervision',29,anchor='middle',weight='bold')
    f.text(1765,376,'Structural supervision',29,anchor='middle',weight='bold')
    f.end()
    f.save(OUT/'structure-detail-training')

def code_symbol(f,cx,cy,kind):
    c='#A9CAFF'
    if kind==0: f.circle(cx,cy,15,fill=c,stroke='none')
    elif kind==1: f.rect(cx-15,cy-15,30,30,fill=c)
    elif kind==2: f.path(f'M{cx} {cy-17}L{cx+17} {cy+15}H{cx-17}Z',fill=c,stroke='none')
    else: f.path(f'M{cx} {cy-18}L{cx+18} {cy}L{cx} {cy+18}L{cx-18} {cy}Z',fill=c,stroke='none')

def residual_trace(f,x,y,phase):
    pts=[]
    for i in range(23):
        xx=x+14+i*49/22
        yy=y+29+6.5*math.sin(i*.23+phase)+2*math.sin(i*.53+phase)
        pts.append((xx,yy))
    f.path('M'+'L'.join(f'{a:.1f} {b:.1f}' for a,b in pts),stroke='#FFE2B7',sw=2.7)

def commit():
    f=Figure(2048,683,'Teacher Forcing versus Commit Forcing and residual rebasing',OUT/'commit-candidate-v6.png')
    f.group('paired-context-comparison')
    f.text(620,77,'History',31,anchor='middle',weight='bold')
    f.text(1143,73,'Boundary state',31,anchor='middle',weight='bold')
    for y,title,tail,generated in [(157,'Teacher Forcing',[1,0,2],False),(430,'Commit Forcing',[1,3,0],True)]:
        f.text(39,y+74,title,31,weight='bold')
        f.rect(743,y-29,593,184,fill='pale_purple',r=17)
        f.path(f'M745 {y-14}Q745 {y-29} 761 {y-29}H875M1205 {y-29}H1320Q1336 {y-29} 1336 {y-14}',stroke='purple',sw=2.1)
        f.text(1040,y-31,'Generated commit' if generated else 'Recorded segment',30,anchor='middle',weight='bold',fill='purple')
        for idx,xx in enumerate([351,431,511,591,754,836,918]):
            f.rect(xx,y,78,73,fill='blue')
            f.rect(xx,y+78,78,55,fill='orange')
            code_symbol(f,xx+39,y+37,[0,1,2,3][idx] if idx<4 else tail[idx-4])
            residual_trace(f,xx,y+78,idx*.6+(1.2 if generated and idx>=4 else 0))
        # Both code streams have the same temporal gap, unlike the raster artifact.
        for yy in [y+44,y+114]:
            for xx in [687,708,729]: f.circle(xx,yy,4.6,fill='ink',stroke='none')
        f.line(1039,y+7,1039,y+136,stroke='purple',sw=3)
        context_pose(f,1075,y-7,1,generated)
        f.path(f'M1209 {y+71}L1218 {y+64}Q1224 {y+99} 1232 {y+46}'
               f'Q1238 {y+27} 1246 {y+73}Q1252 {y+89} 1258 {y+57}'
               f'Q1265 {y+45} 1271 {y+73}Q1280 {y+97} 1288 {y+69}'
               f'L1298 {y+61}L1307 {y+67}H1316',stroke='purple',sw=3.5)
    f.end()
    f.line(1387,43,1387,640,stroke='#DFE4ED',sw=2.4)
    f.group('residual-rebasing')
    f.text(1864,104,'Same recorded target',28,anchor='middle',weight='bold')
    f.line(1538,498,1845,160,stroke='orange',sw=5.3,arrow=True)
    f.line(1919,492,1865,170,stroke='orange',sw=4.1,dash='14 13',opacity=.5,arrow=True)
    f.circle(1525,521,23,fill='blue',stroke='none')
    f.circle(1922,521,23,fill='blue',stroke='none')
    f.circle(1862,142,21,fill='teal',stroke='none')
    f.text(1570,295,'Residual rebasing',28,anchor='middle',fill='orange',weight='bold')
    f.text(1950,335,'Detail',28,anchor='middle',fill='orange',weight='bold')
    f.text(1532,584,'Sampled structure',27,anchor='middle',weight='bold')
    f.text(1899,584,'Recorded structure',27,anchor='middle',weight='bold')
    f.end()
    f.save(OUT/'cof-terminology')

if __name__=='__main__':
    if '--all' in sys.argv:
        from build_music_conditioning_detail import music
        music()
    representation()
    commit()
    print('Reconstructed v6 representation and context-comparison rasters; accepted conditioning unchanged.')
