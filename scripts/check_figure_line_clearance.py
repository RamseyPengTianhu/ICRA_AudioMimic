"""Find stroke/text collisions in native figure PDFs, including Bezier curves.

Text and enclosing boxes are allowed; intersections of their actual borders
with label boxes are not. Findings still require visual inspection because
font bounding boxes include blank ascender/descender space.
"""
from pathlib import Path
import json
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/method-wide-20260912'


def intersects(a,b,r):
    dx,dy=b.x-a.x,b.y-a.y
    lo,hi=0.,1.
    for p,q in [(-dx,a.x-r.x0),(dx,r.x1-a.x),(-dy,a.y-r.y0),(dy,r.y1-a.y)]:
        if abs(p)<1e-9:
            if q<0:return False
        elif p<0:lo=max(lo,q/p)
        else:hi=min(hi,q/p)
    return lo<=hi


def segments(items):
    for i in items:
        if i[0]=='l':yield i[1],i[2]
        elif i[0]=='c':
            p0,p1,p2,p3=i[1:];last=p0
            for n in range(1,49):
                t=n/48;u=1-t
                p=p0*u**3+p1*(3*u*u*t)+p2*(3*u*t*t)+p3*t**3
                yield last,p;last=p
        elif i[0]=='re':
            r=i[1];p=[r.tl,r.tr,r.br,r.bl,r.tl]
            yield from zip(p,p[1:])
        elif i[0]=='qu':
            q=i[1];p=[q.ul,q.ur,q.lr,q.ll,q.ul]
            yield from zip(p,p[1:])


def main():
    results={}
    for name in ['structure-detail-training','cof-terminology']:
        doc=fitz.open(ROOT/'figures/foredance'/f'{name}.pdf');p=doc[0]
        spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
        drawings=p.get_drawings();hits=[]
        for s in spans:
            # Use typographic ascender/descender extent; one point of clearance.
            rect=fitz.Rect(s['bbox'])+(-1,-1,1,1)
            for index,d in enumerate(drawings):
                if d['color'] is None:continue
                if not rect.intersects(fitz.Rect(d['rect'])+(-2,-2,2,2)):continue
                if any(intersects(a,b,rect) for a,b in segments(d['items'])):
                    hits.append({'text':s['text'],'label_box':list(rect),'stroke_box':list(d['rect']),'drawing_index':index})
        results[name]=hits
    (OUT/'line-clearance.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
