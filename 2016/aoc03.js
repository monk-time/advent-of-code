'use strict';

{
    const input = document.body.textContent.match(/(.+\n){3}/g),
        parse = s => s.trim().split(/\s+/).map(d => +d),
        threes = input.map(parse),
        horz = ([a, b, c, d, e, f, g, h, i]) => [[a, b, c], [d, e, f], [g, h, i]],
        vert = ([a, b, c, d, e, f, g, h, i]) => [[a, d, g], [b, e, h], [c, f, i]],
        valid = arr => (([a, b, c]) => a + b > c)(arr.sort((x, y) => x - y)),
        count = f => [].concat(...threes.map(f)).filter(valid).length;

    console.log(...[horz, vert].map(count));
}
