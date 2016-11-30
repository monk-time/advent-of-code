'use strict';
let extend = (obj, src) => Object.assign({}, obj, src);

let getEffect = ({ label, timer, armor, dmg, mana }) => ({
    label, timer,
    apply({ player, boss, timers }) {
        timers = extend(timers, { [label]: timers[label] - 1 });
        boss = dmg ? extend(boss, { hp: boss.hp - dmg }) : boss;
        let shieldDown = armor && (timers[label] === 0);

        player = extend(player, {
            armor: shieldDown ? 0 : armor || player.armor, // removes/sets/keeps armor
            mana: player.mana + (mana || 0)
        });

        return { player, boss, timers };
    }
});

let getSpell = ({ label, cost, dmg, hp, effect }) => ({
    label, cost,
    cast({ player, boss, timers }) {
        if (cost > player.mana) {
            throw new Error('not enough mana');
        }

        if (effect) {
            if (timers[effect.label] > 0) {
                throw new Error('the effect is already active');
            }

            player = extend(player, { mana: player.mana - cost });
            timers = extend(timers, { [effect.label]: effect.timer });
            return { player, boss, timers };
        }

        player = extend(player, {
            hp: player.hp + (hp || 0),
            mana: player.mana - cost
        });
        boss = dmg ? extend(boss, { hp: boss.hp - dmg }) : boss;

        return { player, boss, timers };
    }
});

let effects = {
    shield:   getEffect({ label: 'shield',   timer: 6, armor: 7 }),
    poison:   getEffect({ label: 'poison',   timer: 6, dmg: 3 }),
    recharge: getEffect({ label: 'recharge', timer: 5, mana: 101 })
};

let spells = [
    getSpell({ label: 'missile',  cost: 53,  dmg: 4 }),
    getSpell({ label: 'drain',    cost: 73,  dmg: 2, hp: 2 }),
    getSpell({ label: 'shield',   cost: 113, effect: effects.shield }),
    getSpell({ label: 'poison',   cost: 173, effect: effects.poison }),
    getSpell({ label: 'recharge', cost: 229, effect: effects.recharge })
];

let spellsObj = spells.reduce((obj, spell) => {
    obj[spell.label] = spell; return obj;
}, {});

function applyAllEffects(state) {
    let activeEffects = Object.keys(state.timers).filter(t => state.timers[t] > 0);
    for (let effect of activeEffects) {
        state = effects[effect].apply(state);
    }

    return state;
}

function nextRound(spell, state) {
    if (hard) {
        let player = extend(state.player, { hp: state.player.hp - 1 });
        state = extend(state, { player });
        if (state.player.hp <= 0) {
            return { state, winner: 'boss' };
        }
    }

    state = applyAllEffects(state);
    try {
        state = spellsObj[spell].cast(state);
    } catch (e) {
        return { state, winner: 'boss' };
    }

    if (state.boss.hp <= 0) {
        return { state, winner: 'player' };
    }

    state = applyAllEffects(state);
    if (state.boss.hp <= 0) {
        return { state, winner: 'player' };
    }

    let hp = state.player.hp - Math.max(1, state.boss.dmg - state.player.armor),
        player = extend(state.player, { hp });
    state = extend(state, { player });
    let winner = (state.player.hp <= 0) ? 'boss' : undefined;

    return { state, winner };
}

function minWinningSeq(state, spellsObj) {
    const spells = Object.keys(spellsObj),
          costs = spells.map(k => spellsObj[k].cost);
    let stack = {
            castedInd: [0],
            state: []
        },
        manaSpent = costs[0],
        minMana = { mana: Infinity, seq: [] },
        winner;

    while (stack.castedInd.length) {
        stack.state.push(state); // game state before casting
        let lastSpell = spells[stack.castedInd[stack.castedInd.length - 1]];
        ({ state, winner } = nextRound(lastSpell, state));
        let overMin = manaSpent >= minMana.mana;
        if (!overMin && !winner) { // cast next spell
            stack.castedInd.push(0);
            manaSpent += costs[0];
        } else {
            if (!overMin && winner === 'player') {
                minMana = { mana: manaSpent, seq: stack.castedInd.map(i => spells[i]) };
            }

            let head;
            do {
                head = stack.castedInd.pop();
                state = stack.state.pop();
                manaSpent -= costs[head];
            } while (stack.castedInd.length && head === spells.length - 1);

            if (head < spells.length - 1) {
                stack.castedInd.push(head + 1);
                manaSpent += costs[head + 1];
            }
        }
    }

    return minMana;
}

let [hp, dmg] = document.body.textContent.match(/\d+/g).map(s => +s),
    player = { hp: 50, mana: 500, armor: 0 },
    state = { player, boss: { hp, dmg }, timers: {} },
    hard = false;

console.time('main');
console.log(minWinningSeq(state, spellsObj));
console.timeEnd('main');
// part 1 takes ~ 2 min, part 2 - 7 sec
