'use strict';
function* applyRule([mTo, mFrom], mol) { // applies rules in reverse
    if (mTo === 'e' && mol.length > mFrom.length) {
        return;
    }

    if (mol.includes(mFrom)) {
        yield mol.replace(mFrom, mTo);
    }
}

let tokens = s => s.match(/[A-Z][a-z]?/g).length;
function getNextStepGen(input) { // non-unique results
    let rules = input
        .map(s => s.split(' => '))
        // .sort((a, b) => tokens(b[1]) - tokens(a[1])); // didn't work for my input (bad luck)
        .sort(() => 0.5 - Math.random());
    return function*(mol) {
        for (let rule of rules) {
            yield* applyRule(rule, mol);
        }
    };
}

let input = document.body.textContent.trim().split(/\n+/),
    mStart = input.pop(),
    nextStep = getNextStepGen(input);

console.time('main');

let [mol, i] = [mStart, 0];
while (mol && mol !== 'e') {
    mol = nextStep(mol).next().value;
    i++;
    console.log(i, mol);
}

//console.log(i); // re-try several times until mol resolves to 'e'

console.timeEnd('main');
