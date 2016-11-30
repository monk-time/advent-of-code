'use strict';
let capitalize = s => s[0].toUpperCase() + s.slice(1),
    extend = (obj, src) => Object.assign({}, obj, src),
    log = s => {
        if (debug) {
            console.log(s);
        }
    };

let getEffect = ({ label, timer, armor, dmg, mana }) => ({
    label, timer,
    apply({ player, boss, timers }) {
        let timersNew = extend(timers, { [label]: timers[label] - 1 });
        let shieldDown = armor && (timersNew[label] === 0);
        let playerNew = extend(player, {
            armor: shieldDown ? 0 : armor || player.armor, // removes/sets/leaves armor
            mana: player.mana + (mana || 0)
        });
        let bossNew = dmg ? extend(boss, { hp: boss.hp - dmg }) : boss;

        let msg = capitalize(label);
        if (armor && playerNew.armor !== player.armor) {
            let prefix = playerNew.armor > player.armor ? 'in' : 'de';
            msg += ` ${prefix}creases armor by ${armor}; its`;
        } else if (dmg) {
            msg += ` deals ${dmg} damage; its`;
        } else if (mana) {
            msg += ` provides ${mana} mana; its`;
        } else {
            msg += '\'s';
        }

        log(msg + ` timer is now ${timersNew[label]}.`);
        if (timersNew[label] === 0) {
            log(`${capitalize(label)} wears off.`);
        }

        return { player: playerNew, boss: bossNew, timers: timersNew };
    }
});

let getSpell = ({ label, cost, dmg, hp, effect }) => ({
    label, cost,
    cast({ player, boss, timers }) {
        if (cost > player.mana) {
            throw new Error(`Can't cast ${capitalize(label)}: not enough mana`);
        }

        let msg = `Player casts ${capitalize(label)}`;
        if (effect) {
            if (timers[effect.label] > 0) {
                throw new Error(`Can't cast ${capitalize(effect.label)}: ` +
                                'the effect is already active');
            }

            log(msg + '.');
            let playerNew = extend(player, { mana: player.mana - cost }),
                timersNew = extend(timers, { [effect.label]: effect.timer });
            return { player: playerNew, boss, timers: timersNew };
        }

        let playerNew = extend(player, {
            hp: player.hp + (hp || 0),
            mana: player.mana - cost
        });
        let bossNew = dmg ? extend(boss, { hp: boss.hp - dmg }) : boss;

        msg += (dmg ? `, dealing ${dmg} damage` : '') +
            (hp ? `, healing ${hp} hit points` : '') + '.';
        log(msg);
        return { player: playerNew, boss: bossNew, timers };
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

function logStats(player, boss) {
    log(`- Player has ${player.hp} hit points, ${player.armor} armor, ${player.mana} mana`);
    log(`- Boss has ${boss.hp} hit points`);
}

function nextRound(spell, state) {
    let winner;
    log('\n-- Player turn --');
    logStats(state.player, state.boss);
    if (hard) {
        let playerNew = extend(state.player, { hp: state.player.hp - 1 });
        state = extend(state, { player: playerNew });
        log('Player loses 1 hit point.');
        if (state.player.hp <= 0) {
            log('> (!) Player loses.');
            winner = 'boss';
            return { state, winner };
        }
    }

    state = applyAllEffects(state);
    try {
        state = spellsObj[spell].cast(state);
    } catch (e) {
        log(e.message);
        log('> (!) Player loses.');
        winner = 'boss';
        return { state, winner };
    }

    if (state.boss.hp <= 0) {
        log('> (!) Boss is dead, player wins.');
        winner = 'player';
        return { state, winner };
    }

    log('\n-- Boss turn --');
    logStats(state.player, state.boss);
    state = applyAllEffects(state);
    if (state.boss.hp <= 0) {
        log('> (!) Boss is dead, player wins.');
        winner = 'player';
        return { state, winner };
    }

    let newHp = state.player.hp - Math.max(1, state.boss.dmg - state.player.armor),
        playerNew = extend(state.player, { hp: newHp });
    state = extend(state, { player: playerNew });
    log(`Boss attacks for ${state.boss.dmg - state.player.armor} damage!`);
    if (state.player.hp <= 0) {
        log('> (!) Player loses.');
        winner = 'boss';
    }

    return { state, winner };
}

function simulate(spellSeq, state) {
    let winner, manaSpent = 0;
    for (let spell of spellSeq) {
        ({ state, winner } = nextRound(spell, state));
        manaSpent += spellsObj[spell].cost;
        if (winner) {
            break;
        }
    }

    return { winner, manaSpent };
}

function minWinningSeq(state, spellsObj) {
    const spells = Object.keys(spellsObj),
          costs = spells.map(k => spellsObj[k].cost);
    let stack = {
            castedInd: [0],
            state: []
        },
        manaSpent = costs[0],
        minMana = Infinity,
        minStack,
        winner;

    while (stack.castedInd.length) {
        stack.state.push(state); // game state before casting
        let lastSpell = spells[stack.castedInd[stack.castedInd.length - 1]];
        ({ state, winner } = nextRound(lastSpell, state));
        if (!winner) { // cast next spell
            stack.castedInd.push(0);
            manaSpent += costs[0];
        } else {
            if (winner === 'player' && (manaSpent < minMana)) {
                minStack = [...stack.castedInd];
                minMana = manaSpent;
            }

            let head = stack.castedInd.pop();
            state = stack.state.pop();
            manaSpent -= costs[head];
            while (stack.castedInd.length && head === spells.length - 1) {
                head = stack.castedInd.pop();
                state = stack.state.pop();
                manaSpent -= costs[head];
            }

            if (head < spells.length - 1) {
                stack.castedInd.push(head + 1);
                manaSpent += costs[head + 1];
            }
        }
    }

    if (minStack) {
        minStack = minStack.map(k => spells[k]);
    }

    return { minStack, minMana };
}

// let [hp, dmg] = document.body.textContent.match(/\d+/g).map(s => +s),
//     boss = { hp, dmg },
// let boss = { hp: 14, dmg: 8 },
//     player = { hp: 10, mana: 250, armor: 0 },
let boss = { hp: 71, dmg: 10 },
    player = { hp: 50, mana: 500, armor: 0 },
    state = { player, boss, timers: {} },
    debug = false,
    hard = true;

// simulate(['recharge', 'shield', 'drain', 'poison', 'missile'], state)
console.time('main');
console.log(minWinningSeq(state, spellsObj));
console.timeEnd('main');
// part 1 takes ~ 5 min, part 2 ~ 10 sec
