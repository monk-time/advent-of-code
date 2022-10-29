from typing import Iterable

from PIL import Image

from helpers import read_puzzle

Layer = list[str]
Layers = list[Layer]
WIDTH = 25
HEIGHT = 6


def split_into_layers(arr, size: int) -> Layers:
    return [arr[i:i + size] for i in range(0, len(arr), size)]


def find_layer_with_fewest_0(s: str, width: int, height: int) -> int:
    layers = split_into_layers(s, width * height)
    zeros = [layer.count('0') for layer in layers]
    min_index = zeros.index(min(zeros))
    min_layer = layers[min_index]
    return min_layer.count('1') * min_layer.count('2')


def decode_pixel(pixels: Iterable[str]) -> str:
    return next((px for px in pixels if px != '2'), '2')


def decode_image(s: str, width: int, height: int) -> Layer:
    layers = split_into_layers(s, width * height)
    return [decode_pixel(layer[i] for layer in layers)
            for i in range(width * height)]


def paint(layer: Layer, width: int, height: int):
    colors = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
    pixels = [colors[int(px)] for px in layer]
    im = Image.new('RGB', (width, height))
    im.putdata(pixels)
    im.show()


def solve() -> tuple[int, int]:
    puzzle = read_puzzle()
    paint(decode_image(puzzle, WIDTH, HEIGHT), WIDTH, HEIGHT)
    return find_layer_with_fewest_0(puzzle, WIDTH, HEIGHT), 0


if __name__ == '__main__':
    print(solve())
