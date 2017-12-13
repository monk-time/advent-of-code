'use strict';

{
    const input = document.body.textContent.trim();
    const scanners = input.split('\n').map(s => s.match(/\d+/g).map(Number));
    const walk = delay => scanners
        .filter(([d, r]) => (delay + d) % (2 * (r - 1)) === 0)
        .reduce((severity, [d, r]) => severity + (delay + d) * r, 0);

    let delay = -1;
    while (walk(++delay) !== 0);
    console.log([walk(0), delay]); // 6 sec
}
