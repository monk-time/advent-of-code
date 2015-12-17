'use strict';
function parse(line) {
    return line.split(', ').reduce((acc, s) => {
        let [item, n] = s.split(': ');
        acc[item] = +n;
        return acc;
    }, {});
}

let input = document.body.textContent.trim().split('\n'),
    inputMsg = `children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1`;

let msg = parse(inputMsg.replace(/\n/g, ', ')),
    aunts = input.map(s => parse(s.split(/^Sue \d+: /)[1])),
    isSender = matchF => aunt => Object.keys(aunt).every(k => matchF(aunt[k], msg[k], k)),
    theAunt = matchF => aunts.findIndex(isSender(matchF)) + 1;

let exactMatch = (n, m) => n === m,
    gt = (n, m) => n > m,
    lt = (n, m) => n < m,
    ranges = { cats: gt, trees: gt, pomeranians: lt, goldfish: lt },
    roughMatch = (n, m, key) => (key in ranges ? ranges[key] : exactMatch)(n, m);

console.log(theAunt(exactMatch), theAunt(roughMatch));
