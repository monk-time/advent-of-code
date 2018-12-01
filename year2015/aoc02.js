'use strict';

{
    const wrappers = ([l, w, h]) => [
        2 * (l * w + w * h + h * l) + l * w,
        2 * (l + w) + l * w * h,
    ];

    const input = document.body.textContent.trim();
    const parseBox = line => line.split('x').map(s => +s).sort((x, y) => x - y);
    const boxes = input.split('\n').map(parseBox);
    console.log(boxes.map(wrappers)
        .reduce(([p, r], [p0, r0]) => [p + p0, r + r0], [0, 0]));
}
