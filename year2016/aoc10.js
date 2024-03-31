// https://adventofcode.com/2016/day/10

/* eslint-disable no-return-assign */

'use strict';

{
    class Storage {
        constructor() {
            [this.chips, this.listeners] = [[], []];
        }

        setChip(chip) {
            this.chips.push(chip);
            this.notify();
        }

        attach(...listeners) {
            this.listeners.push(...listeners);
            this.notify();
        }

        notify() {
            if (this.chips.length !== this.listeners.length) return;
            this.chips.sort((a, b) => a - b);
            this.listeners.forEach((storage, i) => {
                storage.setChip(this.chips[i]);
            });
        }
    }

    const [bots, bins] = [[], []];
    const type = t => (t === 'bot' ? bots : bins);
    const get = (t, id) => type(t)[id] || (type(t)[id] = new Storage());
    const value = ([, , val, , id]) =>
        get('bot', +id).setChip(+val);
    const bot = ([, , src, t1, id1, t2, id2]) =>
        get('bot', +src).attach(get(t1, +id1), get(t2, +id2));
    const run = a => a.forEach(m => ({ value, bot })[m[1]](m));
    const parse = s => s.match(/(value|bot) (\d+).*?(bot|output) (\d+)(?:.*?(bot|output) (\d+))?/);
    const input = document.body.textContent.trim().split('\n').map(parse);
    run(input);

    console.log(
        bots.findIndex(({ chips: [l, h] }) => l === 17 && h === 61),
        bins.slice(0, 3).reduce((acc, { chips: [v] }) => acc * v, 1),
    );
}
