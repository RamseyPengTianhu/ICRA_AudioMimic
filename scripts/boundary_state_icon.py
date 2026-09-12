"""Use the overview's existing pose glyph as the shared boundary-state master."""
from pathlib import Path
import re

MASTER=Path(__file__).resolve().parents[1]/'figures/foredance/boundary-state-icon.svg'
GLYPH=re.search(r'(<g\b.*</g>)',MASTER.read_text(),re.S).group(1)

def draw_boundary_state(figure,x,y,height=84):
    figure.raw(f'<g data-icon="boundary-state" transform="translate({x} {y}) scale({height/28})">{GLYPH}</g>')
