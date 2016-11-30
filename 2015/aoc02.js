'use strict';
function paper([l, w, h]) {
    let [lw, wh, hl] = [l * w, w * h, h * l];
    return 2 * (lw + wh + hl) + Math.min(lw, wh, hl);
}

function ribbon([l, w, h]) {
    let minPerim = 2 * Math.min(l + w, w + h, h + l);
    return minPerim + l * w * h;
}

let input = document.querySelector('pre').textContent.trim(),
    parseBox = line => line.split('x').map(s => parseInt(s, 10)),
    boxes = input.split('\n').map(parseBox),
    calc = f => boxes.reduce((sum, box) => sum + f(box), 0);

console.log([paper, ribbon].map(calc));
