// https://adventofcode.com/2015/day/16

'use strict';

{
    const parseAunt = line => line.split(', ').map(s => s.split(': '))
        .reduce((acc, [item, n]) => ({ ...acc, [item]: +n }), {});

    const input = document.body.textContent.trim().split('\n');
    const inputMsg = 'children: 3, cats: 7, samoyeds: 2, pomeranians: 3, ' +
        'akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1';
    const msg = parseAunt(inputMsg);
    const aunts = input.map(s => parseAunt(s.split(/^Sue \d+: /)[1]));
    const isSender = matchF => aunt => Object.keys(aunt)
        .every(k => matchF(aunt[k], msg[k], k));
    const theAunt = matchF => aunts.findIndex(isSender(matchF)) + 1;

    const matchExact = (n, m) => n === m;
    const gt = (n, m) => n > m;
    const lt = (n, m) => n < m;
    const ranges = { cats: gt, trees: gt, pomeranians: lt, goldfish: lt };
    const matchRough = (n, m, key) => (ranges[key] || matchExact)(n, m);

    console.log([matchExact, matchRough].map(theAunt));
}
