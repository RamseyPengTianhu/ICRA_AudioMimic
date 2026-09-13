"""Author-requested full-width refinements of the existing method artwork."""
from pathlib import Path
import math
import re
import shutil
from figure_svg_primitives import Figure
from finalize_method_details import motion_pose, code_symbol
from boundary_state_icon import draw_boundary_state_centered
import finalize_method_details as original
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/method-wide-20260912'
NARROW=ROOT/'output/method-single-column-20260912'


def export(svg,stem):
    stem.with_suffix('.svg').write_text(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(stem.with_suffix('.pdf')))
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(stem.with_suffix('.png')))


def content(f):
    return '\n'.join(f.parts[f.parts.index('<!-- CONTENT -->')+1:])


def new_content():
    f=Figure(2048,600,'','')
    f.raw('<!-- CONTENT -->')
    return f


def supervision_bands(f,y,full):
    """The full output is partitioned into structural and complementary coordinates.

    Matching arrows show which coordinates enter each reconstruction objective;
    the residual remains an input to the full path, not a separate detail loss.
    """
    kind='full' if full else 'structural'
    f.group(kind+'-reconstruction-supervision')
    f.path(f'M1554 {y}H1548V{y+112}H1554',stroke='ink' if full else 'blue',sw=2)
    for j,(label,c) in enumerate([('Structure','blue'),('Detail','orange')]):
        yy=y+j*63
        f.raw(f'<g data-coordinates="{label.lower()}" opacity="{1 if full or j==0 else .28}">')
        for x in [1560,1848]:
            f.rect(x,yy,180,49,fill=c,r=6)
            f.text(x+90,yy+34,label,28,anchor='middle',fill='white' if j==0 else 'ink',weight='bold')
        if full or j==0:
            f.raw(f'<path d="M1754 {yy+24.5}H1837" fill="none" '
                  f'stroke="{"#0769F9" if j==0 else "#FF8A17"}" stroke-width="3.5" '
                  f'marker-start="url(#arrow-{c})" marker-end="url(#arrow-{c})"/>')
        f.end()
    f.end()


def representation():
    # Retain the original long visual arrangement, with the two requested repairs.
    original.OUT=OUT/'baseline'
    original.representation()
    svg=(original.OUT/'structure-detail-training.svg').read_text()
    svg=re.sub(r'font-size="(?:26|27|28)"','font-size="29"',svg)
    svg=svg.replace('height="683"','height="600"').replace('viewBox="0 0 2048 683"','viewBox="0 0 2048 600"')
    f=new_content(); f.group('codebook-geometry')
    f.raw('<circle id="codebook-boundary" cx="798" cy="330" r="228" fill="#E1EFFF"/>')
    others=[(665,220),(730,190),(817,190),(922,186),(637,390),
            (665,442),(736,494),(823,500),(926,455),(972,430)]
    q,z=(790,320),(910,320)
    assert math.dist(q,z)<min(math.dist(p,z) for p in others)
    for x,y in others:f.raw(f'<circle class="prototype" cx="{x}" cy="{y}" r="8.6" fill="#0769F9"/>')
    f.text(798,144,'Codebook',31,anchor='middle',weight='bold')
    dx,dy=z[0]-q[0],z[1]-q[1];length=math.hypot(dx,dy)
    f.line(q[0]+19*dx/length,q[1]+19*dy/length,z[0]-19*dx/length,z[1]-19*dy/length,stroke='orange',sw=4.8,arrow=True)
    f.raw('<circle id="selected-prototype" cx="790" cy="320" r="15.4" fill="#0769F9"/>')
    f.raw('<circle id="encoded-latent" cx="910" cy="320" r="15.4" fill="#080F2D"/>')
    f.text(764,330,'Structure',28,anchor='end',fill='blue')
    f.text(850,296,'Detail',28,anchor='middle',fill='orange')
    f.text(936,330,'Latent',28,anchor='start')
    f.end()
    a=svg.index('<g id="codebook-geometry">');b=svg.index('<g id="two-passes-one-decoder">')
    svg=svg[:a]+content(f)+'\n'+svg[b:]
    svg=svg.replace('M541 327L590 327','M541 327L563 327')
    svg=svg.replace('M761 348C871 382 918 472 1098 475','M799 337C848 423 958 472 1098 475')
    svg=svg.replace('M916 263C1020 269 1054 157 1191 200C1231 208 1251 219 1289 226',
                    'M910 300C934 217 1108 151 1289 226')
    svg=svg.replace('>Input motion</text>','>Motion</text>')
    # Replace the legacy pose-plus-wave cue with the overview's single glyph.
    begin=svg.index('<g transform="translate(1085 277)')
    end=svg.index('<text x="1124"',begin)
    cue=new_content();draw_boundary_state_centered(cue,1148,331,90)
    svg=svg[:begin]+content(cue)+'\n'+svg[end:]
    svg=svg.replace('<text x="1124" y="402"','<text x="1148" y="402"')
    svg=svg.replace('M1220 331L1289 331','M1195 331L1289 331')
    svg=svg.replace('translate(1356 357)','translate(1351.76 357)')
    f=new_content();f.group('input-starting-state-cue')
    draw_boundary_state_centered(f,183,515,80)
    f.text(183,580,'Boundary state',28,anchor='middle',fill='purple')
    f.path('M218 515H477V397',stroke='purple',sw=3.5,arrow=True)
    f.end()
    svg=svg.replace('<g id="codebook-geometry">',content(f)+'\n<g id="codebook-geometry">')
    f=new_content();f.group('full-and-structural-supervision')
    f.text(1650,139,'Reconstruction',27,anchor='middle')
    f.text(1938,139,'Ground truth',27,anchor='middle')
    for yy,title,full in [(169,'Full-motion loss',True),(407,'Structural loss',False)]:
        f.text(1794,100 if full else 354,title,31,anchor='middle',weight='bold')
        supervision_bands(f,yy,full)
    f.end()
    a=svg.index('<g id="full-and-structural-supervision">')
    svg=svg[:a]+content(f)+'\n</svg>'
    # Reproducible reference points to the preserved long design, not a later draft.
    svg=svg.replace(str(original.OUT/'representation-candidate-v6.png'),str(OUT/'structure-detail-training-long-reference.png'))
    for label in ['Structure + detail','Structure only','Boundary state']:
        svg=re.sub(r'<text\b[^>]*>'+re.escape(label)+r'</text>',
                   lambda m:m[0].replace('font-size="29"','font-size="28"').replace('font-weight="bold"','font-weight="normal"'),svg)
    export(svg,OUT/'structure-detail-training')


