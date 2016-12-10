'use strict';

{
    const parse = s => s.match(/(value|bot) (\d+).*?(bot|output) (\d+)(?:.*?(bot|output) (\d+))?/);
    const [bots, outputs] = [[], []];
    const storage = s => s === 'bot' ? bots : outputs;
    const sort = arr => arr.sort((a, b) => a - b);
    const parseSet = ([, , val, , bot]) => {
        bots[+bot] = sort([...bots[+bot] || [], +val]);
    };
    const parseMove = ([, , src, type1, i1, type2, i2]) => {
        storage(type1)[+i1] = [...storage(type1)[+i1] || [], { bot: +src, chip: 0 }];
        storage(type2)[+i2] = [...storage(type2)[+i2] || [], { bot: +src, chip: 1 }];
    };
    const ops = { value: parseSet, bot: parseMove };

    const run = a => a.forEach(m => ops[m[1]](m));
    const input = document.body.textContent.trim().split('\n').map(parse);
    run(input);

    const isFull = b => b.every(chip => typeof chip === 'number');
    const canUpdate = x => typeof x === 'object' && isFull(bots[x.bot]);
    while (!bots.every(isFull) && !outputs.every(isFull)) {
        for (let b of bots) {
            for (let chip of [0, 1]) {
                if (canUpdate(b[chip])) {
                    b[chip] = bots[b[chip].bot][b[chip].chip];
                }
            }
            if (isFull(b)) {
                b = sort(b);
            }
        }
        for (let o of outputs) {
            if (canUpdate(o[0])) {
                o[0] = bots[o[0].bot][o[0].chip];
            }
        }
    }

    console.log([
        bots.findIndex(([l, h]) => l === 17 && h === 61),
        outputs.slice(0, 3).reduce((acc, [o]) => acc * o, 1)]);
}
