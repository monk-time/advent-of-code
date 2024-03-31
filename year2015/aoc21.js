// https://adventofcode.com/2015/day/21

'use strict';

{
    const weapons = [[8,  4, 0], [10, 5, 0], [25, 6, 0], [40, 7, 0], [74,  8, 0]];
    const armors  = [[13, 0, 1], [31, 0, 2], [53, 0, 3], [75, 0, 4], [102, 0, 5]];
    const rings   = [[20, 0, 1], [25, 1, 0], [40, 0, 2], [50, 2, 0], [80,  0, 3], [100, 3, 0]];
    rings.unshift([0, 0, 0]);  // for sets with 1 ring
    armors.unshift([0, 0, 0]); // for sets with no armor

    const arrSum = (a, b, c, d) => a.map((el, i) => el + b[i] + c[i] + d[i]);
    const genItems = function* () {
        for (const w of weapons) {
            for (const ar of armors) {
                yield arrSum(w, ar, [0, 0, 0], [0, 0, 0]); // for sets with 0 rings
                for (let r1i = 0; r1i < rings.length - 1; r1i++) {
                    for (let r2i = r1i + 1; r2i < rings.length; r2i++) {
                        yield arrSum(w, ar, rings[r1i], rings[r2i]);
                    }
                }
            }
        }
    };

    const dps = (dmg, armor) => Math.max(1, dmg - armor);
    const hitsToKill = (hp, armor, dmg) => Math.ceil(hp / dps(dmg, armor));

    const playerWins = ([hpB, dmgB, armorB], hpP, [, dmgP, armorP]) =>
        hitsToKill(hpB, armorB, dmgP) <= hitsToKill(hpP, armorP, dmgB);

    const boss = document.body.textContent.match(/\d+/g).map(Number);
    let [minCostToWin, maxCostToLose] = [Infinity, 0];
    for (const items of genItems()) {
        if (playerWins(boss, 100, items)) {
            minCostToWin = Math.min(minCostToWin, items[0]);
        } else {
            maxCostToLose = Math.max(maxCostToLose, items[0]);
        }
    }

    console.log(minCostToWin, maxCostToLose);
}