def tile(f,x,y,w=42,h=74,kind=0,phase=0,opacity=1):
    f.raw(f'<g opacity="{opacity}">')
    f.rect(x,y,w,h*.56,fill='blue')
    f.rect(x,y+h*.56+3,w,h*.44-3,fill='orange')
    f.raw(f'<g transform="translate({x+w/2} {y+h*.28}) scale({w/72})">')
    code_symbol(f,0,0,kind);f.end()
    pts=[(x+5+j*(w-10)/17,y+h*.80+4*math.sin(j*.25+phase)) for j in range(18)]
    f.path('M'+'L'.join(f'{a:.2f} {b:.2f}' for a,b in pts),stroke='#FFE2B7',sw=2)
    f.end()


def commit():
    f=Figure(2400,700,'Ground-truth contexts versus model-generated contexts in Commit Forcing',OUT/'cof-wide-candidate.png')
    f.text(67,219.4,'TF',44,anchor='middle',weight='bold')
    f.text(67,476.4,'CoF',44,anchor='middle',weight='bold')
    f.text(495,58,'Context construction',38,anchor='middle',weight='bold')
    f.text(1342,58,'Conditioning context',38,anchor='middle',weight='bold')
    # TF reads a recorded segment. It never enters the self-rollout operation.
    f.group('teacher-forcing-recorded-source')
    f.text(495,112,'Ground-truth motion',34,anchor='middle')
    for i,x in enumerate([260,370,480]):motion_pose(f,x,207,.9,i,'input')
    for i in range(4):tile(f,570+i*47,168,43,72,[1,0,2,3][i],i*.6)
    f.path('M766 204H1100',sw=3.5,arrow=True)
    f.end()
    # CoF starts from a recorded seed, samples one horizon, commits the prefix.
    f.group('commit-forcing-self-rollout')
    f.text(236.5,358,'Ground-truth',32,anchor='middle')
    f.text(236.5,395,'context',32,anchor='middle')
    f.rect(142,409,189,104,fill='pale_purple',r=12)
    for i in range(2):tile(f,157+i*40,426.5,36,69,i,i*.6)
    draw_boundary_state_centered(f,290,461,76)
    f.text(439,432,'Rollout',32,anchor='middle')
    f.path('M346 461H532',sw=3.5,arrow=True)
    f.text(634,395,'Commit',34,anchor='middle',weight='bold')
    f.text(834,395,'Discard',34,anchor='middle',fill='gray')
    f.path('M536 415V408H732V415',stroke='purple',sw=2.3)
    f.path('M736 415V408H932V415',stroke='gray',sw=2.3,opacity=.6)
    for i in range(8):
        tile(f,536+i*50,424,46,74,[1,3,0,2,0,2,1,3][i],i*.6+1.2,1 if i<4 else .18)
    f.path('M536 507V516H732V507',stroke='purple',sw=2.3)
    # Only the committed prefix supplies BOTH members of the next context.
    f.path('M634 516V539Q634 551 646 551H1048Q1060 551 1060 539V473Q1060 461 1072 461H1100',stroke='purple',sw=3.6,arrow=True)
    f.text(847,590,'Context update',32,anchor='middle',fill='purple')
    f.end()
    f.group('matched-generation-contexts')
    f.text(1275,112,'History',34,anchor='middle')
    f.text(1530,112,'Boundary state',34,anchor='middle')
    for yy,generated in [(161,False),(418,True)]:
        f.rect(1102,yy-14,480,114,fill='pale_purple',r=12)
        for i in range(2):tile(f,1118+i*38,yy+7,34,72,i,i*.6,.6)
        for by in [yy+27,yy+66]:
            for xx in [1206,1217,1228]:f.circle(xx,by,2.3,fill='ink',stroke='none')
        seq=[1,3,0,2] if generated else [1,0,2,3]
        for i in range(4):tile(f,1244+i*48,yy+7,44,72,seq[i],i*.6+(1.2 if generated else 0))
        f.line(1450,yy+4,1450,yy+87,stroke='purple',sw=2.2)
        draw_boundary_state_centered(f,1530,yy+43,90)
        f.path(f'M1588 {yy+43}H1655',sw=3.3,arrow=True)
        f.path(f'M1658 {yy-4}H1838V{yy+90}H1658Z',fill='pale_blue',stroke='ink',sw=2.2)
        f.text(1748,yy+34,'Motion',34,anchor='middle',weight='bold')
        f.text(1748,yy+75,'generator',34,anchor='middle',weight='bold')
    f.end()
    f.line(1861,80,1861,638,stroke='#DCE2EB',sw=2)
    f.group('same-target-new-residual-origin')
    f.text(2130,93,'Residual rebasing',38,anchor='middle',weight='bold')
    sampled,recorded,target=(1958,529),(2283,529),(2213,205)
    for origin,sw,dash,alpha in [(sampled,4.6,None,1),(recorded,3.4,'11 9',.6)]:
        dx,dy=target[0]-origin[0],target[1]-origin[1];length=math.hypot(dx,dy)
        f.line(origin[0]+20*dx/length,origin[1]+20*dy/length,target[0]-23*dx/length,target[1]-23*dy/length,stroke='orange',sw=sw,dash=dash,opacity=alpha,arrow=True)
    for name,p,c,r in [('sampled-origin',sampled,'#0769F9',17),('recorded-origin',recorded,'#0769F9',17),('fixed-latent-target',target,'#009EAC',20)]:
        f.raw(f'<circle id="{name}" cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{c}"/>')
    f.text(2213,160,'Target latent',34,anchor='middle',fill='teal',weight='bold')
    f.text(2000,340,'Rebased',32,anchor='middle',fill='orange')
    f.text(2000,382,'residual',32,anchor='middle',fill='orange')
    f.text(2323,350,'Target',32,anchor='middle',fill='orange')
    f.text(2323,392,'residual',32,anchor='middle',fill='orange')
    f.text(1958,577,'Sampled',32,anchor='middle')
    f.text(1958,619,'embedding',32,anchor='middle')
    f.text(2283,577,'Target',32,anchor='middle')
    f.text(2283,619,'embedding',32,anchor='middle')
    f.end();f.save(OUT/'cof-terminology')


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for n in ['structure-detail-training','cof-terminology']:
        if not (OUT/f'{n}-long-reference.png').exists():
            shutil.copy2(NARROW/f'{n}-long-reference.png',OUT/f'{n}-long-reference.png')
    representation();commit()
