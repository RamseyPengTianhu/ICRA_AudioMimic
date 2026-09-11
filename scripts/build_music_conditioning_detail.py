"""Accepted physical-time conditioning figure, retained from the v5 reconstruction."""
from pathlib import Path
from figure_svg_primitives import Figure
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/method-detail-redesign-20260911'

def music():
    f=Figure(2048,683,'Physical-time music conditioning',OUT/'music-candidate-v5.png')
    f.group('forecast-projection')
    f.path('M53 256V305C43 325 21 312 35 298C41 292 48 293 53 294M53 256L80 246V291'
           'C69 310 49 299 63 286C68 281 74 282 80 281',stroke='teal',sw=7)
    for j,h in enumerate([22,40,61,78,51,27]):
        f.line(102+j*10,292-h/2,102+j*10,292+h/2,stroke='teal',sw=6)
    f.line(176,294,207,294,arrow=True,sw=3)
    f.path('M216 172L342 227V351L216 405Z',fill='pale_blue',stroke='gray',sw=2.5)
    f.text(278,260,'Project',29,anchor='middle',weight='bold')
    f.text(278,294,'+ time',29,anchor='middle',weight='bold')
    f.circle(278,334,24,stroke='ink',sw=3)
    f.path('M278 316V334L269 345',sw=3)
    f.path('M350 294H356V244H368',arrow=True,sw=2.8)
    f.end()
    f.group('physical-time-alignment')
    f.text(414,211,'Forecast · 25 Hz',31,weight='bold')
    palette=['#68D0D3','#32B8C2','#009EAC','#52C4CB','#A9E2E5']
    for j in range(14):
        f.rect(370+j*54,226,54,36,fill=palette[(j*7)%5])
    f.line(433,327,1110,327,stroke='blue',sw=4)
    for x in [433,523,613,703,793]:
        f.circle(x,327,10,fill='blue',stroke='blue')
    f.text(414,379,'Motion · 15 Hz',31,weight='bold')
    f.circle(973,262,155,fill='white',stroke='ink',sw=3)
    f.raw('<defs><clipPath id="alignment-lens"><circle cx="973" cy="262" r="152"/></clipPath></defs>')
    f.raw('<g clip-path="url(#alignment-lens)">')
    for j in range(5):
        f.rect(856+j*54,185,54,45,fill=palette[j])
    f.line(834,327,1112,327,stroke='blue',sw=4)
    for x in [883,973,1063]:
        f.circle(x,327,11,fill='blue',stroke='white',sw=2)
    f.path('M937 231C940 269 958 283 967 307',stroke='teal',sw=3,arrow=True)
    f.path('M991 231C990 268 986 283 979 307',stroke='teal',sw=3,arrow=True)
    f.text(973,162,'Interpolate',26,anchor='middle')
    f.end()
    f.path('M973 344V447',sw=3,arrow=True)
    for j,w in enumerate([34,35,21,29]):
        x=904+sum([34,35,21,29][:j])+j*4
        f.rect(x,461,w,38,fill=palette[j])
    f.rich(973,548,['ĉ',('i','sub')],38,anchor='middle')
    f.end()
    f.group('separate-residual-film-injections')
    f.path('M1045 479C1220 479 1220 286 1470 286H1622V228',stroke='teal',sw=4.8,arrow=True)
    f.path('M1045 479C1210 479 1190 624 1470 624H1622V541',stroke='teal',sw=4.8,arrow=True)
    for yy,c,title in [(188,'blue','Structure'),(502,'orange','Residual')]:
        f.text(1420,yy-78,title,31,anchor='middle',weight='bold',fill=c)
        f.line(1327,yy,1368,yy,sw=2.7,arrow=True)
        for xx in [1370,1441]:
            f.rect(xx,yy-47,47,94,fill=c,stroke='ink',sw=1.6,r=2)
        f.line(1418,yy,1439,yy,sw=2.5,arrow=True)
        f.line(1489,yy,1547,yy,sw=2.7,arrow=True)
        f.circle(1516,yy,3.2,fill='ink',stroke='none')
        f.path(f'M1516 {yy}V{yy-86}H1810V{yy-24}',sw=2.6,arrow=True)
        f.rich(1518,yy+33,['v',('i','sub')],27,anchor='middle')
        f.rect(1550,yy-36,145,72,fill='pale_teal',stroke='teal',sw=2,r=9)
        f.text(1612,yy+10,'FiLM',29,anchor='middle',weight='bold')
        f.flame(1651,yy-22,40)
        f.line(1696,yy,1721,yy,sw=2.6,arrow=True)
        f.circle(1741,yy,17,stroke='purple',sw=2.5)
        f.text(1741,yy+10,'×',31,anchor='middle',fill='purple')
        f.line(1759,yy,1784,yy,sw=2.6,arrow=True)
        f.circle(1810,yy,23,stroke='ink',sw=2.6)
        f.text(1810,yy+13,'+',41,anchor='middle')
        f.line(1835,yy,1887,yy,sw=2.6,arrow=True)
        for j in range(3):
            f.rect(1893+j*37,yy-16,29,32,fill=c,r=2)
        f.text(2017,yy+7,'···',28,anchor='middle')
        f.path(f'M1714 {yy+97}H1728V{yy+78}H1742V{yy+97}H1761',stroke='purple',sw=3)
        f.path(f'M1741 {yy+72}V{yy+20}',stroke='purple',sw=2.5,arrow=True)
        f.rich(1742,yy+133,['m',('i','sub')],31,anchor='middle',fill='purple')
    f.end()
    f.save(OUT/'music-conditioning-detail')

if __name__=='__main__':
    music()
