import random

from PIL import Image, ImageDraw

from aoc03 import parse_puzzle

IMG_SIZE = (1000, 1000)
random.seed(0)

im = Image.new('RGB', IMG_SIZE, 'white')
draw = ImageDraw.Draw(im, 'RGBA')

claims = parse_puzzle()
for c in claims:
    color = '#{:06x}AA'.format(random.randint(0, 0xFFFFFF))
    draw.rectangle((c.left, c.top, c.left + c.width - 1, c.top + c.height - 1),
                   fill=color, outline='black')

im.save('aoc03.png', 'PNG')
