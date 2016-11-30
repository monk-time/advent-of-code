'use strict';
function* applyRule([mFrom, mTo], mol) {
    if (mTo === 'e' && mol.length > mFrom.length) {
        return;
    }

    let n = 0;
    while ((n = mol.indexOf(mFrom, n)) !== -1) {
        yield mol.slice(0, n) + mTo + mol.slice(n++ + mFrom.length);
    }
}

function getNextStepGen(input) { // non-unique results
    let rules = input.map(s => s.split(' => '));
    return function*(mol) {
        for (let rule of rules) {
            yield* applyRule(rule, mol);
        }
    };
}

let input = document.body.textContent.trim().split(/\n+/),
    mol = input.pop(),
    nextStep = getNextStepGen(input);

console.log(new Set([...nextStep(mol)]).size);

let countF = re => s => (s.match(re) || []).length,
    tokens = countF(/[A-Z][a-z]?/g),
    parens = countF(/Rn|Ar/g),
    commas = countF(/Y/g);

// (c) /u/askalski, my brute-force ran out of memory
console.log(tokens(mol) - parens(mol) - 2 * commas(mol) - 1);
