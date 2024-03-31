// https://adventofcode.com/2015/day/19

'use strict';

{
    const allMatches = (s, s0) => [...s].reduce((a, _, i) =>
        (s.substr(i, s0.length) === s0 ? [...a, i] : a), []);

    const allReplaceAny = (s, s1, s2) => allMatches(s, s1)
        .map(i => s.slice(0, i) + s2 + s.slice(i + s1.length));

    // Returns all possible results after one step (incl. non-unique ones)
    const nextSteps = (rules, mol) => [].concat(...rules
        .map(rule => allReplaceAny(mol, ...rule)));

    // Uses the first rule that can be reversed
    const prevStep = (rules, mol) => {
        const rule = rules.find(([a, b]) => a === 'e' && mol === b || mol.includes(b));
        return rule && mol.replace(rule[1], rule[0]);
    };

    const minStepsToE = (mol, rules) => {
        const molStart = mol;
        let i = 0;
        while (mol !== 'e') { // re-try until mol resolves to 'e'
            [mol, i] = [molStart, 0];
            rules = [...rules].sort(() => 0.5 - Math.random());
            while (mol && mol !== 'e') {
                mol = prevStep(rules, mol);
                i++;
            }
        }

        return i;
    };

    const minStepsToE2 = mol => { // (c) /u/askalski
        const countF = re => s => (s.match(re) || []).length;
        const tokens = countF(/[A-Z][a-z]?/g);
        const parens = countF(/Rn|Ar/g);
        const commas = countF(/Y/g);
        return tokens(mol) - parens(mol) - 2 * commas(mol) - 1;
    };

    const input = document.body.textContent.trim().split(/\n+/);
    const mol = input.pop();
    const rules = input.map(s => s.split(' => '));

    console.log(new Set(nextSteps(rules, mol)).size);
    console.log(minStepsToE(mol, rules), minStepsToE2(mol));
}
