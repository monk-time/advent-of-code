// https://adventofcode.com/2015/day/22

'use strict';

{
    const newGame = () => {
        const [hp, dmg] = document.body.textContent.match(/\d+/g).map(Number);
        const player = { hp: 50, mana: 500, armor: 0 };
        return { player, boss: { hp, dmg }, timers: {} };
    };

    const getEffect = ({ label, timer, armor, dmg, mana }) => ({
        label,
        timer,
        apply: ({ player, boss, timers }) => ({
            player: {
                hp: player.hp,
                mana: player.mana + (mana || 0),
                armor: armor && (timers[label] === 1) ?
                    0 : armor || player.armor, // remove or set/keep armor
            },
            boss: dmg ? { hp: boss.hp - dmg, dmg: boss.dmg } : boss,
            timers: { ...timers, [label]: timers[label] - 1 },
        }),
    });

    const getSpell = ({ label, cost, dmg, hp, effect }) => ({
        label,
        cost,
        cast: ({ player, boss, timers }) =>
            (effect && timers[effect.label] > 0 || cost > player.mana ? null : {
                player: {
                    hp: player.hp + (hp || 0),
                    mana: player.mana - cost,
                    armor: player.armor,
                },
                boss: dmg ? { ...boss, hp: boss.hp - dmg } : boss,
                timers: effect ? { ...timers, [effect.label]: effect.timer } : timers,
            }),
    });

    const effects = {
        shield:   getEffect({ label: 'shield',   timer: 6, armor: 7 }),
        poison:   getEffect({ label: 'poison',   timer: 6, dmg: 3 }),
        recharge: getEffect({ label: 'recharge', timer: 5, mana: 101 }),
    };

    const spells = [
        getSpell({ label: 'missile',  cost: 53,  dmg: 4 }),
        getSpell({ label: 'drain',    cost: 73,  dmg: 2, hp: 2 }),
        getSpell({ label: 'shield',   cost: 113, effect: effects.shield }),
        getSpell({ label: 'poison',   cost: 173, effect: effects.poison }),
        getSpell({ label: 'recharge', cost: 229, effect: effects.recharge }),
    ];

    const applyAllEffects = state => Object.entries(state.timers).reduce(
        (newState, [e, t]) => (t > 0 ? effects[e].apply(newState) : newState),
        state,
    );

    const nextRound = (state, spell, hard) => {
        if (hard) {
            const player = { ...state.player, hp: state.player.hp - 1 };
            state = { ...state, player };
            if (state.player.hp <= 0) return { state, winner: 'boss' };
        }

        state = applyAllEffects(state); // player turn
        state = spell.cast(state);
        if (!state) return { state, winner: 'boss' };
        if (state.boss.hp <= 0) return { state, winner: 'player' };
        state = applyAllEffects(state); // boss turn
        if (state.boss.hp <= 0) return { state, winner: 'player' };

        const hp = state.player.hp - Math.max(1, state.boss.dmg - state.player.armor);
        const player = { ...state.player, hp };
        state = { ...state, player };
        const winner = state.player.hp <= 0 ? 'boss' : undefined;

        return { state, winner };
    };

    const minWinningSeq = (state, hard) => {
        const costs = spells.map(({ cost }) => cost);
        const stack = [];
        let [manaSpent, minMana, next, winner] = [0, Infinity, 0];
        // Brute-force over all combinations of spells, starting from the first one
        while (next < spells.length) { // depth-first search
            stack.push([state, next]); // game state before casting
            ({ state, winner } = nextRound(state, spells[next], hard));
            manaSpent += costs[next];
            const overMin = manaSpent >= minMana;
            if (!overMin && winner === 'player') minMana = manaSpent;
            if (!overMin && !winner) {
                next = 0;
                continue; // cast the next spell
            }

            do { // rewind if lost or exceeded the minimum to win
                [state, next] = stack.pop();
                manaSpent -= costs[next];
            } while (stack.length && next === spells.length - 1);

            next++;
        }

        return minMana;
    };

    console.log([false, true].map(b => minWinningSeq(newGame(), b))); // 16 sec
}
