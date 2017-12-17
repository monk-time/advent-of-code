'use strict';

{
    const steps = +document.querySelector('.puzzle-input').textContent;
    const buffer = [0];
    let pos = 0;
    for (let i = 1; i <= 2017; i++) {
        pos = ((pos + steps) % buffer.length) + 1;
        buffer.splice(pos, 0, i);
    }

    console.log(buffer[(pos + 1) % buffer.length]);

    pos = 0;
    let afterZero = 0;
    for (let i = 1; i <= 50000000; i++) {
        pos = ((pos + steps) % i) + 1;
        if (pos === 1) afterZero = i;
    }

    console.log(afterZero);
}
