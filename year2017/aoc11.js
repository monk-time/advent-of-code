// https://adventofcode.com/2017/day/11

'use strict';

{
    // Using axial coordinates for hex grid
    const delta = { n: [0, -1], s: [0, 1], ne: [1, -1], sw: [-1, 1], nw: [-1, 0], se: [1, 0] };
    const mover = ([dq, dr]) => ([q, r]) => [q + dq, r + dr];
    const dist = ([q, r]) => (Math.abs(q) + Math.abs(q + r) + Math.abs(r)) / 2;
    const trackMax = ({ max }, pos) => ({ pos, max: Math.max(max, dist(pos)) });
    const start = { pos: [0, 0], max: 0 };

    const input = document.body.textContent.trim();
    const moves = input.split(',').map(s => mover(delta[s]));
    const { pos, max } = moves.reduce((acc, move) => trackMax(acc, move(acc.pos)), start);
    console.log(dist(pos), max);
}
