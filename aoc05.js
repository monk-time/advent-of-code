'use strict';
let input = document.querySelector('pre').textContent.trim().split('\n'),
    countNice = regexes => input.filter(s => regexes.every(re => re.test(s))).length;

console.log('Part 1:', countNice([/(?:[aeiou].*?){3}/, /(\w)\1/, /^(?:(?!ab|cd|pq|xy).)+$/]));
console.log('Part 2:', countNice([/(\w{2}).*?\1/, /(\w).\1/]));
