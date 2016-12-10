'use strict';

{
    class Storage {
        setChip(chip) {
            this._chips = [...this._chips || [], chip];
            this.notify();
        }
        attach(...bots) {
            this.listeners = [...this.listeners || [], ...bots];
            this.notify();
        }
        notify() {
            if (this._chips && this._chips.length === 2) {
                this._chips.sort((a, b) => a - b);
                (this.listeners || []).forEach((bot, i) => {
                    bot.setChip(this._chips[i]);
                });
            }
        }
    }
    const [bots, outputs] = [[], []],
        type = t => t === 'bot' ? bots : outputs,
        get = (t, id) => type(t)[id] || (type(t)[id] = new Storage()),
        value = ([, , val, , id]) => get('bot', +id).setChip(+val),
        bot = ([, , src, t1, id1, t2, id2]) => get('bot', +src).attach(get(t1, +id1), get(t2, +id2)),
        run = a => a.forEach(m => ({ value, bot })[m[1]](m)),
        parse = s => s.match(/(value|bot) (\d+).*?(bot|output) (\d+)(?:.*?(bot|output) (\d+))?/),
        input = document.body.textContent.trim().split('\n').map(parse);
    run(input);

    console.log(
        bots.findIndex(({ _chips: [l, h] }) => l === 17 && h === 61),
        outputs.slice(0, 3).reduce((acc, { _chips: [v] }) => acc * v, 1)
    );
}
