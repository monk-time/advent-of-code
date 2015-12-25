'use strict';
function* genItems() {
    let weapons =  [[8, 4, 0], [10, 5, 0], [25, 6, 0], [40, 7, 0], [74, 8, 0]],
        armor   = [[13, 0, 1], [31, 0, 2], [53, 0, 3], [75, 0, 4], [102, 0, 5]],
        rings   = [[20, 0, 1], [25, 1, 0], [40, 0, 2], [50, 2, 0], [80, 0, 3], [100, 3, 0]],
        arrSum = (a, b, c, d) => a.map((el, i) => el + b[i] + c[i] + d[i]);

    rings.unshift([0, 0, 0]); // for sets with 1 ring
    armor.unshift([0, 0, 0]); // for sets with no armor
    for (let w of weapons) {
        for (let ar of armor) {
            yield arrSum(w, ar, [0, 0, 0], [0, 0, 0]); // for sets with 0 rings
            for (let r1i = 0; r1i < rings.length - 1; r1i++) {
                for (let r2i = r1i + 1; r2i < rings.length; r2i++) {
                    yield arrSum(w, ar, rings[r1i], rings[r2i]);
                }
            }
        }
    }
}

let dps = (dmg, armor) => Math.max(1, dmg - armor),
    hits = (hp, armor, dmg) => Math.ceil(hp / dps(dmg, armor));

function simulate([bossHp, bossDmg, bossArmor], pHp, [, pDmg, pArmor]) {
    return hits(bossHp, bossArmor, pDmg) <= hits(pHp, pArmor, bossDmg); // true if player wins
}

let boss = document.body.textContent.match(/\d+/g).map(s => +s),
    [minCostToWin, maxCostToLose] = [Infinity, -Infinity];
for (let items of genItems()) {
    if (simulate(boss, 100, items)) {
        minCostToWin = Math.min(minCostToWin, items[0]);
    } else {
        maxCostToLose = Math.max(maxCostToLose, items[0]);
    }
}

console.log(minCostToWin, maxCostToLose);
