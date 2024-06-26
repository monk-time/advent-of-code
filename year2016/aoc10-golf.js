// https://adventofcode.com/2016/day/10

/* eslint-disable no-return-assign, no-sequences */

'use strict';

{
    /*
    Alternative golfed solution inspired by: https://github.com/NiXXeD/adventofcode/blob/deeca50d7c75102afdbc61ae3aecfb05552937bb/2016/day10/part1.js
    Notes:
      Bot values are stored in lambdas instead of arrays.
      Proxy overloads the set operation of the bot array so that bins and bots
        can be updated similarly.
      A crucial step for this semi-functional solution was the realization
        that there's no way around looping over one type of instructions first.
    */
    const parse = s => s.match(/(\d+).*?(bot|output) (\d+)(?:.*?(bot|output) (\d+))?/);
    const input = document.body.textContent.trim().split('\n').map(parse);
    const bins = [];
    const bots = new Proxy([], { set: (o, id, val) => (o[id] = (o[id] || (f => f))(val), val) });
    const move = (t, val, id) => (t === 'bot' ? bots : bins)[id] = val;
    const getVal = ([, val, , id]) => bots[+id] = +val;
    const getBot = ([, id, tL, iL, tH, iH]) => bots[+id] = a => b =>
        [move(tL, Math.min(a, b), +iL), move(tH, Math.max(a, b), +iH)];
    input.filter(m =>  m[4]).forEach(getBot);
    input.filter(m => !m[4]).forEach(getVal);

    console.log(
        bots.findIndex(([l, h]) => l === 17 && h === 61),
        bins[0] * bins[1] * bins[2],
    );
}
