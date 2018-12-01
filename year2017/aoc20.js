'use strict';

{
    const parse = s => s.split(', ').map(s2 => s2.match(/-?\d+/g).map(Number));
    const input = document.body.textContent.trim().split('\n').map(parse);
    const add = ([a, b, c], [x, y, z]) => [a + x, b + y, c + z];
    const eq = ([a, b, c], [x, y, z]) => a === x && b === y && c === z;
    const oneStep = ([p, v, a]) => [add(add(p, v), a), add(v, a), a];

    let particles = [...input];
    const absAccels = particles.map(([,, a]) => a.map(Math.abs).reduce((x, y) => x + y));
    const minAbs = Math.min(...absAccels);
    // There might be multiple particles with equal absolute acceleration
    console.log(absAccels.reduce((acc, n, i) => (n === minAbs ? [...acc, i] : acc), []));

    particles = [...input];
    // 100 seems to be enough on this input
    for (let i = 0; i < 100; i++) {
        particles = particles.map(oneStep)
            .filter(([p], _, arr) => arr.filter(([p2]) => eq(p, p2)).length === 1);
    }

    console.log(particles.length);
}
