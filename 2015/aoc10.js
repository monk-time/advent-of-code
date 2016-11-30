'use strict';
let input = document.querySelector('.puzzle-input').textContent,
    lookAndSay = s => s.match(/(.)\1*/g).map(s => s.length + s[0]).join(''),
    iterate = (n, s) => [...new Array(n)].reduce(lookAndSay, s);

let step40 = iterate(40, input);
console.log(step40.length, iterate(10, step40).length);
