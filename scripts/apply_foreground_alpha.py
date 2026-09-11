"""Apply an approved foreground mask without changing any original RGB values.

Usage: python apply_foreground_alpha.py SOURCE_RGB.png MASK.png OUTPUT_RGBA.png
The source file is never overwritten. Mask values below 8 become transparent;
values above 247 become opaque; all other edge values retain their softness.
"""
from pathlib import Path
import sys
import numpy as np
from PIL import Image

source, mask, output = map(Path, sys.argv[1:])
assert source.resolve() != output.resolve(), 'Keep the original file'
rgb = Image.open(source).convert('RGB')
alpha = np.array(Image.open(mask).convert('L'))
assert rgb.size == (alpha.shape[1], alpha.shape[0])
alpha[alpha < 8] = 0
alpha[alpha > 247] = 255
result = rgb.copy()
result.putalpha(Image.fromarray(alpha))
result.save(output)
check = Image.open(output)
assert check.mode == 'RGBA' and check.getchannel('A').getextrema()[0] == 0
assert np.array_equal(np.array(check)[:, :, :3], np.array(rgb))
print(f'{output.name}: alpha applied; all original RGB values unchanged')
