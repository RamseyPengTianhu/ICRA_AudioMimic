"""Replace the overview image in an upstream PDF without reflowing its typography.
Usage: python scripts/place_overview_in_pdf.py upstream.pdf output.pdf
Requires PyMuPDF. The SVG's PDF companion is inserted as vector PDF content.
"""
import sys,re
from pathlib import Path
import pymupdf
root=Path(__file__).resolve().parents[1]
source,out=map(Path,sys.argv[1:3])
doc=pymupdf.open(source);figure=pymupdf.open(root/'figures/foredance/overview.pdf')
matches=[]
for page in doc:
 if 'ForeDance overview.' not in page.get_text():continue
 for entry in page.get_images(full=True):
  if entry[2:4]==(1685,934):matches.append((page.number,entry))
assert len(matches)==1,matches
index,entry=matches[0];page=doc[index];rects=page.get_image_rects(entry[0]);assert len(rects)==1
pattern=rb'/'+re.escape(entry[7].encode())+rb'\s+Do\b'
count=0
for xref in page.get_contents():
 data=doc.xref_stream(xref);replacement,n=re.subn(pattern,b'',data)
 if n:doc.update_stream(xref,replacement);count+=n
assert count==1
page.show_pdf_page(rects[0],figure,0,overlay=True)
doc.save(out,garbage=4,deflate=True)
print(f'Replaced overview on page {index+1}; retained {len(doc)} pages.')
