'use strict';

{
    const input = document.body.textContent.match(/(.+\n){3}/g);
    const parse = s => s.trim().split(/\s+/).map(d => +d);
    const threes = input.map(parse);
    const horz = ([a, b, c, d, e, f, g, h, i]) => [[a, b, c], [d, e, f], [g, h, i]];
    const vert = ([a, b, c, d, e, f, g, h, i]) => [[a, d, g], [b, e, h], [c, f, i]];
    const valid = arr => (([a, b, c]) => a + b > c)(arr.sort((x, y) => x - y));
    const count = f => [].concat(...threes.map(f)).filter(valid).length;

    console.log(...[horz, vert].map(count));
}
