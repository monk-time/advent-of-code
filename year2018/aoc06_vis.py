import random

from PIL import Image, ImageColor

from aoc06 import fill_grid, grid_size, parse_coords
from helpers import read_puzzle

random.seed(0)

points = parse_coords(read_puzzle())
colors = [ImageColor.getrgb(v)
          for k, v in ImageColor.colormap.items()
          if k != 'black']
random.shuffle(colors)
colors = {p: colors[i] for i, p in enumerate(points)}
colors['.'] = (0, 0, 0)

xs, ys = grid_size(points)
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

grid = fill_grid(points)

IMG_SIZE = (max_x - min_x + 1, max_y - min_y + 1)
im = Image.new('RGB', IMG_SIZE, 'white')
px = im.load()
for x, y in grid:
    px[x - min_x, y - min_y] = colors[grid[(x, y)]]

im.save('aoc06.png', 'PNG')
