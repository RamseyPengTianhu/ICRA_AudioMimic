"""Use the overview's existing pose glyph as the shared boundary-state master."""
from pathlib import Path
import re

MASTER=Path(__file__).resolve().parents[1]/'figures/foredance/boundary-state-icon.svg'
GLYPH=re.search(r'(<g\b.*</g>)',MASTER.read_text(),re.S).group(1)

def draw_boundary_state(figure,x,y,height=84):
    figure.raw(f'<g data-icon="boundary-state" transform="translate({x} {y}) scale({height/28})">{GLYPH}</g>')


def draw_boundary_state_centered(figure,cx,cy,height=84):
    """Center the master's visible stroked bounds on a diagram port.

    The unchanged glyph occupies x=[2.15,18.25], y=[1.1,27.05], including
    round caps and the filled head, rather than its larger SVG viewport.
    """
    scale=height/28
    x,y=cx-10.2*scale,cy-14.075*scale
    figure.raw(f'<g data-icon="boundary-state" data-center-x="{cx}" data-center-y="{cy}" '
               f'transform="translate({x} {y}) scale({scale})">{GLYPH}</g>')
