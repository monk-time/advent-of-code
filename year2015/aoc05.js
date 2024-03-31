// https://adventofcode.com/2015/day/5

'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const countNice = regexes =>
        input.filter(s => regexes.every(re => re.test(s))).length;

    console.log(
        countNice([/(?:[aeiou].*?){3}/, /(\w)\1/, /^(?:(?!ab|cd|pq|xy).)+$/]),
        countNice([/(\w{2}).*?\1/, /(\w).\1/]),
    );
}
