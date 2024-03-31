// https://adventofcode.com/2015/day/10

'use strict';

{
    const input = document.querySelector('.puzzle-input').textContent;
    const lookAndSay = s => s.match(/(.)\1*/g).map(t => t.length + t[0]).join('');
    const iterate = (n, s) => [...new Array(n)].reduce(lookAndSay, s);

    const step40 = iterate(40, input);
    console.log(step40.length, iterate(10, step40).length);
}
